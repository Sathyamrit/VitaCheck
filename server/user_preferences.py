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