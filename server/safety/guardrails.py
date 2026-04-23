"""
Safety guardrails for VitaCheck diagnostic engine.
Prevents recommendations in emergency situations.
"""

EMERGENCY_SYMPTOMS = {
    "chest pain", "chest discomfort", "chest tightness",
    "difficulty breathing", "shortness of breath", "dyspnea",
    "severe headache", "thunderclap headache", "worst headache",
    "confusion", "loss of consciousness", "fainting", "syncope",
    "severe bleeding", "uncontrolled bleeding", "hemorrhage",
    "severe abdominal pain", "acute abdomen",
    "severe allergic reaction", "anaphylaxis", "angioedema",
    "severe dizziness", "vertigo with chest pain",
    "vision changes", "sudden blindness", "vision loss",
    "sudden weakness", "paralysis", "stroke symptoms",
    "seizure", "convulsion", "loss of control",
}

CONTRAINDICATED_COMBINATIONS = {
    ("warfarin", "vitamin_k"): {
        "severity": "HIGH",
        "reason": "Vitamin K antagonizes warfarin anticoagulation",
        "action": "Maintain consistent vitamin K intake, not supplement"
    },
    ("methotrexate", "folic_acid"): {
        "severity": "MODERATE",
        "reason": "Folic acid may reduce methotrexate efficacy for cancer",
        "action": "Consult oncologist before supplementing (timing critical)"
    },
}

TOXIC_DOSES = {
    "Vitamin A": {"max_daily": 3000, "unit": "IU/day", "risk": "liver toxicity"},
    "Vitamin D": {"max_daily": 4000, "unit": "IU/day", "risk": "hypercalcemia"},
    "Iron": {"max_daily": 45, "unit": "mg/day", "risk": "iron overload"},
    "Selenium": {"max_daily": 400, "unit": "µg/day", "risk": "selenosis"},
    "Zinc": {"max_daily": 40, "unit": "mg/day", "risk": "copper deficiency"},
    "Niacin": {"max_daily": 35, "unit": "mg/day", "risk": "liver damage"},
}

async def check_emergency_symptoms(symptoms: list[str]) -> dict:
    """
    Check if patient has emergency symptoms requiring immediate medical attention.
    
    Returns:
        dict: {
            "is_emergency": bool,
            "detected_symptoms": list,
            "recommendation": str,
            "action": str  # "PROCEED" or "HALT"
        }
    """
    normalized_symptoms = [s.lower().strip() for s in symptoms]
    detected_emergencies = [
        sym for sym in normalized_symptoms 
        if sym in EMERGENCY_SYMPTOMS
    ]
    
    if detected_emergencies:
        return {
            "is_emergency": True,
            "detected_symptoms": detected_emergencies,
            "recommendation": "🚨 EMERGENCY DETECTED: Patient requires immediate medical attention",
            "action": "HALT",
            "call_911": True,
            "details": f"Detected emergency symptoms: {', '.join(detected_emergencies)}"
        }
    
    return {
        "is_emergency": False,
        "detected_symptoms": [],
        "recommendation": "No emergency symptoms detected",
        "action": "PROCEED",
        "call_911": False
    }

async def check_medication_interactions(medications: list[str], recommendations: dict) -> dict:
    """
    Check recommended supplements against current medications for interactions.
    
    Returns:
        dict: {
            "has_interactions": bool,
            "interactions": list,
            "warnings": list,
            "approved_recommendations": dict
        }
    """
    interactions = []
    warnings = []
    approved_recommendations = recommendations.copy()
    
    medications_lower = [m.lower() for m in medications]
    
    for med_pair, interaction_data in CONTRAINDICATED_COMBINATIONS.items():
        med, nutrient = med_pair
        if med in medications_lower and nutrient in recommendations:
            interaction_info = {
                "medication": med,
                "nutrient": nutrient,
                "severity": interaction_data["severity"],
                "reason": interaction_data["reason"],
                "action": interaction_data["action"]
            }
            
            if interaction_data["severity"] == "HIGH":
                interactions.append(interaction_info)
                # Remove from approved recommendations
                if nutrient in approved_recommendations:
                    del approved_recommendations[nutrient]
            else:
                warnings.append(interaction_info)
    
    return {
        "has_interactions": len(interactions) > 0,
        "interactions": interactions,
        "warnings": warnings,
        "approved_recommendations": approved_recommendations
    }

async def check_toxic_doses(recommendations: dict) -> dict:
    """
    Validate recommended doses are within safe upper limits.
    
    Returns:
        dict: {
            "safe": bool,
            "dose_violations": list,
            "corrected_recommendations": dict
        }
    """
    dose_violations = []
    corrected_recommendations = {}
    
    for nutrient, recommendation in recommendations.items():
        if nutrient in TOXIC_DOSES and "dose" in recommendation:
            try:
                suggested_dose = float(recommendation["dose"].split()[0])
                limit = TOXIC_DOSES[nutrient]["max_daily"]
                
                if suggested_dose > limit:
                    violation = {
                        "nutrient": nutrient,
                        "suggested_dose": f"{suggested_dose} {TOXIC_DOSES[nutrient]['unit']}",
                        "max_allowed": f"{limit} {TOXIC_DOSES[nutrient]['unit']}",
                        "risk": TOXIC_DOSES[nutrient]["risk"],
                        "correction": f"Reduce to {limit} {TOXIC_DOSES[nutrient]['unit']}"
                    }
                    dose_violations.append(violation)
                    
                    # Correct the recommendation
                    corrected_recommendations[nutrient] = recommendation.copy()
                    corrected_recommendations[nutrient]["dose"] = f"{limit} {TOXIC_DOSES[nutrient]['unit']}"
                else:
                    corrected_recommendations[nutrient] = recommendation
            except (ValueError, KeyError, AttributeError):
                corrected_recommendations[nutrient] = recommendation
        else:
            corrected_recommendations[nutrient] = recommendation
    
    return {
        "safe": len(dose_violations) == 0,
        "dose_violations": dose_violations,
        "corrected_recommendations": corrected_recommendations
    }

async def check_all_safety_guardrails(symptoms: list[str], medications: list[str], recommendations: dict) -> dict:
    """
    Run all safety checks before returning diagnosis.
    
    Returns:
        dict with complete safety assessment
    """
    # Check 1: Emergency symptoms
    emergency_check = await check_emergency_symptoms(symptoms)
    if emergency_check["is_emergency"]:
        return {
            "safe": False,
            "reason": "EMERGENCY",
            "emergency_check": emergency_check,
            "interaction_check": None,
            "dose_check": None,
            "approved_recommendations": {},
            "warnings": [],
            "recommendation": "🚨 Call 911 immediately"
        }
    
    # Check 2: Medication interactions
    interaction_check = await check_medication_interactions(medications, recommendations)
    approved_after_interactions = interaction_check["approved_recommendations"]
    
    # Check 3: Toxic dose detection
    dose_check = await check_toxic_doses(approved_after_interactions)
    
    return {
        "safe": (not emergency_check["is_emergency"]) and dose_check["safe"],
        "emergency_check": emergency_check,
        "interaction_check": interaction_check,
        "dose_check": dose_check,
        "approved_recommendations": dose_check["corrected_recommendations"],
        "warnings": [
            w for w in interaction_check["warnings"]
        ] + [
            {"type": "dose_warning", "data": v} 
            for v in dose_check["dose_violations"] if not dose_check["safe"]
        ]
    }
