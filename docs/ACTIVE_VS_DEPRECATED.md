# VitaCheck Phase 1: Active vs Deprecated Files

## ✅ ACTIVE FILES (Use These)

### Backend
- **`server/streaming_api.py`** ← Main API server for Phase 1
  - Implements `/chat/stream` endpoint
  - Uses Groq for fast extraction
  - Streams DeepSeek R1 responses
  - **This is the ONLY backend file you need**

- **`server/requirements.txt`**
  - Python dependencies for streaming_api.py

### Frontend  
- **`client/src/pages/DiagnosticDashboard.tsx`** ← Main questionnaire UI
  - Beautiful symptom questionnaire with categories
  - Calls /chat/stream endpoint
  - Displays real-time streaming responses
  - Displays thinking blocks

- **`client/src/hooks/useStreamingDiagnosis.ts`**
  - React hook that connects to /chat/stream
  - Handles SSE streaming
  - Tracks TTFT metrics

### Configuration
- **`.env.example`** → Copy to `.env` and configure
- **`SERVER_SETUP.md`** → Setup & troubleshooting guide

---

## ❌ DEPRECATED FILES (Do NOT Use)

### Backend (REMOVE OR ARCHIVE)
- **`server/main.py`** 
  - ❌ Uses Redis + Celery (background jobs)
  - ❌ Does NOT stream responses
  - ❌ NOT used in Phase 1
  - **Action**: Keep for reference, but don't run

- **`server/tasks.py`**
  - ❌ Uses Ollama directly (slow, ~18 seconds)
  - ❌ Returns JSON only, no thinking blocks
  - ❌ Dramatiq actor pattern (not streaming)
  - **Action**: Keep for reference, but don't run

- **`server/schemas.py`**
  - ❌ For old main.py/tasks.py
  - ❌ Use Pydantic models in streaming_api.py instead
  - **Action**: Can delete

### Frontend (Keep as backup)
- **`client/src/pages/Diagnostic.tsx`** 
  - ⚠️ Old simple version (kept for reference)
  - Use DiagnosticDashboard.tsx instead

---

## 📋 Cleanup Steps (Optional)

If you want to clean up the server directory:

```bash
cd c:\Users\sathy\OneDrive\Desktop\VitaCheck\server

# Option 1: Delete deprecated files (irreversible)
del main.py tasks.py schemas.py

# Option 2: Archive them (safer)
mkdir old_files
move main.py old_files/
move tasks.py old_files/
move schemas.py old_files/
```

---

## 🎯 Current Architecture (Phase 1)

```
USER ← Web Browser (http://localhost:5173)
  ↓
React: DiagnosticDashboard.tsx
  ↓
Hook: useStreamingDiagnosis.ts
  ↓ fetch POST /chat/stream
  ↓
FastAPI: streaming_api.py (http://localhost:8000)
  ├─ Response: Server-Sent Events (SSE)
  └─ Pipeline:
      1. Groq (extraction) <500ms
      2. RAG context <300ms
      3. DeepSeek stream <4.5s
```

---

## ❓ How to Know You're Using the Right Setup

✅ **CORRECT** (Phase 1):
- Response time: 3-5 seconds total
- TTFT: <1 second
- You see `<think>...</think>` reasoning blocks
- Browser shows real-time streaming text
- Groq extraction status appears first
- `streaming_api.py` is running

❌ **WRONG** (Using old files):
- Response time: ~18 seconds
- No streaming (waits for complete response)
- No thinking blocks visible
- `main.py` or `tasks.py` is running
- Ollama logs show long inference times

---

## 📝 Quick Reference

| What | Where | Command |
|------|-------|---------|
| Start API Server | server/ | `python streaming_api.py` |
| Start Frontend | client/ | `npm run dev` |
| Test Health | Terminal | `curl http://localhost:8000/health` |
| View API Docs | Browser | http://localhost:8000/docs |
| Check Ollama | Terminal | `ollama ps` |

---

## 🚀 Next Action

1. ✅ Delete or archive: `main.py`, `tasks.py`, `schemas.py` (optional)
2. ✅ Update `.env` with GROQ_API_KEY
3. ✅ Run: `python streaming_api.py`
4. ✅ Visit: http://localhost:5173
5. ✅ Try the questionnaire!

---

**Questions?** Refer to `SERVER_SETUP.md` for detailed troubleshooting.
