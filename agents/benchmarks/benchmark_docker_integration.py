#!/usr/bin/env python3
"""
Claude Max Docker Integration Performance Benchmark
==================================================
Real performance benchmarking for the Docker-based Claude Max subscription integration.
Tests actual response times with working Claude Max subscription through Docker service.
"""

import asyncio
import json
import statistics
import time
from pathlib import Path
from typing import List, Dict, Any
import sys
import os

# Add paths for imports
sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent / "pydantic_ai" / "shared" / "custom_provider" / "claude_max"))

try:
    from api_service_client import ClaudeAPIServiceClient
    DOCKER_CLIENT_AVAILABLE = True
    print("✅ Docker integration client available")
except ImportError as e:
    print(f"❌ Docker integration client not available: {e}")
    DOCKER_CLIENT_AVAILABLE = False

try:
    import aiohttp
    AIOHTTP_AVAILABLE = True
except ImportError:
    print("❌ aiohttp not available - installing...")
    os.system("pip install aiohttp")
    import aiohttp
    AIOHTTP_AVAILABLE = True


class DockerIntegrationBenchmark:
    """Performance benchmarking for Docker-based Claude Max integration"""
    
    def __init__(self):
        self.api_base_url = "http://localhost:47291"
        self.client = ClaudeAPIServiceClient() if DOCKER_CLIENT_AVAILABLE else None
        self.results = {
            "test_timestamp": time.time(),
            "test_type": "docker_integration_benchmark",
            "service_info": {},
            "health_check": {},
            "single_request": {},
            "concurrent_requests": {},
            "model_comparison": {},
            "parallel_scaling": {},
            "analysis": {}
        }
    
    async def check_service_health(self) -> Dict[str, Any]:
        """Verify Docker service is running and healthy"""
        print("🔍 Checking Docker service health...")
        
        try:
            async with aiohttp.ClientSession() as session:
                start_time = time.time()
                async with session.get(
                    f"{self.api_base_url}/health",
                    timeout=aiohttp.ClientTimeout(total=20)
                ) as response:
                    end_time = time.time()
                    
                    if response.status == 200:
                        health_data = await response.json()
                        health_data["response_time"] = end_time - start_time
                        print(f"✅ Service healthy - Response time: {health_data['response_time']:.3f}s")
                        return health_data
                    else:
                        error_data = {
                            "status": "unhealthy",
                            "response_code": response.status,
                            "response_time": end_time - start_time
                        }
                        print(f"❌ Service unhealthy - Status: {response.status}")
                        return error_data
                        
        except Exception as e:
            print(f"❌ Health check failed: {e}")
            return {"status": "error", "error": str(e)}
    
    async def benchmark_single_requests(self, iterations: int = 5) -> Dict[str, Any]:
        """Benchmark single request performance with real Claude responses"""
        print(f"🔬 Benchmarking single requests ({iterations} iterations)...")
        
        if not self.client:
            print("❌ Docker client not available")
            return {"error": "Docker client not available"}
        
        # Test with meaningful prompt that requires actual Claude processing
        test_prompt = "Explain in exactly 3 sentences what makes Python a popular programming language."
        
        times = []
        responses = []
        
        for i in range(iterations):
            print(f"   Request {i+1}/{iterations}...")
            start_time = time.time()
            
            try:
                response = await self.client.send_prompt(test_prompt, "custom:max-subscription")
                end_time = time.time()
                
                request_time = end_time - start_time
                times.append(request_time)
                responses.append(len(response))  # Response length as quality indicator
                
                print(f"   ✅ Completed in {request_time:.2f}s - Response: {len(response)} chars")
                
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
            "avg_response_length": statistics.mean(responses),
            "raw_times": times,
            "raw_response_lengths": responses
        }
        
        print(f"   📊 Average: {results['avg_time']:.2f}s, Range: {results['min_time']:.2f}s - {results['max_time']:.2f}s")
        return results
    
    async def benchmark_concurrent_requests(self, concurrency_levels: List[int] = [2, 3, 5]) -> Dict[str, Any]:
        """Benchmark concurrent request performance"""
        print(f"🚀 Benchmarking concurrent requests...")
        
        if not self.client:
            return {"error": "Docker client not available"}
        
        # Use shorter prompts for concurrent testing to reduce Claude processing time variation
        test_prompt = "Say 'Max subscription working' and add the current time."
        
        concurrent_results = {}
        
        for concurrency in concurrency_levels:
            print(f"\n   Testing {concurrency} concurrent requests...")
            
            start_time = time.time()
            
            # Create concurrent tasks
            tasks = []
            for i in range(concurrency):
                task = self.client.send_prompt(
                    f"{test_prompt} Request #{i+1}.", 
                    "custom:max-subscription"
                )
                tasks.append(task)
            
            # Execute all tasks concurrently
            try:
                responses = await asyncio.gather(*tasks, return_exceptions=True)
                end_time = time.time()
                
                total_time = end_time - start_time
                successful_responses = [r for r in responses if not isinstance(r, Exception)]
                failed_requests = concurrency - len(successful_responses)
                
                concurrent_results[concurrency] = {
                    "total_time": total_time,
                    "successful_requests": len(successful_responses),
                    "failed_requests": failed_requests,
                    "requests_per_second": len(successful_responses) / total_time if total_time > 0 else 0,
                    "avg_time_per_request": total_time / len(successful_responses) if successful_responses else 0,
                    "avg_response_length": statistics.mean([len(r) for r in successful_responses]) if successful_responses else 0
                }
                
                print(f"      ✅ {len(successful_responses)}/{concurrency} succeeded in {total_time:.2f}s")
                print(f"      📊 {concurrent_results[concurrency]['requests_per_second']:.2f} req/s")
                
                if failed_requests > 0:
                    print(f"      ⚠️  {failed_requests} requests failed")
                    for i, resp in enumerate(responses):
                        if isinstance(resp, Exception):
                            print(f"         Request {i+1}: {resp}")
                
            except Exception as e:
                print(f"      ❌ Concurrent test failed: {e}")
                concurrent_results[concurrency] = {"error": str(e)}
        
        return concurrent_results
    
    async def benchmark_model_comparison(self) -> Dict[str, Any]:
        """Compare performance across different Claude models"""
        print("🎯 Benchmarking model performance comparison...")
        
        if not self.client:
            return {"error": "Docker client not available"}
        
        # Test models available through our integration
        models = [
            ("custom:max-subscription", "sonnet"),  # Default
            ("custom:claude-opus-4", "opus"),       # Opus
            ("custom:claude-sonnet-4", "sonnet"),   # Explicit Sonnet
            ("custom:claude-3-5-haiku", "haiku")    # Haiku
        ]
        
        test_prompt = "List 3 benefits of using Docker in software development."
        model_results = {}
        
        for custom_model, actual_model in models:
            print(f"\n   Testing {custom_model} ({actual_model})...")
            
            try:
                start_time = time.time()
                response = await self.client.send_prompt(test_prompt, custom_model)
                end_time = time.time()
                
                request_time = end_time - start_time
                
                model_results[custom_model] = {
                    "actual_model": actual_model,
                    "response_time": request_time,
                    "response_length": len(response),
                    "success": True
                }
                
                print(f"      ✅ {request_time:.2f}s - {len(response)} chars")
                
            except Exception as e:
                print(f"      ❌ Failed: {e}")
                model_results[custom_model] = {
                    "actual_model": actual_model,
                    "error": str(e),
                    "success": False
                }
        
        return model_results
    
    async def benchmark_parallel_scaling(self) -> Dict[str, Any]:
        """Test how well the integration scales with parallel requests"""
        print("📈 Testing parallel scaling efficiency...")
        
        if not self.client:
            return {"error": "Docker client not available"}
        
        test_prompt = "Respond with exactly: 'Parallel test successful'"
        baseline_time = None
        scaling_results = {}
        
        # Test scaling from 1 to higher concurrency levels
        concurrency_levels = [1, 2, 3, 4, 5]
        
        for concurrency in concurrency_levels:
            print(f"\n   Testing {concurrency} parallel requests...")
            
            start_time = time.time()
            
            if concurrency == 1:
                # Single request baseline
                try:
                    response = await self.client.send_prompt(test_prompt, "custom:max-subscription")
                    end_time = time.time()
                    total_time = end_time - start_time
                    baseline_time = total_time
                    successful = 1
                except Exception as e:
                    total_time = 0
                    successful = 0
                    print(f"      ❌ Baseline failed: {e}")
            else:
                # Multiple parallel requests
                tasks = [
                    self.client.send_prompt(f"{test_prompt} #{i+1}", "custom:max-subscription")
                    for i in range(concurrency)
                ]
                
                try:
                    responses = await asyncio.gather(*tasks, return_exceptions=True)
                    end_time = time.time()
                    total_time = end_time - start_time
                    successful = sum(1 for r in responses if not isinstance(r, Exception))
                except Exception as e:
                    total_time = 0
                    successful = 0
                    print(f"      ❌ Parallel test failed: {e}")
            
            # Calculate efficiency metrics
            if baseline_time and total_time > 0:
                theoretical_time = baseline_time * concurrency  # Sequential time
                speedup = theoretical_time / total_time
                efficiency = speedup / concurrency * 100
            else:
                speedup = 0
                efficiency = 0
            
            scaling_results[concurrency] = {
                "total_time": total_time,
                "successful_requests": successful,
                "failed_requests": concurrency - successful,
                "speedup": speedup,
                "efficiency_percent": efficiency,
                "requests_per_second": successful / total_time if total_time > 0 else 0
            }
            
            if total_time > 0:
                print(f"      ✅ {successful}/{concurrency} in {total_time:.2f}s - Efficiency: {efficiency:.1f}%")
            else:
                print(f"      ❌ Failed")
        
        return scaling_results
    
    def analyze_performance(self) -> Dict[str, Any]:
        """Analyze performance results and provide insights"""
        analysis = {
            "performance_grade": "A",
            "bottlenecks": [],
            "recommendations": [],
            "observations": []
        }
        
        # Analyze single request performance
        if "avg_time" in self.results.get("single_request", {}):
            avg_time = self.results["single_request"]["avg_time"]
            
            if avg_time > 30.0:
                analysis["performance_grade"] = "D"
                analysis["bottlenecks"].append("Very high response times (>30s)")
                analysis["recommendations"].append("Check Claude CLI authentication and Docker service health")
            elif avg_time > 20.0:
                analysis["performance_grade"] = "C"
                analysis["bottlenecks"].append("High response times (>20s)")
                analysis["recommendations"].append("Monitor Docker service performance")
            elif avg_time > 10.0:
                analysis["performance_grade"] = "B"
                analysis["observations"].append(f"Response time {avg_time:.1f}s is normal for Claude Max subscription")
            else:
                analysis["observations"].append(f"Excellent response time: {avg_time:.1f}s")
        
        # Analyze concurrent performance
        if self.results.get("concurrent_requests"):
            failures = sum(
                stats.get("failed_requests", 0) 
                for stats in self.results["concurrent_requests"].values()
                if isinstance(stats, dict)
            )
            
            if failures > 0:
                analysis["bottlenecks"].append("Some concurrent requests failed")
                analysis["recommendations"].append("Consider implementing request retry logic")
            else:
                analysis["observations"].append("All concurrent requests succeeded")
        
        # Analyze parallel scaling
        if self.results.get("parallel_scaling"):
            max_efficiency = max(
                stats.get("efficiency_percent", 0)
                for stats in self.results["parallel_scaling"].values()
                if isinstance(stats, dict)
            )
            
            if max_efficiency > 80:
                analysis["observations"].append(f"Excellent parallel efficiency: {max_efficiency:.1f}%")
            elif max_efficiency > 60:
                analysis["observations"].append(f"Good parallel efficiency: {max_efficiency:.1f}%")
            else:
                analysis["bottlenecks"].append("Low parallel efficiency")
                analysis["recommendations"].append("Investigate Docker service concurrency limits")
        
        return analysis
    
    async def run_full_benchmark(self) -> Dict[str, Any]:
        """Run complete benchmark suite"""
        print("🧪 Claude Max Docker Integration Performance Benchmark")
        print("=" * 60)
        
        # Service health check
        self.results["health_check"] = await self.check_service_health()
        
        if self.results["health_check"].get("status") != "healthy":
            print("❌ Service not healthy - aborting benchmark")
            return self.results
        
        # Service info
        if self.client:
            self.results["service_info"] = self.client.get_service_status()
        
        # Single request benchmark
        self.results["single_request"] = await self.benchmark_single_requests()
        
        # Concurrent request benchmark
        self.results["concurrent_requests"] = await self.benchmark_concurrent_requests()
        
        # Model comparison benchmark
        self.results["model_comparison"] = await self.benchmark_model_comparison()
        
        # Parallel scaling benchmark  
        self.results["parallel_scaling"] = await self.benchmark_parallel_scaling()
        
        # Performance analysis
        self.results["analysis"] = self.analyze_performance()
        
        return self.results
    
    def save_results(self, filepath: str = "results/docker_benchmark_results.json"):
        """Save benchmark results to file"""
        results_dir = Path(filepath).parent
        results_dir.mkdir(exist_ok=True)
        
        with open(filepath, 'w') as f:
            json.dump(self.results, f, indent=2)
        print(f"📊 Results saved to {filepath}")
    
    def print_summary(self):
        """Print comprehensive benchmark summary"""
        print("\n" + "=" * 60)
        print("📊 DOCKER INTEGRATION BENCHMARK SUMMARY")
        print("=" * 60)
        
        # Service status
        health = self.results.get("health_check", {})
        if health.get("status") == "healthy":
            print(f"✅ Service Status: {health['status']} ({health.get('response_time', 0):.3f}s)")
        else:
            print(f"❌ Service Status: {health.get('status', 'unknown')}")
        
        # Single request performance
        single = self.results.get("single_request", {})
        if "avg_time" in single:
            print(f"📈 Average Response Time: {single['avg_time']:.2f}s")
            print(f"📊 Response Time Range: {single['min_time']:.2f}s - {single['max_time']:.2f}s")
            print(f"📝 Average Response Length: {single.get('avg_response_length', 0):.0f} chars")
        
        # Concurrent performance
        concurrent = self.results.get("concurrent_requests", {})
        if concurrent:
            best_rps = max(
                stats.get("requests_per_second", 0)
                for stats in concurrent.values()
                if isinstance(stats, dict) and "requests_per_second" in stats
            )
            print(f"🚀 Best Throughput: {best_rps:.2f} req/s")
        
        # Model comparison
        models = self.results.get("model_comparison", {})
        if models:
            successful_models = [k for k, v in models.items() if v.get("success")]
            print(f"🎯 Working Models: {len(successful_models)}/4")
            
            if successful_models:
                fastest_model = min(
                    successful_models, 
                    key=lambda m: models[m].get("response_time", float('inf'))
                )
                print(f"⚡ Fastest Model: {fastest_model} ({models[fastest_model]['response_time']:.2f}s)")
        
        # Scaling efficiency
        scaling = self.results.get("parallel_scaling", {})
        if scaling:
            max_efficiency = max(
                stats.get("efficiency_percent", 0)
                for stats in scaling.values()
                if isinstance(stats, dict)
            )
            print(f"📈 Max Parallel Efficiency: {max_efficiency:.1f}%")
        
        # Performance grade and recommendations
        analysis = self.results.get("analysis", {})
        if analysis:
            print(f"🏆 Performance Grade: {analysis.get('performance_grade', 'N/A')}")
            
            if analysis.get("observations"):
                print("\n💡 Key Observations:")
                for obs in analysis["observations"]:
                    print(f"  • {obs}")
            
            if analysis.get("recommendations"):
                print("\n🔧 Recommendations:")
                for rec in analysis["recommendations"]:
                    print(f"  • {rec}")
        
        print("=" * 60)


async def main():
    """Run Docker integration benchmark"""
    if not DOCKER_CLIENT_AVAILABLE:
        print("❌ Docker integration client not available")
        print("📋 Ensure the Docker service is running and imports are working")
        return
    
    benchmark = DockerIntegrationBenchmark()
    
    try:
        await benchmark.run_full_benchmark()
        benchmark.print_summary()
        benchmark.save_results("results/docker_benchmark_results.json")
        
    except KeyboardInterrupt:
        print("\n⚠️  Benchmark interrupted by user")
    except Exception as e:
        print(f"❌ Benchmark failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())