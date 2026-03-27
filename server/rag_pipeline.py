"""
RAG Pipeline: Retrieves micronutrient context and augments prompts
"""

from vector_store import vector_store
from typing import List, Dict, Tuple
import re

class RAGPipeline:
    """Retrieval-Augmented Generation for diagnosis"""
    
    def __init__(self):
        # Initialize vector store
        vector_store.initialize()
    
    def extract_symptoms_from_text(self, text: str) -> List[str]:
        """
        Extract symptoms from patient input
        
        Used before retrieval to identify what to search for
        """
        symptoms = []
        
        # Common symptom keywords
        symptom_keywords = [
            "fatigue", "tired", "tiredness", "weakness", "weak", 
            "brain fog", "fog", "memory", "concentration", "focus", 
            "numbness", "tingling", "paresthesia",
            "cramps", "muscle", "weakness", "hair loss", 
            "pale", "rash", "diarrhea", "constipation", 
            "heartbeat", "palpitations", "anxiety", "depression",
            "insomnia", "sleep", "sleepless", "migraine", "headache", 
            "dizziness", "dizzy", "wound healing", "infections", 
            "taste", "smell", "cold hands", "cold feet",
            "shortness of breath", "breath", "breathing",
            "irritability", "personality", "tremor", "trembling",
            "twitching", "cognitive", "difficulty concentrating",
            "restless leg", "autoimmune", "immune", "erection",
            "erectile dysfunction"
        ]
        
        text_lower = text.lower()
        
        for keyword in symptom_keywords:
            if keyword in text_lower:
                symptoms.append(keyword)
        
        # Remove duplicates while preserving order
        seen = set()
        unique_symptoms = []
        for symptom in symptoms:
            if symptom not in seen:
                seen.add(symptom)
                unique_symptoms.append(symptom)
        
        return unique_symptoms
    
    def retrieve_context(self, symptoms: List[str]) -> Tuple[str, List[Dict]]:
        """
        Retrieve micronutrient context from vector store
        
        Returns:
            (formatted_context, raw_results)
        """
        context = vector_store.get_context_for_symptoms(symptoms)
        
        # Also get raw results for citation tracking
        all_results = []
        for symptom in symptoms:
            results = vector_store.search(symptom, k=3)
            all_results.extend(results)
        
        return context, all_results
    
    def create_augmented_prompt(
        self, 
        original_prompt: str, 
        symptoms: List[str],
        context: str
    ) -> str:
        """
        Augment prompt with RAG context
        
        Instructs LLM to use retrieved context for grounded response
        """
        augmented_prompt = f"""You are a micronutrient deficiency diagnostic assistant.

Based on the patient's symptoms, analyze the micronutrient information provided below and:
1. Identify likely deficiencies
2. Explain the connection between symptoms and deficiencies
3. Recommend food sources and supplementation strategies
4. Include relevant RDA and optimal ranges
5. Note any drug-nutrient interactions (if medications mentioned)
6. Provide evidence-based recommendations

IMPORTANT: Use ONLY the micronutrient information provided below. Do not make up information.
Always cite which micronutrient information supported your conclusion (e.g., "According to Vitamin B12: ...").

---

RETRIEVED MICRONUTRIENT INFORMATION:

{context}

---

PATIENT INFORMATION:

Symptoms mentioned: {', '.join(symptoms) if symptoms else 'Not specified'}

{original_prompt}

---

Provide a comprehensive analysis grounded in the micronutrient information above.
Include citations and evidence for all recommendations.
"""
        
        return augmented_prompt
    
    def process_diagnosis_request(self, patient_text: str) -> Dict:
        """
        Full RAG pipeline: extract → retrieve → augment
        
        Returns:
            {
                "original_text": patient input,
                "extracted_symptoms": list of symptoms,
                "retrieved_context": formatted context string,
                "augmented_prompt": prompt for LLM,
                "raw_results": raw search results
            }
        """
        # Step 1: Extract symptoms
        symptoms = self.extract_symptoms_from_text(patient_text)
        
        # Step 2: Retrieve context
        context, raw_results = self.retrieve_context(symptoms)
        
        # Step 3: Create augmented prompt
        augmented_prompt = self.create_augmented_prompt(
            patient_text, 
            symptoms,
            context
        )
        
        return {
            "original_text": patient_text,
            "extracted_symptoms": symptoms,
            "retrieved_context": context,
            "augmented_prompt": augmented_prompt,
            "raw_results": raw_results,
        }


# Global RAG pipeline instance
rag_pipeline = RAGPipeline()

if __name__ == "__main__":
    # Test RAG
    test_input = """
    Patient: 35-year-old female
    Chief Complaint: Extreme fatigue and brain fog for 2 months
    Associated Symptoms: Weakness, numbness in hands and feet, pale skin
    Medical History: Vegetarian diet, no meat for 3 years
    Current Medications: Metformin 500mg for PCOS
    Allergies: None
    """
    
    print("="*70)
    print("TESTING RAG PIPELINE")
    print("="*70)
    
    result = rag_pipeline.process_diagnosis_request(test_input)
    
    print(f"\n[SYMPTOMS]")
    for symptom in result['extracted_symptoms']:
        print(f"  • {symptom}")
    
    print(f"\n[MICRONUTRIENTS] {len(result['raw_results'])} found")
    for res in result['raw_results'][:5]:
        print(f"  • {res['micronutrient']} ({res['relevance']:.1%})")
    
    print(f"\n[AUGMENTED PROMPT] (first 400 chars)")
    print(result['augmented_prompt'][:400] + "...\n")
    
    print(f"[OK] RAG Pipeline ready for LLM augmentation")
