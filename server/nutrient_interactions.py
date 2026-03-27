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