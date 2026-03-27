# VitaCheck DeepSeek R1 8B Implementation Roadmap

## Executive Summary
This document provides a phased implementation strategy for integrating the DeepSeek R1 8B reasoning model into VitaCheck, enabling sub-5-second micronutrient diagnostic responses with expert-level reasoning transparency.

**Target Timeline**: 6-7 weeks  
**Primary Focus**: Asynchronous API with streaming endpoints (Phase 1 priority)

---

## Current Project State

| Component | Status | Location |
|-----------|--------|----------|
| React Frontend | ✅ Complete | `/client` (Vite, React 19, Tailwind) |
| FastAPI Backend | ✅ Partial | `/server` (async, Redis, Celery tasks) |
| LLM Integration | ❌ Not started | — |
| Vector Database | ❌ Not started | — |
| Fine-tuning Pipeline | ❌ Not started | — |
| Evaluation Suite | ❌ Not started | — |

**Assets in Hand**:
- Training data ready for fine-tuning ✅
- Asyncio/Redis infrastructure ✅
- Structured data schemas ✅

---

## Phase 1: Asynchronous Streaming API Foundation (Week 1)

**Objective**: Convert blocking endpoints to streaming Server-Sent Events (SSE) for real-time response delivery.

### 1.1 Upgrade FastAPI Backend for Streaming

**File**: `server/main.py`

```python
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import asyncio

@app.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    """
    Returns Server-Sent Events stream of diagnostic reasoning.
    Time to First Token (TTFT): <1s
    Total response time: <5s
    """
    async def token_generator():
        # Stage 1: Extractor (fast symptom parsing)
        extracted = await extract_symptoms(request)
        yield f"data: {json.dumps({'type': 'extracted', 'data': extracted})}\n\n"
        
        # Stage 2: RAG retrieval (parallel)
        rag_context = await retrieve_context(extracted['symptoms'])
        yield f"data: {json.dumps({'type': 'rag_context', 'data': rag_context})}\n\n"
        
        # Stage 3: DeepSeek reasoning (with thinking blocks)
        async for token in deepseek_reasoning_stream(extracted, rag_context):
            yield f"data: {json.dumps({'type': 'token', 'data': token})}\n\n"
            await asyncio.sleep(0)  # Yield control
    
    return StreamingResponse(
        token_generator(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache"}
    )
```

### 1.2 Implement Two-Stage Prompting System

**Architecture**:
- **Stage 1 (Extractor)**: Fast model (Groq API or local Llama 3.1 8B)
  - Input: Raw user symptoms & demographics
  - Output: Structured JSON (symptoms, age, medications, allergies)
  - Latency: <500ms
  
- **Stage 2 (Reasoner)**: DeepSeek R1 8B fine-tuned
  - Input: Structured JSON + RAG context
  - Output: Diagnostic reasoning with <think> blocks
  - Latency: <4.5s

**File**: `server/llm_pipeline.py` (new)

```python
from enum import Enum
import httpx

class LLMStage(Enum):
    EXTRACTOR = "groq"  # Fast extraction
    REASONER = "deepseek"  # Deep reasoning

async def extract_symptoms(raw_input: str) -> dict:
    """Stage 1: Convert unstructured symptoms to JSON."""
    prompt = f"""Extract the following from the patient input:
    - symptoms (list)
    - age (int)
    - sex (str)
    - medications (list)
    - allergies (list)
    
    Input: {raw_input}
    Return as JSON."""
    
    response = await groq_api_call(prompt)
    return json.loads(response)

async def deepseek_reasoning(symptoms: dict, rag_context: str):
    """Stage 2: Generate diagnostic reasoning."""
    system_prompt = """You are a micronutrient diagnostic expert. Use the provided symptoms 
    and medical context to reason through possible deficiencies."""
    
    user_prompt = f"""
    Patient Profile: {symptoms}
    
    Retrieved Context (from medical literature):
    {rag_context}
    
    Provide a diagnostic assessment with your reasoning in <think> blocks."""
    
    async for token in vllm_stream(system_prompt, user_prompt):
        yield token
```

### 1.3 Update Client-Side for Streaming

**File**: `client/src/hooks/useSymptomChecker.ts` (extend)

```typescript
export async function useStreamingDiagnosis(userInput: string) {
  const eventSource = new EventSource('/chat/stream', {
    method: 'POST',
    body: JSON.stringify({ text: userInput })
  });
  
  const state = {
    extracted: null,
    ragContext: null,
    thinkingProcess: '',
    diagnosis: ''
  };
  
  return new Promise((resolve, reject) => {
    eventSource.onmessage = (event) => {
      const parsed = JSON.parse(event.data);
      
      if (parsed.type === 'extracted') state.extracted = parsed.data;
      if (parsed.type === 'rag_context') state.ragContext = parsed.data;
      if (parsed.type === 'thinking') state.thinkingProcess += parsed.data;
      if (parsed.type === 'token') state.diagnosis += parsed.data;
    };
    
    eventSource.onerror = reject;
    eventSource.addEventListener('end', () => {
      eventSource.close();
      resolve(state);
    });
  });
}
```

### 1.4 Deliverables (Week 1)
- [ ] FastAPI streaming endpoint at `/chat/stream`
- [ ] Two-stage pipeline architecture defined
- [ ] Groq API integration (free tier)
- [ ] Client SSE event listener
- [ ] Response time <1s TTFT on local testing

---

## Phase 2: Model Infrastructure & Inference Serving (Week 2-3)

**Objective**: Deploy DeepSeek R1 8B for low-latency inference.

### 2.1 Option A: Local Development (8GB GPU)

Use **Ollama** for simplicity:

```bash
# Install Ollama (https://ollama.ai)
ollama pull deepseek-r1:8b

# Start server on port 11434
ollama serve
```

**File**: `server/model_server.py`

```python
import httpx

OLLAMA_URL = "http://localhost:11434/api/generate"

async def generate_with_ollama(prompt: str, system: str = ""):
    async with httpx.AsyncClient() as client:
        async with client.stream(
            "POST",
            OLLAMA_URL,
            json={
                "model": "deepseek-r1:8b",
                "prompt": prompt,
                "system": system,
                "stream": True,
            }
        ) as response:
            async for line in response.aiter_lines():
                if line:
                    data = json.loads(line)
                    yield data.get("response", "")
```

### 2.2 Option B: Cloud Deployment (Hugging Face Spaces ZeroGPU)

Create a Spaces app for inference:

**File**: `hf_spaces/app.py`

```python
import gradio as gr
from transformers import pipeline

model = pipeline("text-generation", model="deepseek-ai/DeepSeek-R1-Distill-Llama-8B")

def diagnose(symptoms: str):
    output = model(symptoms, max_new_tokens=500)
    return output[0]['generated_text']

interface = gr.Interface(fn=diagnose, inputs="text", outputs="text")
interface.launch()
```

Deploy: Push to HF Spaces with ZeroGPU enabled.

### 2.3 Latency Benchmarking

**File**: `server/benchmarks/inference_latency.py`

```python
import time

async def benchmark_deepseek():
    test_prompt = "I have persistent fatigue and muscle pain. What micronutrient deficiency might this indicate?"
    
    start = time.time()
    async for token in generate_with_ollama(test_prompt):
        ttft = time.time() - start if not hasattr(benchmark_deepseek, 'ttft') else None
        if ttft and ttft < 1.0:
            benchmark_deepseek.ttft = ttft
            print(f"✅ TTFT: {ttft:.2f}s")
    
    total = time.time() - start
    print(f"✅ Total latency: {total:.2f}s")
```

**Target Metrics**:
- Prefill latency: <500ms
- Time to First Token: <1s
- Total response: <5s

### 2.4 Deliverables (Week 2-3)
- [ ] Ollama running locally with deepseek-r1:8b
- [ ] Streaming inference from FastAPI
- [ ] Latency benchmarks <5s total
- [ ] HF Spaces deployment ready (backup option)
- [ ] Environment variables configured

---

## Phase 3: RAG Pipeline Integration (Week 3-4)

**Objective**: Add micronutrient knowledge base for factual accuracy.

### 3.1 Set Up Vector Database (ChromaDB)

```bash
pip install chromadb
```

**File**: `server/rag/vector_store.py`

```python
import chromadb
from chromadb.config import Settings

# Initialize ChromaDB
chroma_client = chromadb.Client(Settings(
    chroma_db_impl="duckdb",
    persist_directory="./chroma_data",
    anonymized_telemetry=False,
))

collection = chroma_client.get_or_create_collection(name="micronutrients")

async def upsert_micronutrient_data():
    """Populate with USDA FoodData Central & medical abstracts."""
    documents = load_usda_nutrients()  # From USDA API
    documents.extend(load_pubmed_abstracts())  # From PubMed
    
    for doc in documents:
        embedding = await get_embedding(doc['text'])  # Using sentence-transformers
        collection.upsert(
            ids=[doc['id']],
            documents=[doc['text']],
            embeddings=[embedding],
            metadatas=[doc['metadata']]
        )

async def retrieve_context(symptoms: list) -> str:
    """Semantic search for relevant micronutrient info."""
    query_text = " ".join(symptoms)
    query_embedding = await get_embedding(query_text)
    
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=5,
        include=["documents", "metadatas", "distances"]
    )
    
    return "\n".join(results['documents'][0])
```

### 3.2 Integrate USDA FoodData Central API

**File**: `server/rag/usda_integration.py`

```python
import httpx

USDA_API_KEY = os.getenv("USDA_FDC_API_KEY")
USDA_URL = "https://fdc.nal.usda.gov/api/foods/search"

async def fetch_nutrient_profile(food_name: str) -> dict:
    """Get micronutrient data for a specific food."""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            USDA_URL,
            params={
                "query": food_name,
                "pageSize": 1,
                "api_key": USDA_API_KEY
            }
        )
        data = response.json()
        
        if data['foods']:
            food = data['foods'][0]
            nutrients = {
                n['nutrientName']: n['value']
                for n in food.get('foodNutrients', [])
            }
            return nutrients
    return None

# Normalize and store in ChromaDB
async def populate_nutrient_database():
    """One-time: Load USDA database into vector store."""
    foods = ["spinach", "salmon", "eggs", "almonds", "chickpeas", ...]
    
    for food in foods:
        profile = await fetch_nutrient_profile(food)
        doc_text = f"{food}: {json.dumps(profile)}"
        # Store in ChromaDB...
```

### 3.3 Prompt Augmentation Pipeline

**File**: `server/llm_pipeline.py` (extend)

```python
async def deepseek_reasoning_with_rag(symptoms: dict, rag_context: str):
    """
    Inject retrieved context into prompt to reduce hallucinations.
    """
    system_prompt = f"""You are a micronutrient diagnostic expert.

IMPORTANT: Base your response ONLY on the provided medical context below.
Do not rely on general knowledge for nutrient facts.

=== RETRIEVED MEDICAL CONTEXT ===
{rag_context}
=================================

Analyze the patient's symptoms and suggest the most likely micronutrient deficiencies."""
    
    user_prompt = f"""Patient Profile:
- Symptoms: {', '.join(symptoms['symptoms'])}
- Age: {symptoms['age']}
- Current Medications: {', '.join(symptoms['medications'])}
- Known Allergies: {', '.join(symptoms['allergies'])}

What micronutrient deficiencies should be considered?"""
    
    async for token in generate_with_ollama(user_prompt, system_prompt):
        yield token
```

### 3.4 Deliverables (Week 3-4)
- [ ] ChromaDB initialized with USDA data
- [ ] Semantic search integrated
- [ ] RAG retrieval <300ms
- [ ] Hallucination rate reduced to <2%
- [ ] Context injection working end-to-end

---

## Phase 4: Fine-Tuning Pipeline (Week 4-5)

**Objective**: Train DeepSeek R1 8B on micronutrient-specific data using QLoRA.

### 4.1 Environment Setup

```bash
# Install dependencies
pip install unsloth
pip install torch torchvision torchaudio
pip install datasets transformers bitsandbytes
pip install peft accelerate
pip install wandb  # For tracking
```

### 4.2 QLoRA Fine-Tuning Script

**File**: `training/fine_tune_deepseek.py`

```python
from unsloth import FastLanguageModel, get_peft_model_state_dict
from transformers import TrainingArguments, TrainerCallback
from datasets import Dataset
import torch

# Load model with Unsloth optimizations
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name="unsloth/DeepSeek-R1-Distill-Llama-8B-bnb-4bit",
    max_seq_length=2048,
    dtype=torch.float16,
    load_in_4bit=True,
)

# Add LoRA adapters
model = FastLanguageModel.get_peft_model(
    model,
    r=16,  # LoRA rank
    lora_alpha=32,  # Scaling factor (2 * rank)
    lora_dropout=0.05,
    bias="none",
    use_gradient_checkpointing="unsloth",
    random_state=42,
    target_modules=["q_proj", "v_proj", "up_proj", "down_proj"],  # Attention + MLP
)

# Prepare training data
def format_coaching_template(example):
    """Format data for DeepSeek reasoning."""
    text = f"""<|im_start|>system
You are an expert micronutrient diagnostic assistant. Reason through symptoms step-by-step.
<|im_end|>
<|im_start|>user
{example['instruction']}
<|im_end|>
<|im_start|>assistant
<think>
{example['thinking']}
</think>
{example['response']}
<|im_end|>"""
    return {"text": text}

# Load your prepared dataset
dataset = Dataset.from_dict({
    "instruction": [...],  # From your training data
    "thinking": [...],     # CoT reasoning steps
    "response": [...]      # Final diagnosis
})

dataset = dataset.map(format_coaching_template)

# Training configuration
training_args = TrainingArguments(
    output_dir="./outputs/deepseek_vitacheck",
    num_train_epochs=3,
    per_device_train_batch_size=4,
    gradient_accumulation_steps=4,
    warmup_steps=100,
    learning_rate=2e-4,
    fp16=True,
    logging_steps=10,
    save_steps=100,
    optim="paged_adamw_8bit",
    weight_decay=0.01,
    max_grad_norm=1.0,
)

from transformers import Trainer

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset,
    tokenizer=tokenizer,
)

trainer.train()

# Save adapter
model.save_pretrained("./adapters/vitacheck_adapter")
tokenizer.save_pretrained("./adapters/vitacheck_adapter")
```

### 4.3 Training Data Format

**File**: `training/data/micronutrient_training_data.jsonl`

Example entry:
```json
{
  "instruction": "A 32-year-old female reports persistent fatigue, brittle nails, and shortness of breath on light exertion. She follows a vegetarian diet with limited fortified foods.",
  "thinking": "The symptom triad of fatigue, brittle nails, and exertional dyspnea suggests anemia. Vegetarian diet without fortification increases iron deficiency risk. Need to consider B12 and folate as well given the vegetarian status. BMI and menstrual history would help confirm.",
  "response": "Based on the presentation, **iron deficiency anemia** is the most likely diagnosis. The combination of fatigue, brittle nails (koilonychia), and dyspnea on exertion are classic iron deficiency signs. The vegetarian diet without fortified foods increases risk. Recommend: 1) Serum ferritin and CBC testing, 2) Increase heme iron (poultry, fish if possible) or use iron supplements, 3) Enhance iron absorption with vitamin C. Consider B12/folate supplementation given dietary pattern."
}
```

### 4.4 Evaluation During Training

**File**: `training/evaluate_adapter.py`

```python
from deepeval import evaluate
from deepeval.metrics import AnswerRelevancyMetric, FaithfulnessMetric

# Test set of 50 expert-validated cases
test_cases = load_test_dataset()

def evaluate_adapter():
    adapter = load_peft_model("./adapters/vitacheck_adapter")
    
    for test_case in test_cases:
        output = generate_diagnosis(adapter, test_case['input'])
        
        relevancy = AnswerRelevancyMetric(output, test_case['ground_truth'])
        faithfulness = FaithfulnessMetric(
            output, 
            facts=[test_case['medical_facts']]
        )
        
        if relevancy.score < 0.7 or faithfulness.score < 0.8:
            print(f"⚠️ Case {test_case['id']} failed quality check")
    
    print("✅ Adapter evaluation complete")
```

### 4.5 Deliverables (Week 4-5)
- [ ] QLoRA fine-tuning script ready
- [ ] Training data formatted (800-1000 examples minimum)
- [ ] Training runs for 3 epochs
- [ ] Evaluation metrics tracked (loss, accuracy)
- [ ] Adapter weights saved to HuggingFace Hub

---

## Phase 5: Evaluation & Safety Framework (Week 5-6)

**Objective**: Implement benchmarking and safety guardrails.

### 5.1 Safety Guardrails

**File**: `server/safety/guardrails.py`

```python
EMERGENCY_SYMPTOMS = {
    "chest pain", "difficulty breathing", "severe headache", 
    "confusion", "loss of consciousness", "severe bleeding"
}

TOXIC_DOSES = {
    "Vitamin A": {"max": 3000, "unit": "IU/day"},  # Upper limit
    "Iron": {"max": 45, "unit": "mg/day"},
    "Selenium": {"max": 400, "unit": "µg/day"},
}

async def check_safety_guardrails(symptoms: list, diagnosis: str) -> dict:
    """
    Enforce hard constraints before returning diagnosis.
    """
    # Rule 1: Emergency symptoms
    for symptom in symptoms:
        if symptom.lower() in EMERGENCY_SYMPTOMS:
            return {
                "safe": False,
                "override": "🚨 EMERGENCY: This patient needs immediate medical attention. Do not proceed with nutritional assessment.",
                "recommendation": "Direct to nearest emergency room or call 911."
            }
    
    # Rule 2: Toxic dose detection
    for nutrient, limits in TOXIC_DOSES.items():
        if nutrient in diagnosis and "mg" in diagnosis:
            # Parse suggested dose and compare
            suggested = extract_dose(diagnosis, nutrient)
            if suggested > limits['max']:
                return {
                    "safe": False,
                    "issue": f"Suggested {nutrient} dose exceeds safe upper limit",
                    "max_safe": limits['max'],
                    "override": f"Reduce recommendation to {limits['max']} {limits['unit']}"
                }
    
    return {"safe": True}

# Inject into streaming pipeline
async def deepseek_stream_with_safety(symptoms: dict, rag_context: str):
    safety_check = await check_safety_guardrails(symptoms['symptoms'], "")
    if not safety_check['safe']:
        yield safety_check['override']
        return
    
    async for token in deepseek_reasoning_with_rag(symptoms, rag_context):
        yield token
```

### 5.2 Evaluation Suite with DeepEval

**File**: `server/benchmarks/deepeval_suite.py`

```python
from deepeval import evaluate
from deepeval.metrics import (
    AnswerRelevancyMetric,
    FaithfulnessMetric,
    HallucinationMetric,
    BiasMetric
)

class DiagnosticAccuracyMetric:
    """Custom metric for micronutrient diagnostic accuracy."""
    def __init__(self, expected_diagnosis: str, ground_truth_tests: list):
        self.expected = expected_diagnosis
        self.ground_truth = ground_truth_tests
    
    def measure(self, output: str) -> float:
        """Score 0-1 based on expert validation."""
        # Use GPT-4o as LLM judge
        return llm_judge_score(output, self.expected, self.ground_truth)

async def run_benchmark_suite():
    """Run 50-case clinical accuracy benchmark."""
    test_cases = load_test_dataset(count=50)
    results = {
        "accuracy": [],
        "faithfulness": [],
        "hallucination_rate": [],
        "bias_score": []
    }
    
    for case in test_cases:
        output = await generate_diagnosis(case['symptoms'])
        
        metrics = {
            "accuracy": await measure_clinical_accuracy(output, case['expected']),
            "faithfulness": FaithfulnessMetric(output, [case['context']]).measure(),
            "hallucination": HallucinationMetric(output, [case['context']]).measure(),
            "bias": BiasMetric(output).measure(),
        }
        
        for metric, value in metrics.items():
            results[metric].append(value)
    
    summary = {
        "avg_accuracy": sum(results["accuracy"]) / len(results["accuracy"]),
        "hallucination_rate": 1 - (sum(results["hallucination"]) / len(results["hallucination"])),
        "bias_score": sum(results["bias"]) / len(results["bias"]),
        "status": "PASS" if sum(results["accuracy"]) / len(results["accuracy"]) > 0.85 else "FAIL"
    }
    
    return summary
```

**Target Metrics** (from document):
- Diagnostic Accuracy (CrAR): >85%
- F1-Score: >0.90
- Hallucination Rate: <1%
- Response Latency: <5s

### 5.3 CI/CD Benchmarking

**File**: `.github/workflows/benchmark.yml`

```yaml
name: Model Benchmark

on: [push]

jobs:
  evaluate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run benchmark suite
        run: python server/benchmarks/deepeval_suite.py
      - name: Fail if accuracy < 85%
        run: |
          if [ $ACCURACY -lt 85 ]; then
            echo "Model accuracy below threshold"
            exit 1
          fi
```

### 5.4 Deliverables (Week 5-6)
- [ ] Safety guardrails implemented
- [ ] Emergency symptom detection
- [ ] DeepEval benchmark suite
- [ ] 50-case clinical validation runs
- [ ] Metrics dashboard (Weights & Biases)
- [ ] CI/CD benchmarking pipeline

---

## Phase 6: Optimization & Deployment (Week 6-7)

**Objective**: Optimize for production and deploy to cloud.

### 6.1 Quantization for Deployment

```bash
# Convert to GGUF format (4-bit quantization)
python -m llama_cpp.server \
  --model ./models/deepseek-r1-8b.gguf \
  --n_gpu_layers 35 \
  --n_ctx 2048
```

### 6.2 HuggingFace Spaces Deployment

**File**: `hf_spaces/app.py`

```python
import gradio as gr
from transformers import AutoTokenizer, AutoModelForCausalLM
import

 torch

# Load fine-tuned adapter
adapter_id = "your-username/vitacheck-deepseek-adapter"
model_id = "deepseek-ai/DeepSeek-R1-Distill-Llama-8B"

tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    torch_dtype=torch.float16,
    device_map="auto"
)

# Load LoRA adapter
from peft import PeftModel
model = PeftModel.from_pretrained(model, adapter_id)

def diagnose_stream(symptoms: str):
    inputs = tokenizer(symptoms, return_tensors="pt").to(model.device)
    
    with torch.no_grad():
        for token in model.generate(**inputs, max_new_tokens=500, do_sample=False):
            decoded = tokenizer.decode(token, skip_special_tokens=True)
            yield decoded

interface = gr.Interface(
    fn=diagnose_stream,
    inputs="text",
    outputs="text",
    title="VitaCheck AI",
    description="Micronutrient diagnostic reasoning"
)

interface.launch()
```

**Deploy**:
1. Push to GitHub
2. Create HF Spaces app
3. Connect to ZeroGPU
4. Enable streaming interface

### 6.3 Production Checklist

- [ ] Load testing completed (100+ concurrent requests)
- [ ] Latency benchmarks verified (<5s)
- [ ] Error handling & logging
- [ ] Rate limiting configured
- [ ] API documentation (FastAPI Swagger)
- [ ] Client error boundaries
- [ ] Monitoring & alerting
- [ ] Database backups
- [ ] Security headers (CORS, CSP)

### 6.4 Monitoring & Observability

**File**: `server/monitoring.py`

```python
from prometheus_client import Counter, Histogram
import time

# Metrics
request_count = Counter('vitacheck_requests_total', 'Total requests')
response_latency = Histogram('vitacheck_response_seconds', 'Response latency')
hallucination_rate = Gauge('vitacheck_hallucinations', 'Hallucination rate')

@app.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    start = time.time()
    request_count.inc()
    
    try:
        async for token in token_generator():
            yield token
    finally:
        response_latency.observe(time.time() - start)
```

### 6.5 Deliverables (Week 6-7)
- [ ] GGUF quantization completed
- [ ] HF Spaces deployment live
- [ ] Load testing passed
- [ ] Monitoring dashboard active
- [ ] Documentation complete
- [ ] Production launch

---

## Critical Decision Points

### Model Serving Strategy
| Option | Latency | Cost | Setup Time | Recommendation |
|--------|---------|------|------------|-----------------|
| Ollama (Local) | 3-5s | $0 | 30min | **Start here** (dev) |
| vLLM (Cloud VM) | 1-3s | ~$10/mo | 2hrs | Scale if needed |
| HF Spaces ZeroGPU | 2-4s | Free | 1hr | Production (backup) |
| Groq API (Extractor) | <500ms | Free tier | 15min | Use for Stage 1 |

### Data Strategy
- **Fine-tuning**: Use your prepared dataset for medical reasoning
- **RAG**: Essential for current micronutrient facts (USDA, drug interactions)
- **Hybrid**: Fine-tune for "intuition," RAG for "facts"

### Safety-First Approach
1. Implement emergency guardrails FIRST (Phase 5)
2. Never skip bias testing
3. Always include "consult a physician" disclaimer
4. Track hallucinations in production

---

## Success Metrics

| Metric | Target | Phase |
|--------|--------|-------|
| TTFT | <1s | 1, 6 |
| Total Latency | <5s | 1, 6 |
| Diagnostic Accuracy | >85% | 4, 5 |
| Hallucination Rate | <1% | 3, 5 |
| Uptime | 99.5% | 7 |
| Cost (monthly) | <$50 | 6 |

---

## Troubleshooting Guide

### **Problem**: Latency >5s
- **Solution**: Check GPU utilization with `nvidia-smi`
- **Escalation**: Switch to vLLM from Ollama

### **Problem**: Out of Memory (OOM) during fine-tuning
- **Solution**: Already handled by Unsloth + QLoRA
- **Fallback**: Reduce batch size or rank

### **Problem**: High hallucination rate
- **Solution**: Implement RAG (Phase 3) and safety guardrails (Phase 5)

### **Problem**: Low diagnostic accuracy
- **Solution**: Increase training data size; audit fine-tuning data quality

---

## Resource Links

- **Base Model**: [deepseek-ai/DeepSeek-R1-Distill-Llama-8B](https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Llama-8B)
- **Fine-tuning**: [Unsloth Docs](https://github.com/unslothai/unsloth)
- **Inference**: [vLLM](https://docs.vllm.ai/), [Ollama](https://ollama.ai)
- **RAG**: [LangChain Docs](https://python.langchain.com/)
- **Evaluation**: [DeepEval GitHub](https://github.com/confident-ai/deepeval)
- **Hosting**: [HF Spaces ZeroGPU](https://huggingface.co/docs/hub/spaces-zerogpu)

---

**Next Steps**: Begin Phase 1 implementation immediately. Estimated completion: 6-7 weeks to full production deployment.
