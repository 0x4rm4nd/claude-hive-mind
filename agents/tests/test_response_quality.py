#!/usr/bin/env python3
"""
Response Quality and Format Compatibility Test
==============================================
Tests the Docker-based Claude Max integration for response quality,
format compatibility, and different use cases across all model types.
"""

import asyncio
import json
import time
from typing import Dict, List, Any
import aiohttp


class ResponseQualityTester:
    """Test response quality and format compatibility"""
    
    def __init__(self):
        self.api_base_url = "http://localhost:47291"
        self.results = {
            "test_timestamp": time.time(),
            "service_health": {},
            "model_tests": {},
            "format_tests": {},
            "quality_metrics": {},
            "compatibility_analysis": {}
        }
    
    async def check_service_health(self) -> bool:
        """Verify Docker service is running and healthy"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.api_base_url}/health") as response:
                    if response.status == 200:
                        health_data = await response.json()
                        self.results["service_health"] = health_data
                        return health_data.get("status") == "healthy"
        except Exception as e:
            self.results["service_health"] = {"error": str(e)}
            return False
        return False
    
    async def send_request(self, prompt: str, model: str) -> Dict[str, Any]:
        """Send request and measure response"""
        start_time = time.time()
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.api_base_url}/claude",
                    json={"prompt": prompt, "model": model, "timeout": 60},
                    timeout=aiohttp.ClientTimeout(total=80)
                ) as response:
                    end_time = time.time()
                    
                    if response.status == 200:
                        result = await response.json()
                        return {
                            "success": True,
                            "response": result["response"],
                            "response_time": end_time - start_time,
                            "response_length": len(result["response"]),
                            "status_code": response.status
                        }
                    else:
                        error_text = await response.text()
                        return {
                            "success": False,
                            "error": error_text,
                            "response_time": end_time - start_time,
                            "status_code": response.status
                        }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "response_time": time.time() - start_time
            }
    
    async def test_model_quality(self) -> Dict[str, Any]:
        """Test response quality across different models"""
        print("🎯 Testing Model Response Quality")
        print("=" * 40)
        
        models = [
            ("custom:max-subscription", "sonnet"),
            ("custom:claude-opus-4", "opus"), 
            ("custom:claude-sonnet-4", "sonnet"),
            ("custom:claude-3-5-haiku", "haiku")
        ]
        
        test_prompt = "Explain the benefits of microservices architecture in exactly 3 bullet points."
        
        model_results = {}
        
        for custom_model, actual_model in models:
            print(f"\n📝 Testing {custom_model} ({actual_model}):")
            
            result = await self.send_request(test_prompt, actual_model)
            
            if result["success"]:
                response = result["response"]
                quality_score = self.analyze_response_quality(response, test_prompt)
                
                model_results[custom_model] = {
                    "actual_model": actual_model,
                    "response_time": result["response_time"],
                    "response_length": result["response_length"],
                    "quality_score": quality_score,
                    "response_preview": response[:150] + "..." if len(response) > 150 else response,
                    "success": True
                }
                
                print(f"   ✅ Success ({result['response_time']:.2f}s, {result['response_length']} chars)")
                print(f"   📊 Quality Score: {quality_score:.1f}/10")
                print(f"   📝 Preview: {response[:100]}...")
                
            else:
                model_results[custom_model] = {
                    "actual_model": actual_model,
                    "error": result["error"],
                    "response_time": result["response_time"],
                    "success": False
                }
                print(f"   ❌ Failed: {result['error']}")
        
        return model_results
    
    async def test_format_compatibility(self) -> Dict[str, Any]:
        """Test different response formats and structures"""
        print("\n📋 Testing Format Compatibility")
        print("=" * 35)
        
        format_tests = [
            ("Simple Text", "Say 'Hello World' in a friendly way.", "text"),
            ("Numbered List", "List 5 programming languages with numbers.", "list"),
            ("Code Block", "Write a Python function to calculate factorial.", "code"),
            ("JSON-like", "Show user data in JSON format with name, age, email.", "json"),
            ("Markdown", "Create a simple markdown document about Docker.", "markdown"),
            ("Technical Analysis", "Compare REST vs GraphQL APIs in a table format.", "structured")
        ]
        
        format_results = {}
        
        for test_name, prompt, expected_format in format_tests:
            print(f"\n📝 {test_name} ({expected_format}):")
            
            result = await self.send_request(prompt, "sonnet")
            
            if result["success"]:
                response = result["response"]
                format_score = self.analyze_format_compatibility(response, expected_format)
                
                format_results[test_name] = {
                    "expected_format": expected_format,
                    "response_time": result["response_time"],
                    "format_score": format_score,
                    "response_preview": response[:200] + "..." if len(response) > 200 else response,
                    "success": True
                }
                
                print(f"   ✅ Success ({result['response_time']:.2f}s)")
                print(f"   📊 Format Score: {format_score:.1f}/10")
                print(f"   📝 Preview: {response[:100]}...")
                
            else:
                format_results[test_name] = {
                    "expected_format": expected_format,
                    "error": result["error"],
                    "success": False
                }
                print(f"   ❌ Failed: {result['error']}")
        
        return format_results
    
    def analyze_response_quality(self, response: str, prompt: str) -> float:
        """Analyze response quality on a scale of 1-10"""
        score = 5.0  # Base score
        
        # Length appropriateness
        if 50 <= len(response) <= 1000:
            score += 1.0
        elif len(response) < 20:
            score -= 2.0
        
        # Contains key terms from prompt
        prompt_words = prompt.lower().split()
        response_lower = response.lower()
        matches = sum(1 for word in prompt_words if word in response_lower)
        score += min(2.0, matches * 0.3)
        
        # Structure indicators
        if any(indicator in response for indicator in ['•', '-', '1.', '2.', '3.']):
            score += 1.0
        
        # Code formatting
        if '```' in response or 'def ' in response or 'function' in response:
            score += 0.5
        
        # Completeness (not truncated)
        if response.endswith(('.', '!', '?', '```')) and not response.endswith('...'):
            score += 1.0
        
        return min(10.0, max(1.0, score))
    
    def analyze_format_compatibility(self, response: str, expected_format: str) -> float:
        """Analyze format compatibility on a scale of 1-10"""
        score = 5.0  # Base score
        
        if expected_format == "text":
            if len(response.split('\n')) <= 3 and not response.startswith(('1.', '-', '•')):
                score += 3.0
        elif expected_format == "list":
            if any(indicator in response for indicator in ['1.', '2.', '3.', '-', '•']):
                score += 4.0
        elif expected_format == "code":
            if '```' in response or 'def ' in response:
                score += 4.0
        elif expected_format == "json":
            if '{' in response and '}' in response:
                score += 3.0
        elif expected_format == "markdown":
            if any(md in response for md in ['#', '**', '*', '```', '-']):
                score += 3.0
        elif expected_format == "structured":
            if '|' in response or response.count('\n') >= 3:
                score += 3.0
        
        return min(10.0, max(1.0, score))
    
    async def test_worker_simulation(self) -> Dict[str, Any]:
        """Simulate different worker type requests"""
        print("\n🔧 Testing Worker Type Scenarios")
        print("=" * 35)
        
        worker_scenarios = [
            ("Analyzer", "Analyze the security implications of using Docker containers.", "security analysis"),
            ("Architect", "Design a scalable microservices architecture for an e-commerce platform.", "architecture design"),  
            ("Backend", "Explain database indexing strategies for high-performance applications.", "backend knowledge"),
            ("Designer", "Describe best practices for responsive web design.", "design principles"),
            ("DevOps", "Outline a CI/CD pipeline for a Node.js application.", "devops process"),
            ("Frontend", "Compare React vs Vue.js for building modern web applications.", "frontend comparison"),
            ("Researcher", "Research current trends in artificial intelligence and machine learning.", "research synthesis"),
            ("Test", "Design a comprehensive testing strategy for a REST API.", "testing methodology")
        ]
        
        worker_results = {}
        
        for worker_type, prompt, expected_content in worker_scenarios:
            print(f"\n📝 {worker_type} Worker:")
            
            result = await self.send_request(prompt, "sonnet")
            
            if result["success"]:
                response = result["response"]
                relevance_score = self.analyze_worker_relevance(response, expected_content)
                
                worker_results[worker_type] = {
                    "prompt": prompt,
                    "expected_content": expected_content,
                    "response_time": result["response_time"],
                    "response_length": result["response_length"],
                    "relevance_score": relevance_score,
                    "response_preview": response[:150] + "..." if len(response) > 150 else response,
                    "success": True
                }
                
                print(f"   ✅ Success ({result['response_time']:.2f}s, {result['response_length']} chars)")
                print(f"   📊 Relevance Score: {relevance_score:.1f}/10")
                
            else:
                worker_results[worker_type] = {
                    "error": result["error"],
                    "success": False
                }
                print(f"   ❌ Failed: {result['error']}")
        
        return worker_results
    
    def analyze_worker_relevance(self, response: str, expected_content: str) -> float:
        """Analyze how well response matches expected worker output"""
        score = 5.0  # Base score
        
        # Check for domain-specific keywords
        content_keywords = {
            "security analysis": ["security", "vulnerability", "threat", "risk", "attack"],
            "architecture design": ["architecture", "scalable", "design", "pattern", "system"],
            "backend knowledge": ["database", "api", "server", "performance", "index"],
            "design principles": ["design", "user", "responsive", "ux", "interface"],
            "devops process": ["ci/cd", "pipeline", "deploy", "automation", "docker"],
            "frontend comparison": ["react", "vue", "component", "state", "frontend"],
            "research synthesis": ["research", "trend", "analysis", "study", "current"],
            "testing methodology": ["test", "testing", "strategy", "api", "automation"]
        }
        
        if expected_content in content_keywords:
            keywords = content_keywords[expected_content]
            response_lower = response.lower()
            matches = sum(1 for keyword in keywords if keyword in response_lower)
            score += min(3.0, matches * 0.6)
        
        # Length and depth
        if len(response) >= 200:
            score += 1.0
        
        # Structure and completeness
        if response.count('.') >= 3:  # Multiple complete sentences
            score += 1.0
        
        return min(10.0, max(1.0, score))
    
    def generate_compatibility_report(self) -> Dict[str, Any]:
        """Generate final compatibility analysis"""
        model_scores = []
        format_scores = []
        worker_scores = []
        
        for model_data in self.results["model_tests"].values():
            if model_data.get("success"):
                model_scores.append(model_data["quality_score"])
        
        for format_data in self.results["format_tests"].values():
            if format_data.get("success"):
                format_scores.append(format_data["format_score"])
        
        for worker_data in self.results["worker_tests"].values():
            if worker_data.get("success"):
                worker_scores.append(worker_data["relevance_score"])
        
        return {
            "overall_quality_score": sum(model_scores) / len(model_scores) if model_scores else 0,
            "format_compatibility_score": sum(format_scores) / len(format_scores) if format_scores else 0,
            "worker_relevance_score": sum(worker_scores) / len(worker_scores) if worker_scores else 0,
            "total_tests_passed": (
                len(model_scores) + len(format_scores) + len(worker_scores)
            ),
            "models_working": len(model_scores),
            "formats_supported": len(format_scores),
            "worker_types_compatible": len(worker_scores)
        }
    
    async def run_full_test_suite(self) -> Dict[str, Any]:
        """Run comprehensive response quality and compatibility tests"""
        print("🧪 Response Quality and Format Compatibility Test Suite")
        print("=" * 60)
        
        # Check service health
        if not await self.check_service_health():
            print("❌ Docker service not healthy - aborting tests")
            return self.results
        
        print(f"✅ Service Status: {self.results['service_health']['status']}")
        
        # Run all test suites
        self.results["model_tests"] = await self.test_model_quality()
        self.results["format_tests"] = await self.test_format_compatibility()
        self.results["worker_tests"] = await self.test_worker_simulation()
        
        # Generate compatibility analysis
        self.results["compatibility_analysis"] = self.generate_compatibility_report()
        
        return self.results
    
    def print_summary(self):
        """Print comprehensive test summary"""
        print("\n" + "=" * 60)
        print("📊 RESPONSE QUALITY AND COMPATIBILITY SUMMARY")
        print("=" * 60)
        
        # Service status
        health = self.results.get("service_health", {})
        print(f"🔧 Service Status: {health.get('status', 'unknown')}")
        
        # Compatibility analysis
        analysis = self.results.get("compatibility_analysis", {})
        if analysis:
            print(f"📈 Overall Quality Score: {analysis.get('overall_quality_score', 0):.1f}/10")
            print(f"📋 Format Compatibility Score: {analysis.get('format_compatibility_score', 0):.1f}/10") 
            print(f"🔧 Worker Relevance Score: {analysis.get('worker_relevance_score', 0):.1f}/10")
            print(f"✅ Total Tests Passed: {analysis.get('total_tests_passed', 0)}")
            print(f"🎯 Models Working: {analysis.get('models_working', 0)}/4")
            print(f"📝 Formats Supported: {analysis.get('formats_supported', 0)}/6") 
            print(f"🔧 Worker Types Compatible: {analysis.get('worker_types_compatible', 0)}/8")
        
        # Quality assessment
        if analysis.get('overall_quality_score', 0) >= 7.0:
            print("\n🎉 EXCELLENT RESPONSE QUALITY")
        elif analysis.get('overall_quality_score', 0) >= 5.0:
            print("\n✅ GOOD RESPONSE QUALITY")
        else:
            print("\n⚠️ RESPONSE QUALITY NEEDS IMPROVEMENT")
        
        print("=" * 60)


async def main():
    """Run response quality and format compatibility tests"""
    tester = ResponseQualityTester()
    
    try:
        await tester.run_full_test_suite()
        tester.print_summary()
        
        # Save detailed results
        with open('response_quality_results.json', 'w') as f:
            json.dump(tester.results, f, indent=2)
        print(f"\n📊 Detailed results saved to response_quality_results.json")
        
    except KeyboardInterrupt:
        print("\n⚠️  Test interrupted by user")
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())