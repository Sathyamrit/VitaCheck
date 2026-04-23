"""
Unit tests for safety guardrails.
"""

import pytest
import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from guardrails import (
    check_emergency_symptoms,
    check_medication_interactions,
    check_toxic_doses,
    check_all_safety_guardrails
)

# Run async tests with pytest-asyncio
pytestmark = pytest.mark.asyncio

@pytest.fixture
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

async def test_emergency_detection_positive():
    """Test emergency symptom detection - positive case."""
    result = await check_emergency_symptoms(["chest pain", "difficulty breathing"])
    assert result["is_emergency"] == True
    assert len(result["detected_symptoms"]) > 0
    assert result["action"] == "HALT"

async def test_emergency_detection_negative():
    """Test emergency symptom detection - negative case."""
    result = await check_emergency_symptoms(["fatigue", "muscle pain"])
    assert result["is_emergency"] == False
    assert len(result["detected_symptoms"]) == 0
    assert result["action"] == "PROCEED"

async def test_medication_interactions_high_severity():
    """Test medication-nutrient interaction detection - HIGH severity."""
    result = await check_medication_interactions(
        medications=["warfarin"],
        recommendations={"vitamin_k": {"dose": "500 µg/day"}}
    )
    assert result["has_interactions"] == True
    assert "vitamin_k" not in result["approved_recommendations"]
    assert len(result["interactions"]) > 0

async def test_medication_interactions_none():
    """Test no interactions when medications are safe."""
    result = await check_medication_interactions(
        medications=["aspirin"],
        recommendations={"vitamin_c": {"dose": "1000 mg/day"}}
    )
    assert result["has_interactions"] == False
    assert "vitamin_c" in result["approved_recommendations"]

async def test_toxic_dose_prevention():
    """Test toxic dose detection and correction."""
    result = await check_toxic_doses({
        "Iron": {"dose": "100 mg/day", "form": "ferrous sulfate"}
    })
    assert result["safe"] == False
    assert len(result["dose_violations"]) > 0
    corrected_dose = result["corrected_recommendations"]["Iron"]["dose"]
    assert "45" in corrected_dose

async def test_toxic_dose_safe():
    """Test safe dose passes through."""
    result = await check_toxic_doses({
        "Iron": {"dose": "25 mg/day", "form": "ferrous sulfate"}
    })
    assert result["safe"] == True
    assert len(result["dose_violations"]) == 0

async def test_comprehensive_safety_emergency():
    """Test all guardrails together - emergency case."""
    result = await check_all_safety_guardrails(
        symptoms=["chest pain"],
        medications=["warfarin"],
        recommendations={"vitamin_k": {}}
    )
    assert result["safe"] == False
    assert result["emergency_check"]["is_emergency"] == True

async def test_comprehensive_safety_safe():
    """Test all guardrails together - safe case."""
    result = await check_all_safety_guardrails(
        symptoms=["fatigue", "muscle pain"],
        medications=[],
        recommendations={"vitamin_d": {"dose": "2000 IU/day"}}
    )
    assert result["safe"] == True
    assert result["emergency_check"]["is_emergency"] == False

# Run tests
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
