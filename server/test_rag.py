"""
Test suite for RAG pipeline
"""

import asyncio
import time
import json
from rag_pipeline import rag_pipeline
from vector_store import vector_store

def test_symptom_extraction():
    """Test symptom extraction from patient text"""
    test_cases = [
        "I am experiencing extreme fatigue and brain fog",
        "Weakness and numbness in my hands and feet",
        "Hair loss and skin rashes with diarrhea",
    ]
    
    print("\n" + "="*70)
    print("TEST 1: SYMPTOM EXTRACTION")
    print("="*70)
    
    for test_input in test_cases:
        symptoms = rag_pipeline.extract_symptoms_from_text(test_input)
        print(f"\nInput: {test_input}")
        print(f"Extracted: {symptoms}")

def test_vector_search():
    """Test vector store retrieval"""
    test_queries = [
        "severe fatigue and weakness",
        "numbness in hands and feet",
        "hair loss and immune system weakness",
    ]
    
    print("\n" + "="*70)
    print("TEST 2: VECTOR STORE RETRIEVAL")
    print("="*70)
    
    for query in test_queries:
        results = vector_store.search(query, k=3)
        print(f"\nQuery: {query}")
        if results:
            print(f"Top result: {results[0]['micronutrient']} ({results[0]['relevance']:.1%})")
            for i, result in enumerate(results, 1):
                print(f"  {i}. {result['micronutrient']}: {result['relevance']:.1%}")
        else:
            print("No results found")

def test_prompt_augmentation():
    """Test full RAG pipeline"""
    patient_text = """
    35-year-old female
    Chief Complaint: 2 months of extreme fatigue and brain fog
    Symptoms: Weakness, numbness in hands and feet, pale skin, cold hands
    Diet: Vegetarian (no meat for 3 years)
    Medications: Metformin for PCOS
    """
    
    print("\n" + "="*70)
    print("TEST 3: FULL RAG PIPELINE")
    print("="*70)
    
    start = time.time()
    result = rag_pipeline.process_diagnosis_request(patient_text)
    elapsed = time.time() - start
    
    print(f"\n⏱ Processing time: {elapsed*1000:.0f}ms")
    print(f"📋 Extracted symptoms: {result['extracted_symptoms']}")
    print(f"🔍 Retrieved micronutrients: {len(result['raw_results'])}")
    print(f"\n📄 Augmented prompt (first 300 chars):")
    print(result['augmented_prompt'][:300] + "...")

def test_search_performance():
    """Test retrieval latency"""
    queries = [
        "fatigue", "weakness", "numbness",
        "hair loss", "memory problems", "anxiety"
    ]
    
    print("\n" + "="*70)
    print("TEST 4: SEARCH PERFORMANCE")
    print("="*70)
    
    times = []
    for query in queries:
        start = time.time()
        results = vector_store.search(query, k=5)
        elapsed = time.time() - start
        times.append(elapsed * 1000)
        
        top_nutrient = results[0]['micronutrient'] if results else "N/A"
        top_relevance = results[0]['relevance'] if results else 0
        print(f"{query:<15} → {elapsed*1000:>6.1f}ms, Top: {top_nutrient} ({top_relevance:.1%})")
    
    print(f"\n✓ Avg latency: {sum(times)/len(times):.1f}ms")
    print(f"✓ Max latency: {max(times):.1f}ms")
    print(f"✓ Min latency: {min(times):.1f}ms")

if __name__ == "__main__":
    print("\n🚀 VITACHECK PHASE 3 - RAG PIPELINE TESTS\n")
    
    try:
        # Initialize
        print("Initializing vector store...")
        vector_store.initialize()
        
        # Run tests
        test_symptom_extraction()
        test_vector_search()
        test_prompt_augmentation()
        test_search_performance()
        
        print("\n✅ All tests completed!")
    
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
