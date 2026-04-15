# Phase 1 Architecture Diagram

## High-Level Flow

```
┌─────────────────────────────────────────────────────────────────────────┐
│                          USER INTERFACE (React)                          │
│                                                                           │
│  Input: "I feel constantly tired and weak"                              │
│         ↓                                                               │
│  useStreamingDiagnosis() Hook                                           │
└─────────────────────────────────────────────────────────────────────────┘
                                    ↓ (fetch POST)
┌─────────────────────────────────────────────────────────────────────────┐
│                  FastAPI Backend (streaming_api.py)                      │
│                                                                           │
│  /chat/stream endpoint                                                  │
│  ├─ Returns StreamingResponse (text/event-stream)                       │
│  └─ Yields events in real-time                                          │
└─────────────────────────────────────────────────────────────────────────┘
                                    ↓
         ┌──────────────────────────┴──────────────────────────┐
         │                                                      │
         ↓                                                      ↓
    ╔═════════════╗                                      ╔═════════════╗
    │  STAGE 1    │                                      │  RAG SETUP  │
    │  EXTRACTOR  │                                      │  (Phase 1)  │
    ║═════════════║                                      ║═════════════║
    │ Groq API    │                                      │ Placeholder │
    │ (<500ms)    │                                      │ Context     │
    │             │                                      │ (expand in  │
    │ Input:      │                                      │  Phase 3)   │
    │ Raw text    │                                      │             │
    │             │                                      │ Returns:    │
    │ Output:     │                                      │ Medical     │
    │ {           │                                      │ facts       │
    │  symptoms,  │                                      │ (~300ms)    │
    │  age,       │                                      │             │
    │  sex,       │                                      │ Future:     │
    │  meds,      │                                      │ ChromaDB    │
    │  allergies  │                                      │ + USDA FDC  │
    │ }           │                                      │             │
    └─────────────┘                                      └─────────────┘
         ↓                                                      ↓
         └──────────────────────────┬──────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────────┐
│                    STAGE 2: DEEP REASONING                               │
│                                                                           │
│  DeepSeek R1 8B via Ollama (~4.5s)                                      │
│                                                                           │
│  System Prompt:                                                          │
│  ─────────────                                                           │
│  "You are a micronutrient diagnostic expert.                            │
│   Show your reasoning in <think> blocks.                                │
│   Base recommendations on provided context."                            │
│                                                                           │
│  User Prompt:                                                            │
│  ─────────────                                                           │
│  Extracted symptoms + RAG context                                       │
│                                                                           │
│  Output Stream:                                                          │
│  ──────────────                                                          │
│  <think>                                                                │
│    The symptom triad of fatigue, weakness, and...                      │
│    suggests iron deficiency anemia given the...                        │
│  </think>                                                              │
│                                                                           │
│  Based on your presentation, iron deficiency...                        │
└─────────────────────────────────────────────────────────────────────────┘
                                    ↓ (tokens streamed)
┌─────────────────────────────────────────────────────────────────────────┐
│                        EVENT STREAM (SSE)                                │
│                                                                           │
│  data: {"type": "status", "message": "Extracting..."}                  │
│  data: {"type": "extracted", "data": {...}}                            │
│  data: {"type": "status", "message": "Generating..."}                  │
│  data: {"type": "token", "content": "Based"}                           │
│  data: {"type": "token", "content": " on"}                             │
│  data: {"type": "token", "content": " your"}                           │
│  ...                                                                     │
│  data: {"type": "completed", "message": "Done"}                        │
└─────────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────────┐
│                    React Component (Real-time Display)                   │
│                                                                           │
│  ✅ Extracted: Fatigue, Weakness, Age: 35, Sex: Female                 │
│  ⏱️  TTFT: 887ms ⚡                                                       │
│  ⏱️  Total: 3245ms                                                       │
│  □ Diagnosis:                                                            │
│    Based on your presentation, iron deficiency anemia is most likely...│
│                                                                           │
│  [New Analysis]                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

## Response Timeline

```
0ms    ├─ User submits input
       │
       ├─ FastAPI receives request
       │
5ms    ├─ Groq API called (extraction)
       │
450ms  ├─ Groq response: Extracted JSON
       │
500ms  ├─ RAG context retrieved (placeholder in Phase 1)
       │
800ms  ├─ DeepSeek prefill (loading prompt into GPU)
       │
987ms  ├─ 🎯 FIRST TOKEN GENERATED ⚡ (TTFT < 1s)
       │
       ├─ Tokens streamed continuously...
       │  - "Based on your presentation"
       │  - ", iron deficiency anemia"
       │  - " is most likely the cause."
       │  ...
       │
3245ms ├─ Final token: "."
       │
3250ms └─ Stream completed
```

## Event Flow Sequence Diagram

```
Frontend                    Backend                  Groq API        Ollama
   │                           │                         │              │
   ├──── POST /chat/stream ────>│                         │              │
   │                           │                         │              │
   │                           ├──── Extract Symptoms ──>│              │
   │                           │                         │              │
   │                           │<─ {"symptoms": [...]} ──┤              │
   │                           │                         │              │
   │<── "status": "extracting" ─┤                         │              │
   │                           │                         │              │
   │<── "extracted": {...}  ───┤                         │              │
   │                           │                         │              │
   │                           ├─── DeepSeek Prompt ────────────────────>│
   │                           │                                        │
   │<── "status": "generating" ─┤                                        │
   │                           │                         │              │
   │<── "token": "Based"    ───┤<────────── token ──────────────────────┤
   │                           │                         │              │
   │<── "token": " on"     ────┤<────────── token ──────────────────────┤
   │                           │                         │              │
   │<── "token": " your"   ────┤<────────── token ──────────────────────┤
   │                           │                         │              │
   │                           │                         │ (streaming)  │
   │<── "token": "..."     ────┤<────────────────────────────────────────┤
   │                           │                         │              │
   │<── "completed"        ────┤                         │              │
   │                           │                         │              │
   └─────────────────────────────────────────────────────────────────────

Timing:
├─ T0:    POST request received
├─ T50:   Groq extraction begins
├─ T450:  Extraction complete
├─ T800:  DeepSeek prefill begins
├─ T987:  🎯 TTFT (first token)
├─ T3245: Last token
└─ T3250: Stream closed
```

## Architecture Components

### 1. Frontend (React + TypeScript)

```
client/src/
├── components/
│   └── dashboard/
│       └── DiagnosticDashboard.tsx    ← Main UI
├── hooks/
│   └── useStreamingDiagnosis.ts        ← New streaming hook (SSE)
└── types/
    └── index.ts
```

**Key Features**:
- EventSource listener for SSE
- Real-time token display
- TTFT & total latency tracking
- Error handling

### 2. Backend (FastAPI)

```
server/
├── streaming_api.py                    ← Phase 1 implementation
├── requirements.txt
├── schemas.py                          ← Pydantic models
├── tasks.py                            ← Background jobs
└── main.py                             ← Original (legacy)
```

**Key Features**:
- `/chat/stream` endpoint
- Two-stage pipeline (Extractor + Reasoner)
- Async token generation
- SSE streaming

### 3. External Services

```
┌─────────────────┐
│  Groq Cloud API │  ← Fast extraction (<500ms)
│  (Free tier)    │    Ultra-fast LPU hardware
└─────────────────┘
         ↑
    HTTPS POST

┌──────────────────┐
│ Bollama + GPU    │  ← DeepSeek reasoning (<4.5s)
│ (Local or cloud) │    Streaming token generation
└──────────────────┘
         ↑
    HTTP POST (local)
```

## HTTP Request/Response

### Request

```http
POST /chat/stream HTTP/1.1
Host: localhost:8000
Content-Type: application/json

{
  "text": "I feel constantly tired and weak",
  "user_id": "user123"
}
```

### Response (Status 200)

```http
HTTP/1.1 200 OK
Content-Type: text/event-stream
Cache-Control: no-cache
Connection: keep-alive

data: {"type":"status","message":"Extracting symptoms..."}

data: {"type":"extracted","data":{"symptoms":["tired","weak"],"age":35,"sex":"female","medications":[],"allergies":[]}}

data: {"type":"status","message":"Generating diagnosis..."}

data: {"type":"token","content":"Based"}

data: {"type":"token","content":" on"}

data: {"type":"token","content":" your"}

...

data: {"type":"completed","message":"Diagnosis complete"}
```

## Latency Budget (Phase 1)

```
Target: <5s total response time

├─ T0-50ms     : Network latency + request parsing
├─ T50-500ms   : Groq extraction (Stage 1)
├─ T500-800ms  : RAG retrieval (placeholder in Phase 1)
├─ T800-987ms  : DeepSeek prefill (GPU loading)
├─ T987-3500ms : Token generation (streaming)
│               └─ Users see TTFT <1s ✅
└─ T3500-3550ms: Cleanup + response complete
```

## Data Flow (Detailed)

```
Raw User Input
"I feel constantly tired and weak, especially in my legs"
    ↓
[STAGE 1: GROQ EXTRACTION]
    ├─ API call: POST https://api.groq.com/openai/v1/chat/completions
    ├─ Prompt instruction: Extract JSON with symptoms, age, sex, meds, allergies
    ├─ Model: mixtral-8x7b-32768 (ultra-fast)
    ├─ Latency: 320ms
    └─ Output:
        {
          "symptoms": ["fatigue", "weakness", "leg pain"],
          "age": 35,
          "sex": "female",
          "medications": ["metformin"],
          "allergies": ["penicillin"]
        }
    ↓
[RAG RETRIEVAL - Phase 1 Placeholder]
    ├─ Query: "fatigue weakness leg pain"
    ├─ Latency: 180ms (simulated)
    └─ Context retrieved:
        {
          "iron_deficiency": "Causes fatigue, weakness, pale complexion",
          "b12_deficiency": "Neurological symptoms, peripheral neuropathy",
          "magnesium_deficiency": "Muscle cramps, arrhythmias"
        }
    ↓
[STAGE 2: DEEPSEEK REASONING]
    ├─ GPU Load: DeepSeek 8B model + LoRA adapters
    │            Model already in VRAM (1-2GB reserved)
    ├─ Input tokens: 450 (symptoms + context + system prompt)
    ├─ Prefill latency: ~200ms
    ├─ First token generated: ~187ms after prefill
    ├─ Generation:
    │  - 500 output tokens at ~30 tokens/sec (8GB GPU)
    │  - 16-17 seconds of generation
    │  - But user sees tokens in real-time!
    │  - Displayed as soon as generated
    │
    └─ Output (streaming):
        <think>
        The patient presents with fatigue, leg weakness, and
        is on metformin. Metformin reduces B12 absorption.
        Could be: Iron deficiency → anemia, B12 deficiency,
        or Magnesium deficiency given leg symptoms.
        </think>

        Based on your symptoms, **iron deficiency anemia** is most likely.
        The combination of fatigue, weakness, and leg pain suggests...
    ↓
[EVENT STREAM TO FRONTEND]
    ├─ TTFT: 987ms (target <1s) ✅
    ├─ Real-time token streaming
    ├─ React component updates on each token
    └─ Total visible latency: <1s (TTFT) + continuous streaming
```

---

**Next**: Run Phase 1 with `PHASE1_QUICKSTART.md`
