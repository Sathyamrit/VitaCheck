"""
Micronutrient Knowledge Base
Stores all vitamin/mineral information for RAG retrieval
"""

from dataclasses import dataclass
from typing import List, Dict, Optional
import json

@dataclass
class Micronutrient:
    """Micronutrient information entry"""
    name: str                          # e.g., "Vitamin B12"
    category: str                      # e.g., "Vitamin", "Mineral"
    
    # Deficiency symptoms
    deficiency_symptoms: List[str]     # e.g., ["fatigue", "weakness", "brain fog"]
    
    # Normal ranges
    rda_male: str                      # Recommended Daily Allowance (male)
    rda_female: str                    # Recommended Daily Allowance (female)
    optimal_range: str                 # e.g., "200-900 mcg/day"
    
    # Sources
    food_sources: List[Dict[str, str]]  # [{"food": "beef liver", "amount": "100g", "content": "68 mcg"}]
    
    # Absorption & interactions
    absorption_factors: Dict[str, str]  # e.g., {"intrinsic_factor": "required", "stomach_acid": "required"}
    drug_nutrient_interactions: List[str]  # e.g., ["metformin reduces B12", "PPIs reduce B12"]
    
    # Additional notes
    bioavailability: str               # e.g., "Higher in animal products"
    supplementation_notes: str         # Side effects, forms, timing
    
    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "category": self.category,
            "deficiency_symptoms": self.deficiency_symptoms,
            "rda_male": self.rda_male,
            "rda_female": self.rda_female,
            "optimal_range": self.optimal_range,
            "food_sources": self.food_sources,
            "absorption_factors": self.absorption_factors,
            "drug_nutrient_interactions": self.drug_nutrient_interactions,
            "bioavailability": self.bioavailability,
            "supplementation_notes": self.supplementation_notes,
        }
    
    def to_text(self) -> str:
        """Convert to searchable text format"""
        text_parts = [
            f"Micronutrient: {self.name}",
            f"Category: {self.category}",
            f"Deficiency Symptoms: {', '.join(self.deficiency_symptoms)}",
            f"RDA (Male): {self.rda_male}",
            f"RDA (Female): {self.rda_female}",
            f"Optimal Range: {self.optimal_range}",
            "Food Sources:",
        ]
        
        for source in self.food_sources:
            text_parts.append(f"  - {source['food']}: {source['content']} (per {source['amount']})")
        
        text_parts.extend([
            f"Absorption: {json.dumps(self.absorption_factors)}",
            f"Drug Interactions: {', '.join(self.drug_nutrient_interactions)}",
            f"Bioavailability: {self.bioavailability}",
            f"Supplementation: {self.supplementation_notes}",
        ])
        
        return "\n".join(text_parts)


# Knowledge Base: USDA + Medical Data
MICRONUTRIENT_DB = [
    # Vitamin B12
    Micronutrient(
        name="Vitamin B12 (Cobalamin)",
        category="Vitamin",
        deficiency_symptoms=[
            "fatigue", "weakness", "brain fog", "memory problems",
            "paresthesia", "numbness in hands", "numbness in feet", "pale skin",
            "shortness of breath", "dizziness", "depression",
            "difficulty concentrating", "irritability"
        ],
        rda_male="2.4 mcg",
        rda_female="2.4 mcg",
        optimal_range="200-900 pmol/L (serum level)",
        food_sources=[
            {"food": "beef liver", "amount": "100g", "content": "68 mcg"},
            {"food": "salmon", "amount": "100g", "content": "3.2 mcg"},
            {"food": "eggs", "amount": "2 large", "content": "1.6 mcg"},
            {"food": "milk", "amount": "1 cup", "content": "1.2 mcg"},
            {"food": "chicken breast", "amount": "100g", "content": "0.3 mcg"},
            {"food": "Greek yogurt", "amount": "1 cup", "content": "1.3 mcg"},
        ],
        absorption_factors={
            "intrinsic_factor": "Required (produced in stomach)",
            "stomach_acid": "Required for absorption",
            "calcium": "Enhances absorption",
            "proteases": "Required for release from food"
        },
        drug_nutrient_interactions=[
            "Metformin: Reduces B12 absorption (20-30% of users)",
            "PPIs (proton pump inhibitors): Reduce stomach acid, impair absorption",
            "H2-blockers: Reduce stomach acid, impair absorption",
            "Antibiotics: May affect gut flora producing B12",
            "Nitrous oxide: Inactivates B12 (chronic use)",
        ],
        bioavailability="50-98% from animal products | 0-10.7% from plant sources",
        supplementation_notes="Available as cyanocobalamin, methylcobalamin, or hydroxocobalamin. Sublingual forms may bypass GI absorption issues. Injections for severe deficiency."
    ),
    
    # Iron
    Micronutrient(
        name="Iron",
        category="Mineral",
        deficiency_symptoms=[
            "fatigue", "weakness", "pale skin", "shortness of breath",
            "dizziness", "cold hands", "cold feet", "brittle nails",
            "tachycardia", "headache", "difficulty concentrating",
            "restless leg syndrome", "cravings"
        ],
        rda_male="8.7 mg",
        rda_female="14.8 mg (19-50 years) | 8.7 mg (50+)",
        optimal_range="60-170 mcg/dL (serum) | ferritin 20-200 ng/mL",
        food_sources=[
            {"food": "beef liver", "amount": "100g", "content": "5.2 mg (heme)"},
            {"food": "spinach (cooked)", "amount": "100g", "content": "3.2 mg (non-heme)"},
            {"food": "red lentils", "amount": "100g", "content": "6.5 mg (non-heme)"},
            {"food": "chickpeas", "amount": "100g", "content": "4.3 mg (non-heme)"},
            {"food": "beef", "amount": "100g", "content": "2.6 mg (heme)"},
            {"food": "dark chocolate", "amount": "100g", "content": "12 mg (non-heme)"},
        ],
        absorption_factors={
            "heme_vs_non_heme": "Heme iron (meat): 15-35% absorption | Non-heme (plants): 2-10%",
            "vitamin_c": "Enhances non-heme iron absorption (take with citrus/tomato)",
            "tannins": "Inhibit absorption (avoid with tea/coffee during meals)",
            "phytates": "Inhibit absorption (soaking grains reduces phytates)",
            "calcium": "Inhibits non-heme iron absorption"
        },
        drug_nutrient_interactions=[
            "PPIs: Reduce iron absorption",
            "H2-blockers: Reduce iron absorption",
            "Tetracyclines: Compete for absorption",
            "Fluoroquinolones: Compete for absorption",
        ],
        bioavailability="15-35% for heme | 2-10% for non-heme (increases with vitamin C)",
        supplementation_notes="Take with vitamin C on empty stomach for best absorption. May cause constipation, nausea (start low, increase gradually)."
    ),
    
    # Vitamin D
    Micronutrient(
        name="Vitamin D",
        category="Vitamin",
        deficiency_symptoms=[
            "fatigue", "muscle weakness", "bone pain", "skeletal pain",
            "depression", "seasonal affective disorder", "muscle aches",
            "recurrent infections", "delayed wound healing",
            "autoimmune flares", "cognitive impairment"
        ],
        rda_male="10 mcg (20 IU)",
        rda_female="10 mcg (20 IU)",
        optimal_range="30-100 ng/mL (75-250 nmol/L)",
        food_sources=[
            {"food": "fatty salmon", "amount": "100g", "content": "570 IU"},
            {"food": "cod liver oil", "amount": "1 tbsp", "content": "4000-5000 IU"},
            {"food": "egg yolk", "amount": "1 large", "content": "40-50 IU"},
            {"food": "fortified milk", "amount": "1 cup", "content": "100-200 IU"},
            {"food": "mushrooms (sun-exposed)", "amount": "100g", "content": "2000 IU"},
            {"food": "fortified orange juice", "amount": "1 cup", "content": "100 IU"},
        ],
        absorption_factors={
            "sunlight": "Skin synthesis: 10-30 min/day UVB exposure",
            "fat": "Fat-soluble vitamin, requires fat for absorption",
            "liver": "Converted to 25-OH vitamin D (storage form)",
            "kidney": "Converted to active 1,25-OH vitamin D"
        },
        drug_nutrient_interactions=[
            "Corticosteroids: Reduce vitamin D activation",
            "Anticonvulsants: Impair vitamin D metabolism",
            "Rifampin: Accelerates vitamin D breakdown",
            "Antifungals: May affect vitamin D metabolism",
        ],
        bioavailability="50-80% absorption (75-80% at >1000 IU doses)",
        supplementation_notes="Forms: D2 (ergocalciferol) vs D3 (cholecalciferol). D3 more bioavailable. Take with fat. Best in morning. Safe up to 4,000 IU daily."
    ),
    
    # Magnesium
    Micronutrient(
        name="Magnesium",
        category="Mineral",
        deficiency_symptoms=[
            "muscle cramps", "muscle weakness", "muscle twitching",
            "tremors", "anxiety", "insomnia", "irritability",
            "constipation", "migraines", "irregular heartbeat",
            "fatigue", "difficulty concentrating", "personality changes"
        ],
        rda_male="420 mg",
        rda_female="320 mg",
        optimal_range="1.7-2.2 mg/dL (serum) | 24-30 mg/kg (RBC magnesium)",
        food_sources=[
            {"food": "pumpkin seeds", "amount": "100g", "content": "592 mg"},
            {"food": "almonds", "amount": "100g", "content": "270 mg"},
            {"food": "spinach (cooked)", "amount": "100g", "content": "79 mg"},
            {"food": "black beans", "amount": "100g", "content": "60 mg"},
            {"food": "avocado", "amount": "1 whole", "content": "58 mg"},
            {"food": "dark chocolate", "amount": "100g", "content": "176 mg"},
        ],
        absorption_factors={
            "fiber": "Phytates and fiber can inhibit absorption",
            "calcium": "High calcium:magnesium ratio impairs absorption",
            "fat": "Fat-soluble, requires fat for absorption",
            "acidity": "Lower GI pH enhances absorption"
        },
        drug_nutrient_interactions=[
            "PPIs: Reduce magnesium absorption",
            "Diuretics: Increase magnesium excretion",
            "Bisphosphonates: Take separate (2+ hours apart)",
            "Fluoroquinolones: Take separate",
        ],
        bioavailability="30-40% absorption (varies by form)",
        supplementation_notes="Forms: Citrate (best absorption), malate, taurate, glycinate. Avoid magnesium oxide (laxative effect). Evening dosing aids sleep."
    ),
    
    # Zinc
    Micronutrient(
        name="Zinc",
        category="Mineral",
        deficiency_symptoms=[
            "hair loss", "skin rashes", "diarrhea", "weakened immunity",
            "recurrent infections", "slow wound healing", "loss of taste",
            "loss of smell", "erectile dysfunction", "night blindness",
            "depression", "cognitive impairment"
        ],
        rda_male="11 mg",
        rda_female="8 mg",
        optimal_range="70-120 mcg/dL (serum zinc)",
        food_sources=[
            {"food": "oysters", "amount": "100g", "content": "29 mg"},
            {"food": "beef liver", "amount": "100g", "content": "4 mg"},
            {"food": "chicken breast", "amount": "100g", "content": "0.8 mg"},
            {"food": "cashews", "amount": "100g", "content": "5.6 mg"},
            {"food": "pumpkin seeds", "amount": "100g", "content": "8 mg"},
            {"food": "chickpeas (cooked)", "amount": "100g", "content": "1.5 mg"},
        ],
        absorption_factors={
            "phytates": "Plant phytates inhibit absorption",
            "folate": "Low folate impairs absorption",
            "protein": "Protein enhances absorption",
            "copper": "High copper impairs zinc absorption"
        },
        drug_nutrient_interactions=[
            "Corticosteroids: Increase urinary zinc loss",
            "Diuretics: Increase zinc excretion",
            "Antibiotics: May impair absorption",
            "ACE inhibitors: May increase zinc loss",
        ],
        bioavailability="20-40% from animal products | 5-15% from plant sources",
        supplementation_notes="Do not exceed 40 mg daily from supplements. May cause nausea. Lozenges effective for colds (take at first symptom)."
    ),
]


class KnowledgeBase:
    """Micronutrient Knowledge Base Manager"""
    
    def __init__(self):
        self.nutrients = {n.name: n for n in MICRONUTRIENT_DB}
    
    def get_by_symptom(self, symptom: str) -> List[Micronutrient]:
        """Find micronutrients associated with a symptom"""
        symptom_lower = symptom.lower()
        matches = []
        
        for nutrient in MICRONUTRIENT_DB:
            for deficiency_symptom in nutrient.deficiency_symptoms:
                if symptom_lower in deficiency_symptom.lower() or deficiency_symptom.lower() in symptom_lower:
                    matches.append(nutrient)
                    break
        
        return matches
    
    def get_by_name(self, name: str) -> Optional[Micronutrient]:
        """Get specific micronutrient"""
        return self.nutrients.get(name)
    
    def to_texts(self) -> List[str]:
        """Convert all nutrients to searchable text"""
        return [n.to_text() for n in MICRONUTRIENT_DB]
    
    def to_ids(self) -> List[str]:
        """Get IDs for ChromaDB"""
        return [n.name.lower().replace(" ", "_").replace("(", "").replace(")", "") for n in MICRONUTRIENT_DB]


# Global KB instance
kb = KnowledgeBase()

if __name__ == "__main__":
    print(f"Knowledge Base: {len(kb.nutrients)} micronutrients")
    
    # Example: Find nutrients for fatigue
    fatigue_matches = kb.get_by_symptom("fatigue")
    print(f"\nFatigue-related deficiencies: {len(fatigue_matches)}")
    for m in fatigue_matches:
        print(f"  - {m.name}")
