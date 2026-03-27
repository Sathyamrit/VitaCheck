"""
ChromaDB Vector Store Manager
Handles embedding storage and semantic search
"""

import chromadb
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Tuple
from micronutrient_kb import kb, MICRONUTRIENT_DB
import os
import numpy as np

class VectorStore:
    """Vector database for semantic search"""
    
    def __init__(self, persist_dir: str = "./chroma_db"):
        """Initialize ChromaDB with persistent storage"""
        # Create directory if it doesn't exist
        os.makedirs(persist_dir, exist_ok=True)
        
        # Initialize ChromaDB client with persistence
        self.client = chromadb.PersistentClient(path=persist_dir)
        
        # Create or get collection
        self.collection = self.client.get_or_create_collection(
            name="micronutrients",
            metadata={"hnsw:space": "cosine"}
        )
        
        # Load embedding model (free, offline)
        print("Loading embedding model...")
        self.embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
        
        self.is_initialized = False
        self.persist_dir = persist_dir
    
    def initialize(self):
        """Load knowledge base into vector store (one-time setup)"""
        if self.is_initialized:
            return
        
        # Check if already populated
        if self.collection.count() > 0:
            print(f"[OK] Vector store already initialized with {self.collection.count()} items")
            self.is_initialized = True
            return
        
        print("Initializing vector store...")
        
        # Get all micronutrient texts
        texts = kb.to_texts()
        ids = kb.to_ids()
        
        # Generate embeddings
        print(f"Generating embeddings for {len(texts)} micronutrients...")
        embeddings = self.embedding_model.encode(texts, show_progress_bar=True)
        
        # Add to ChromaDB
        self.collection.add(
            embeddings=embeddings.tolist(),
            documents=texts,
            ids=ids,
            metadatas=[
                {
                    "name": MICRONUTRIENT_DB[i].name,
                    "category": MICRONUTRIENT_DB[i].category
                }
                for i in range(len(texts))
            ]
        )
        
        print(f"[OK] Vector store initialized with {len(texts)} micronutrients")
        self.is_initialized = True
    
    def search(self, query: str, k: int = 5) -> List[Dict]:
        """
        Semantic search for micronutrients
        
        Args:
            query: Search query or symptoms
            k: Number of results
        
        Returns:
            List of relevant micronutrients with scores
        """
        if not self.is_initialized:
            self.initialize()
        
        # Generate query embedding
        query_embedding = self.embedding_model.encode([query])[0].tolist()
        
        # Search in ChromaDB
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=k,
        )
        
        # Format results
        formatted_results = []
        
        if results['documents'] and len(results['documents']) > 0:
            for i, doc in enumerate(results['documents'][0]):
                distance = results['distances'][0][i] if results['distances'] else 0
                similarity_score = 1 - distance  # Convert distance to similarity
                
                formatted_results.append({
                    "micronutrient": results['metadatas'][0][i]['name'],
                    "category": results['metadatas'][0][i]['category'],
                    "relevance": similarity_score,  # 0-1 (higher = more relevant)
                    "content": doc,
                })
        
        return formatted_results
    
    def get_context_for_symptoms(self, symptoms: List[str]) -> str:
        """
        Build RAG context from symptoms
        
        Args:
            symptoms: List of patient symptoms
        
        Returns:
            Formatted context string for LLM
        """
        all_results = []
        
        for symptom in symptoms:
            results = self.search(symptom, k=3)
            all_results.extend(results)
        
        # Remove duplicates by micronutrient name
        seen = set()
        unique_results = []
        
        for result in all_results:
            if result['micronutrient'] not in seen:
                seen.add(result['micronutrient'])
                unique_results.append(result)
        
        # Sort by relevance
        unique_results.sort(key=lambda x: x['relevance'], reverse=True)
        
        # Format as context
        context = "## RELEVANT MICRONUTRIENT INFORMATION\n\n"
        
        for i, result in enumerate(unique_results[:5], 1):
            context += f"### {i}. {result['micronutrient']} (Category: {result['category']})\n"
            context += f"**Relevance Score**: {result['relevance']:.1%}\n"
            context += f"\n{result['content']}\n\n"
        
        return context


# Global vector store instance
vector_store = VectorStore()

if __name__ == "__main__":
    # Initialize on first run
    vector_store.initialize()
    
    # Test search
    test_symptoms = ["fatigue", "weakness"]
    
    print("\n" + "="*70)
    print("SEARCHING FOR: " + ", ".join(test_symptoms))
    print("="*70 + "\n")
    
    for symptom in test_symptoms:
        results = vector_store.search(symptom, k=3)
        print(f"\n📋 Results for '{symptom}':")
        for result in results:
            print(f"  • {result['micronutrient']} ({result['category']}) - {result['relevance']:.1%} relevant")
