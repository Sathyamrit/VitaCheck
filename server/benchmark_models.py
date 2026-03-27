"""
VitaCheck Phase 2: Model Quantization & Performance Benchmark
Tests different quantization levels and measures TTFT, TPS, and latency.
"""

import asyncio
import time
import json
import httpx
from typing import Dict, List, Optional
import subprocess
import sys

class ModelBenchmark:
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url
        self.results = []
        
    async def test_endpoint(self, url: str, timeout: int = 5) -> bool:
        """Check if endpoint is reachable."""
        try:
            async with httpx.AsyncClient(timeout=timeout) as client:
                response = await client.get(url)
                return response.status_code == 200
        except:
            return False
    
    async def benchmark_stream(
        self, 
        model: str, 
        prompt: str, 
        runs: int = 3,
        timeout: int = 120
    ) -> Optional[Dict]:
        """
        Benchmark model with streaming.
        Returns: avg_ttft, avg_tps, avg_latency
        """
        print(f"\n  Benchmarking: {model}")
        
        metrics = {
            "model": model,
            "prompt_length": len(prompt),
            "runs": runs,
            "ttft_ms": [],
            "tps": [],
            "latency_ms": [],
            "token_count": [],
        }
        
        for run in range(runs):
            print(f"    Run {run+1}/{runs}...", end=" ", flush=True)
            
            start_time = time.time()
            first_token_time = None
            token_count = 0
            
            try:
                async with httpx.AsyncClient(timeout=timeout) as client:
                    async with client.stream(
                        "POST",
                        f"{self.base_url}/api/generate",
                        json={
                            "model": model,
                            "prompt": prompt,
                            "stream": True,
                            "temperature": 0.7,
                            "top_p": 0.9,
                        }
                    ) as response:
                        if response.status_code != 200:
                            print(f"ERROR: HTTP {response.status_code}")
                            return None
                        
                        async for line in response.aiter_lines():
                            if line:
                                # TTFT: time to first token
                                if first_token_time is None:
                                    first_token_time = time.time() - start_time
                                    metrics["ttft_ms"].append(first_token_time * 1000)
                                
                                token_count += 1
                                await asyncio.sleep(0)
            
            except httpx.TimeoutException:
                print("TIMEOUT")
                continue
            except Exception as e:
                print(f"ERROR: {e}")
                continue
            
            end_time = time.time()
            total_latency = (end_time - start_time) * 1000
            elapsed = (end_time - start_time)
            tps = (token_count / elapsed) if elapsed > 0 else 0
            
            metrics["tps"].append(tps)
            metrics["latency_ms"].append(total_latency)
            metrics["token_count"].append(token_count)
            
            print(f"✓ TTFT: {metrics['ttft_ms'][-1]:.0f}ms | TPS: {tps:.1f} | Tokens: {token_count}")
        
        # Only return if we got valid data
        if not metrics["ttft_ms"]:
            print(f"  FAILED to benchmark {model}")
            return None
        
        # Calculate averages
        result = {
            "model": model,
            "ttft_avg_ms": sum(metrics["ttft_ms"]) / len(metrics["ttft_ms"]),
            "ttft_min_ms": min(metrics["ttft_ms"]),
            "ttft_max_ms": max(metrics["ttft_ms"]),
            "tps_avg": sum(metrics["tps"]) / len(metrics["tps"]),
            "tps_min": min(metrics["tps"]),
            "tps_max": max(metrics["tps"]),
            "latency_avg_ms": sum(metrics["latency_ms"]) / len(metrics["latency_ms"]),
            "latency_min_ms": min(metrics["latency_ms"]),
            "latency_max_ms": max(metrics["latency_ms"]),
            "tokens_avg": sum(metrics["token_count"]) / len(metrics["token_count"]),
            "runs_completed": len(metrics["ttft_ms"]),
        }
        
        return result
    
    async def run_comparison(self, models: List[str], prompt: str, runs: int = 3):
        """Compare multiple models."""
        print(f"\n{'='*80}")
        print("VitaCheck PHASE 2: MODEL QUANTIZATION BENCHMARK")
        print(f"{'='*80}")
        print(f"\nConfiguration:")
        print(f"  Prompt length: {len(prompt)} characters")
        print(f"  Runs per model: {runs}")
        print(f"  Ollama endpoint: {self.base_url}")
        
        # Check if Ollama is running
        if not await self.test_endpoint(f"{self.base_url}/api/tags"):
            print("\n❌ ERROR: Ollama is not running!")
            print("   Start Ollama with: ollama serve")
            return {
                "status": "failed",
                "reason": "Ollama not running",
                "results": []
            }
        
        print("  ✓ Ollama is running")
        print(f"\nBenchmarking {len(models)} model(s)...")
        
        for model in models:
            print(f"\n• Testing: {model}")
            result = await self.benchmark_stream(model, prompt, runs)
            
            if result:
                self.results.append(result)
            else:
                print(f"  ✗ Failed to benchmark {model}")
        
        # Summary
        if not self.results:
            print("\n❌ No results collected!")
            return {"status": "failed", "reason": "No models benchmarked", "results": []}
        
        print(f"\n{'='*80}")
        print("RESULTS SUMMARY")
        print(f"{'='*80}\n")
        print(f"{'Model':<30} {'TTFT (ms)':<15} {'TPS':<12} {'Latency (ms)':<15}")
        print("-" * 80)
        
        baseline = None
        sorted_results = sorted(self.results, key=lambda x: x["ttft_avg_ms"])
        
        for result in sorted_results:
            ttft = result["ttft_avg_ms"]
            tps = result["tps_avg"]
            latency = result["latency_avg_ms"]
            
            if baseline is None:
                baseline = result
                marker = " (baseline)"
            else:
                ttft_improvement = ((baseline["ttft_avg_ms"] - ttft) 
                                   / baseline["ttft_avg_ms"] * 100)
                latency_improvement = ((baseline["latency_avg_ms"] - latency)
                                      / baseline["latency_avg_ms"] * 100)
                marker = f" ({ttft_improvement:+.1f}%, {latency_improvement:+.1f}% latency)"
            
            print(f"{result['model']:<30} "
                  f"{ttft:<14.0f} "
                  f"{tps:<11.1f} "
                  f"{latency:<14.0f}{marker}")
        
        print(f"\n{'='*80}\n")
        
        # Detailed Results
        print("DETAILED RESULTS:\n")
        for result in sorted_results:
            print(f"• {result['model']}")
            print(f"  TTFT:     {result['ttft_avg_ms']:.0f}ms (min: {result['ttft_min_ms']:.0f}, max: {result['ttft_max_ms']:.0f})")
            print(f"  TPS:      {result['tps_avg']:.1f} tokens/sec (min: {result['tps_min']:.1f}, max: {result['tps_max']:.1f})")
            print(f"  Latency:  {result['latency_avg_ms']:.0f}ms (min: {result['latency_min_ms']:.0f}, max: {result['latency_max_ms']:.0f})")
            print(f"  Avg Tokens: {result['tokens_avg']:.0f}")
            print()
        
        # Recommendations
        print("RECOMMENDATIONS:\n")
        best_ttft = sorted_results[0]
        print(f"✓ Fastest TTFT: {best_ttft['model']} ({best_ttft['ttft_avg_ms']:.0f}ms)")
        
        best_tps = max(sorted_results, key=lambda x: x["tps_avg"])
        print(f"✓ Best Throughput: {best_tps['model']} ({best_tps['tps_avg']:.1f} tokens/sec)")
        
        best_latency = sorted_results[0]
        print(f"✓ Lowest Total Latency: {best_latency['model']} ({best_latency['latency_avg_ms']:.0f}ms)")
        
        # Save results
        output = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "configuration": {
                "ollama_url": self.base_url,
                "prompt_length": len(prompt),
                "runs_per_model": runs,
            },
            "results": sorted_results,
            "summary": {
                "models_tested": len(self.results),
                "baseline_model": baseline["model"],
            }
        }
        
        with open("benchmark_results_phase2.json", "w") as f:
            json.dump(output, f, indent=2)
        print(f"\n✓ Results saved to: benchmark_results_phase2.json\n")
        
        return output


async def main():
    """Run benchmarks."""
    
    # Test prompt (realistic micronutrient diagnostic)
    test_prompt = """Patient Profile:
Symptoms: tiredness, weakness, brain fog, poor concentration
Age: 35
Sex: female
Current medications: Birth control pill
Allergies: Shellfish

Analyze this patient for likely micronutrient deficiencies. Consider:
1. Symptom patterns
2. Common deficiencies by age/sex
3. Medication interactions
4. Most likely deficiencies
5. Recommended blood tests
6. Dietary sources for supplementation"""
    
    # Models to test (add more as they become available)
    models_to_test = [
        "deepseek-r1:8b",    # Current 8-bit (baseline)
        # "deepseek-r1:4b",  # 4-bit if available
        # "mistral:7b",      # Alternative model comparison
    ]
    
    # Run benchmark
    benchmark = ModelBenchmark()
    results = await benchmark.run_comparison(
        models_to_test, 
        test_prompt, 
        runs=3  # Number of runs per model
    )
    
    # Print status
    if results["status"] == "failed":
        print(f"\n❌ Benchmark failed: {results['reason']}")
        sys.exit(1)
    else:
        print("✓ Benchmark completed successfully!")
        sys.exit(0)


if __name__ == "__main__":
    print("Starting VitaCheck Phase 2 Benchmark...\n")
    
    # Check for required packages
    try:
        import httpx
    except ImportError:
        print("❌ Missing 'httpx' package. Install with: pip install httpx")
        sys.exit(1)
    
    # Run async benchmarks
    asyncio.run(main())
