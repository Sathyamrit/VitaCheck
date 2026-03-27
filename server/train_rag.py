#!/usr/bin/env python3
"""
RAG Training Script: Load custom datasets into ChromaDB
Supports CSV, JSON, and manual entry
"""

import csv
import json
import argparse
import sys
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict
import pandas as pd

from vector_store import vector_store
from micronutrient_kb import Micronutrient, MICRONUTRIENT_DB


@dataclass
class TrainingMetrics:
    """Metrics for training run"""
    total_added: int = 0
    total_updated: int = 0
    total_errors: int = 0
    items: List[Dict] = None
    
    def __post_init__(self):
        if self.items is None:
            self.items = []


class RAGTrainer:
    """Train RAG with custom datasets"""
    
    def __init__(self):
        self.vector_store = vector_store
        self.metrics = TrainingMetrics()
    
    def load_csv(self, filepath: str, mapping: Optional[Dict] = None) -> List[Dict]:
        """
        Load micronutrients from CSV
        
        Expected columns (or map them):
        - name: Nutrient name
        - category: Vitamin/Mineral
        - deficiency_symptoms: comma-separated list
        - rda_male: male RDA
        - rda_female: female RDA
        - food_sources: JSON or semicolon-separated
        - drug_interactions: comma-separated
        """
        print(f"\n[INFO] Loading CSV: {filepath}")
        
        df = pd.read_csv(filepath)
        items = []
        
        print(f"[INFO] Found {len(df)} rows")
        
        for idx, row in df.iterrows():
            try:
                # Map columns if provided
                if mapping:
                    row = row.rename(mapping)
                
                # Parse symptoms (comma or semicolon separated)
                symptoms = row.get('deficiency_symptoms', '')
                if isinstance(symptoms, str):
                    symptoms = [s.strip() for s in symptoms.replace(';', ',').split(',')]
                else:
                    symptoms = []
                
                # Parse food sources (JSON or semicolon-separated)
                food_sources = row.get('food_sources', '')
                if isinstance(food_sources, str) and food_sources.startswith('['):
                    try:
                        food_sources = json.loads(food_sources)
                    except:
                        food_sources = [{'food': item.strip(), 'content': 'N/A'} for item in food_sources.split(';')]
                else:
                    food_sources = []
                
                # Parse interactions (comma-separated)
                interactions = row.get('drug_nutrient_interactions', '')
                if isinstance(interactions, str):
                    interactions = [i.strip() for i in interactions.split(',') if i.strip()]
                else:
                    interactions = []
                
                # Parse absorption factors (JSON or simple dict)
                absorption = row.get('absorption_factors', '{}')
                if isinstance(absorption, str):
                    try:
                        absorption = json.loads(absorption)
                    except:
                        absorption = {}
                else:
                    absorption = {}
                
                nutrient = Micronutrient(
                    name=row.get('name', f'Nutrient_{idx}'),
                    category=row.get('category', 'Other'),
                    deficiency_symptoms=symptoms,
                    rda_male=row.get('rda_male', 'N/A'),
                    rda_female=row.get('rda_female', 'N/A'),
                    optimal_range=row.get('optimal_range', 'N/A'),
                    food_sources=food_sources,
                    absorption_factors=absorption,
                    drug_nutrient_interactions=interactions,
                    bioavailability=row.get('bioavailability', 'N/A'),
                    supplementation_notes=row.get('supplementation_notes', 'N/A'),
                )
                
                items.append(nutrient)
                print(f"[OK] Row {idx+1}: {nutrient.name}")
                
            except Exception as e:
                print(f"[ERROR] Row {idx+1}: {e}")
                self.metrics.total_errors += 1
        
        print(f"\n[OK] CSV loaded: {len(items)} nutrients")
        return items
    
    def load_json(self, filepath: str) -> List[Dict]:
        """
        Load micronutrients from JSON
        
        Expected format:
        [
            {
                "name": "Vitamin B12",
                "category": "Vitamin",
                "deficiency_symptoms": ["fatigue", "weakness"],
                ...
            }
        ]
        """
        print(f"\n[INFO] Loading JSON: {filepath}")
        
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        if not isinstance(data, list):
            data = [data]
        
        items = []
        for idx, item in enumerate(data):
            try:
                nutrient = Micronutrient(**item)
                items.append(nutrient)
                print(f"[OK] Item {idx+1}: {nutrient.name}")
            except Exception as e:
                print(f"[ERROR] Item {idx+1}: {e}")
                self.metrics.total_errors += 1
        
        print(f"\n[OK] JSON loaded: {len(items)} nutrients")
        return items
    
    def add_to_vector_store(self, nutrients: List[Micronutrient]) -> int:
        """Add nutrients to ChromaDB vector store"""
        print(f"\n[INFO] Adding {len(nutrients)} nutrients to vector store...")
        
        # Convert to text and generate IDs
        texts = [n.to_text() for n in nutrients]
        ids = [n.name.lower().replace(" ", "_").replace("(", "").replace(")", "") for n in nutrients]
        
        # Generate embeddings
        print("[INFO] Generating embeddings...")
        embeddings = self.vector_store.embedding_model.encode(texts, show_progress_bar=True)
        
        # Add to ChromaDB
        try:
            self.vector_store.collection.add(
                embeddings=embeddings.tolist(),
                documents=texts,
                ids=ids,
                metadatas=[
                    {
                        "name": nutrient.name,
                        "category": nutrient.category,
                    }
                    for nutrient in nutrients
                ]
            )
            
            added = len(nutrients)
            self.metrics.total_added += added
            self.metrics.items.extend([
                {"name": n.name, "category": n.category, "status": "added"}
                for n in nutrients
            ])
            
            print(f"\n[OK] {added} nutrients added to vector store")
            return added
            
        except Exception as e:
            print(f"[ERROR] Failed to add to vector store: {e}")
            self.metrics.total_errors += len(nutrients)
            return 0
    
    def train_from_file(self, filepath: str, format: str = 'auto', mapping: Optional[Dict] = None) -> int:
        """Train from file (CSV or JSON)"""
        filepath = Path(filepath)
        
        if not filepath.exists():
            print(f"[ERROR] File not found: {filepath}")
            return 0
        
        # Auto-detect format
        if format == 'auto':
            format = filepath.suffix.lower().lstrip('.')
        
        # Load file
        if format == 'csv':
            nutrients = self.load_csv(str(filepath), mapping)
        elif format == 'json':
            nutrients = self.load_json(str(filepath))
        else:
            print(f"[ERROR] Unknown format: {format}")
            return 0
        
        # Add to vector store
        added = self.add_to_vector_store(nutrients)
        
        return added
    
    def print_report(self):
        """Print training report"""
        print("\n" + "="*70)
        print("TRAINING REPORT")
        print("="*70)
        print(f"Total Added: {self.metrics.total_added}")
        print(f"Total Updated: {self.metrics.total_updated}")
        print(f"Total Errors: {self.metrics.total_errors}")
        print(f"\nItems Added:")
        for item in self.metrics.items:
            print(f"  • {item['name']} ({item['category']})")
        
        print(f"\n[OK] Training complete!")


def main():
    parser = argparse.ArgumentParser(
        description="Train RAG with custom micronutrient datasets"
    )
    parser.add_argument(
        "file",
        help="CSV or JSON file with micronutrient data"
    )
    parser.add_argument(
        "--format",
        choices=['csv', 'json', 'auto'],
        default='auto',
        help="File format (auto-detect by default)"
    )
    parser.add_argument(
        "--mapping",
        help="JSON mapping of CSV columns (e.g., '{\"food_sources\": \"foods\"}')"
    )
    parser.add_argument(
        "--append",
        action='store_true',
        default=True,
        help="Append to existing vector store (default)"
    )
    
    args = parser.parse_args()
    
    # Initialize trainer
    trainer = RAGTrainer()
    
    # Parse mapping if provided
    mapping = None
    if args.mapping:
        try:
            mapping = json.loads(args.mapping)
        except:
            print("[ERROR] Invalid mapping JSON")
            return 1
    
    print("\n" + "="*70)
    print("VITACHECK RAG TRAINING")
    print("="*70)
    
    # Train from file
    added = trainer.train_from_file(args.file, args.format, mapping)
    
    # Print report
    trainer.print_report()
    
    return 0 if added > 0 else 1


if __name__ == "__main__":
    sys.exit(main())
