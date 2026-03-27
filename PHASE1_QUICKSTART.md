# Phase 1: Quick Start Guide

## Overview
This guide gets you running with streaming diagnostic responses in 30 minutes.

## Prerequisites

### 1. System Requirements
- **GPU**: NVIDIA GPU with 8GB+ VRAM (for local inference)
- **RAM**: 8GB+ system RAM
- **OS**: Windows, Mac, or Linux

### 2. Install Ollama (Model Server)

**Windows/Mac**:
1. Download: https://ollama.ai/download
2. Run installer
3. Verify: Open terminal and type `ollama --version`

**Linux**:
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

### 3. Pull DeepSeek R1 Model

```bash
# This downloads ~5GB (grab a coffee ☕)
ollama pull deepseek-r1:8b

# Should complete with: [████████████████████] 100%
```

Start Ollama server (keeps running in background):
```bash
ollama serve
```

### 4. Get Groq API Key (Free)

1. Visit: https://console.groq.com
2. Sign up (free)
3. Create API key
4. Copy key somewhere safe

### 5. Create `.env` File

Create `.env` in project root:

```bash
# Groq API (for fast symptom extraction)
GROQ_API_KEY=your_api_key_here

# Ollama Server URL
OLLAMA_URL=http://localhost:11434
```

## Backend Setup

### Install Python Dependencies

```bash
cd server
pip install -r requirements.txt
```

**File**: `server/requirements.txt` (create if missing)

```
fastapi==0.104.1
uvicorn==0.24.0
pydantic==2.5.0
httpx==0.25.0
python-dotenv==1.0.0
redis==5.0.0
aiofiles==23.2.0
```

### Run Streaming API

```bash
python streaming_api.py
```

**Expected output:**
```
╔════════════════════════════════════════════════════════════╗
║  VitaCheck Phase 1: Streaming API                         ║
║  Starting async diagnostic engine...                       ║
╚════════════════════════════════════════════════════════════╝

📍 Endpoints:
   POST   /chat/stream     (Streaming diagnosis)
   GET    /health          (Health check)

🚀 Start: http://localhost:8000
📚 Docs: http://localhost:8000/docs
```

### Test API with curl

```bash
# Check health
curl http://localhost:8000/health

# Stream diagnosis
curl -X POST http://localhost:8000/chat/stream \
  -H "Content-Type: application/json" \
  -d '{"text": "I feel constantly tired and weak, especially in my legs"}'

# Expected response (streaming):
data: {"type": "status", "message": "Extracting symptoms..."}
data: {"type": "extracted", "data": {...}}
data: {"type": "status", "message": "Generating diagnosis..."}
data: {"type": "token", "content": "Based"}
data: {"type": "token", "content": " on"}
...
```

## Frontend Setup

### Install React Hook

The new hook is already created at:
- `client/src/hooks/useStreamingDiagnosis.ts`

### Create Dashboard Component

Create `client/src/components/dashboard/DiagnosticDashboard.tsx`:

```tsx
import React, { useState } from 'react';
import { useStreamingDiagnosis } from '../../hooks/useStreamingDiagnosis';

export function DiagnosticDashboard() {
  const [input, setInput] = useState('');
  const {
    diagnosis,
    status,
    ttft,
    totalTime,
    extracted,
    error,
    streamDiagnosis,
    resetDiagnosis,
  } = useStreamingDiagnosis();

  const handleSubmit = async () => {
    if (!input.trim()) return;
    await streamDiagnosis(input);
  };

  return (
    <div className="max-w-2xl mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Micronutrient Diagnostic</h1>

      {/* Input Section */}
      <div className="mb-4">
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Describe your symptoms..."
          className="w-full h-24 p-3 border rounded-lg"
          disabled={status === 'streaming'}
        />
        <button
          onClick={handleSubmit}
          disabled={status === 'streaming' || !input.trim()}
          className="mt-2 px-4 py-2 bg-blue-600 text-white rounded-lg disabled:bg-gray-400"
        >
          {status === 'streaming' ? 'Analyzing...' : 'Get Diagnosis'}
        </button>
      </div>

      {/* Metrics */}
      {status !== 'idle' && (
        <div className="grid grid-cols-2 gap-2 mb-4 text-sm">
          <div className="p-2 bg-gray-100 rounded">
            <strong>Status:</strong> {status}
          </div>
          {ttft && (
            <div className="p-2 bg-gray-100 rounded">
              <strong>TTFT:</strong> {ttft}ms ⚡
            </div>
          )}
          {totalTime && (
            <div className="p-2 bg-gray-100 rounded">
              <strong>Total:</strong> {totalTime}ms
            </div>
          )}
        </div>
      )}

      {/* Extracted Data */}
      {extracted && (
        <div className="mb-4 p-3 bg-blue-50 rounded-lg">
          <strong className="block mb-2">Extracted Information:</strong>
          <ul className="text-sm space-y-1">
            <li>Symptoms: {extracted.symptoms.join(', ')}</li>
            <li>Age: {extracted.age}</li>
            <li>Sex: {extracted.sex}</li>
          </ul>
        </div>
      )}

      {/* Diagnosis Output */}
      {diagnosis && (
        <div className="mb-4 p-4 bg-green-50 rounded-lg border border-green-200">
          <strong className="block mb-2">Diagnostic Analysis:</strong>
          <div className="whitespace-pre-wrap text-sm">{diagnosis}</div>
        </div>
      )}

      {/* Error */}
      {error && (
        <div className="p-3 bg-red-100 border border-red-400 rounded-lg text-red-700">
          ⚠️ {error}
        </div>
      )}

      {/* Reset Button */}
      {status === 'completed' && (
        <button
          onClick={() => {
            resetDiagnosis();
            setInput('');
          }}
          className="px-4 py-2 bg-gray-600 text-white rounded-lg"
        >
          New Analysis
        </button>
      )}
    </div>
  );
}
```

### Update App.tsx

```tsx
import { DiagnosticDashboard } from './components/dashboard/DiagnosticDashboard';

function App() {
  return (
    <div>
      {/* Your existing navbar/layout */}
      <DiagnosticDashboard />
    </div>
  );
}
```

### Run Frontend

```bash
cd client
npm run dev
```

Visit: http://localhost:5173

## Testing the Full Pipeline

### Test Scenario 1: Simple Query

**Input:**
```
I've had fatigue and muscle weakness for 2 weeks
```

**Expected Flow:**
1. ✅ Groq extracts symptoms (< 500ms)
2. ✅ RAG retrieves context (< 300ms)
3. ✅ DeepSeek streams diagnosis (< 4.5s)
4. ✅ TTFT < 1s
5. ✅ Total latency < 5s

### Test Scenario 2: Complex Patient History

**Input:**
```
I'm a 45-year-old female vegetarian with persistent fatigue, brittle nails, and shortness of breath on light exertion. I take metformin for prediabetes and have a shellfish allergy. My energy has been declining for 3 months.
```

**Expected Output:**
```
<think>
Presenting symptoms suggest anemia given fatigue, dyspnea, and brittle nails. 
Vegetarian diet increases iron deficiency risk. Metformin can interfere with B12 absorption.
Need to consider: Iron deficiency anemia, B12 deficiency, folate deficiency.
</think>

Based on your presentation, **iron deficiency anemia** is most likely...
```

## Troubleshooting

### Problem: `Connection refused localhost:11434`
- **Solution**: Make sure Ollama is running
  ```bash
  ollama serve
  ```

### Problem: `GROQ_API_KEY not found`
- **Solution**: Check `.env` file exists in project root
  ```bash
  echo "GROQ_API_KEY=your_key" > .env
  ```

### Problem: `OutOfMemory` on GPU
- **Solution**: Close other GPU applications or use smaller model
  ```bash
  # Use 4-bit quantized version (smaller)
  ollama pull neurallm/deepseek-r1:8b-q4
  ```

### Problem: Latency > 5s
- **Solution**: Check:
  1. GPU utilization: `nvidia-smi`
  2. Network latency with Groq
  3. System RAM (should have 8GB free)

### Problem: Medical context incomplete
- **Solution**: Phase 3 (RAG integration) is not yet implemented
  - Placeholder context is returned in Phase 1
  - Full USDA database integration comes in Phase 3

## Next Steps After Phase 1

Once streaming is working:

1. **Phase 2 (Week 2-3)**: Model optimization + cloud deployment
2. **Phase 3 (Week 3-4)**: Add RAG vector database
3. **Phase 4 (Week 4-5)**: Fine-tuning on your dataset
4. **Phase 5 (Week 5-6)**: Safety guardrails + evaluation
5. **Phase 6 (Week 6-7)**: Production deployment

## Performance Benchmarks

| Component | Target | Actual |
|-----------|--------|--------|
| Groq Extraction | <500ms | ⏱️ Check with curl |
| RAG Retrieval | <300ms | N/A (Phase 3) |
| DeepSeek Prefill | <500ms | ⏱️ Check with curl |
| TTFT | <1s | ⏱️ Check with curl |
| Total Response | <5s | ⏱️ Check with curl |

## Monitoring

### Check Server Logs
```bash
# Terminal 1: Run server with debug
python streaming_api.py --debug
```

### Monitor GPU
```bash
# Terminal 2: Watch GPU usage
watch nvidia-smi
```

### Test API Continuously
```bash
# Terminal 3: Load test
while true; do
  curl -X POST http://localhost:8000/chat/stream \
    -H "Content-Type: application/json" \
    -d '{"text": "Test symptoms"}' | head -20
  sleep 5
done
```

## Resources

- **Ollama Docs**: https://github.com/ollama/ollama
- **FastAPI Streaming**: https://fastapi.tiangolo.com/advanced/response-streams/
- **Groq API**: https://console.groq.com/docs
- **DeepSeek Model**: https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Llama-8B

---

**Done!** You now have a functioning streaming diagnostic API. Time to first token: <1s ⚡

Next: Read `IMPLEMENTATION_ROADMAP.md` for Phase 2 (inference optimization) planning.
