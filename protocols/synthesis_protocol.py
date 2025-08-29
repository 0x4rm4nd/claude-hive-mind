#!/usr/bin/env python3
"""
Synthesis Protocol Implementation 
========================================
Handles result synthesis and cross-worker analysis.
"""

import json
from datetime import datetime
from typing import Dict, Any, List, Optional
from .protocol_loader import BaseProtocol, ProtocolConfig

class SynthesisProtocol(BaseProtocol):
    """Manages synthesis of worker results"""
    
    def prepare(self, worker_list: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Prepare for synthesis by setting up tracking structures"""
        preparation = {
            "timestamp": datetime.now().isoformat(),
            "expected_workers": [w["type"] for w in worker_list],
            "received_results": [],
            "synthesis_ready": False,
            "synthesis_strategy": self.determine_strategy(len(worker_list))
        }
        
        self.log_execution("prepare", preparation)
        return preparation
    
    def determine_strategy(self, worker_count: int) -> str:
        """Determine synthesis strategy based on worker count"""
        if worker_count == 1:
            return "single_source"
        elif worker_count == 2:
            return "dual_comparison"
        elif worker_count <= 4:
            return "multi_perspective"
        else:
            return "comprehensive_integration"
    
    def synthesize(self) -> Dict[str, Any]:
        """
        Synthesize all worker results into cohesive insights
        """
        if not self.config.session_id:
            raise ValueError("Session ID required for synthesis")
        
        session_path = f"Docs/hive-mind/sessions/{self.config.session_id}"
        
        # Collect all worker outputs
        worker_outputs = self.collect_worker_outputs(session_path)
        
        # Perform cross-reference analysis
        cross_references = self.analyze_cross_references(worker_outputs)
        
        # Generate priority matrix
        priority_matrix = self.generate_priority_matrix(worker_outputs)
        
        # Create synthesis document
        synthesis = {
            "timestamp": datetime.now().isoformat(),
            "session_id": self.config.session_id,
            "workers_analyzed": list(worker_outputs.keys()),
            "key_findings": self.extract_key_findings(worker_outputs),
            "cross_worker_insights": cross_references,
            "priority_matrix": priority_matrix,
            "consensus_items": self.identify_consensus(worker_outputs),
            "conflicting_items": self.identify_conflicts(worker_outputs),
            "recommendations": self.synthesize_recommendations(worker_outputs),
            "evidence_map": self.create_evidence_map(worker_outputs)
        }
        
        # Write synthesis document
        self.write_synthesis_document(synthesis)
        
        self.log_execution("synthesize", {
            "workers_synthesized": len(worker_outputs),
            "findings_count": len(synthesis["key_findings"]),
            "recommendations_count": len(synthesis["recommendations"])
        })
        
        return synthesis
    
    def collect_worker_outputs(self, session_path: str) -> Dict[str, Any]:
        """Collect all worker JSON responses and notes"""
        outputs = {}
        
        # Pseudo-code for actual file operations
        # json_files = Glob(f"{session_path}/workers/json/*.json")
        # for json_file in json_files:
        #     worker_type = extract_worker_type(json_file)
        #     outputs[worker_type] = {
        #         "json": json.loads(Read(json_file)),
        #         "notes": Read(f"{session_path}/workers/{worker_type}-notes.md")
        #     }
        
        # Placeholder for demonstration
        return {
            "analyzer-worker": {
                "json": {"findings": [], "recommendations": []},
                "notes": "Analysis notes..."
            }
        }
    
    def analyze_cross_references(self, outputs: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify cross-worker patterns and correlations"""
        cross_refs = []
        
        # Compare findings across workers
        all_findings = {}
        for worker, output in outputs.items():
            if "json" in output and "findings" in output["json"]:
                for finding in output["json"]["findings"]:
                    category = finding.get("category", "general")
                    if category not in all_findings:
                        all_findings[category] = []
                    all_findings[category].append({
                        "worker": worker,
                        "finding": finding
                    })
        
        # Identify patterns
        for category, findings in all_findings.items():
            if len(findings) > 1:
                cross_refs.append({
                    "category": category,
                    "workers": [f["worker"] for f in findings],
                    "correlation": "multiple workers identified similar issues",
                    "confidence": len(findings) / len(outputs)
                })
        
        return cross_refs
    
    def generate_priority_matrix(self, outputs: Dict[str, Any]) -> Dict[str, List[Dict]]:
        """Generate prioritized action matrix"""
        matrix = {
            "immediate": [],
            "short_term": [],
            "long_term": [],
            "optional": []
        }
        
        # Aggregate recommendations with priority scoring
        for worker, output in outputs.items():
            if "json" in output and "recommendations" in output["json"]:
                for rec in output["json"]["recommendations"]:
                    priority = rec.get("priority", "long_term")
                    
                    # Enhance with worker context
                    enhanced_rec = {
                        **rec,
                        "source_worker": worker,
                        "confidence": self.calculate_confidence(rec, outputs)
                    }
                    
                    if priority in matrix:
                        matrix[priority].append(enhanced_rec)
        
        # Sort each priority level by confidence
        for priority in matrix:
            matrix[priority].sort(key=lambda x: x.get("confidence", 0), reverse=True)
        
        return matrix
    
    def extract_key_findings(self, outputs: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract and rank key findings from all workers"""
        findings = []
        
        for worker, output in outputs.items():
            if "json" in output and "findings" in output["json"]:
                for finding in output["json"]["findings"]:
                    # Score based on severity and evidence
                    severity_scores = {
                        "critical": 4,
                        "high": 3,
                        "medium": 2,
                        "low": 1
                    }
                    
                    score = severity_scores.get(finding.get("severity", "low"), 1)
                    
                    findings.append({
                        "finding": finding.get("description", ""),
                        "severity": finding.get("severity", "medium"),
                        "category": finding.get("category", "general"),
                        "source": worker,
                        "evidence": finding.get("evidence", ""),
                        "score": score
                    })
        
        # Sort by score and return top findings
        findings.sort(key=lambda x: x["score"], reverse=True)
        return findings[:10]  # Top 10 findings
    
    def identify_consensus(self, outputs: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify items with consensus across workers"""
        consensus_items = []
        
        # Track mentions across workers
        mention_tracker = {}
        
        for worker, output in outputs.items():
            if "json" in output and "findings" in output["json"]:
                for finding in output["json"]["findings"]:
                    key = f"{finding.get('category', '')}:{finding.get('description', '')[:50]}"
                    if key not in mention_tracker:
                        mention_tracker[key] = {
                            "workers": [],
                            "finding": finding
                        }
                    mention_tracker[key]["workers"].append(worker)
        
        # Identify consensus (mentioned by >50% of workers)
        threshold = len(outputs) * 0.5
        for key, data in mention_tracker.items():
            if len(data["workers"]) >= threshold:
                consensus_items.append({
                    "item": data["finding"],
                    "agreement_level": len(data["workers"]) / len(outputs),
                    "workers": data["workers"]
                })
        
        return consensus_items
    
    def identify_conflicts(self, outputs: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify conflicting recommendations or findings"""
        conflicts = []
        
        # Compare recommendations for conflicts
        all_recommendations = []
        for worker, output in outputs.items():
            if "json" in output and "recommendations" in output["json"]:
                for rec in output["json"]["recommendations"]:
                    all_recommendations.append({
                        "worker": worker,
                        "action": rec.get("action", ""),
                        "category": rec.get("category", "general")
                    })
        
        # Simple conflict detection (would be more sophisticated in practice)
        for i, rec1 in enumerate(all_recommendations):
            for rec2 in all_recommendations[i+1:]:
                if rec1["category"] == rec2["category"] and \
                   self.are_conflicting(rec1["action"], rec2["action"]):
                    conflicts.append({
                        "category": rec1["category"],
                        "worker1": rec1["worker"],
                        "action1": rec1["action"],
                        "worker2": rec2["worker"],
                        "action2": rec2["action"],
                        "resolution_needed": True
                    })
        
        return conflicts
    
    def are_conflicting(self, action1: str, action2: str) -> bool:
        """Determine if two actions are conflicting"""
        # Simple keyword-based conflict detection
        opposing_pairs = [
            ("increase", "decrease"),
            ("add", "remove"),
            ("enable", "disable"),
            ("expand", "reduce")
        ]
        
        action1_lower = action1.lower()
        action2_lower = action2.lower()
        
        for pair in opposing_pairs:
            if (pair[0] in action1_lower and pair[1] in action2_lower) or \
               (pair[1] in action1_lower and pair[0] in action2_lower):
                return True
        
        return False
    
    def synthesize_recommendations(self, outputs: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Synthesize and deduplicate recommendations"""
        recommendations = []
        seen_actions = set()
        
        # Collect all recommendations
        for worker, output in outputs.items():
            if "json" in output and "recommendations" in output["json"]:
                for rec in output["json"]["recommendations"]:
                    action_key = rec.get("action", "")[:100]
                    
                    if action_key not in seen_actions:
                        seen_actions.add(action_key)
                        recommendations.append({
                            **rec,
                            "sources": [worker],
                            "consensus_score": 1
                        })
                    else:
                        # Find and update existing recommendation
                        for existing in recommendations:
                            if existing.get("action", "")[:100] == action_key:
                                existing["sources"].append(worker)
                                existing["consensus_score"] += 1
                                break
        
        # Sort by consensus score and priority
        recommendations.sort(
            key=lambda x: (x["consensus_score"], x.get("priority", "low")),
            reverse=True
        )
        
        return recommendations
    
    def create_evidence_map(self, outputs: Dict[str, Any]) -> Dict[str, List[str]]:
        """Create map of evidence references"""
        evidence_map = {}
        
        for worker, output in outputs.items():
            evidence_map[worker] = []
            
            # Add JSON response reference
            evidence_map[worker].append(f"workers/json/{worker}-response.json")
            
            # Add notes reference
            evidence_map[worker].append(f"workers/{worker}-notes.md")
            
            # Add any additional evidence files mentioned
            if "json" in output and "evidence_files" in output["json"]:
                evidence_map[worker].extend(output["json"]["evidence_files"])
        
        return evidence_map
    
    def calculate_confidence(self, item: Dict, all_outputs: Dict) -> float:
        """Calculate confidence score for an item"""
        confidence = 0.5  # Base confidence
        
        # Increase confidence if multiple workers agree
        similar_count = 0
        for output in all_outputs.values():
            if self.contains_similar(item, output):
                similar_count += 1
        
        if similar_count > 1:
            confidence += (similar_count - 1) * 0.1
        
        # Adjust based on severity/priority
        if item.get("severity") == "critical" or item.get("priority") == "immediate":
            confidence += 0.2
        
        return min(confidence, 1.0)  # Cap at 1.0
    
    def contains_similar(self, item: Dict, output: Dict) -> bool:
        """Check if output contains similar item"""
        if "json" not in output:
            return False
        
        # Check in findings
        if "findings" in output["json"]:
            for finding in output["json"]["findings"]:
                if finding.get("category") == item.get("category"):
                    return True
        
        # Check in recommendations
        if "recommendations" in output["json"]:
            for rec in output["json"]["recommendations"]:
                if rec.get("action", "")[:50] == item.get("action", "")[:50]:
                    return True
        
        return False
    
    def write_synthesis_document(self, synthesis: Dict[str, Any]) -> None:
        """Write comprehensive synthesis document"""
        session_path = f"Docs/hive-mind/sessions/{self.config.session_id}"
        
        # Create markdown document
        doc = f"""# Research Synthesis
        
## Session: {synthesis['session_id']}
**Generated**: {synthesis['timestamp']}
**Workers Analyzed**: {', '.join(synthesis['workers_analyzed'])}

## Key Findings

"""
        
        for finding in synthesis["key_findings"]:
            doc += f"- **[{finding['severity'].upper()}]** {finding['finding']} (Source: {finding['source']})\n"
        
        doc += "\n## Cross-Worker Insights\n\n"
        for insight in synthesis["cross_worker_insights"]:
            doc += f"- {insight['correlation']} (Confidence: {insight['confidence']:.1%})\n"
        
        doc += "\n## Priority Matrix\n\n"
        for priority, items in synthesis["priority_matrix"].items():
            doc += f"### {priority.replace('_', ' ').title()}\n"
            for item in items[:5]:  # Top 5 per category
                doc += f"- {item.get('action', 'Action')} (Confidence: {item.get('confidence', 0):.1%})\n"
            doc += "\n"
        
        doc += "\n## Evidence References\n\n"
        for worker, refs in synthesis["evidence_map"].items():
            doc += f"- **{worker}**: {', '.join(refs)}\n"
        
        # Write(f"{session_path}/RESEARCH_SYNTHESIS.md", doc)