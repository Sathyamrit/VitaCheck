# Phase 2: Which Folder To Run Each Command? 🗂️

**Quick Answer**: Follow the 📂 folder icon shown next to each command!

---

## Day 1: Setup & Benchmarking

### 1️⃣ Create Conda Environment

```
📂 Run from ANY FOLDER (or root is fine)
```

**Command**:
```bash
conda create -n vitacheck-phase2 python=3.11 -y
conda activate vitacheck-phase2
```

**Where to type**: 
- PowerShell terminal (anywhere - conda is system-wide)
- Or: `c:\Users\sathy\OneDrive\Desktop\VitaCheck`

---

### 2️⃣ Install PyTorch

```
📂 Run from ANY FOLDER
```

**Command**:
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

**Where to type**: 
- Same terminal, already have `vitacheck-phase2` conda environment activated

---

### 3️⃣ Install Optimization Tools

```
📂 Run from ANY FOLDER
```

**Command**:
```bash
pip install transformers accelerate optimum bitsandbytes auto-gptq psutil
```

**Where to type**: 
- Same terminal

---

### 4️⃣ Run Benchmark (IMPORTANT!)

```
📂 Run from: c:\Users\sathy\OneDrive\Desktop\VitaCheck\server
```

**How to get there**:
```powershell
# From root (c:\Users\sathy\OneDrive\Desktop\VitaCheck)
cd server

# Or from anywhere:
cd c:\Users\sathy\OneDrive\Desktop\VitaCheck\server
```

**Command to run** (make sure you're in the server folder):
```bash
python benchmark_models.py
```

**Expected output**: 
- `benchmark_results_phase2.json` created
- Performance metrics displayed

---

## Day 2: Quantization Testing

### 1️⃣ Install ONNX Runtime

```
📂 Run from ANY FOLDER
```

**Command**:
```bash
pip install onnxruntime onnxruntime-gpu huggingface-hub
```

---

### 2️⃣ Create Test Script

```
📂 File location: c:\Users\sathy\OneDrive\Desktop\VitaCheck\server\test_quantization.py
```

**Don't run commands - just CREATE the file**

1. Go to VS Code file explorer
2. Right-click in `server` folder → New File
3. Name it: `test_quantization.py`
4. Copy the full Python code from PHASE2_QUICKSTART.md Section 2.2 into this file
5. Save it (Ctrl+S)

---

### 3️⃣ Run Quantization Comparison

```
📂 Run from: c:\Users\sathy\OneDrive\Desktop\VitaCheck (ROOT)
```

**How to get there from root**:
```powershell
cd c:\Users\sathy\OneDrive\Desktop\VitaCheck

# Then run:
python server/test_quantization.py
```

**Expected output**: 
- Comparison between FP16 and 4-bit quantization
- Memory usage, latency, TPS for each
- Recommendation

---

## Day 3-4: vLLM Integration

### 1️⃣ Install vLLM

```
📂 Run from ANY FOLDER
```

**Command**:
```bash
pip install vllm
```

**Verify it worked**:
```bash
python -c "from vllm import LLM; print('vLLM ready')"
```

---

### 2️⃣ Start vLLM Server

```
📂 Run from: c:\Users\sathy\OneDrive\Desktop\VitaCheck (ROOT)
📍 Terminal: TERMINAL 1 (Keep running)
```

**Command**:
```powershell
cd c:\Users\sathy\OneDrive\Desktop\VitaCheck
python server/vllm_server.py
```

**Expected output**: 
- Server starts on http://localhost:8001
- ⚠️ **Keep this terminal running!**

---

### 3️⃣ Test vLLM Server

```
📂 Run from: ANY FOLDER
📍 Terminal: TERMINAL 2 (New terminal tab/window)
```

**Command**:
```bash
curl -X POST http://localhost:8001/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Symptoms: tired and weak. Age: 30. Sex: male. Analyze micronutrient deficiencies.",
    "temperature": 0.7,
    "max_tokens": 500
  }'
```

**Expected output**: 
- Streaming response from vLLM
- Shows tokens being generated

---

### 4️⃣ Benchmark vLLM vs Ollama

```
📂 Run from: c:\Users\sathy\OneDrive\Desktop\VitaCheck\server
📍 Terminal: TERMINAL 3 (New terminal tab/window)
```

**First make sure Ollama is running** (start it in a separate terminal):
```bash
ollama serve
```

**Then benchmark**:
```powershell
cd c:\Users\sathy\OneDrive\Desktop\VitaCheck\server
python benchmark_models.py
```

**Expected output**: 
- Benchmarks for both Ollama and vLLM
- Comparison showing performance differences
- Results in `benchmark_results_phase2.json`

---

## Day 5: Integration & Results

### 1️⃣ Update streaming_api.py

```
📂 File location: c:\Users\sathy\OneDrive\Desktop\VitaCheck\server\streaming_api.py
```

**How to edit**:
1. Open VS Code
2. Open file: `server/streaming_api.py`
3. Go to the top of the file (near imports)
4. Add these lines:
```python
MODEL_BACKEND = os.getenv("MODEL_BACKEND", "ollama")  # or "vllm"

if MODEL_BACKEND == "vllm":
    INFERENCE_ENDPOINT = "http://localhost:8001"
else:
    INFERENCE_ENDPOINT = "http://localhost:11434"
```
5. Save the file (Ctrl+S)

---

### 2️⃣ Create Performance Report

```
📂 File location: c:\Users\sathy\OneDrive\Desktop\VitaCheck\PHASE2_BENCHMARK_RESULTS.md
```

**How to create**:
1. Right-click in root folder → New File
2. Name it: `PHASE2_BENCHMARK_RESULTS.md`
3. Copy the markdown template from PHASE2_QUICKSTART.md Section 4.2
4. Fill in your actual benchmark results
5. Save

---

### 3️⃣ Create Cloud Deployment Guide

```
📂 File location: c:\Users\sathy\OneDrive\Desktop\VitaCheck\PHASE2_CLOUD_DEPLOYMENT.md
```

**How to create**:
1. Right-click in root folder → New File
2. Name it: `PHASE2_CLOUD_DEPLOYMENT.md`
3. Copy the template from PHASE2_QUICKSTART.md Section 4.3
4. Save

---

## 📊 Terminal Setup Reference

For Day 3-4 (vLLM testing), you need **3 terminals**:

```
┌─────────────────────────────────────────┐
│ TERMINAL 1: vLLM Server                 │
│ cd c:\...VitaCheck                      │
│ python server/vllm_server.py            │
│ (keep running)                          │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ TERMINAL 2: Test vLLM                   │
│ (any folder)                            │
│ curl -X POST http://localhost:8001/...  │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ TERMINAL 3: Benchmark                   │
│ cd c:\...VitaCheck\server               │
│ python benchmark_models.py              │
└─────────────────────────────────────────┘
```

---

## 🎯 TL;DR (Too Long; Didn't Read)

| Step | Where | What |
|------|-------|------|
| Install packages | Any folder | `pip install ...` |
| Run benchmarks | `server/` folder | `python benchmark_models.py` |
| Run test scripts | `root/` folder | `python server/test_quantization.py` |
| Start servers | `root/` folder | `python server/vllm_server.py` |
| Edit files | VS Code | `server/streaming_api.py` |
| Create files | `root/` folder | New `.md` files |

---

## ✅ Verification Checklist

- [ ] Opened PowerShell in VS Code
- [ ] Activated `vitacheck-phase2` conda environment
- [ ] Can run commands in `server/` folder
- [ ] Can run commands in root folder
- [ ] Can create new files in VS Code
- [ ] Start Day 1 with benchmarking!

**Start with PHASE2_QUICKSTART.md → Day 1** 🚀
