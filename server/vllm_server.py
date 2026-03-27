"""
VitaCheck Phase 2: vLLM Inference Server
Alternative high-performance backend using vLLM for batch processing and optimization.

Usage:
    python vllm_server.py

Environment:
    - MODEL_NAME: HuggingFace model ID (default: deepseek-ai/DeepSeek-R1-Distill-Qwen-8B)
    - CUDA_VISIBLE_DEVICES: GPU IDs to use (default: 0)
    - MAX_MODEL_LEN: Context window (default: 8192)
"""

import os
import json
import time
import asyncio
from typing import AsyncGenerator, Optional
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

try:
    from vllm import LLM, SamplingParams
    from vllm.utils import random_uuid
    from vllm.engine.arg_utils import EngineArgs
except ImportError:
    print("ERROR: vLLM not installed!")
    print("Install with: pip install vllm")
    exit(1)

# ============================================================================
# CONFIGURATION
# ============================================================================

MODEL_NAME = os.getenv("MODEL_NAME", "deepseek-ai/DeepSeek-R1-Distill-Qwen-8B")
MAX_MODEL_LEN = int(os.getenv("MAX_MODEL_LEN", "8192"))
GPU_MEMORY_FRACTION = float(os.getenv("GPU_MEMORY_FRACTION", "0.9"))
DTYPE = os.getenv("DTYPE", "float16")

print(f"""
vLLM Configuration:
  Model: {MODEL_NAME}
  Max Context: {MAX_MODEL_LEN} tokens
  GPU Memory: {GPU_MEMORY_FRACTION*100:.0f}%
  Data Type: {DTYPE}
""")

# ============================================================================
# GLOBAL LLM ENGINE
# ============================================================================

llm_engine: Optional[LLM] = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize and cleanup LLM engine."""
    global llm_engine
    
    print("Initializing vLLM engine...")
    
    try:
        llm_engine = LLM(
            model=MODEL_NAME,
            tensor_parallel_size=1,
            gpu_memory_utilization=GPU_MEMORY_FRACTION,
            dtype=DTYPE,
            max_model_len=MAX_MODEL_LEN,
            enable_chunked_prefill=True,  # Better throughput for streaming
            max_num_seqs=32,  # Batch size capability
            max_seq_len_to_capture=8192,
            trust_remote_code=True,
        )
        print(f"✓ vLLM engine initialized with {MODEL_NAME}")
    except Exception as e:
        print(f"✗ Failed to initialize vLLM: {e}")
        raise
    
    yield
    
    # Cleanup
    if llm_engine:
        print("Shutting down vLLM engine...")
        del llm_engine

# ============================================================================
# DATA MODELS
# ============================================================================

class GenerateRequest(BaseModel):
    """Request for text generation."""
    prompt: str
    temperature: float = 0.7
    top_p: float = 0.9
    max_tokens: int = 1500
    repetition_penalty: float = 1.1

class GenerateResponse(BaseModel):
    """Response metadata."""
    status: str
    model: str
    prompt_tokens: int
    completion_tokens: int

# ============================================================================
# FASTAPI APP
# ============================================================================

app = FastAPI(
    title="VitaCheck vLLM Server",
    description="High-performance inference backend using vLLM",
    version="2.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================================
# STREAMING ENDPOINT
# ============================================================================

async def generate_stream(
    prompt: str,
    temperature: float,
    top_p: float,
    max_tokens: int,
    repetition_penalty: float
) -> AsyncGenerator[str, None]:
    """Stream tokens from vLLM."""
    
    if llm_engine is None:
        raise RuntimeError("LLM engine not initialized")
    
    sampling_params = SamplingParams(
        temperature=temperature,
        top_p=top_p,
        max_tokens=max_tokens,
        repetition_penalty=repetition_penalty,
    )
    
    # Important: vLLM expects list of prompts even for single generation
    request_id = random_uuid()
    
    start_time = time.time()
    token_count = 0
    
    try:
        # Generate with streaming
        generators = llm_engine.generate(
            prompts=[prompt],
            sampling_params=sampling_params,
            request_id=request_id,
        )
        
        # Iterate through outputs
        for output in generators:
            # Extract generated tokens
            generated_text = output.outputs[0].text
            
            # Stream back to client (sending full generated text at once)
            # For true token-by-token streaming, we'd need to intercept at a lower level
            if generated_text:
                yield json.dumps({
                    "type": "token",
                    "content": generated_text,
                    "token_count": len(output.outputs[0].token_ids),
                }) + "\n"
                token_count = len(output.outputs[0].token_ids)
    
    except Exception as e:
        yield json.dumps({
            "type": "error",
            "message": str(e)
        }) + "\n"
    
    finally:
        elapsed = time.time() - start_time
        tps = (token_count / elapsed) if elapsed > 0 else 0
        
        # Send completion metadata
        yield json.dumps({
            "type": "completed",
            "prompt_tokens": len(prompt.split()),
            "completion_tokens": token_count,
            "latency_ms": elapsed * 1000,
            "tokens_per_second": tps,
        }) + "\n"

@app.post("/generate")
async def generate(request: GenerateRequest):
    """Generate text with streaming."""
    
    return StreamingResponse(
        generate_stream(
            request.prompt,
            request.temperature,
            request.top_p,
            request.max_tokens,
            request.repetition_penalty,
        ),
        media_type="application/x-ndjson",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        }
    )

# ============================================================================
# HEALTH CHECKS
# ============================================================================

@app.get("/health")
async def health():
    """Health check endpoint."""
    
    if llm_engine is None:
        return {
            "status": "unhealthy",
            "reason": "Engine not initialized"
        }, 503
    
    return {
        "status": "healthy",
        "engine": "vLLM",
        "model": MODEL_NAME,
        "dtype": DTYPE,
        "max_context": MAX_MODEL_LEN,
        "gpu_memory_fraction": GPU_MEMORY_FRACTION,
    }

@app.get("/model-info")
async def model_info():
    """Get model information."""
    
    if llm_engine is None:
        raise HTTPException(status_code=503, detail="Engine not initialized")
    
    return {
        "model_name": MODEL_NAME,
        "context_length": MAX_MODEL_LEN,
        "data_type": DTYPE,
        "supports_batching": True,
        "supports_streaming": True,
        "max_batch_size": 32,
    }

# ============================================================================
# METRICS & MONITORING
# ============================================================================

class MetricsCollector:
    def __init__(self):
        self.requests_processed = 0
        self.total_tokens_generated = 0
        self.total_latency_ms = 0
    
    def record(self, tokens: int, latency_ms: float):
        self.requests_processed += 1
        self.total_tokens_generated += tokens
        self.total_latency_ms += latency_ms
    
    def get_stats(self):
        avg_latency = (self.total_latency_ms / self.requests_processed 
                      if self.requests_processed > 0 else 0)
        avg_tps = (self.total_tokens_generated / (self.total_latency_ms / 1000)
                  if self.total_latency_ms > 0 else 0)
        
        return {
            "requests_processed": self.requests_processed,
            "total_tokens_generated": self.total_tokens_generated,
            "avg_latency_ms": avg_latency,
            "avg_tokens_per_second": avg_tps,
        }

metrics = MetricsCollector()

@app.get("/metrics")
async def get_metrics():
    """Get performance metrics."""
    return metrics.get_stats()

# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    
    print(f"""
{'='*70}
VitaCheck Phase 2: vLLM Inference Server
{'='*70}

Endpoints:
  POST   /generate      - Generate text with streaming
  GET    /health        - Health check
  GET    /model-info    - Model information
  GET    /metrics       - Performance metrics
  GET    /docs          - API documentation

Starting server on: http://0.0.0.0:8001
Model: {MODEL_NAME}

Press Ctrl+C to stop.
{'='*70}
""")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8001,  # Different port from Ollama (8000) and main API (8000)
        log_level="info",
    )
