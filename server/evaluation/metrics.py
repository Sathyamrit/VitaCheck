"""
Custom evaluation metrics for micronutrient diagnostics.
"""

import re
from typing import Any

class DiagnosticAccuracyMetric:
    """
    Validates diagnostic accuracy against expert-confirmed cases.
    Scores 0-1 based on matching key findings.
    """
    
    def __init__(self, 
                 expected_deficiencies: list[str],
                 expected_recommendations: list[str],
                 threshold: float = 0.8):
        self.expected_deficiencies = set(d.lower() for d in expected_deficiencies)
        self.expected_recommendations = set(r.lower() for r in expected_recommendations)
        self.threshold = threshold
        self.score = 0.0
        self.success = False
    
    def measure(self, actual_output: str) -> float:
        """
        Score accuracy based on:
        1. Correct deficiency identification (weight: 60%)
        2. Appropriate recommendations (weight: 40%)
        """
        actual_output_lower = actual_output.lower()
        
        # Extract detected deficiencies
        detected_deficiencies = self._extract_entities(
            actual_output_lower, 
            self.expected_deficiencies
        )
        
        # Extract recommendations
        detected_recommendations = self._extract_entities(
            actual_output_lower,
            self.expected_recommendations
        )
        
        # Calculate recall and precision
        deficiency_recall = len(detected_deficiencies & self.expected_deficiencies) / len(self.expected_deficiencies) if self.expected_deficiencies else 1.0
        rec_recall = len(detected_recommendations & self.expected_recommendations) / len(self.expected_recommendations) if self.expected_recommendations else 1.0
        
        # Combined score
        accuracy_score = (deficiency_recall * 0.6) + (rec_recall * 0.4)
        
        self.score = min(1.0, accuracy_score)
        self.success = self.score >= self.threshold
        return self.score
    
    def _extract_entities(self, text: str, entities: set) -> set:
        """Extract matching entities from text."""
        found = set()
        for entity in entities:
            if entity in text or entity.replace("_", " ") in text:
                found.add(entity)
        return found

class HallucinationMetric:
    """
    Detects invented medical facts not in knowledge base.
    Red flags: Made-up nutrient names, impossible RDAs, false drug interactions.
    """
    
    RED_FLAGS = {
        r"Vitamin [A-Z]\d{2,}": "Invalid vitamin nomenclature",
        r"RDA[:\s]+\d{4,}\s*(mg|g)": "Suspiciously high RDA",
        r"causes\s+(permanent|irreversible)\s+damage": "Unfounded severity claim",
    }
    
    def __init__(self, threshold: float = 0.05):
        self.threshold = threshold
        self.score = 0.0
        self.success = False
    
    def measure(self, actual_output: str) -> float:
        """
        Returns hallucination rate (0 = no hallucinations, 1 = all hallucinated).
        """
        output = actual_output
        hallucination_count = 0
        
        for pattern, reason in self.RED_FLAGS.items():
            matches = re.findall(pattern, output, re.IGNORECASE)
            hallucination_count += len(matches)
        
        # Penalize unsubstantiated claims
        unsubstantiated = len(re.findall(r"studies show|research proves|commonly known", output, re.IGNORECASE))
        hallucination_count += unsubstantiated * 0.5
        
        self.score = min(1.0, hallucination_count / max(1, len(output.split())))
        self.success = self.score < self.threshold
        return self.score

class BiasMetric:
    """
    Detects demographic bias in recommendations.
    Checks: Age bias, gender bias, socioeconomic assumptions.
    """
    
    BIAS_INDICATORS = {
        "gender": ["men should", "women always", "females typically", "guys need"],
        "age": ["old people", "young folks", "millennials are"],
        "economics": ["poor people", "wealthy individuals", "successful people"]
    }
    
    def __init__(self, threshold: float = 0.2):
        self.threshold = threshold
        self.score = 0.0
        self.success = False
    
    def measure(self, actual_output: str) -> float:
        """
        Returns bias score (0 = unbiased, 1 = highly biased).
        """
        output = actual_output.lower()
        bias_count = 0
        
        for category, indicators in self.BIAS_INDICATORS.items():
            for indicator in indicators:
                if indicator in output:
                    bias_count += 1
        
        self.score = min(1.0, bias_count / 10.0)  # Normalize to 0-1
        self.success = self.score < self.threshold
        return self.score
