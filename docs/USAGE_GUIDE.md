# VitaCheck Phase 1: Status & Usage Guide

## Current System Status

### ✅ Components Working
- **Streaming API**: FastAPI server running on port 8000
- **Groq Extraction**: Fast symptom parsing (100-200ms)
- **DeepSeek R1 8B**: Reasoning model operational via Ollama
- **SSE Streaming**: Real-time token delivery to frontend
- **React Client**: Beautiful questionnaire UI with live updates
- **Error Handling**: Graceful fallbacks for service failures

### ⏱️ Performance Reality (Not a Bug)

**Expected Total Time: 45-60 seconds**
- Groq extraction: 0.2-0.5s
- RAG context: 0.3-0.5s  
- DeepSeek thinking: 12-20s (**This is normal for reasoning models**)
- DeepSeek output generation: 20-35s
- **User sees first result**: 10-15 seconds after clicking "Start AI Analysis"

**Why it's this long:**
- DeepSeek R1 generates `<think>` blocks before producing output
- Thinking phase takes 10-20s for complex clinical reasoning
- Then model generates 2000+ chars clinical assessment
- This is **expected behavior**, not a performance bug

### 🎯 Key Features

1. **Multi-stage Questionnaire**
   - 7 symptom categories with severity scoring (0-4)
   - Narrative text input for patterns and context
   - Beautiful, responsive UI

2. **Streaming Response**
   - Real-time token delivery as model generates text
   - Live metrics (TTFT, total time)
   - Extracted entities displayed
   - Status updates during processing

3. **Micronutrient Diagnosis**
   - Symptom analysis
   - Likely deficiency identification (prioritized list)
   - Recommended tests (blood work, micronutrient panels)
   - Dietary sources for nutrients

4. **Robust Infrastructure**
   - Groq API fallback (when available)
   - Ollama error handling
   - Configuration via .env file
   - Health check endpoint

## How to Use

#install requirements in server
pip install -r requirements.txt

### 1. Start All Services

```bash
# Terminal 1: Ollama server
ollama serve

# Terminal 2: Make sure model is pulled (run once)
ollama pull deepseek-r1:8b

# Terminal 3: Start FastAPI backend
cd server
python streaming_api.py

# Terminal 4: Start React frontend
cd client
npm run dev
```

### 2. Visit the Application
- **Frontend**: http://localhost:5173
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

### 3. Use the Diagnostic Tool
1. Click through 7 symptom categories
2. Rate each symptom 0-4 (0 = none, 4 = severe)
3. Provide narrative description (optional but helpful)
4. Click "Start AI Analysis"
5. **Wait 10-15 seconds for first output** ⏳
6. Watch real-time diagnosis stream in
7. Review symptoms analysis and recommendations

## Architecture Overview

```
┌─────────────────────┐
│   React Frontend    │ (http://localhost:5173)
│ DiagnosticDashboard │
└──────────┬──────────┘
           │ Sends symptom data + narrative
           │ Receives SSE stream
           ▼
┌─────────────────────┐
│   FastAPI Server    │ (http://localhost:8000)
│  streaming_api.py   │
└────┬──────────┬─────┘
     │          │
  [Stage 1]  [Stage 2]
Groq ├─────→ DeepSeek R1
Extract      via Ollama
symptoms     (streaming tokens)
(fast)       (reasoning model)
     │          │
     └─────┬────┘
         (Streams via SSE)
          to frontend
```

### Stage 1: Groq Extraction (100-500ms)
```
User Input: "I feel tired and weak"
    ↓
[Groq API - Fast extraction]
    ↓
Output: {
  "symptoms": ["tiredness", "weakness"],
  "age": 0,
  "sex": "unknown",
  "medications": [],
  "allergies": []
}
```

### Stage 2: DeepSeek Reasoning (20-40s)
```
Input: Extracted symptoms + RAG context
    ↓
[DeepSeek R1 8B thinking...]  ← 10-20s (internal reasoning)
    ↓
[DeepSeek R1 generating symptoms analysis...]
    ↓
[DeepSeek R1 identifying deficiencies...]
    ↓
[DeepSeek R1 recommending tests...]
    ↓
[DeepSeek R1 suggesting dietary sources...]
    ↓
Streamed to frontend token-by-token
```

## Configuration

### .env File
```bash
# Groq API key (get from https://console.groq.com/)
GROQ_API_KEY=your_key_here

# Ollama server URL
OLLAMA_URL=http://localhost:11434

# Frontend API URL
VITE_API_URL=http://localhost:8000
```

### Environment Variables
- `GROQ_API_KEY`: Optional - enables fast extraction. If not set, uses fallback keyword matching
- `OLLAMA_URL`: Where Ollama server is listening (default: http://localhost:11434)
- `VITE_API_URL`: Frontend connects to this API endpoint

## Testing the API Directly

### Health Check
```bash
curl http://localhost:8000/health
# Response: {"status": "healthy", "ollama": "running", "groq": "configured"}
```

### Test Streaming Endpoint
```bash
curl -X POST http://localhost:8000/chat/stream \
  -H "Content-Type: application/json" \
  -d '{"text": "I feel tired and weak"}'

# Response (SSE stream):
# data: {"type": "status", "message": "Extracting symptoms..."}
# data: {"type": "extracted", "data": {...}}
# data: {"type": "token", "content": "Okay, let's analyze..."}
# ...more tokens...
# data: {"type": "completed", "message": "Diagnosis complete"}
```

### Timing Benchmark
```bash
time curl -X POST http://localhost:8000/chat/stream \
  -H "Content-Type: application/json" \
  -d '{"text": "tired"}' 2>&1 | wc -l

# Total: ~45-60 seconds
# First data line appears: ~12-15 seconds in
```

## Troubleshooting

### Issue: "Port 8000 already in use"
```bash
# Find process using port 8000
netstat -ano | findstr :8000

# Kill the process (on Windows)
taskkill /PID <PID> /F
```

### Issue: Ollama connection error
```bash
# Check Ollama is running
curl http://localhost:11434/api/tags

# If error, start Ollama
ollama serve
```

### Issue: Model not found
```bash
# Pull the model
ollama pull deepseek-r1:8b

# Verify it's loaded
curl http://localhost:11434/api/tags | grep deepseek
```

### Issue: Response takes 2+ minutes
- This is likely a memory issue or model not fully loaded
- Check Ollama process isn't out of memory
- Restart Ollama: `ollama serve`
- Pre-warm the model: `ollama run deepseek-r1:8b "hello"`

### Issue: UI not connecting to API
- Check frontend is accessing correct URL: http://localhost:8000
- Check CORS headers in streaming_api.py
- Try health check: `curl http://localhost:8000/health`

## Performance Comparison

| Model | TTFT | Total Time | Reasoning | Quality |
|-------|------|-----------|-----------|---------|
| **DeepSeek R1 8B** (current) | 13-15s | 45-60s | YES | Excellent |
| Mixtral 8x7b | 1-2s | 5-10s | NO | Good |
| Llama 3.1 8B | 1-2s | 3-5s | NO | Good |
| ChatGPT o1 (API) | 30s | 60s+ | YES | Excellent |
| GPT-4 (API) | 00-3s | 5-15s | NO | Excellent |

**Current choice:** DeepSeek R1 for superior reasoning at cost of latency

## Next Steps (Phase 2-3)

- [ ] Model optimization (4-bit quantization, vLLM)
- [ ] Prompt engineering (shorter thinking phase)
- [ ] Response caching (common presentations)
- [ ] Hybrid approach (fast extraction + optional reasoning)
- [ ] RAG integration (USDA FoodData Central)
- [ ] Fine-tuning on medical domain

## Support

For issues or questions:
1. Check PERFORMANCE_ANALYSIS.md for detailed timing breakdown
2. Review streaming_api.py comments for API internals
3. Check client-side hook: useStreamingDiagnosis.ts
4. Run health_check.py for diagnostics

## Summary

✅ **System is working correctly!**

The 45-60 second response time is not a bug—it's the architectural choice to use a reasoning model for better medical analysis. The first result appears ~10-15 seconds after submission, then streams in real-time.

For faster responses but lower quality reasoning, we can switch to Mixtral (5-10s) or fall back to traditional models (3-5s).
