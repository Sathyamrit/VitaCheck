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
OLLAMA_GENERATE = f"{OLLAMA_BASE_URL}/api/generate"


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
    extracted: ExtractedSymptoms,
    rag_context: str
) -> AsyncGenerator[str, None]:
    """
    Stream tokens from DeepSeek R1 8B via Ollama.
    The model's internal <think> blocks are preserved in output for transparency.
    
    Latency target: <4.5s total (includes prefill + decoding)
    """
    
    # Build prompt that encourages thinking blocks
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
    
    # ====== HEALTH CHECK ======
    @app.get("/health")
    async def health():
        """Check API and model health."""
        return {
            "status": "healthy",
            "ollama": await check_ollama_health(),
            "groq": "configured" if GROQ_API_KEY else "not configured"
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
    print("VitaCheck Phase 1: Streaming Diagnostic API")
    print("DeepSeek R1 8B + Groq Extraction")
    print("=" * 60)
    print()
    print("CONFIGURATION:")
    print(f"  Groq API: {'YES' if GROQ_API_KEY else 'NO (fallback mode)'}")
    print(f"  Ollama URL: {OLLAMA_BASE_URL}")
    print(f"  Model: deepseek-r1:8b")
    print()
    print("ENDPOINTS:")
    print("  POST   /chat/stream     - Streaming diagnosis (SSE)")
    print("  GET    /health          - Health check")
    print("  GET    /docs            - API documentation")
    print()
    print("EXPECTED PERFORMANCE:")
    print("  Stage 1 (Groq extraction): <500ms")
    print("  Stage 2 (DeepSeek reasoning): <4.5s")
    print("  Total Time-to-First-Token: <1s")
    print()
    print("REQUIREMENTS:")
    print("  1. Ollama running: ollama serve")
    print("  2. Model loaded: ollama pull deepseek-r1:8b")
    print("  3. .env file with GROQ_API_KEY (optional)")
    print()
    print(f"Starting server: http://localhost:8000")
    print("=" * 60)
    print()
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
