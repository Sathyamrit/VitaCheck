#!/usr/bin/env python
"""
Phase 5 Benchmark Runner - Evaluate diagnostic accuracy and safety metrics
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from evaluation.benchmark_suite import BenchmarkSuite

async def main():
    suite = BenchmarkSuite()
    
    print('=' * 70)
    print('PHASE 5: BENCHMARK SUITE EXECUTION')
    print('=' * 70)
    print(f'Loaded test cases: {len(suite.test_cases)}')
    print()
    
    # Mock diagnosis function for testing
    async def mock_diagnosis(symptoms):
        deficiencies = {
            'fatigue': 'Vitamin D',
            'muscle pain': 'Magnesium',
            'brain fog': 'Vitamin B12',
            'pale skin': 'Iron',
            'brittle nails': 'Iron',
            'weakness': 'Vitamin D'
        }
        found = [deficiencies.get(s, 'Micronutrient') for s in symptoms if s in deficiencies]
        recs = ' and '.join(found) if found else 'Vitamin D'
        return f'Based on symptoms ({", ".join(symptoms)}), recommend {recs} supplementation.'
    
    # Run benchmark
    report = await suite.run_benchmark(diagnosis_fn=mock_diagnosis, num_cases=30)
    
    print()
    print('=' * 70)
    print('BENCHMARK RESULTS')
    print('=' * 70)
    print(f'Overall Status: {report["overall_status"]}')
    print(f'Tests Evaluated: {report["test_count"]}')
    print()
    
    print('📊 ACCURACY METRICS:')
    acc = report['metrics']['accuracy']
    print(f'  Mean:     {acc["mean"]:.2%}')
    print(f'  Median:   {acc["median"]:.2%}')
    print(f'  Range:    {acc["min"]:.2%} - {acc["max"]:.2%}')
    print(f'  Passed:   {acc["passed"]}/{report["test_count"]} (>85% threshold)')
    print()
    
    print('🚨 HALLUCINATION METRICS:')
    hall = report['metrics']['hallucination']
    print(f'  Mean:     {hall["mean"]:.2%}')
    print(f'  Max:      {hall["max"]:.2%}')
    print(f'  Passed:   {hall["passed"]}/{report["test_count"]} (<1% threshold)')
    print()
    
    print('⚖️  BIAS METRICS:')
    bias = report['metrics']['bias']
    print(f'  Mean:     {bias["mean"]:.2%}')
    print(f'  Max:      {bias["max"]:.2%}')
    print(f'  Passed:   {bias["passed"]}/{report["test_count"]} (<20% threshold)')
    print()
    
    print('⏱️  LATENCY METRICS:')
    lat = report['metrics']['latency']
    print(f'  Mean:     {lat["mean_ms"]:.1f} ms')
    print(f'  Max:      {lat["max_ms"]:.1f} ms')
    print(f'  Passed:   {lat["passed"]}/{report["test_count"]} (<5s threshold)')
    print()
    
    print('=' * 70)
    print(f'✅ BENCHMARK COMPLETE - Status: {report["overall_status"]}')
    print('=' * 70)

if __name__ == "__main__":
    asyncio.run(main())
