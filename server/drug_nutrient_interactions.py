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