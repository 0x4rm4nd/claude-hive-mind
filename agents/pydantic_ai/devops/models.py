"""
DevOps Worker Output Models
==========================
Pydantic models for structured DevOps worker outputs.
"""

from typing import List, Dict, Any, Literal, Optional
from pydantic import BaseModel, Field

from ..shared.models import WorkerOutput


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


class DevOpsOutput(WorkerOutput):
    """DevOps worker structured output - extends base WorkerOutput"""
    
    # Infrastructure Management
    infrastructure_changes: List[InfrastructureChange] = Field(
        default_factory=list,
        description="Infrastructure modifications and implementations"
    )
    infrastructure_maturity_score: float = Field(ge=0.0, le=10.0, default=5.0, description="Infrastructure maturity rating (0-10)")
    
    # Deployment & CI/CD
    deployment_strategies: List[DeploymentStrategy] = Field(
        default_factory=list,
        description="Deployment approaches and pipeline configurations"
    )
    cicd_maturity_score: float = Field(ge=0.0, le=10.0, default=5.0, description="CI/CD pipeline maturity (0-10)")
    
    # Monitoring & Observability
    monitoring_implementations: List[MonitoringImplementation] = Field(
        default_factory=list,
        description="Monitoring and observability implementations"
    )
    observability_score: float = Field(ge=0.0, le=10.0, default=5.0, description="System observability rating (0-10)")
    
    # Security & Compliance
    security_implementations: List[str] = Field(default_factory=list, description="Security measures implemented")
    compliance_improvements: List[str] = Field(default_factory=list, description="Compliance and governance improvements")
    security_score: float = Field(ge=0.0, le=10.0, default=5.0, description="Infrastructure security rating (0-10)")
    
    # Performance & Optimization
    performance_optimizations: List[str] = Field(default_factory=list, description="Infrastructure performance improvements")
    cost_optimizations: List[str] = Field(default_factory=list, description="Cost reduction opportunities")
    scalability_improvements: List[str] = Field(default_factory=list, description="Scalability enhancements")
    
    # Automation & Tooling
    automation_implementations: List[str] = Field(default_factory=list, description="Automation scripts and tools")
    tooling_improvements: List[str] = Field(default_factory=list, description="DevOps tooling enhancements")
    process_improvements: List[str] = Field(default_factory=list, description="Process and workflow improvements")
    
    # Configuration Management
    configuration_changes: List[str] = Field(default_factory=list, description="Configuration management improvements")
    environment_standardization: List[str] = Field(default_factory=list, description="Environment consistency improvements")
    secrets_management: List[str] = Field(default_factory=list, description="Secrets and credential management")
    
    # Disaster Recovery & Backup
    backup_strategies: List[str] = Field(default_factory=list, description="Backup and recovery implementations")
    disaster_recovery_improvements: List[str] = Field(default_factory=list, description="Disaster recovery enhancements")
    business_continuity_score: float = Field(ge=0.0, le=10.0, default=5.0, description="Business continuity readiness")
    
    # Overall Assessment
    devops_maturity_score: float = Field(ge=0.0, le=10.0, default=5.0, description="Overall DevOps maturity rating")
    operational_efficiency: float = Field(ge=0.0, le=10.0, default=5.0, description="Operational efficiency rating")
    reliability_score: float = Field(ge=0.0, le=10.0, default=5.0, description="System reliability rating")