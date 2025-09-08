"""
DevOps Worker Output Models
==========================
Pydantic models for structured DevOps worker outputs.
"""

from typing import List, Dict, Any, Literal, Optional
from pydantic import BaseModel, Field

from shared.models import WorkerOutput


class InfrastructureChange(BaseModel):
    """Infrastructure modification or implementation"""
    change_type: Literal["container", "networking", "storage", "compute", "security", "monitoring"] = Field(description="Type of infrastructure change")
    description: str = Field(description="Detailed description of infrastructure change")
    implementation_approach: str = Field(description="Technical approach and tools used")
    configuration_files: List[str] = Field(default_factory=list, description="Configuration files affected or created")
    deployment_impact: Literal["none", "low", "medium", "high"] = Field(description="Impact on running services")
    rollback_strategy: str = Field(description="How to rollback this change if needed")
    cost_impact: Literal["decrease", "neutral", "increase_low", "increase_medium", "increase_high"] = Field(description="Expected cost impact")
    security_implications: List[str] = Field(default_factory=list, description="Security considerations for this change")


class DeploymentStrategy(BaseModel):
    """Deployment approach and pipeline configuration"""
    strategy_name: str = Field(description="Name of deployment strategy")
    deployment_type: Literal["blue_green", "rolling", "canary", "recreate", "a_b_testing"] = Field(description="Deployment pattern")
    description: str = Field(description="Deployment strategy description and benefits")
    pipeline_stages: List[str] = Field(default_factory=list, description="CI/CD pipeline stages")
    automation_level: float = Field(ge=0.0, le=10.0, description="Level of deployment automation (0-10)")
    rollback_time: str = Field(description="Expected rollback time if needed")
    risk_mitigation: List[str] = Field(default_factory=list, description="Risk mitigation strategies")
    monitoring_requirements: List[str] = Field(default_factory=list, description="Required monitoring during deployment")


class MonitoringImplementation(BaseModel):
    """Monitoring and observability implementation"""
    monitoring_type: Literal["metrics", "logging", "tracing", "alerting", "health_checks"] = Field(description="Type of monitoring")
    description: str = Field(description="Monitoring implementation description")
    tools_used: List[str] = Field(default_factory=list, description="Monitoring tools and platforms")
    metrics_collected: List[str] = Field(default_factory=list, description="Specific metrics being monitored")
    alert_conditions: List[str] = Field(default_factory=list, description="Conditions that trigger alerts")
    dashboard_components: List[str] = Field(default_factory=list, description="Dashboard visualizations and components")
    retention_policy: str = Field(default="", description="Data retention and archival policy")
    integration_points: List[str] = Field(default_factory=list, description="Integration with other monitoring systems")


