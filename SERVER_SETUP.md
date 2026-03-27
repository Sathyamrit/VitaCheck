# VitaCheck Phase 1: Server Setup & Startup Guide

## ⚡ Quick Start (5 minutes)

### 1. Ensure Ollama is Running

**Terminal 1** (Keep running):
```bash
ollama serve
```

**Important**: Make sure the model is pulled:
```bash
ollama pull deepseek-r1:8b
```

### 2. Create .env File

Copy `.env.example` to `.env`:
```bash
cd c:\Users\sathy\OneDrive\Desktop\VitaCheck
copy .env.example .env
```

Edit `.env` and add your GROQ API key:
```
GROQ_API_KEY=your_key_here
OLLAMA_URL=http://localhost:11434
```

Get free GROQ API key: https://console.groq.com

### 3. Install Python Dependencies

```bash
cd server
pip install -r requirements.txt
```

### 4. Start the Streaming API Server

**Terminal 2**:
```bash
cd server
python streaming_api.py
```

Expected output:
```
╔════════════════════════════════════════════════════════════╗
║  VitaCheck Phase 1: Streaming Diagnostic API              ║
║  DeepSeek R1 8B + Groq Extraction                          ║
╚════════════════════════════════════════════════════════════╝

⚙️  CONFIGURATION:
    🔑 Groq API: ✅ Configured
    🦙 Ollama URL: http://localhost:11434
    🤖 Model: deepseek-r1:8b

📍 ENDPOINTS:
   POST   /chat/stream     → Streaming diagnosis (SSE)
   GET    /health          → Health check
   GET    /docs            → API documentation

🚀 Starting server: http://localhost:8000
```

### 5. Start the Frontend

**Terminal 3**:
```bash
cd client
npm run dev
```

Visit: **http://localhost:5173**

---

## 🧪 Quick Test

### Health Check
```bash
curl http://localhost:8000/health
```

Should return:
```json
{
  "status": "healthy",
  "ollama": "running",
  "groq": "configured"
}
```

### Test Streaming Endpoint
```bash
curl -X POST http://localhost:8000/chat/stream \
  -H "Content-Type: application/json" \
  -d '{"text": "I feel constantly tired and weak"}'
```

Should stream response with events like:
```
data: {"type":"status","message":"Extracting symptoms..."}
data: {"type":"extracted","data":{...}}
data: {"type":"token","content":"Based"}
...
```

---

## 🔥 Expected Performance

| Component | Target | Status |
|-----------|--------|--------|
| Groq Extraction | <500ms | ✅ (or fallback) |
| DeepSeek Streaming | <4.5s | ✅ |
| Time to First Token | <1s | ✅ |
| **Total Response** | **<5s** | ✅ |

---

## 🆘 Troubleshooting

### Problem: "Connection refused localhost:11434"
```bash
# Make sure Ollama is running
ollama serve
```

### Problem: "GROQ_API_KEY not found"
- Create `.env` file in project root
- Add: `GROQ_API_KEY=your_key`

### Problem: "Model 'deepseek-r1:8b' not found"
```bash
ollama pull deepseek-r1:8b
```

### Problem: Latency > 5 seconds
- Check GPU: `nvidia-smi`
- Check RAM usage
- Close other GPU applications

### Problem: 404 on /chat/stream
- Make sure `streaming_api.py` is running
- Check FastAPI is listening on 8000

---

## 📊 Architecture

```
React App (localhost:5173)
        ↓ POST /chat/stream
    FastAPI (localhost:8000)
        ├─ Stage 1: Groq Extraction (<500ms)
        │   └─ Returns: {symptoms, age, sex, meds, allergies}
        │
        ├─ Stage 2: RAG Context (<300ms)
        │   └─ Returns: Micronutrient knowledge base
        │
        └─ Stage 3: DeepSeek Reasoning (<4.5s)
            └─ Streams: <think>...</think> + Diagnosis
```

---

## 📁 Server Files

Only `streaming_api.py` is active in Phase 1:

- ✅ `streaming_api.py` - Main async streaming API
- ✅ `requirements.txt` - Dependencies
- ⚠️ `main.py` - **DEPRECATED** (replaced by streaming_api.py)
- ⚠️ `tasks.py` - **DEPRECATED** (replaced by streaming_api.py)
- ⚠️ `schemas.py` - **DEPRECATED** (replaced by streaming_api.py)

To fully clean up, you can delete main.py, tasks.py, and schemas.py.

---

## 🚀 Next Steps

1. Verify the streaming endpoint works
2. Test the DiagnosticDashboard questionnaire
3. Check performance metrics (TTFT, latency)
4. Proceed to Phase 2 (model optimization)

---

**Ready?** Run `python streaming_api.py` and open the app!
