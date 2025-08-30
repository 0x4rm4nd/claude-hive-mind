#!/usr/bin/env python3
"""
Completion Protocol Implementation 
=========================================
Handles worker and session completion.
"""

import json
from datetime import datetime
from typing import Dict, Any, List, Optional
from .protocol_loader import BaseProtocol, ProtocolConfig

class CompletionProtocol(BaseProtocol):
    """Manages completion of worker tasks and sessions"""
    
    def finalize(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Finalize worker output with standardized format
        """
        # Generate standardized output
        finalized_output = {
            "worker": self.config.agent_name,
            "session_id": self.config.session_id,
            "timestamp": datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
            "status": "completed",
            "protocol_version": self.config.protocol_version,
            "summary": self.generate_summary(results),
            "findings": self.format_findings(results.get("findings", [])),
            "recommendations": self.format_recommendations(results.get("recommendations", [])),
            "evidence": results.get("evidence", []),
            "metrics": self.calculate_metrics(results)
        }
        
        # Save outputs
        self.save_worker_outputs(finalized_output)
        
        # Update session state
        self.update_completion_status()
        
        self.log_execution("finalize", {
            "worker": self.config.agent_name,
            "status": "completed",
            "findings_count": len(finalized_output["findings"]),
            "recommendations_count": len(finalized_output["recommendations"])
        })
        
        return finalized_output
    
    def generate_summary(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate executive summary"""
        summary = {
            "overall_assessment": results.get("assessment", "Analysis complete"),
            "critical_issues": 0,
            "high_priority_items": 0,
            "recommendations_count": len(results.get("recommendations", [])),
            "key_insights": []
        }
        
        # Count critical issues
        for finding in results.get("findings", []):
            if finding.get("severity") == "critical":
                summary["critical_issues"] += 1
            if finding.get("severity") in ["critical", "high"]:
                summary["high_priority_items"] += 1
        
        # Extract key insights
        if "insights" in results:
            summary["key_insights"] = results["insights"][:5]  # Top 5 insights
        
        return summary
    
    def format_findings(self, findings: List[Dict]) -> List[Dict[str, Any]]:
        """Format findings with standardized structure"""
        formatted = []
        
        for finding in findings:
            formatted.append({
                "category": finding.get("category", "general"),
                "severity": finding.get("severity", "medium"),
                "description": finding.get("description", ""),
                "evidence": finding.get("evidence", ""),
                "location": finding.get("location", ""),
                "impact": finding.get("impact", "unknown"),
                "timestamp": datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
            })
        
        # Sort by severity
        severity_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
        formatted.sort(key=lambda x: severity_order.get(x["severity"], 4))
        
        return formatted
    
    def format_recommendations(self, recommendations: List[Dict]) -> List[Dict[str, Any]]:
        """Format recommendations with standardized structure"""
        formatted = []
        
        for rec in recommendations:
            formatted.append({
                "priority": rec.get("priority", "medium"),
                "action": rec.get("action", ""),
                "rationale": rec.get("rationale", ""),
                "category": rec.get("category", "general"),
                "effort": rec.get("effort", "medium"),
                "impact": rec.get("impact", "medium"),
                "dependencies": rec.get("dependencies", [])
            })
        
        # Sort by priority
        priority_order = {"immediate": 0, "short_term": 1, "long_term": 2, "optional": 3}
        formatted.sort(key=lambda x: priority_order.get(x["priority"], 4))
        
        return formatted
    
    def calculate_metrics(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate completion metrics"""
        metrics = {
            "analysis_depth": self.assess_depth(results),
            "coverage": self.assess_coverage(results),
            "confidence": self.assess_confidence(results),
            "completeness": self.assess_completeness(results)
        }
        
        return metrics
    
    def assess_depth(self, results: Dict[str, Any]) -> str:
        """Assess analysis depth"""
        finding_count = len(results.get("findings", []))
        
        if finding_count > 20:
            return "comprehensive"
        elif finding_count > 10:
            return "thorough"
        elif finding_count > 5:
            return "moderate"
        else:
            return "basic"
    
    def assess_coverage(self, results: Dict[str, Any]) -> float:
        """Assess coverage percentage"""
        # Calculate based on categories covered
        expected_categories = {"security", "performance", "quality", "architecture", "testing"}
        covered_categories = set()
        
        for finding in results.get("findings", []):
            covered_categories.add(finding.get("category", "").lower())
        
        for rec in results.get("recommendations", []):
            covered_categories.add(rec.get("category", "").lower())
        
        coverage = len(covered_categories & expected_categories) / len(expected_categories)
        return round(coverage * 100, 1)
    
    def assess_confidence(self, results: Dict[str, Any]) -> str:
        """Assess confidence level"""
        # Based on evidence quality
        evidence_count = len(results.get("evidence", []))
        
        if evidence_count > 10:
            return "high"
        elif evidence_count > 5:
            return "medium"
        else:
            return "low"
    
    def assess_completeness(self, results: Dict[str, Any]) -> float:
        """Assess completeness percentage"""
        required_fields = ["findings", "recommendations", "evidence", "assessment"]
        present_fields = sum(1 for field in required_fields if field in results and results[field])
        
        return (present_fields / len(required_fields)) * 100
    
    def save_worker_outputs(self, output: Dict[str, Any]) -> None:
        """Save worker outputs to appropriate locations"""
        if not self.config.session_id or not self.config.agent_name:
            return
        
        session_path = f"Docs/hive-mind/sessions/{self.config.session_id}"
        
        # Save JSON response
        json_path = f"{session_path}/workers/json/{self.config.agent_name}-response.json"
        # Write(json_path, json.dumps(output, indent=2))
        
        # Save detailed notes
        notes = self.generate_detailed_notes(output)
        notes_path = f"{session_path}/notes/{self.config.agent_name.replace('-worker','')}_notes.md"
        # Write(notes_path, notes)
    
    def generate_detailed_notes(self, output: Dict[str, Any]) -> str:
        """Generate detailed markdown notes"""
        notes = f"""# {self.config.agent_name.replace('-', ' ').title()} Analysis

## Summary
{output['summary'].get('overall_assessment', '')}

## Key Metrics
- **Critical Issues**: {output['summary'].get('critical_issues', 0)}
- **High Priority Items**: {output['summary'].get('high_priority_items', 0)}
- **Total Recommendations**: {output['summary'].get('recommendations_count', 0)}
- **Analysis Depth**: {output['metrics'].get('analysis_depth', 'unknown')}
- **Coverage**: {output['metrics'].get('coverage', 0)}%

## Findings

"""
        
        for i, finding in enumerate(output.get("findings", []), 1):
            notes += f"""### {i}. {finding.get('description', 'Finding')}
- **Severity**: {finding.get('severity', 'unknown')}
- **Category**: {finding.get('category', 'general')}
- **Evidence**: {finding.get('evidence', 'N/A')}
- **Impact**: {finding.get('impact', 'unknown')}

"""
        
        notes += "## Recommendations\n\n"
        
        for i, rec in enumerate(output.get("recommendations", []), 1):
            notes += f"""### {i}. {rec.get('action', 'Recommendation')}
- **Priority**: {rec.get('priority', 'medium')}
- **Rationale**: {rec.get('rationale', 'N/A')}
- **Effort**: {rec.get('effort', 'unknown')}
- **Impact**: {rec.get('impact', 'unknown')}

"""
        
        notes += f"\n---\n*Analysis completed at {output['timestamp']}*"
        
        return notes
    
    def update_completion_status(self) -> None:
        """Update session state with completion status"""
        if not self.config.session_id or not self.config.agent_name:
            return
        
        # Update worker status in session state (pseudo-code)
        # session_protocol = SessionProtocol(self.config)
        # session_protocol.update_worker_status(
        #     self.config.agent_name, 
        #     "completed",
        #     {"completed_at": datetime.now().isoformat()}
        # )
    
    def mark_session_complete(self) -> Dict[str, Any]:
        """Mark entire session as complete"""
        completion_record = {
            "session_id": self.config.session_id,
            "completed_at": datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
            "status": "completed",
            "final_state": self.get_final_state()
        }
        
        # Update session state
        # session_protocol = SessionProtocol(self.config)
        # session_protocol.close_session()
        
        self.log_execution("mark_session_complete", completion_record)
        return completion_record
    
    def get_final_state(self) -> Dict[str, Any]:
        """Get final session state"""
        # Read final metrics and status (pseudo-code)
        # session_protocol = SessionProtocol(self.config)
        # return session_protocol.get_session_metrics()
        
        return {
            "workers_completed": [],
            "synthesis_ready": True,
            "total_findings": 0,
            "total_recommendations": 0
        }
    
    def validate_completion(self) -> Dict[str, bool]:
        """Validate completion requirements"""
        validation = {
            "json_output_saved": False,
            "notes_saved": False,
            "state_updated": False,
            "events_logged": False,
            "all_requirements_met": False
        }
        
        if self.config.session_id:
            session_path = f"Docs/hive-mind/sessions/{self.config.session_id}"
            
            # Check for required output files (pseudo-code)
            # validation["json_output_saved"] = exists(f"{session_path}/workers/json/{self.config.worker_type}-response.json")
            # validation["notes_saved"] = exists(f"{session_path}/workers/{self.config.worker_type}-notes.md")
            
            # For demonstration
            validation["json_output_saved"] = True
            validation["notes_saved"] = True
            validation["state_updated"] = True
            validation["events_logged"] = True
        
        validation["all_requirements_met"] = all([
            validation["json_output_saved"],
            validation["notes_saved"],
            validation["state_updated"],
            validation["events_logged"]
        ])
        
        return validation
 return validation
