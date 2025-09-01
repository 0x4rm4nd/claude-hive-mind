#!/usr/bin/env python3
"""
Max Subscription Performance Benchmark
=====================================
Benchmarks Claude Code subprocess overhead and concurrency handling
for Max subscription integration.
"""

import asyncio
import json
import statistics
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import List, Dict, Any

# Add current directory to path for imports
import sys
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

from shared.max_subscription_provider import MaxSubscriptionProvider


class PerformanceBenchmark:
    """Performance benchmarking suite for Max subscription provider"""
    
    def __init__(self):
        self.provider = MaxSubscriptionProvider()
        self.results = {
            "test_timestamp": time.time(),
            "single_request": {},
            "concurrent_requests": {},
            "latency_distribution": {},
            "resource_usage": {}
        }
    
    async def benchmark_single_request(self, iterations: int = 10) -> Dict[str, Any]:
        """Benchmark single request performance"""
        print(f"🔬 Benchmarking single requests ({iterations} iterations)...")
        
        # Test message
        test_messages = [
            {"role": "user", "content": "Say 'Hello from Max subscription benchmark' in exactly 5 words."}
        ]
        
        times = []
        for i in range(iterations):
            start_time = time.time()
            
            try:
                response = await self.provider.request_structured_response(
                    test_messages, 
                    "custom:claude-sonnet-4"  # Use Sonnet for consistency
                )
                end_time = time.time()
                
                request_time = end_time - start_time
                times.append(request_time)
                
                print(f"   Request {i+1}/{iterations}: {request_time:.2f}s")
                
            except Exception as e:
                print(f"   ❌ Request {i+1} failed: {e}")
                continue
        
        if not times:
            return {"error": "All requests failed"}
        
        results = {
            "iterations": len(times),
            "avg_time": statistics.mean(times),
            "min_time": min(times),
            "max_time": max(times),
            "median_time": statistics.median(times),
            "std_dev": statistics.stdev(times) if len(times) > 1 else 0,
            "raw_times": times
        }
        
        print(f"   ✅ Average: {results['avg_time']:.2f}s, Min: {results['min_time']:.2f}s, Max: {results['max_time']:.2f}s")
        return results
    
    async def benchmark_concurrent_requests(self, concurrency_levels: List[int] = [2, 5, 10]) -> Dict[str, Any]:
        """Benchmark concurrent request performance"""
        print(f"🚀 Benchmarking concurrent requests...")
        
        test_messages = [
            {"role": "user", "content": "Respond with exactly one word: 'Success'"}
        ]
        
        concurrent_results = {}
        
        for concurrency in concurrency_levels:
            print(f"\n   Testing {concurrency} concurrent requests...")
            
            start_time = time.time()
            
            # Create concurrent tasks
            tasks = []
            for i in range(concurrency):
                task = self.provider.request_structured_response(
                    test_messages, 
                    "custom:claude-sonnet-4"
                )
                tasks.append(task)
            
            # Execute all tasks concurrently
            try:
                responses = await asyncio.gather(*tasks, return_exceptions=True)
                end_time = time.time()
                
                total_time = end_time - start_time
                successful_requests = sum(1 for r in responses if not isinstance(r, Exception))
                failed_requests = concurrency - successful_requests
                
                concurrent_results[concurrency] = {
                    "total_time": total_time,
                    "successful_requests": successful_requests,
                    "failed_requests": failed_requests,
                    "requests_per_second": successful_requests / total_time if total_time > 0 else 0,
                    "avg_time_per_request": total_time / successful_requests if successful_requests > 0 else 0
                }
                
                print(f"      ✅ {successful_requests}/{concurrency} succeeded in {total_time:.2f}s")
                print(f"      📊 {concurrent_results[concurrency]['requests_per_second']:.2f} req/s")
                
            except Exception as e:
                print(f"      ❌ Concurrent test failed: {e}")
                concurrent_results[concurrency] = {"error": str(e)}
        
        return concurrent_results
    
    def benchmark_model_selection_overhead(self) -> Dict[str, Any]:
        """Benchmark model selection and mapping logic"""
        print("⚡ Benchmarking model selection overhead...")
        
        test_cases = [
            'custom:max-subscription',
            'custom:claude-opus-4',
            'custom:claude-sonnet-4',
            'custom:claude-3-7-sonnet',
            'custom:claude-3-5-haiku',
            'unknown-model'
        ]
        
        iterations = 10000  # Many iterations for micro-benchmark
        results = {}
        
        for model in test_cases:
            times = []
            
            for _ in range(iterations):
                start_time = time.perf_counter()
                
                # Simulate model selection logic
                if model == 'custom:max-subscription':
                    actual_model = self.provider.default_model
                elif model in self.provider.claude_code_model_mapping:
                    actual_model = model
                else:
                    actual_model = self.provider.default_model
                
                claude_code_model = self.provider.claude_code_model_mapping.get(actual_model, 'sonnet')
                
                end_time = time.perf_counter()
                times.append(end_time - start_time)
            
            results[model] = {
                "avg_time_microseconds": statistics.mean(times) * 1_000_000,
                "total_iterations": iterations
            }
        
        for model, stats in results.items():
            print(f"   {model}: {stats['avg_time_microseconds']:.2f}μs")
        
        return results
    
    async def run_full_benchmark(self) -> Dict[str, Any]:
        """Run complete benchmark suite"""
        print("🧪 Max Subscription Performance Benchmark")
        print("=" * 45)
        
        # Single request benchmark
        self.results["single_request"] = await self.benchmark_single_request()
        
        # Concurrent request benchmark  
        self.results["concurrent_requests"] = await self.benchmark_concurrent_requests()
        
        # Model selection overhead
        self.results["model_selection_overhead"] = self.benchmark_model_selection_overhead()
        
        # Performance analysis
        self.results["analysis"] = self._analyze_performance()
        
        return self.results
    
    def _analyze_performance(self) -> Dict[str, Any]:
        """Analyze performance results and provide recommendations"""
        analysis = {
            "recommendations": [],
            "performance_grade": "A",  # Default optimistic grade
            "bottlenecks": []
        }
        
        # Analyze single request performance
        if "avg_time" in self.results["single_request"]:
            avg_time = self.results["single_request"]["avg_time"]
            
            if avg_time > 10.0:
                analysis["performance_grade"] = "D"
                analysis["bottlenecks"].append("High single request latency")
                analysis["recommendations"].append("Investigate Claude Code subprocess startup overhead")
            elif avg_time > 5.0:
                analysis["performance_grade"] = "C"
                analysis["bottlenecks"].append("Moderate single request latency")
            elif avg_time > 2.0:
                analysis["performance_grade"] = "B"
        
        # Analyze concurrent performance
        if self.results["concurrent_requests"]:
            for concurrency, stats in self.results["concurrent_requests"].items():
                if "failed_requests" in stats and stats["failed_requests"] > 0:
                    analysis["bottlenecks"].append(f"Request failures at {concurrency} concurrency")
                    analysis["recommendations"].append("Consider connection pooling or rate limiting")
        
        # Analyze model selection overhead
        if self.results["model_selection_overhead"]:
            max_overhead = max(
                stats["avg_time_microseconds"] 
                for stats in self.results["model_selection_overhead"].values()
            )
            
            if max_overhead > 100:  # > 100 microseconds
                analysis["bottlenecks"].append("High model selection overhead")
                analysis["recommendations"].append("Optimize model mapping logic")
        
        return analysis
    
    def save_results(self, filepath: str = "results/benchmark_results.json"):
        """Save benchmark results to file"""
        with open(filepath, 'w') as f:
            json.dump(self.results, f, indent=2)
        print(f"📊 Results saved to {filepath}")
    
    def print_summary(self):
        """Print benchmark summary"""
        print("\n" + "=" * 45)
        print("📊 BENCHMARK SUMMARY")
        print("=" * 45)
        
        if "avg_time" in self.results["single_request"]:
            avg = self.results["single_request"]["avg_time"]
            print(f"Single Request Average: {avg:.2f}s")
        
        if self.results["concurrent_requests"]:
            best_throughput = max(
                stats.get("requests_per_second", 0)
                for stats in self.results["concurrent_requests"].values()
                if isinstance(stats, dict) and "requests_per_second" in stats
            )
            print(f"Best Throughput: {best_throughput:.2f} req/s")
        
        if "analysis" in self.results:
            grade = self.results["analysis"]["performance_grade"]
            print(f"Performance Grade: {grade}")
            
            if self.results["analysis"]["recommendations"]:
                print("\nRecommendations:")
                for rec in self.results["analysis"]["recommendations"]:
                    print(f"  • {rec}")


async def main():
    """Run performance benchmark"""
    benchmark = PerformanceBenchmark()
    
    try:
        await benchmark.run_full_benchmark()
        benchmark.print_summary()
        benchmark.save_results("results/benchmark_results.json")
        
    except KeyboardInterrupt:
        print("\n⚠️  Benchmark interrupted by user")
    except Exception as e:
        print(f"❌ Benchmark failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())