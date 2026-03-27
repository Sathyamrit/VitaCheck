import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
import time

# Model to test - using Mistral-7B (widely available, good for quantization testing)
# Alternative: "meta-llama/Llama-2-7b" or "Qwen/Qwen1.5-7B-Chat"
MODEL_ID = "mistralai/Mistral-7B-Instruct-v0.1"

def load_model_fp16():
    """Load model in FP16 (half precision)."""
    print(f"   Downloading {MODEL_ID}...")
    
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_ID,
        torch_dtype=torch.float16,
        device_map="auto",
        trust_remote_code=True
    )
    tokenizer = AutoTokenizer.from_pretrained(
        MODEL_ID,
        trust_remote_code=True
    )
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    
    return model, tokenizer

def load_model_int4():
    """Load model in 4-bit quantization."""
    print(f"   Loading {MODEL_ID} with 4-bit quantization...")
    model_id = MODEL_ID
    
    # 4-bit quantization config
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_use_double_quant=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.float16
    )
    
    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        quantization_config=bnb_config,
        device_map="auto",
        trust_remote_code=True
    )
    tokenizer = AutoTokenizer.from_pretrained(
        model_id,
        trust_remote_code=True
    )
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    
    return model, tokenizer

def benchmark_generation(model, tokenizer, prompt, num_tokens=500):
    """Benchmark text generation."""
    
    inputs = tokenizer(prompt, return_tensors="pt").to("cuda")
    
    # Warmup
    with torch.no_grad():
        model.generate(**inputs, max_new_tokens=10)
    
    # Benchmark
    start = time.time()
    
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=num_tokens,
        )
    
    elapsed = time.time() - start
    tokens_generated = outputs.shape[1] - inputs["input_ids"].shape[1]
    
    return {
        "latency_ms": elapsed * 1000,
        "tokens": tokens_generated,
        "tps": tokens_generated / elapsed if elapsed > 0 else 0,
    }

def test_quantizations():
    """Compare quantization methods."""
    
    prompt = """Patient Profile:
Symptoms: tiredness, weakness, fatigue
Age: 35
Sex: female
Medications: None
Allergies: None

Please analyze for potential micronutrient deficiencies and recommend dietary changes."""
    
    print("\n" + "="*70)
    print("PHASE 2: QUANTIZATION COMPARISON TEST")
    print("="*70)
    print(f"\nModel: {MODEL_ID}")
    print(f"Prompt length: {len(prompt)} characters")
    print("\n" + "-" * 70)
    
    # Test FP16
    print("\n1️⃣  Testing FP16 (Half Precision)...")
    try:
        model_fp16, tokenizer = load_model_fp16()
        
        # Get GPU memory before
        torch.cuda.empty_cache()
        torch.cuda.reset_peak_memory_stats()
        
        result_fp16 = benchmark_generation(model_fp16, tokenizer, prompt)
        mem_fp16 = torch.cuda.max_memory_allocated() / 1024**3
        
        print(f"   ✓ Latency: {result_fp16['latency_ms']:.0f}ms")
        print(f"   ✓ Throughput (TPS): {result_fp16['tps']:.2f} tokens/sec")
        print(f"   ✓ Memory Used: {mem_fp16:.2f}GB")
        print(f"   ✓ Tokens Generated: {result_fp16['tokens']}")
        
        del model_fp16
        torch.cuda.empty_cache()
    except Exception as e:
        print(f"   ✗ Error: {str(e)[:100]}...")
        print(f"\n   💡 Troubleshooting:")
        print(f"      - Check internet connection (model needs downloading)")
        print(f"      - Ensure at least 20GB free disk space")
        print(f"      - Run: pip install --upgrade transformers accelerate")
        result_fp16 = None
    
    # Test 4-bit
    print("\n2️⃣  Testing 4-bit Quantization (NF4)...")
    try:
        model_int4, tokenizer = load_model_int4()
        
        # Get GPU memory before
        torch.cuda.empty_cache()
        torch.cuda.reset_peak_memory_stats()
        
        result_int4 = benchmark_generation(model_int4, tokenizer, prompt)
        mem_int4 = torch.cuda.max_memory_allocated() / 1024**3
        
        print(f"   ✓ Latency: {result_int4['latency_ms']:.0f}ms")
        print(f"   ✓ Throughput (TPS): {result_int4['tps']:.2f} tokens/sec")
        print(f"   ✓ Memory Used: {mem_int4:.2f}GB")
        print(f"   ✓ Tokens Generated: {result_int4['tokens']}")
        
        del model_int4
        torch.cuda.empty_cache()
    except Exception as e:
        print(f"   ✗ Error: {str(e)[:100]}...")
        print(f"\n   💡 Troubleshooting:")
        print(f"      - Check bitsandbytes installation: pip install bitsandbytes")
        print(f"      - Verify CUDA availability: python -c \"import torch; print(torch.cuda.is_available())\"")
        result_int4 = None
    
    # Compare results
    print("\n" + "="*70)
    if result_fp16 and result_int4:
        print("COMPARISON: FP16 vs 4-bit Quantization")
        print("="*70)
        
        latency_improvement = (result_fp16['latency_ms'] - result_int4['latency_ms']) / result_fp16['latency_ms'] * 100
        memory_reduction = (mem_fp16 - mem_int4) / mem_fp16 * 100
        tps_improvement = (result_int4['tps'] - result_fp16['tps']) / result_fp16['tps'] * 100
        
        print(f"\n📊 Metrics Comparison:")
        print(f"   Latency Change:  {latency_improvement:+.1f}% (lower is better)")
        print(f"   Memory Reduction: {memory_reduction:+.1f}% (higher is better)")
        print(f"   Throughput Change: {tps_improvement:+.1f}% (higher is better)")
        
        print(f"\n📊 Absolute Values:")
        print(f"   {'Metric':<20} {'FP16':<20} {'4-bit':<20}")
        print(f"   {'-'*60}")
        print(f"   {'Latency':<20} {result_fp16['latency_ms']:>7.0f}ms {result_int4['latency_ms']:>18.0f}ms")
        print(f"   {'Memory':<20} {mem_fp16:>7.2f}GB {mem_int4:>18.2f}GB")
        print(f"   {'TPS':<20} {result_fp16['tps']:>7.2f} tok/s {result_int4['tps']:>17.2f} tok/s")
        
        print(f"\n{'='*70}")
        if memory_reduction > 30:
            print("✅ RECOMMENDATION: Switch to 4-bit quantization for Phase 2")
            print(f"   Reason: {memory_reduction:.1f}% memory reduction achieved")
        else:
            print("⚠️  MIXED RESULTS: Review carefully before switching")
            print(f"   Memory reduction only {memory_reduction:.1f}% (target was >30%)")
        print(f"{'='*70}\n")
    else:
        print("❌ BENCHMARK INCOMPLETE")
        print("   Could not compare - one or both tests failed")
        print(f"   FP16 test: {'✓' if result_fp16 else '✗'}")
        print(f"   4-bit test: {'✓' if result_int4 else '✗'}")
        print(f"{'='*70}\n")

if __name__ == "__main__":
    test_quantizations()