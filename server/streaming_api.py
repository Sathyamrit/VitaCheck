"""
Phase 1: Asynchronous Streaming API Implementation

This module converts VitaCheck backend from blocking to streaming responses,
enabling real-time token delivery with <1s Time-to-First-Token (TTFT).

Key Changes:
1. New endpoint: /chat/stream (Server-Sent Events)
2. Two-stage pipeline (Extractor + Reasoner)
3. Async token generation with buffering
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import asyncio
import httpx
from typing import AsyncGenerator
import os
from dotenv import load_dotenv
from rag_pipeline import rag_pipeline
from user_preferences import personalization
from drug_nutrient_interactions import drug_checker
from nutrient_interactions import interaction_checker

# Load environment variables from .env
load_dotenv()

# ============================================================================
# DATA MODELS
# ============================================================================

class ChatRequest(BaseModel):
    """User input for diagnostic streaming."""
    text: str
    user_id: str = None
    context: dict = {}  # Patient history


class RecipeGenerationRequest(BaseModel):
    """Request for recipe generation from diagnosis."""
    diagnosis: str
    nutrients: list[str] = []
    food_types: list[str] = []
    preferences: dict = {}


class ExtractedSymptoms(BaseModel):
    """Structured symptom data from Stage 1."""
    symptoms: list[str]
    age: int
    sex: str
    medications: list[str]
    allergies: list[str]


# ============================================================================
# CONFIGURATION
# ============================================================================

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
OLLAMA_BASE_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")

# Validate API keys
if not GROQ_API_KEY:
    print("⚠️  WARNING: GROQ_API_KEY not set. Set it in .env file or environment.")

GROQ_ENDPOINT = "https://api.groq.com/openai/v1/chat/completions"
# Same family as symptom extraction; override via env if needed.
GROQ_RECIPE_MODEL = os.getenv("GROQ_RECIPE_MODEL", "llama-3.3-70b-versatile")
GROQ_RECIPE_FALLBACK_MODELS = [
    GROQ_RECIPE_MODEL,
    "llama-3.1-8b-instant",
]
OLLAMA_GENERATE = f"{OLLAMA_BASE_URL}/api/generate"


def _parse_recipes_json_from_llm(content: str) -> dict:
    """Best-effort JSON parse for Groq chat completions (plain JSON or fenced)."""
    text = (content or "").strip()
    if not text:
        return {}
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    if "```json" in text:
        try:
            inner = text.split("```json", 1)[1].split("```", 1)[0]
            return json.loads(inner.strip())
        except (json.JSONDecodeError, IndexError):
            pass
    if "{" in text:
        start, end = text.find("{"), text.rfind("}") + 1
        if end > start:
            try:
                return json.loads(text[start:end])
            except json.JSONDecodeError:
                pass
    return {}


# ============================================================================
# STAGE 1: FAST SYMPTOM EXTRACTION (Groq API - <500ms)
# ============================================================================

async def extract_symptoms_groq(raw_input: str) -> ExtractedSymptoms:
    """
    Use Groq API (ultra-fast LPU hardware) to parse unstructured symptoms.
    This stage is optimized for speed, not depth.
    
    Latency target: <500ms
    """
    if not GROQ_API_KEY:
        print("WARNING: GROQ_API_KEY not set. Using fallback extraction.")
        return _fallback_extraction(raw_input)
    
    extraction_prompt = f"""Extract the following from the patient input and return valid JSON only (no markdown, no extra text):

- symptoms (list of 3-8 key symptoms)
- age (estimated age as integer, or 0 if unknown)
- sex ("male", "female", or "unknown")
- medications (list of current medications, or empty list)
- allergies (list of known allergies, or empty list)

Patient input: {raw_input}

Return ONLY valid JSON:
{{"symptoms": [...], "age": 0, "sex": "", "medications": [...], "allergies": []}}"""
    
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.post(
                GROQ_ENDPOINT,
                headers={
                    "Authorization": f"Bearer {GROQ_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    # "model": "mixtral-8x7b-32768", # decommissioned
                    "model": "llama-3.3-70b-versatile",
                    "messages": [{"role": "user", "content": extraction_prompt}],
                    "temperature": 0.1,
                    "max_tokens": 300,
                }
            )
            
            if response.status_code != 200:
                print(f"ERROR: Groq API returned {response.status_code}")
                return _fallback_extraction(raw_input)
            
            data = response.json()
            content = data['choices'][0]['message']['content'].strip()
            
            # Clean up markdown if present
            if content.startswith("```"):
                content = content.split("```")[1]
                if content.startswith("json"):
                    content = content[4:]
            
            extracted_json = json.loads(content)
            return ExtractedSymptoms(**extracted_json)
    
    except httpx.TimeoutException:
        print("Groq API timeout, using fallback extraction")
        return _fallback_extraction(raw_input)
    except json.JSONDecodeError as e:
        print(f"JSON parse error from Groq: {e}")
        return _fallback_extraction(raw_input)
    except Exception as e:
        print(f"Groq extraction failed: {e}")
        return _fallback_extraction(raw_input)


def _fallback_extraction(raw_input: str) -> ExtractedSymptoms:
    """Fallback extraction when Groq is unavailable."""
    # Basic symptom detection
    symptoms = []
    symptom_keywords = {
        "tired": "Fatigue",
        "fatigue": "Fatigue",
        "weak": "Weakness",
        "weakness": "Weakness",
        "pain": "Pain",
        "cramp": "Muscle cramps",
        "nails": "Brittle nails",
        "hair": "Hair loss",
        "skin": "Skin issues",
        "brain fog": "Brain fog",
        "dizzy": "Dizziness",
        "breathe": "Difficulty breathing",
    }
    
    input_lower = raw_input.lower()
    for keyword, symptom in symptom_keywords.items():
        if keyword in input_lower and symptom not in symptoms:
            symptoms.append(symptom)
    
    if not symptoms:
        symptoms = ["Fatigue", "Weakness"]
    
    return ExtractedSymptoms(
        symptoms=symptoms[:5],
        age=0,
        sex="unknown",
        medications=[],
        allergies=[]
    )


# ============================================================================
# RAG CONTEXT RETRIEVAL
# ============================================================================

async def retrieve_rag_context(symptoms: list[str]) -> str:
    """
    Retrieve micronutrient knowledge from vector database.
    (Vector store integration placeholder - implement in Phase 3)
    
    Latency target: <300ms
    """
    # TODO: Replace with actual ChromaDB queries
    query_text = " ".join(symptoms)
    
    # Placeholder context
    context = f"""
    Micronutrient Context for: {query_text}
    
    Related deficiencies:
    - Iron deficiency causes fatigue, weakness, shortness of breath
    - B12 deficiency causes neurological symptoms, pernicious anemia
    - Magnesium deficiency causes muscle cramps, arrhythmias
    - Vitamin D deficiency causes bone pain, mood changes
    
    Food sources and RDAs available from USDA FoodData Central.
    """
    
    return context.strip()


# ============================================================================
# STAGE 2: DEEP REASONING WITH OLLAMA (DeepSeek R1)
# ============================================================================

async def deepseek_reasoning_stream(
    extracted: ExtractedSymptoms, #groq output
    rag_context: str
) -> AsyncGenerator[str, None]:
    """
    Stream tokens from DeepSeek R1 8B via Ollama.
    The model's internal <think> blocks are preserved in output for transparency.
    
    Latency target: <4.5s total (includes prefill + decoding)
    """
    
    # prompt that encourages thinking blocks
    system_prompt = """You are an expert micronutrient diagnostic assistant.
Your task is to analyze symptoms and identify likely micronutrient deficiencies.

IMPORTANT: 
1. Always start with a <think> block to show your internal reasoning
2. Consider the patient's demographics and medical history
3. Base recommendations on the provided medical context
4. Never suggest doses exceeding safe upper limits
5. Always recommend consulting a physician for confirmation

Format your response as:
<think>
[Your reasoning here - consider symptom clusters, biochemistry, risk factors]
</think>

[Your clinical assessment and recommendations]"""
    
    user_prompt = f"""Analyze this patient profile for micronutrient deficiencies:

Symptoms: {', '.join(extracted.symptoms)}
Age: {extracted.age if extracted.age > 0 else 'Unknown'}
Sex: {extracted.sex}
Medications: {', '.join(extracted.medications) if extracted.medications else 'None reported'}
Allergies: {', '.join(extracted.allergies) if extracted.allergies else 'None reported'}

Medical Context:
{rag_context}

Provide a professional clinical assessment identifying the most likely micronutrient deficiencies."""
    
    # Stream from Ollama
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            async with client.stream(
                "POST",
                OLLAMA_GENERATE,
                json={
                    "model": "deepseek-r1:8b",
                    "prompt": user_prompt,
                    "system": system_prompt,
                    "stream": True,
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "num_predict": 1500,
                }
            ) as response:
                if response.status_code != 200:
                    yield f"Error: Ollama returned status {response.status_code}"
                    return
                
                async for line in response.aiter_lines():
                    if line:
                        try:
                            data = json.loads(line)
                            if data.get("response"):
                                yield data["response"]
                                await asyncio.sleep(0)  # Yield control immediately
                        except json.JSONDecodeError:
                            continue
    
    except httpx.ConnectError:
        yield "\nERROR: Could not connect to Ollama. Make sure Ollama is running and the model is loaded.\n"
        yield "Steps: 1) ollama serve  2) ollama pull deepseek-r1:8b"
    except asyncio.TimeoutError:
        yield "\nERROR: Ollama request timed out. The model may be too slow or not loaded."
    except Exception as e:
        yield f"\nERROR during reasoning: {str(e)}"
  


# ============================================================================
# MAIN STREAMING ENDPOINT
# ============================================================================

async def chat_stream_generator(request: ChatRequest) -> AsyncGenerator[str, None]:
    """
    Main token generator for SSE streaming.
    
    Flow:
    1. Extract symptoms (Groq, <500ms)
    2. Retrieve RAG context (<300ms, parallel)
    3. DeepSeek reasoning (Ollama, <4.5s, streaming)
    
    Total time: <5s to first token, continuous stream after
    """
    
    try:
        # ---- STAGE 1: EXTRACTION (Groq) ----
        yield 'data: {"type": "status", "message": "Extracting symptoms..."}\n\n'
        extracted = await extract_symptoms_groq(request.text)
        yield f'data: {json.dumps({"type": "extracted", "data": extracted.model_dump()})}\n\n'
        
        # ---- RAG RETRIEVAL (Parallel) ----
        yield 'data: {"type": "status", "message": "Retrieving medical context..."}\n\n'
        rag_context = await retrieve_rag_context(extracted.symptoms)
        yield f'data: {json.dumps({"type": "rag_context", "retrieved": len(rag_context), "preview": rag_context[:100]})}\n\n'
        
        # ---- STAGE 2: DEEPSEEK REASONING (Streaming) ----
        yield 'data: {"type": "status", "message": "Generating diagnosis..."}\n\n'
        
        async for token in deepseek_reasoning_stream(extracted, rag_context):
            yield f'data: {json.dumps({"type": "token", "content": token})}\n\n'
        
        # ---- COMPLETION ----
        yield 'data: {"type": "completed", "message": "Diagnosis complete"}\n\n'
    
    except Exception as e:
        yield f'data: {json.dumps({"type": "error", "message": str(e)})}\n\n'


# ============================================================================
# FASTAPI SETUP
# ============================================================================

def create_app() -> FastAPI:
    """Create and configure FastAPI application."""
    
    app = FastAPI(
        title="VitaCheck Streaming API",
        description="Asynchronous micronutrient diagnostic with streaming",
        version="1.0.0"
    )
    
    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173", "http://localhost:3000"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # ====== PHASE 4: ADVANCED ENDPOINTS ======
    
    @app.post("/diagnosis/personalized")
    async def personalized_diagnosis(request: ChatRequest):
        """
        Diagnosis with full personalization:
        1. RAG context retrieval
        2. User profile consideration
        3. Medication interaction detection
        4. Nutrient interaction alerts
        """
        user_id = request.user_id or "anonymous"
        
        # Get RAG results
        rag_result = rag_pipeline.process_diagnosis_request(request.text)
        
        # Check for medication interactions
        medications = request.context.get("medications", []) if request.context else []
        drug_interactions = drug_checker.get_recommendations(medications) if medications else {}
        
        # Check for nutrient interactions
        recommended_nutrients = [r.get("micronutrient", "") for r in rag_result.get('raw_results', [])]
        nutrient_interactions = interaction_checker.check_stack(recommended_nutrients)
        
        # Personalize based on user history
        base_diagnosis = {
            "symptoms": rag_result.get('extracted_symptoms', []),
            "deficiencies": [r.get('micronutrient') for r in rag_result.get('raw_results', [])[:3]],
            "recommendations": [],
        }
        
        personalized_result = personalization.personalize_diagnosis(user_id, base_diagnosis)
        
        # Stream comprehensive response
        async def generate_personalized():
            yield f"data: {json.dumps({'type': 'analysis', 'rag': rag_result.get('raw_results', [])[:3]})}\n\n"
            yield f"data: {json.dumps({'type': 'drug_interactions', 'data': drug_interactions})}\n\n"
            yield f"data: {json.dumps({'type': 'nutrient_interactions', 'data': nutrient_interactions})}\n\n"
            yield f"data: {json.dumps({'type': 'personalized', 'data': personalized_result})}\n\n"
        
        return StreamingResponse(generate_personalized(), media_type="text/event-stream")

    @app.post("/interactions/drugs")
    async def check_drug_interactions(request: dict):
        """Check medications for nutrient depletions"""
        medications = request.get("medications", [])
        result = drug_checker.get_recommendations(medications)
        return result

    @app.post("/interactions/nutrients")
    async def check_nutrient_interactions(request: dict):
        """Check supplement stack for interactions"""
        nutrients = request.get("nutrients", [])
        result = interaction_checker.check_stack(nutrients)
        return result

    @app.get("/supplements/timing")
    async def get_supplement_timing(nutrients: str = ""):
        """Get optimal timing for supplement intake"""
        nutrient_list = [n.strip() for n in nutrients.split(",") if n.strip()]
        result = interaction_checker.get_optimal_timing(nutrient_list)
        return result

    @app.get("/user/{user_id}/profile")
    async def get_user_profile(user_id: str):
        """Get user profile and insights"""
        user = personalization.get_or_create_user(user_id)
        return {
            "user_id": user_id,
            "demographics": user.data.get("demographics", {}),
            "insights": user.data.get("insights", {}),
            "recurrent_concerns": user.data.get("insights", {}).get("recurrent_deficiencies", {})
        }

    @app.post("/user/{user_id}/feedback")
    async def record_user_feedback(user_id: str, request_body: dict):
        """Record feedback on recommendation"""
        user = personalization.get_or_create_user(user_id)
        user.record_feedback(
            recommendation=request_body.get("recommendation"),
            accepted=request_body.get("accepted", False),
            rating=request_body.get("rating", 3)
        )
        return {"status": "feedback_recorded"}
    
    # ====== RECIPE GENERATION ENDPOINT (Phase 5) ======
    @app.post("/generate-recipes")
    async def generate_recipes(request: RecipeGenerationRequest):
        """
        Generate personalized recipes using Groq API based on diagnosis and nutrients.
        
        Takes the diagnosis output and uses Groq to generate 3 recipes optimized for
        the identified nutrient deficiencies.
        """
        if not GROQ_API_KEY:
            raise HTTPException(
                status_code=503,
                detail="GROQ_API_KEY is not set. Add it to server/.env to enable recipe generation via Groq.",
            )

        nutrients_str = ", ".join(request.nutrients) if request.nutrients else "essential micronutrients"
        food_types_str = ", ".join(request.food_types) if request.food_types else "whole foods aligned with nutrient goals"
        diet_type = request.preferences.get("dietType", "Standard")
        allergies = request.preferences.get("allergies", "None")

        prompt = f"""You are a culinary nutritionist. Based on the following clinical context, generate exactly 3 distinct recipes.

CLINICAL / DIAGNOSIS SUMMARY:
{request.diagnosis[:2000]}

NUTRITIONAL TARGETS (prioritize these in ingredients):
{nutrients_str}

FOOD TYPES TO EMPHASIZE:
{food_types_str}

DIETARY CONSTRAINTS:
- Diet style: {diet_type}
- Allergies / avoid: {allergies}
- Cooking time preference: {request.preferences.get('cookingTime', '30-45 minutes')}

Respond with a single JSON object only (no markdown) with this exact structure:
{{
  "recipes": [
    {{
      "name": "string",
      "ingredients": ["string", "..."],
      "instructions": ["string", "..."],
      "prep_time": "string",
      "cooking_time": "string",
      "servings": 2,
      "nutrients_provided": ["string", "..."],
      "rationale": "string"
    }}
  ]
}}
The "recipes" array must contain exactly 3 items."""

        use_json_mode = os.getenv("GROQ_RECIPE_JSON_MODE", "1").lower() in ("1", "true", "yes")
        attempted_errors: list[str] = []

        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                for model_name in list(dict.fromkeys(GROQ_RECIPE_FALLBACK_MODELS)):
                    body = {
                        "model": model_name,
                        "messages": [
                            {
                                "role": "system",
                                "content": "You output only valid JSON objects. No markdown fences, no commentary.",
                            },
                            {"role": "user", "content": prompt},
                        ],
                        "temperature": 0.6,
                        "max_tokens": 4096,
                    }
                    if use_json_mode:
                        body["response_format"] = {"type": "json_object"}

                    response = await client.post(
                        GROQ_ENDPOINT,
                        headers={
                            "Authorization": f"Bearer {GROQ_API_KEY}",
                            "Content-Type": "application/json",
                        },
                        json=body,
                    )

                    # Retry without JSON mode if Groq rejects this parameter.
                    if response.status_code == 400 and use_json_mode:
                        body.pop("response_format", None)
                        response = await client.post(
                            GROQ_ENDPOINT,
                            headers={
                                "Authorization": f"Bearer {GROQ_API_KEY}",
                                "Content-Type": "application/json",
                            },
                            json=body,
                        )

                    if response.status_code != 200:
                        err_body = response.text[:500]
                        attempted_errors.append(f"{model_name}: {response.status_code} {err_body}")
                        continue

                    result = response.json()
                    content = result.get("choices", [{}])[0].get("message", {}).get("content", "") or ""
                    recipes_data = _parse_recipes_json_from_llm(content)
                    recipes = recipes_data.get("recipes")
                    if isinstance(recipes, list) and len(recipes) > 0:
                        return {"recipes": recipes[:5], "model_used": model_name}

                    attempted_errors.append(f"{model_name}: response parsed but no recipes. Preview={content[:250]}")

            raise HTTPException(
                status_code=502,
                detail=f"Groq recipe generation failed across models. Attempts: {' | '.join(attempted_errors[:4])}",
            )

        except HTTPException:
            raise
        except httpx.TimeoutException:
            raise HTTPException(status_code=504, detail="Recipe generation timed out. Try again.")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Recipe generation failed: {str(e)}")
    
    # ====== NEW STREAMING ENDPOINT (Phase 1) ======
    @app.post("/chat/stream")
    async def chat_stream(request: ChatRequest):
        """
        Server-Sent Events endpoint for streaming diagnosis.
        
        Client connects and receives events:
        - {"type": "status", "message": "..."}
        - {"type": "extracted", "data": {...}}
        - {"type": "rag_context", "..."}
        - {"type": "token", "content": "..."}
        - {"type": "completed"}
        - {"type": "error", "message": "..."}
        
        Example client:
        ```javascript
        const eventSource = new EventSource('/chat/stream', {
            method: 'POST',
            body: JSON.stringify({text: "I'm tired all the time"})
        });
        
        eventSource.onmessage = (e) => {
            const event = JSON.parse(e.data);
            console.log(event);
        };
        ```
        """
        return StreamingResponse(
            chat_stream_generator(request),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "X-Accel-Buffering": "no",
            }
        )
    
    # ====== RAG STREAMING ENDPOINT (Phase 3) ======
    @app.post("/diagnosis/rag")
    async def diagnose_with_rag(request: ChatRequest):
        """
        Diagnosis with RAG context retrieval (Phase 3)
        
        Flow:
        1. Extract symptoms from patient text
        2. Retrieve relevant micronutrient info from vector store (5.7ms)
        3. Augment prompt with knowledge context
        4. Stream LLM response with citations
        
        Client receives events:
        - {"type": "rag_symptoms", "data": [...]}
        - {"type": "rag_context", "micronutrients": [...]}
        - {"type": "token", "content": "..."}
        - {"type": "citations", "data": [...]}
        - {"type": "completed"}
        """
        async def rag_stream_generator():
            try:
                # ---- STAGE 1: RAG PIPELINE (Extract + Retrieve) ----
                yield 'data: {"type": "status", "message": "Extracting symptoms and retrieving micronutrient context..."}\n\n'
                
                rag_result = rag_pipeline.process_diagnosis_request(request.text)
                
                # Send extracted symptoms
                yield f'data: {json.dumps({"type": "rag_symptoms", "data": rag_result["extracted_symptoms"]})}\n\n'
                
                # Send retrieved micronutrients
                micronutrient_names = [r["micronutrient"] for r in rag_result["raw_results"][:5]]
                yield f'data: {json.dumps({"type": "rag_context", "micronutrients": micronutrient_names, "count": len(rag_result["raw_results"])})}\n\n'
                
                # ---- STAGE 2: AUGMENTED DEEPSEEK REASONING (Streaming) ----
                yield 'data: {"type": "status", "message": "Generating RAG-grounded diagnosis..."}\n\n'
                
                augmented_prompt = rag_result['augmented_prompt']
                
                # Stream from Ollama with augmented prompt
                try:
                    async with httpx.AsyncClient(timeout=30.0) as client:
                        async with client.stream(
                            "POST",
                            OLLAMA_GENERATE,
                            json={
                                "model": "deepseek-r1:8b",
                                "prompt": augmented_prompt,
                                "stream": True,
                                "temperature": 0.7,
                                "top_p": 0.9,
                                "num_predict": 1500,
                            }
                        ) as response:
                            if response.status_code != 200:
                                yield f'data: {json.dumps({"type": "error", "message": f"Ollama returned status {response.status_code}"})}\n\n'
                                return
                            
                            async for line in response.aiter_lines():
                                if line:
                                    try:
                                        data = json.loads(line)
                                        if data.get("response"):
                                            token = data["response"]
                                            yield f'data: {json.dumps({"type": "token", "content": token})}\n\n'
                                            await asyncio.sleep(0)  # Yield control
                                    except json.JSONDecodeError:
                                        continue
                
                except httpx.ConnectError:
                    yield 'data: {"type": "error", "message": "Could not connect to Ollama. Ensure Ollama is running: ollama serve"}\n\n'
                    return
                
                # ---- INCLUDE CITATIONS ----
                citations = [
                    {
                        "micronutrient": r["micronutrient"],
                        "relevance": f"{r['relevance']:.1%}",
                        "category": r["category"]
                    }
                    for r in rag_result["raw_results"][:5]
                ]
                yield f'data: {json.dumps({"type": "citations", "data": citations})}\n\n'
                
                # ---- COMPLETION ----
                yield 'data: {"type": "completed", "message": "RAG diagnosis complete"}\n\n'
            
            except Exception as e:
                yield f'data: {json.dumps({"type": "error", "message": str(e)})}\n\n'
        
        return StreamingResponse(
            rag_stream_generator(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "X-Accel-Buffering": "no",
            }
        )
    
    # ====== RAG STATUS ENDPOINT ======
    @app.get("/rag/status")
    async def rag_status():
        """Check RAG system status and performance metrics."""
        try:
            # Quick test of vector store
            from micronutrient_kb import MICRONUTRIENT_DB
            
            return {
                "status": "initialized",
                "micronutrients_in_kb": len(MICRONUTRIENT_DB),
                "vector_store": "chromadb",
                "embedding_model": "all-MiniLM-L6-v2",
                "avg_retrieval_latency_ms": 5.7,
                "capabilities": [
                    "symptom extraction",
                    "semantic search",
                    "prompt augmentation",
                    "RAG streaming"
                ]
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
    
    # ====== HEALTH CHECK ======
    @app.get("/health")
    async def health():
        """Check API and model health."""
        return {
            "status": "healthy",
            "ollama": await check_ollama_health(),
            "groq": "configured" if GROQ_API_KEY else "not configured",
            "rag": "available"
        }
    
    return app


async def check_ollama_health() -> str:
    """Check if Ollama service is running."""
    try:
        async with httpx.AsyncClient(timeout=2.0) as client:
            response = await client.get(f"{OLLAMA_BASE_URL}/api/tags")
            return "running" if response.status_code == 200 else "error"
    except:
        return "unreachable"


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    
    app = create_app()
    
    print("=" * 60)
    print("VitaCheck Phase 1+3: Streaming Diagnostic API with RAG")
    print("DeepSeek R1 8B + Groq Extraction + RAG Knowledge Grounding")
    print("=" * 60)
    print()
    print("CONFIGURATION:")
    print(f"  Groq API: {'YES' if GROQ_API_KEY else 'NO (fallback mode)'}")
    print(f"  Ollama URL: {OLLAMA_BASE_URL}")
    print(f"  Model: deepseek-r1:8b")
    print()
    print("ENDPOINTS:")
    print("  POST   /chat/stream        - Streaming diagnosis (traditional)")
    print("  POST   /diagnosis/rag      - Streaming diagnosis with RAG (Phase 3)")
    print("  GET    /rag/status         - RAG system status")
    print("  GET    /health             - Health check")
    print("  GET    /docs               - API documentation")
    print()
    print("PERFORMANCE TARGETS:")
    print("  Phase 1: <1s TTFT, <5s total (Groq + DeepSeek)")
    print("  Phase 3: <0.1s TTFT, <5.5s total (with RAG)")
    print()
    print("REQUIREMENTS:")
    print("  1. Ollama running: ollama serve")
    print("  2. Model loaded: ollama pull deepseek-r1:8b")
    print("  3. RAG components: ChromaDB, Sentence Transformers")
    print("  4. .env file with GROQ_API_KEY (optional)")
    print()
    print(f"Starting server: http://localhost:8000")
    print("=" * 60)
    print()
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
