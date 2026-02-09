import dramatiq
from dramatiq.brokers.redis import RedisBroker
from dramatiq.middleware import CurrentMessage 
import redis 
import json
import ollama
import re

# Setup broker with Middleware
# CRITICAL: get_current_message() requires this middleware to be explicitly added
redis_broker = RedisBroker(url="redis://localhost:6379/0")
redis_broker.add_middleware(CurrentMessage()) 
dramatiq.set_broker(redis_broker)

# Results database
status_db = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

@dramatiq.actor(max_retries=3)
def generate_ai_diagnosis(user_id, patient_data):
    try:
        symptoms_list = ", ".join(patient_data['symptoms'])
        
        # 1. Real AI System Prompt
        system_instructions = (
            "ACT AS: A Senior Functional Medicine Clinician specialized in micronutrient biochemistry. "
            "CONTEXT: You are analyzing a patient profile derived from a weighted 0-4 point scale "
            "Medical Symptom Questionnaire (MSQ). "
            
            "DIAGNOSTIC GUIDELINES: "
            "1. SYSTEMIC CLUSTERING: Do not analyze symptoms in isolation. Group indicators by system. "
            "   - Oral/Dental + Energy often signals Vitamin D/Calcium enamel thinning or B12 gaps. [3, 4]"
            "   - Appendage changes (nails/hair) + Sluggishness signals Iron/Biotin mineralization issues."
            "   - Skin texture + Sun-sensitivity signals Niacin (B3) or Zinc disruption."
            "2. PATHOGNOMONIC PRIORITY: Prioritize highly specific signs. For example, 'spoon-shaped nails' is "
            "   a classic marker for Anemia, and 'yellow teeth' in a non-smoker suggests enamel porosity. [5, 6, 7]"
            "3. CALCULATION: A total MSQ score > 50 indicates high metabolic dysfunction."

            "OUTPUT REQUIREMENTS: "
            "You must return ONLY a structured JSON object. "
            "Keys: "
            "- 'diagnosis': A high-fidelity summary of suspected deficiencies. "
            "- 'clinician_notes': Use 'Explainable AI' (XAI) heuristics. Detail the reasoning 'why' specific "
            "  symptom clusters led to this conclusion. Use calm, authoritative language."
            "- 'confidence_score': An integer (0-100) reflecting the density and specificity of the provided symptoms. "
            
            "RESTRICTION: Return NO introductory text or reasoning tags like <think>. Return ONLY the JSON."
        )

        user_input = (
            f"Patient: {patient_data['age']}yo {patient_data['sex']}. "
            f"Symptoms: {symptoms_list}. "
            "Generate report in JSON."
        )

        # 2. Local Inference using DeepSeek-R1 via Ollama
        response = ollama.chat(
            model='deepseek-r1:8b',
            messages=[
                {'role': 'system', 'content': system_instructions},
                {'role': 'user', 'content': user_input}
            ]
        )
        
        raw_text = response['message']['content']

        # 3. Robust Regex Extraction
        # DeepSeek includes reasoning in <think> tags. This finds the JSON block only.
        json_match = re.search(r'\{.*\}', raw_text, re.DOTALL)
        if not json_match:
            raise ValueError("AI response did not contain a valid JSON block.")
            
        ai_data = json.loads(json_match.group())

        # 4. Data Coercion Fix
        # Prevents "data.diagnosis.toLowerCase is not a function" on React
        diagnosis_val = ai_data.get('diagnosis', "Unknown Deficiency")
        if isinstance(diagnosis_val, dict):
            diagnosis_val = diagnosis_val.get('primary_condition', str(diagnosis_val))

        final_output = {
            "diagnosis": str(diagnosis_val), # Force String coercion
            "clinician_notes": str(ai_data.get('clinician_notes', "Verification recommended.")),
            "confidence": ai_data.get('confidence_score', "N/A"),
            "user_info": {
                "name": patient_data.get('user_name'),
                "age": patient_data.get('age'),
                "sex": patient_data.get('sex')
            }
        }

        # 5. Store result in Redis
        message = CurrentMessage.get_current_message()
        if message:
            msg_id = message.message_id
            status_db.set(f"result:{msg_id}", json.dumps(final_output))
            status_db.set(f"status:{msg_id}", "completed")

    except Exception as e:
        message = CurrentMessage.get_current_message()
        if message:
            status_db.set(f"status:{message.message_id}", "failed")
        raise e
    
@dramatiq.actor(max_retries=3)
def generate_meal_plan(diagnosis, preferences):
    try:
        # 1. Specialized Prompt for Bioavailability [2]
        system_instructions = (
            "ACT AS: A Clinical Dietitian and Gourmet Chef. "
            "TASK: Generate a 2-day sample meal plan to address a specific deficiency. "
            "RULES: "
            f"1. ADHERENCE: Strictly follow these preferences: {preferences}. "
            f"2. SAFETY: Omit all ingredients related to these allergies: {preferences['allergies']}. "
            "3. NUTRITION: Prioritize high nutrient density for the diagnosed condition. "
            "FORMAT: Return ONLY a JSON list of objects with 'name', 'rationale', 'prep_time'."
        )

        user_input = f"Diagnosis: {diagnosis}. Generate a plan in JSON format."

        # 2. Local Inference via DeepSeek-R1 [3, 4]
        response = ollama.chat(
            model='deepseek-r1:8b',
            messages=[
                {'role': 'system', 'content': system_instructions},
                {'role': 'user', 'content': user_input}
            ]
        )
        
        raw_text = response['message']['content']
        json_match = re.search(r'\[.*\]', raw_text, re.DOTALL) # Match JSON array
        
        if not json_match:
            raise ValueError("AI failed to generate a recipe list.")

        recipes = json.loads(json_match.group())

        # 3. Store in Redis using a unique key for recipes
        msg = CurrentMessage.get_current_message()
        if msg:
            status_db.set(f"recipes_result:{msg.message_id}", json.dumps(recipes))
            status_db.set(f"recipes_status:{msg.message_id}", "completed")

    except Exception as e:
        msg = CurrentMessage.get_current_message()
        if msg:
            status_db.set(f"recipes_status:{msg.message_id}", "failed")
        raise e    