"""
Expand knowledge base to 30+ micronutrients
Run once to populate ChromaDB with full dataset
"""

import sys
from train_rag import RAGTrainer

def expand_knowledge_base():
    """Load expanded micronutrients into ChromaDB"""
    
    print("="*70)
    print("EXPANDING KNOWLEDGE BASE TO 30+ MICRONUTRIENTS")
    print("="*70)
    
    # Initialize trainer
    trainer = RAGTrainer()
    
    # Train with expanded CSV
    try:
        added = trainer.train_from_file(
            "expanded_micronutrients.csv",
            format="csv"
        )
        
        print("\n" + "="*70)
        print("EXPANSION COMPLETE")
        print("="*70)
        print(f"[OK] {added} new micronutrients added to KB")
        print("[OK] Vector store now contains 30+ micronutrients")
        
        # Print report
        trainer.print_report()
        
        return True
        
    except Exception as e:
        print(f"[ERROR] Failed to expand KB: {e}")
        return False

if __name__ == "__main__":
    success = expand_knowledge_base()
    sys.exit(0 if success else 1)