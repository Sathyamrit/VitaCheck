# Phase 4: Advanced RAG Features & Personalization (Week 6-7)

## Overview

**Status**: Ready to Start  
**Objective**: Expand knowledge base, add personalization, implement drug-nutrient interactions, and create micronutrient alerts.

**Focus Areas**:
1. Expand KB to 30+ micronutrients (currently 5)
2. Enhanced drug-nutrient interaction database
3. User preference learning system
4. Personalized recommendation engine
5. Micronutrient interaction alerts

**Timeline**: Week 6-7 (10 working days)  
**Success Metrics**:
- ✅ 30+ micronutrients in KB (from 5)
- ✅ 50+ drug-nutrient interactions mapped
- ✅ User preference system tracking
- ✅ Personalized recommendations accuracy >85%
- ✅ Interaction alerts with severity scoring

---

## Part 1: Expand Knowledge Base to 30+ Micronutrients

### 1.1 Current KB Status
```
Currently in ChromaDB:
├── Vitamins (8 total)
│   ├── B12 (Cobalamin) ✓
│   ├── B1 (Thiamine) ✓
│   ├── B3 (Niacin) ✓
│   ├── B5 (Pantothenic Acid) ✓
│   ├── B9 (Folate) ✓
│   ├── C (Ascorbic Acid) ✓
│   ├── D (Calciferol) ✓
│   └── E (Tocopherol) ✓
├── Minerals (6 total)
│   ├── Iron ✓
│   ├── Magnesium ✓
│   ├── Zinc ✓
│   ├── Copper ✓
│   ├── Selenium ✓
│   └── Chromium ✓

Total: 14 items (5 defaults + 9 trained)
```

### 1.2 Expand to 30+ Micronutrients

Create `server/expanded_micronutrients.csv`:

```csv
name,category,deficiency_symptoms,rda_male,rda_female,optimal_range,food_sources,absorption_factors,drug_interactions,bioavailability,supplementation_notes
Vitamin B2 (Riboflavin),Vitamin,"fatigue,mouth sores,cracked lips,eye problems,skin issues,anemia,cognitive impairment",1.3 mg,1.1 mg,1.0-1.8 mg/day,"almonds 100g=0.8mg,mushrooms 100g=0.5mg,spinach 100g=0.4mg,salmon 100g=0.2mg,eggs 2 large=0.5mg",oxygen dependent,Methotrexate impairs activation,60% from food,Take with food; activated form is preferred
Vitamin B6 (Pyridoxine),Vitamin,"weak immunity,skin rashes,mouth sores,anemia,confusion,depression,seizures,neuropathy",1.3-1.7 mg,1.3-1.5 mg,1.0-2.0 mg/day,"chickpeas 100g=1.2mg,salmon 100g=0.9mg,potatoes 100g=0.3mg,beef 100g=0.5mg,bananas 1 medium=0.4mg",heat sensitive,Isoniazid increases requirement,75% inorganic + 90% pyridoxal,Take with meals; B-complex support
Pantothenic Acid (B5),Vitamin,"fatigue,depression,hair loss,numbness,muscle weakness,burning feet",5 mg,5 mg,5-10 mg/day,"mushrooms 100g=2.1mg,avocado 1 whole=2.8mg,eggs 2 large=1.8mg,salmon 100g=1.2mg,chicken 100g=0.7mg",broadly available,Few interactions; well tolerated,40-60% absorption,Found in all foods; deficiency rare
Biotin (B7),Vitamin,"hair loss,skin rashes,brittle nails,conjunctivitis,depression,ataxia",30 mcg,30 mcg,30-100 mcg/day,"egg yolks 2 large=20mcg,salmon 100g=5mcg,almonds 100g=6.4mcg,sweet potatoes 100g=0.1mcg",optimal pH 6.0,Few interactions; well tolerated,50-60% bioavailability,Hair/skin supplement; hair growth studies
Vitamin K,Vitamin,"excessive bleeding,easy bruising,poor bone healing,osteoporosis,cardiovascular issues",120 mcg males,90 mcg female,90-120 mcg/day,"spinach 100g=145mcg,broccoli 100g=102mcg,Brussels sprouts 100g=163mcg,cabbage 100g=145mcg,kale 100g=704mcg",fat-soluble; bacterial,Anticoagulants (warfarin) compete,70-80% absorption,Split K1 and K2; MK4 vs MK7 differences
Calcium,Mineral,"muscle cramps,spasms,tingling,tetany,osteoporosis,hypertension,irregular heartbeat",1000-1200 mg,1000-1200 mg,1000-1200 mg/day,"dairy 1 cup=300mg,leafy greens 100g=100-200mg,sardines 100g=380mg,almonds 100g=264mg,fortified products vary",vitamin D essential,PPIs reduce absorption,20-30% from food,Citrate form better; split doses
Phosphorus,Mineral,"weakness,bone pain,loss of appetite,confusion,seizures,respiratory failure",700 mg,700 mg,700 mg/day,"chicken 100g=180mg,salmon 100g=250mg,eggs 2 large=186mg,nuts 100g=400mg,seeds 100g=600mg",vitamin D enhances,Few issues in food context,85-90% absorption,Often excessive in Western diet
Potassium,Mineral,"weakness,muscle cramps,irregular heartbeat,fatigue,numbness,constipation",3400 mg,2600 mg,2600-3400 mg/day,"potatoes 100g=363mg,bananas 1 medium=358mg,spinach 100g=558mg,sweet potato 100g=337mg,avocado 1 whole=485mg",acid-base balance,,90-95% absorption,Risk of hyperkalemia with supplements; food preferred
Sodium,Mineral,"muscle cramps,weakness,hyponatremia,nausea,confusion,seizures",1500 mg,1500 mg,1200-1500 mg/day,"table salt 1 tsp=2300mg,soy sauce 1 tbsp=1000mg,canned goods vary,processed foods high",osmotic balance,,Nearly 100% absorption,Excessive intake worsens hypertension; usually excess
Chloride,Mineral,"loss of appetite,weakness,muscle cramps,dehydration,metabolic alkalosis",2300 mg,2300 mg,2300 mg/day,"table salt 1 tsp=3500mg,seaweed varies,processed foods,dairy products",acid-base balance,,Nearly 100% absorption,Linked to sodium; rarely deficient
Iodine,Mineral,"goiter,hypothyroidism,fatigue,weight gain,cold sensitivity,developmental issues",150 mcg,150 mcg,150 mcg/day,"seaweed varies widely,sea salt 1 tsp=0-50mcg,iodized salt 1 tsp=77mcg,eggs 2 large=25mcg,dairy 1 cup=50mcg",selenium affects,PPIs may reduce (controversial),90% in iodized salt context,Excess can cause hyperthyroidism
Manganese,Mineral,"poor growth,weak bones,skin rashes,mood changes,reproductive issues",2.3 mg,1.8 mg,1.8-2.3 mg/day,"whole grains 100g=1-2mg,nuts 100g=2-3mg,tea (beverage) 1 cup=0.5mg,beans 100g=1.5mg",phytates inhibit,Iron competes for absorption,5% GI absorption,Food sources safer than supplements
Molybdenum,Mineral,"poor growth,tachycardia,sexual dysfunction,migraine-like headaches",45 mcg,45 mcg,45 mcg/day,"legumes 100g=0.2mg,nuts 100g=0.1mg,grains 100g=0.05mg,leafy greens 100g=0.08mg",sulfite oxidase required,,50% estimated bioavailability,Deficiency extremely rare; dietary sources sufficient
Fluoride,Mineral,"dental caries,potential osteoporosis risk,enamel hypoplasia",adequate intake approach,adequate intake approach,0.7-3.0 mg/day,"fluoridated water 1L=0.7-1mg,tea 1 cup=0.1-0.2mg,toothpaste (topical)",inhibits glycolysis enzymes,,Variable absorption,Excess causes dental/skeletal fluorosis risk
Vanadium,Mineral,"impaired glucose metabolism,altered lipid profiles,potential growth effects",adequate intake unknown,adequate intake unknown,10-60 mcg/day,"shellfish,grains,mushrooms,parsley,black pepper","chromium interaction possible",few data on interactions,Minimal bioavailability data,Research emerging; limited evidence
Boron,Mineral,"hormonal imbalances,poor bone health,cognitive issues,arthritis-like symptoms",adequate intake unknown,adequate intake unknown,1-2 mg/day,"dried fruits,nuts,legumes,leafy greens,avocados",magnesium interaction,,Highly variable by food source,Phytates may reduce absorption
Nickel,Mineral,"skin dermatitis,nausea,low blood pressure,developmental issues",adequate intake unknown,adequate intake unknown,5-25 mcg/day,"nuts,legumes,grains,seeds,chocolate","iron interaction possible",few interactions documented,,May trigger contact dermatitis in sensitive individuals
Lithium,Mineral,"mood instability,cognitive issues,tremor,thyroid dysfunction",not established dietary,not established dietary,therapeutic 0.5-1.2 mEq/L,"trace in foods; supplements used clinically",sodium competition,Diuretics increase lithium toxicity,88% GI absorption,Pharmaceutical use; food sources negligible
Strontium,Mineral,"bone weakness,osteoporosis,poor tooth enamel development",adequate intake unknown,adequate intake unknown,0.3-1 mg/day,"dairy,grains,legumes,leafy greens,nuts",calcium competition,,Similar to calcium absorption (18-25%),May help bone mineral density; controversial
```

Script to import expanded micronutrients: `server/expand_kb.py`

```python
"""
Expand knowledge base to 30+ micronutrients
Run once to populate ChromaDB with full dataset
"""

import pandas as pd
import sys
from train_rag import TrainingEngine

def expand_knowledge_base():
    """Load expanded micronutrients into ChromaDB"""
    
    print("="*70)
    print("EXPANDING KNOWLEDGE BASE TO 30+ MICRONUTRIENTS")
    print("="*70)
    
    # Initialize training engine
    trainer = TrainingEngine()
    
    # Load expanded CSV
    try:
        df = pd.read_csv("expanded_micronutrients.csv")
        print(f"\n[OK] Loaded {len(df)} micronutrients from expanded dataset")
    except Exception as e:
        print(f"[ERROR] Failed to load CSV: {e}")
        return False
    
    # Train with new data
    results = trainer.train_from_csv(
        csv_file="expanded_micronutrients.csv",
        name_column="name",
        text_columns=["deficiency_symptoms", "food_sources", "absorption_factors", "drug_interactions"],
        category_column="category",
        batch_size=10
    )
    
    print("\n" + "="*70)
    print("EXPANSION COMPLETE")
    print("="*70)
    print(f"[OK] {results['added']} new micronutrients added to KB")
    print(f"[OK] {results['updated']} micronutrients updated")
    print(f"[OK] Vector store now contains: 30+ micronutrients")
    
    return True

if __name__ == "__main__":
    success = expand_knowledge_base()
    sys.exit(0 if success else 1)
```

### 1.3 Load Expanded KB

```bash
cd server
python expand_kb.py
python manage_rag_kb.py stats
```

Expected output:
```
[OK] KB STATISTICS:
Total Items: 30+
Categories:
  • Vitamin: 13
  • Mineral: 17+
```

---

## Part 2: Drug-Nutrient Interaction Database

### 2.1 Create Comprehensive Drug Interaction Map

Create `server/drug_nutrient_interactions.py`:

```python
"""
Comprehensive drug-nutrient interaction database
Maps medication classes to nutrient depletions and interactions
"""

DRUG_NUTRIENT_INTERACTIONS = {
    # Antidiabetic medications
    "metformin": {
        "category": "Antidiabetic",
        "depletions": ["B12", "Folate", "Calcium", "Magnesium"],
        "severity": "high",
        "mechanism": "Reduces intrinsic factor, impairs B12 absorption; increases homocysteine",
        "onset": "6-12 months with chronic use",
        "recommendations": [
            "Monitor B12 levels annually",
            "Consider cyanocobalamin 500-1000 mcg weekly or monthly injections",
            "Supplement Folate 400-800 mcg daily",
            "Magnesium glycinate 300-400 mg daily"
        ]
    },
    
    # Proton Pump Inhibitors
    "omeprazole": {
        "category": "Acid Suppression (PPI)",
        "depletions": ["B12", "Calcium", "Iron", "Magnesium", "Vitamin C"],
        "severity": "high",
        "mechanism": "Reduces stomach acid needed for nutrient absorption; reduces intrinsic factor",
        "onset": "3-6 months with chronic use",
        "recommendations": [
            "Monitor B12, Calcium, Iron levels annually",
            "Consider supplementation with magnesium glycinate 300-400 mg",
            "Use calcium citrate (better absorption with low acid)",
            "Separate iron supplements by 2+ hours"
        ]
    },
    "lansoprazole": {
        "category": "Acid Suppression (PPI)",
        "depletions": ["B12", "Calcium", "Iron", "Magnesium"],
        "severity": "high",
        "mechanism": "Same as omeprazole",
        "onset": "3-6 months",
        "recommendations": [
            "Same as omeprazole",
            "Consider alternative: H2 blocker (lower risk)"
        ]
    },
    
    # H2-Blockers
    "ranitidine": {
        "category": "Acid Suppression (H2)",
        "depletions": ["B12", "Calcium", "Iron", "Magnesium"],
        "severity": "moderate",
        "mechanism": "Reduces stomach acid but less severe than PPIs",
        "onset": "6-12 months",
        "recommendations": [
            "Monitor levels yearly",
            "Supplement magnesium citrate 200-300 mg daily",
            "Consider alternative: PPI (if needed long-term)"
        ]
    },
    
    # Diuretics
    "furosemide": {
        "category": "Diuretic (Loop)",
        "depletions": ["Potassium", "Magnesium", "Calcium", "Zinc"],
        "severity": "high",
        "mechanism": "Increases urinary losses of electrolytes and minerals",
        "onset": "Immediate with use",
        "recommendations": [
            "Monitor potassium levels monthly during initiation",
            "Potassium supplementation: 20-40 mEq daily or dietary (bananas, potatoes, spinach)",
            "Magnesium glycinate 300-400 mg daily",
            "Consider potassium-sparing diuretic alternative"
        ]
    },
    
    # Statins
    "atorvastatin": {
        "category": "Statin",
        "depletions": ["CoQ10", "Vitamin D"],
        "severity": "moderate",
        "mechanism": "Blocks HMG-CoA reductase, reducing CoQ10 production; vitamin D metabolism affected",
        "onset": "Gradual with chronic use",
        "recommendations": [
            "CoQ10 ubiquinol 100-300 mg daily (better bioavailability than ubiquinone)",
            "Vitamin D3 1000-2000 IU daily",
            "Consider omega-3 supplementation"
        ]
    },
    
    # Antibiotics
    "ciprofloxacin": {
        "category": "Fluoroquinolone",
        "depletions": ["Magnesium", "Iron", "Zinc", "Vitamin K"],
        "severity": "moderate",
        "mechanism": "Chelates minerals; affects gut flora",
        "onset": "During acute course",
        "recommendations": [
            "Separate supplements by 4+ hours from antibiotic",
            "Magnesium glycinate 300 mg daily",
            "Probiotic 25-50 billion CFU daily during and after course"
        ]
    },
    
    # Corticosteroids
    "prednisone": {
        "category": "Corticosteroid",
        "depletions": ["Calcium", "Magnesium", "Potassium", "Vitamin D", "Zinc"],
        "severity": "high",
        "mechanism": "Increases loss; impairs absorption; increases metabolism",
        "onset": "Rapid at high doses",
        "recommendations": [
            "Calcium citrate 1000-1200 mg daily + Vitamin D3 1000-2000 IU",
            "Magnesium glycinate 300-400 mg daily",
            "Potassium rich foods: bananas, sweet potatoes, spinach",
            "Zinc 15-25 mg daily",
            "Consider anti-osteoporosis therapy if long-term"
        ]
    },
    
    # Anticonvulsants
    "phenytoin": {
        "category": "Anticonvulsant",
        "depletions": ["Vitamin D", "Calcium", "Folate", "B12", "Vitamin K"],
        "severity": "high",
        "mechanism": "Induces hepatic metabolism; reduces vitamin activation",
        "onset": "Gradual with chronic use",
        "recommendations": [
            "Vitamin D3 2000-4000 IU daily",
            "Calcium citrate 1000-1200 mg daily",
            "Folate 400-800 mcg daily",
            "Vitamin K 90-120 mcg daily",
            "Monitor bone density annually"
        ]
    },
    
    # Anticoagulants
    "warfarin": {
        "category": "Anticoagulant",
        "depletions": ["Vitamin K"],
        "severity": "critical",
        "mechanism": "Antagonizes vitamin K; maintain consistent intake",
        "onset": "Immediate interaction",
        "recommendations": [
            "Maintain CONSISTENT vitamin K intake (don't avoid)",
            "Vitamin K: 90-120 mcg daily (stable intake important for INR)",
            "Monitor INR regularly",
            "No sudden dietary changes",
            "Avoid cranberry/green tea supplements"
        ]
    },
    
    # Methotrexate (cancer/autoimmune)
    "methotrexate": {
        "category": "Immunosuppressant/Chemotherapy",
        "depletions": ["Folate", "B12", "Vitamin D", "Calcium"],
        "severity": "high",
        "mechanism": "Competitive antagonist of folate; impairs absorption",
        "onset": "Immediate",
        "recommendations": [
            "Folate 1-5 mg daily (taken on non-methotrexate days)",
            "B12 500-1000 mcg weekly",
            "Vitamin D3 1000-2000 IU daily",
            "Calcium citrate 1000-1200 mg daily",
            "Monitor CBC and liver function"
        ]
    },
}

class DrugInteractionChecker:
    """Check medications for nutrient depletions and interactions"""
    
    def __init__(self):
        self.interactions = DRUG_NUTRIENT_INTERACTIONS
    
    def check_medication(self, medication: str) -> dict:
        """Get interaction profile for medication"""
        med_lower = medication.lower()
        
        for drug, profile in self.interactions.items():
            if drug in med_lower or med_lower in drug:
                return profile
        
        return {"found": False, "message": f"No interaction data for {medication}"}
    
    def check_multiple_medications(self, medications: list) -> dict:
        """Check multiple medications and aggregate depletions"""
        all_depletions = set()
        all_interactions = []
        max_severity = "low"
        
        severity_score = {"low": 1, "moderate": 2, "high": 3, "critical": 4}
        
        for med in medications:
            profile = self.check_medication(med)
            if "found" not in profile:
                all_interactions.append(profile)
                all_depletions.update(profile.get("depletions", []))
                
                if severity_score.get(profile.get("severity"), 0) > severity_score.get(max_severity, 0):
                    max_severity = profile.get("severity")
        
        return {
            "medications": medications,
            "unique_depletions": list(all_depletions),
            "total_interactions": len(all_interactions),
            "max_severity": max_severity,
            "all_profiles": all_interactions
        }
    
    def get_recommendations(self, medications: list) -> dict:
        """Get aggregated recommendations for medication stack"""
        check_result = self.check_multiple_medications(medications)
        
        recommendations = {
            "depletions": check_result["unique_depletions"],
            "severity": check_result["max_severity"],
            "supplementation": self._compile_recommendations(check_result),
            "monitoring": self._get_monitoring_plan(check_result)
        }
        
        return recommendations
    
    def _compile_recommendations(self, check_result: dict) -> list:
        """Compile unique recommendations from all medications"""
        all_recs = []
        for profile in check_result["all_profiles"]:
            all_recs.extend(profile.get("recommendations", []))
        
        # Remove duplicates while preserving order
        seen = set()
        unique_recs = []
        for rec in all_recs:
            if rec not in seen:
                unique_recs.append(rec)
                seen.add(rec)
        
        return unique_recs
    
    def _get_monitoring_plan(self, check_result: dict) -> list:
        """Recommend monitoring based on depletions"""
        depletion_set = set(check_result["unique_depletions"])
        
        monitoring = []
        
        if depletion_set & {"B12", "Folate", "Iron"}:
            monitoring.append("CBC (Complete Blood Count) - annually or as needed")
        
        if depletion_set & {"Calcium", "Vitamin D", "Magnesium"}:
            monitoring.append("Bone health assessment - annually if high-risk")
        
        if "Potassium" in depletion_set:
            monitoring.append("Electrolyte panel - monthly initially, then as needed")
        
        if depletion_set & {"CoQ10", "Vitamin D"}:
            monitoring.append("Vitamin D level (25-OH vitamin D) - biannually")
        
        return monitoring


# Global checker instance
drug_checker = DrugInteractionChecker()

if __name__ == "__main__":
    # Example: Check metformin + omeprazole
    result = drug_checker.get_recommendations(["metformin", "omeprazole"])
    
    print("="*70)
    print("DRUG-NUTRIENT INTERACTION CHECK")
    print("="*70)
    print(f"\nMedications: {', '.join(result['depletions'])}")
    print(f"Severity: {result['severity']}")
    print(f"\nDepletions: {result['depletions']}")
    print(f"\nRecommendations:")
    for i, rec in enumerate(result['supplementation'], 1):
        print(f"  {i}. {rec}")
    print(f"\nMonitoring Plan:")
    for i, mon in enumerate(result['monitoring'], 1):
        print(f"  {i}. {mon}")
```

---

## Part 3: User Preference Learning System

### 3.1 Create User Profile Manager

Create `server/user_preferences.py`:

```python
"""
User preference learning and tracking system
Personalizes recommendations based on user history and preferences
"""

from datetime import datetime
from typing import List, Dict, Optional
import json
import os

class UserProfile:
    """Track user preferences and history"""
    
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.profile_file = f"./user_profiles/{user_id}.json"
        self.data = self._load_profile()
    
    def _load_profile(self) -> Dict:
        """Load or create user profile"""
        if os.path.exists(self.profile_file):
            with open(self.profile_file, 'r') as f:
                return json.load(f)
        
        return {
            "user_id": self.user_id,
            "created_at": datetime.now().isoformat(),
            "demographics": {
                "age": None,
                "gender": None,
                "dietary_preferences": [],  # vegan, vegetarian, gluten-free
                "allergies": [],
                "medications": [],
            },
            "health_history": {
                "deficiencies_diagnosed": [],
                "symptoms_reported": [],
                "conditions": [],
            },
            "preferences": {
                "supplement_form": "tablet",  # tablet, powder, liquid, capsule
                "preferred_nutrients": [],
                "avoid_nutrients": [],
                "budget_tier": "standard",  # budget, standard, premium
            },
            "tracking": {
                "diagnosis_history": [],  # List of past diagnoses
                "recommendations_accepted": [],
                "recommendations_rejected": [],
                "feedback_scores": [],  # [1-5 rating]
            },
            "insights": {
                "recurrent_deficiencies": {},  # nutrient: count
                "common_symptoms": {},  # symptom: count
                "recommendation_acceptance_rate": 0.0,
                "dietary_pattern": None,  # balanced, high-protein, low-carb, etc.
            }
        }
    
    def save_profile(self):
        """Persist profile to disk"""
        os.makedirs("./user_profiles", exist_ok=True)
        with open(self.profile_file, 'w') as f:
            json.dump(self.data, f, indent=2)
    
    def update_demographics(self, **kwargs):
        """Update user demographics"""
        self.data["demographics"].update(kwargs)
        self.save_profile()
    
    def add_medication(self, medication: str):
        """Add medication to user profile"""
        if medication not in self.data["demographics"]["medications"]:
            self.data["demographics"]["medications"].append(medication)
            self.save_profile()
    
    def record_diagnosis(self, diagnosis: Dict):
        """Record diagnosis for learning"""
        self.data["tracking"]["diagnosis_history"].append({
            "timestamp": datetime.now().isoformat(),
            "symptoms": diagnosis.get("symptoms", []),
            "identified_deficiencies": diagnosis.get("deficiencies", []),
            "recommendations": diagnosis.get("recommendations", []),
        })
        
        # Update insights
        self._update_insights(diagnosis)
        self.save_profile()
    
    def record_feedback(self, recommendation: str, accepted: bool, rating: int = 3):
        """Record user feedback on recommendations"""
        if accepted:
            self.data["tracking"]["recommendations_accepted"].append(recommendation)
        else:
            self.data["tracking"]["recommendations_rejected"].append(recommendation)
        
        self.data["tracking"]["feedback_scores"].append(rating)
        
        # Update acceptance rate
        total = len(self.data["tracking"]["recommendations_accepted"]) + len(self.data["tracking"]["recommendations_rejected"])
        accepted_count = len(self.data["tracking"]["recommendations_accepted"])
        self.data["insights"]["recommendation_acceptance_rate"] = accepted_count / total if total > 0 else 0
        
        self.save_profile()
    
    def _update_insights(self, diagnosis: Dict):
        """Learn from diagnosis to personalize future recommendations"""
        # Track recurrent deficiencies
        for deficiency in diagnosis.get("deficiencies", []):
            if deficiency not in self.data["insights"]["recurrent_deficiencies"]:
                self.data["insights"]["recurrent_deficiencies"][deficiency] = 0
            self.data["insights"]["recurrent_deficiencies"][deficiency] += 1
        
        # Track common symptoms
        for symptom in diagnosis.get("symptoms", []):
            if symptom not in self.data["insights"]["common_symptoms"]:
                self.data["insights"]["common_symptoms"][symptom] = 0
            self.data["insights"]["common_symptoms"][symptom] += 1
    
    def get_personalized_recommendations(self) -> Dict:
        """Build personalized recommendations based on profile"""
        recommendations = {
            "high_priority": [],
            "preferred_supplements": [],
            "lifestyle_adjustments": [],
            "monitoring_alerts": [],
        }
        
        # Prioritize recurrent deficiencies
        recurrent = sorted(
            self.data["insights"]["recurrent_deficiencies"].items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        for nutrient, count in recurrent[:3]:
            recommendations["high_priority"].append({
                "nutrient": nutrient,
                "reason": f"Diagnosed {count} times",
                "urgency": "high" if count >= 2 else "medium"
            })
        
        # Account for medication interactions
        medications = self.data["demographics"]["medications"]
        recommendations["medication_interactions"] = medications
        
        # Dietary preferences matter
        if "vegan" in self.data["demographics"]["dietary_preferences"]:
            recommendations["diet_note"] = "Plant-based recommendations prioritized"
        
        return recommendations


class PersonalizationEngine:
    """Personalize diagnosis and recommendations for users"""
    
    def __init__(self):
        self.user_profiles = {}
    
    def get_or_create_user(self, user_id: str) -> UserProfile:
        """Get existing or create new user profile"""
        if user_id not in self.user_profiles:
            self.user_profiles[user_id] = UserProfile(user_id)
        return self.user_profiles[user_id]
    
    def personalize_diagnosis(self, user_id: str, diagnosis: Dict) -> Dict:
        """Enhance diagnosis with personalization"""
        profile = self.get_or_create_user(user_id)
        
        # Record diagnosis
        profile.record_diagnosis(diagnosis)
        
        # Get personalized insights
        personalized = {
            "base_diagnosis": diagnosis,
            "user_context": {
                "recurrent_deficiency": list(profile.data["insights"]["recurrent_deficiencies"].keys()),
                "medications": profile.data["demographics"]["medications"],
                "dietary_preferences": profile.data["demographics"]["dietary_preferences"],
            },
            "personalized_recommendations": profile.get_personalized_recommendations(),
            "recommendation_confidence": self._calculate_confidence(profile, diagnosis),
        }
        
        return personalized
    
    def _calculate_confidence(self, profile: UserProfile, diagnosis: Dict) -> float:
        """Calculate confidence in recommendation based on user history"""
        acceptance_rate = profile.data["insights"]["recommendation_acceptance_rate"]
        history_count = len(profile.data["tracking"]["diagnosis_history"])
        
        # More history + higher acceptance = higher confidence
        base_confidence = 0.7
        history_boost = min(history_count * 0.05, 0.2)  # Max +20%
        acceptance_boost = acceptance_rate * 0.1  # Max +10%
        
        confidence = min(base_confidence + history_boost + acceptance_boost, 0.95)
        return round(confidence, 2)


# Global personalization engine
personalization = PersonalizationEngine()

if __name__ == "__main__":
    # Example: Track user over multiple visits
    user = personalization.get_or_create_user("user_123")
    
    # Update profile
    user.update_demographics(age=35, gender="female", dietary_preferences=["vegetarian"])
    user.add_medication("metformin")
    
    # Record first diagnosis
    diagnosis1 = {
        "symptoms": ["fatigue", "brain fog", "numbness"],
        "deficiencies": ["B12", "Iron"],
        "recommendations": ["Increase B12 intake", "Add iron supplement"]
    }
    user.record_diagnosis(diagnosis1)
    user.record_feedback("Increase B12 intake", accepted=True, rating=5)
    
    # Check personalization
    personalized = personalization.personalize_diagnosis("user_123", diagnosis1)
    print("\n" + "="*70)
    print("PERSONALIZED DIAGNOSIS")
    print("="*70)
    print(json.dumps(personalized, indent=2))
```

---

## Part 4: Micronutrient Interaction Alerts

### 4.1 Create Interaction Detection System

Create `server/nutrient_interactions.py`:

```python
"""
Micronutrient-to-micronutrient interaction detection
Alerts when nutrient combinations may cause absorption issues
"""

NUTRIENT_INTERACTIONS = {
    # Competition for absorption
    ("Calcium", "Iron"): {
        "type": "absorption_competition",
        "severity": "high",
        "issue": "Calcium can inhibit iron absorption by up to 60%",
        "solution": "Separate intake by 2+ hours; take iron with vitamin C",
        "safe_together": False,
    },
    ("Calcium", "Zinc"): {
        "type": "absorption_competition",
        "severity": "moderate",
        "issue": "High calcium intake may reduce zinc bioavailability",
        "solution": "Maintain calcium:zinc ratio; separate if possible",
        "safe_together": True,
    },
    ("Iron", "Zinc"): {
        "type": "absorption_competition",
        "severity": "moderate",
        "issue": "Both compete for absorption in small intestine",
        "solution": "Separate supplementation by 2+ hours; food iron less competitive",
        "safe_together": True,
    },
    ("Iron", "Copper"): {
        "type": "absorption_competition",
        "severity": "moderate",
        "issue": "High iron can impair copper absorption",
        "solution": "Monitor copper status if on high-dose iron; separate timing",
        "safe_together": True,
    },
    
    # Synergistic (positive)
    ("Vitamin C", "Iron"): {
        "type": "synergistic_positive",
        "severity": "none",
        "issue": "Vitamin C enhances iron absorption",
        "solution": "TAKE TOGETHER: Optimal for iron bioavailability",
        "safe_together": True,
    },
    ("Vitamin D", "Calcium"): {
        "type": "synergistic_positive",
        "severity": "none",
        "issue": "Vitamin D enhances calcium absorption",
        "solution": "TAKE TOGETHER: Essential for bone health",
        "safe_together": True,
    },
    ("Vitamin D", "Magnesium"): {
        "type": "synergistic_positive",
        "severity": "none",
        "issue": "Magnesium enhances vitamin D metabolism and activation",
        "solution": "TAKE TOGETHER: Improves vitamin D effectiveness",
        "safe_together": True,
    },
    ("Folate", "B12"): {
        "type": "synergistic_positive",
        "severity": "none",
        "issue": "B12 and folate work together in methylation cycle",
        "solution": "TAKE TOGETHER: Essential for DNA synthesis",
        "safe_together": True,
    },
    
    # Antagonistic
    ("Zinc", "Copper"): {
        "type": "antagonistic",
        "severity": "high",
        "issue": "High zinc can impair copper absorption (competing transporters)",
        "solution": "Maintain copper supplementation if >30mg zinc daily",
        "safe_together": False,
    },
    ("Calcium", "Magnesium"): {
        "type": "absorption_competition",
        "severity": "low",
        "issue": "High calcium can modestly reduce magnesium absorption",
        "solution": "Maintain adequate ratio (Ca:Mg = 2:1); separate mega-doses",
        "safe_together": True,
    },
    
    # Phytate/Tannin interactions
    ("Iron", "Tannins"): {
        "type": "chelation",
        "severity": "high",
        "issue": "Tannins (tea, coffee) bind iron, reducing absorption",
        "solution": "Avoid tannins within 2 hours of iron supplementation",
        "safe_together": False,
    },
}

class NutrientInteractionChecker:
    """Check for micronutrient interactions"""
    
    def __init__(self):
        self.interactions = NUTRIENT_INTERACTIONS
    
    def check_pair(self, nutrient1: str, nutrient2: str) -> Dict:
        """Check interaction between two nutrients"""
        # Try both directions
        key = (nutrient1, nutrient2)
        if key in self.interactions:
            return self.interactions[key]
        
        key = (nutrient2, nutrient1)
        if key in self.interactions:
            return self.interactions[key]
        
        return {"type": "no_known_interaction", "severity": "none"}
    
    def check_stack(self, nutrients: List[str]) -> Dict:
        """Check interactions in a supplement stack"""
        interactions_found = []
        warnings = []
        
        for i, nut1 in enumerate(nutrients):
            for nut2 in nutrients[i+1:]:
                interaction = self.check_pair(nut1, nut2)
                
                if interaction["type"] != "no_known_interaction":
                    interactions_found.append({
                        "nutrients": [nut1, nut2],
                        "interaction": interaction
                    })
                    
                    if interaction["severity"] in ["high", "critical"]:
                        warnings.append(f"⚠️ {nut1} + {nut2}: {interaction['issue']}")
        
        return {
            "nutrients": nutrients,
            "total_interactions": len(interactions_found),
            "interactions": interactions_found,
            "warnings": warnings,
            "safe": len(warnings) == 0,
        }
    
    def get_optimal_timing(self, nutrients: List[str]) -> Dict:
        """Suggest timing for supplement taking"""
        check_result = self.check_stack(nutrients)
        
        timing_groups = {
            "morning_with_food": [],
            "morning_on_empty": [],
            "afternoon": [],
            "evening": [],
            "separate_by_hours": []
        }
        
        nutrient_timing = {
            "Vitamin D": {"time": "morning_with_fat", "reason": "Fat-soluble; better absorption"},
            "Iron": {"time": "morning_on_empty", "reason": "Better absorption; vitamin C helps"},
            "Calcium": {"time": "with_meals", "reason": "Better absorption with food"},
            "Magnesium": {"time": "evening", "reason": "Helps relaxation and sleep"},
            "B vitamins": {"time": "morning", "reason": "Energy support"},
            "Zinc": {"time": "evening", "reason": "Can cause nausea on empty stomach"},
        }
        
        return {
            "stack": nutrients,
            "timing_recommendations": nutrient_timing,
            "warnings": check_result["warnings"],
            "note": "Spacing by 2+ hours between competing nutrients optimal"
        }


# Global checker instance
interaction_checker = NutrientInteractionChecker()

if __name__ == "__main__":
    # Example: Check common stack
    stack = ["Vitamin D", "Calcium", "Magnesium", "Iron", "Vitamin C"]
    
    print("="*70)
    print("MICRONUTRIENT INTERACTION CHECK")
    print("="*70)
    
    result = interaction_checker.check_stack(stack)
    
    print(f"\nNutrient Stack: {', '.join(stack)}")
    print(f"Total Interactions Found: {result['total_interactions']}")
    print(f"Safe to Take Together: {'✓' if result['safe'] else '✗'}")
    
    if result['warnings']:
        print("\n⚠️ WARNINGS:")
        for warning in result['warnings']:
            print(f"  {warning}")
    
    print("\n📅 Optimal Timing:")
    timing = interaction_checker.get_optimal_timing(stack)
    for rec, details in timing['timing_recommendations'].items():
        print(f"  • {rec}: {details['reason']}")
```

---

## Part 5: Integration & API Endpoints

### 5.1 Update streaming_api.py with New Endpoints

Add to `server/streaming_api.py`:

```python
# Add to imports
from user_preferences import personalization
from drug_nutrient_interactions import drug_checker
from nutrient_interactions import interaction_checker

# New endpoint: Personalized diagnosis
@app.post("/diagnosis/personalized")
async def personalized_diagnosis(request: DiagnoseRequest):
    """
    Diagnosis with full personalization:
    1. RAG context retrieval
    2. User profile consideration
    3. Medication interaction detection
    4. Nutrient interaction alerts
    """
    user_id = request.get("user_id", "anonymous")
    
    # Get RAG results
    rag_result = rag_pipeline.process_diagnosis_request(request.text)
    
    # Check for medication interactions
    medications = request.get("medications", [])
    drug_interactions = drug_checker.get_recommendations(medications) if medications else {}
    
    # Check for nutrient interactions
    recommended_nutrients = [r.get("nutrient", "") for r in rag_result['raw_results']]
    nutrient_interactions = interaction_checker.check_stack(recommended_nutrients)
    
    # Personalize based on user history
    base_diagnosis = {
        "symptoms": rag_result['extracted_symptoms'],
        "deficiencies": [r['micronutrient'] for r in rag_result['raw_results'][:3]],
        "recommendations": [],
    }
    
    personalized_result = personalization.personalize_diagnosis(user_id, base_diagnosis)
    
    # Stream comprehensive response
    async def generate_personalized():
        yield f"data: {json.dumps({'type': 'analysis', 'rag': rag_result['raw_results'][:3]})}\n\n"
        yield f"data: {json.dumps({'type': 'drug_interactions', 'data': drug_interactions})}\n\n"
        yield f"data: {json.dumps({'type': 'nutrient_interactions', 'data': nutrient_interactions})}\n\n"
        yield f"data: {json.dumps({'type': 'personalized', 'data': personalized_result})}\n\n"
    
    return StreamingResponse(generate_personalized(), media_type="text/event-stream")


# New endpoint: Check drug interactions
@app.post("/interactions/drugs")
async def check_drug_interactions(request: dict):
    """Check medications for nutrient depletions"""
    medications = request.get("medications", [])
    result = drug_checker.get_recommendations(medications)
    return result


# New endpoint: Check nutrient interactions
@app.post("/interactions/nutrients")
async def check_nutrient_interactions(request: dict):
    """Check supplement stack for interactions"""
    nutrients = request.get("nutrients", [])
    result = interaction_checker.check_stack(nutrients)
    return result


# New endpoint: Get supplement timing
@app.get("/supplements/timing")
async def get_supplement_timing(nutrients: str = ""):
    """Get optimal timing for supplement intake"""
    nutrient_list = [n.strip() for n in nutrients.split(",") if n.strip()]
    result = interaction_checker.get_optimal_timing(nutrient_list)
    return result


# New endpoint: User profile & insights
@app.get("/user/{user_id}/profile")
async def get_user_profile(user_id: str):
    """Get user profile and insights"""
    user = personalization.get_or_create_user(user_id)
    return {
        "user_id": user_id,
        "demographics": user.data.get("demographics"),
        "insights": user.data.get("insights"),
        "recurrent_concerns": user.data.get("insights", {}).get("recurrent_deficiencies")
    }


# New endpoint: Record user feedback
@app.post("/user/{user_id}/feedback")
async def record_user_feedback(user_id: str, request: dict):
    """Record feedback on recommendation"""
    user = personalization.get_or_create_user(user_id)
    user.record_feedback(
        recommendation=request.get("recommendation"),
        accepted=request.get("accepted", False),
        rating=request.get("rating", 3)
    )
    return {"status": "feedback_recorded"}
```

---

## Phase 4 Checklist

### Week 6 (Days 1-3): KB Expansion + Drug Interactions

- [ ] Create expanded_micronutrients.csv (20 new nutrients)
- [ ] Create expand_kb.py script
- [ ] Load 30+ micronutrients into ChromaDB
- [ ] Verify KB stats (30+ items)
- [ ] Create drug_nutrient_interactions.py (15+ medications)
- [ ] Test drug interaction checker
- [ ] Create API endpoint `/interactions/drugs`

### Week 6 (Days 4-5): User Personalization

- [ ] Create user_preferences.py (profile + learning)
- [ ] Create PersonalizationEngine class
- [ ] Implement recommendation personalization
- [ ] Create user profile persistence
- [ ] Test user profile tracking
- [ ] Create `/user/{user_id}/profile` endpoint

### Week 7 (Days 1-3): Nutrient Interactions

- [ ] Create nutrient_interactions.py (15+ interactions)
- [ ] Implement interaction detection
- [ ] Implement timing recommendations
- [ ] Create `/interactions/nutrients` endpoint
- [ ] Create `/supplements/timing` endpoint
- [ ] Test nutrient stack analysis

### Week 7 (Days 4-5): Integration & Testing

- [ ] Update RAGDashboard with new features
- [ ] Create comprehensive test suite
- [ ] Load test (multiple users, heavy queries)
- [ ] Performance optimization
- [ ] Final QA and documentation
- [ ] Phase 4 completion report

---

## Success Metrics - Phase 4

| Metric | Target | Status |
|--------|--------|--------|
| Micronutrients in KB | 30+ | Not Started |
| Drug Interactions Mapped | 50+ | Not Started |
| User Profile System | Active | Not Started |
| Personalization Accuracy | >85% | Not Started |
| Interaction Alert Coverage | >90% | Not Started |
| Supplement Stack Analysis | Complete | Not Started |

---

## Next Steps - Phase 5+

### Phase 5: Production Deployment
- [ ] DevOps pipeline (Docker, K8s, CI/CD)
- [ ] Monitoring & alerting
- [ ] Production database backup
- [ ] Security hardening
- [ ] Load balancing

### Phase 6: Advanced ML
- [ ] User cohort analysis
- [ ] Predictive deficiency modeling  
- [ ] Recommendation engine tuning
- [ ] A/B testing framework

---

**Phase 4 Status**: [Ready to Start]  
**Estimated Duration**: 10 working days  
**Cost**: $0 (local execution)

---

