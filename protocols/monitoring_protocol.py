#!/usr/bin/env python3
"""
Monitoring Protocol Implementation 
=========================================
Handles continuous monitoring and health checks.
"""

import json
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from .protocol_loader import BaseProtocol, ProtocolConfig

class MonitoringProtocol(BaseProtocol):
    """Manages worker monitoring and health checks"""
    
    def __init__(self, config: ProtocolConfig):
        super().__init__(config)
        self.monitoring_state = {
            "start_time": None,
            "last_heartbeat": None,
            "checkpoints": [],
            "health_status": "unknown",
            "stall_detected": False
        }
    
    def start_monitoring(self) -> Dict[str, Any]:
        """Initialize monitoring for a worker"""
        self.monitoring_state["start_time"] = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
        self.monitoring_state["health_status"] = "healthy"
        self.monitoring_state["last_heartbeat"] = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
        
        self.log_execution("start_monitoring", self.monitoring_state)
        return self.monitoring_state
    
    def heartbeat(self, status: Optional[str] = None, metadata: Optional[Dict] = None) -> Dict[str, Any]:
        """Record heartbeat from worker"""
        now = datetime.utcnow()
        self.monitoring_state["last_heartbeat"] = now.strftime('%Y-%m-%dT%H:%M:%SZ')
        
        if status:
            self.monitoring_state["health_status"] = status
        
        heartbeat_data = {
            "timestamp": now.isoformat(),
            "worker": self.config.agent_name,
            "status": self.monitoring_state["health_status"],
            "metadata": metadata or {}
        }
        
        # Check for stalls
        if self.monitoring_state["start_time"]:
            # Support Z or ISO with offset
            try:
                if isinstance(self.monitoring_state["start_time"], str) and self.monitoring_state["start_time"].endswith('Z'):
                    start = datetime.strptime(self.monitoring_state["start_time"], '%Y-%m-%dT%H:%M:%SZ')
                else:
                    start = datetime.fromisoformat(self.monitoring_state["start_time"]) 
            except Exception:
                start = now
            duration = (now - start).total_seconds()
            
            # Stall detection based on timeout
            if self.config.timeout is not None and duration > self.config.timeout:
                self.monitoring_state["stall_detected"] = True
                heartbeat_data["alert"] = "stall_detected"
        
        self.log_execution("heartbeat", heartbeat_data)
        return heartbeat_data
    
    def check_health(self) -> Dict[str, Any]:
        """Check worker health status"""
        health_report = {
            "timestamp": datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
            "worker": self.config.agent_name,
            "health_status": self.monitoring_state["health_status"],
            "stall_detected": self.monitoring_state["stall_detected"],
            "last_heartbeat": self.monitoring_state["last_heartbeat"],
            "metrics": self.calculate_health_metrics()
        }
        
        # Determine overall health
        if self.monitoring_state["stall_detected"]:
            health_report["health_status"] = "stalled"
        elif not self.monitoring_state["last_heartbeat"]:
            health_report["health_status"] = "unknown"
        else:
            try:
                if isinstance(self.monitoring_state["last_heartbeat"], str) and self.monitoring_state["last_heartbeat"].endswith('Z'):
                    last_heartbeat = datetime.strptime(self.monitoring_state["last_heartbeat"], '%Y-%m-%dT%H:%M:%SZ')
                else:
                    last_heartbeat = datetime.fromisoformat(self.monitoring_state["last_heartbeat"]) 
            except Exception:
                last_heartbeat = datetime.utcnow()
            time_since_heartbeat = (datetime.utcnow() - last_heartbeat).total_seconds()
            
            if time_since_heartbeat > 120:  # 2 minutes without heartbeat
                health_report["health_status"] = "unresponsive"
            elif time_since_heartbeat > 60:  # 1 minute without heartbeat
                health_report["health_status"] = "warning"
            else:
                health_report["health_status"] = "healthy"
        
        self.log_execution("check_health", health_report)
        return health_report
    
    def add_checkpoint(self, checkpoint_name: str, metadata: Optional[Dict] = None) -> Dict[str, Any]:
        """Add monitoring checkpoint"""
        checkpoint = {
            "name": checkpoint_name,
            "timestamp": datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
            "metadata": metadata or {}
        }
        
        self.monitoring_state["checkpoints"].append(checkpoint)
        
        self.log_execution("add_checkpoint", checkpoint)
        return checkpoint
    
    def calculate_health_metrics(self) -> Dict[str, Any]:
        """Calculate health metrics"""
        metrics = {
            "uptime_seconds": 0,
            "checkpoint_count": len(self.monitoring_state["checkpoints"]),
            "time_since_last_heartbeat": None
        }
        
        if self.monitoring_state["start_time"]:
            try:
                if isinstance(self.monitoring_state["start_time"], str) and self.monitoring_state["start_time"].endswith('Z'):
                    start = datetime.strptime(self.monitoring_state["start_time"], '%Y-%m-%dT%H:%M:%SZ')
                else:
                    start = datetime.fromisoformat(self.monitoring_state["start_time"]) 
            except Exception:
                start = datetime.utcnow()
            metrics["uptime_seconds"] = (datetime.utcnow() - start).total_seconds()
        
        if self.monitoring_state["last_heartbeat"]:
            try:
                if isinstance(self.monitoring_state["last_heartbeat"], str) and self.monitoring_state["last_heartbeat"].endswith('Z'):
                    last = datetime.strptime(self.monitoring_state["last_heartbeat"], '%Y-%m-%dT%H:%M:%SZ')
                else:
                    last = datetime.fromisoformat(self.monitoring_state["last_heartbeat"]) 
            except Exception:
                last = datetime.utcnow()
            metrics["time_since_last_heartbeat"] = (datetime.utcnow() - last).total_seconds()
        
        return metrics
    
    def monitor_progress(self) -> Dict[str, Any]:
        """Monitor task progress"""
        # Read todo items to assess progress (pseudo-code)
        # todos = TodoRead()
        
        progress = {
            "timestamp": datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
            "worker": self.config.agent_name,
            "checkpoints_completed": len(self.monitoring_state["checkpoints"]),
            "estimated_completion": self.estimate_completion(),
            "is_blocked": self.monitoring_state["stall_detected"]
        }
        
        self.log_execution("monitor_progress", progress)
        return progress
    
    def estimate_completion(self) -> Optional[float]:
        """Estimate completion percentage"""
        if not self.monitoring_state["checkpoints"]:
            return 0.0
        
        # Simple estimation based on checkpoints
        # Would be more sophisticated in practice
        expected_checkpoints = 10  # Expected number of checkpoints
        completed = len(self.monitoring_state["checkpoints"])
        
        return min((completed / expected_checkpoints) * 100, 100.0)
