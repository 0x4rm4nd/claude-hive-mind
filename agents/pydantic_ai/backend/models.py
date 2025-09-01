"""
Backend Worker Output Models
============================
Pydantic models defining structured output formats for API development and database design analysis.
"""

from typing import List, Dict, Any, Literal, Optional
from pydantic import BaseModel, Field

from shared.models import WorkerOutput


class APIEndpoint(BaseModel):
    """API endpoint specification and implementation details.
    
    Represents a complete API endpoint definition with authentication,
    authorization, schema validation, and implementation requirements.
    """

    method: Literal["GET", "POST", "PUT", "DELETE", "PATCH"] = Field(
        description="HTTP method"
    )
    path: str = Field(description="Endpoint path (e.g., '/api/v1/users/{id}')")
    description: str = Field(description="Endpoint purpose and functionality")
    request_schema: Optional[Dict[str, Any]] = Field(
        default=None, description="Request body schema"
    )
    response_schema: Dict[str, Any] = Field(description="Response body schema")
    authentication_required: bool = Field(
        default=True, description="Whether endpoint requires authentication"
    )
    authorization_roles: List[str] = Field(
        default_factory=list, description="Required roles for access"
    )
    implementation_status: Literal["new", "modified", "existing"] = Field(
        description="Implementation state"
    )
    testing_requirements: List[str] = Field(
        default_factory=list, description="Specific testing needs for this endpoint"
    )


class DatabaseChange(BaseModel):
    """Database schema or query modifications.
    
    Represents a specific database change with impact assessment,
    affected tables, and implementation guidance.
    """

    change_type: Literal["migration", "index", "constraint", "optimization"] = Field(
        description="Type of database change"
    )
    description: str = Field(description="Detailed description of the change")
    affected_tables: List[str] = Field(
        default_factory=list, description="Database tables affected"
    )
    sql_preview: str = Field(default="", description="SQL preview or migration snippet")
    risk_level: Literal["low", "medium", "high", "critical"] = Field(
        description="Risk level of implementing this change"
    )
    rollback_strategy: str = Field(description="How to rollback this change if needed")
    performance_impact: str = Field(description="Expected performance impact")
    dependencies: List[str] = Field(
        default_factory=list, description="Other changes this depends on"
    )


class ServiceImplementation(BaseModel):
    """Service layer implementation or modification"""

    service_name: str = Field(description="Name of the service being implemented")
    service_type: Literal["business_logic", "data_access", "integration", "utility"] = (
        Field(description="Service category")
    )
    description: str = Field(description="Service purpose and functionality")
    implementation_approach: str = Field(
        description="Technical approach and patterns used"
    )
    dependencies: List[str] = Field(
        default_factory=list, description="Services or components this depends on"
    )
    interfaces: List[str] = Field(
        default_factory=list, description="Interfaces this service exposes"
    )
    testing_strategy: str = Field(description="Unit and integration testing approach")
    error_handling: str = Field(description="Error handling and resilience patterns")


class BackendOutput(WorkerOutput):
    """Backend worker structured output - extends base WorkerOutput"""

    # API Development
    api_endpoints: List[APIEndpoint] = Field(
        default_factory=list, description="API endpoints created or modified"
    )
    api_design_score: float = Field(
        ge=0.0, le=10.0, default=5.0, description="API design quality rating (0-10)"
    )

    # Database Design
    database_changes: List[DatabaseChange] = Field(
        default_factory=list, description="Database schema and optimization changes"
    )
    database_design_score: float = Field(
        ge=0.0,
        le=10.0,
        default=5.0,
        description="Database design quality rating (0-10)",
    )

    # Service Implementation
    service_implementations: List[ServiceImplementation] = Field(
        default_factory=list,
        description="Service layer implementations and modifications",
    )
    service_architecture_score: float = Field(
        ge=0.0, le=10.0, default=5.0, description="Service architecture quality (0-10)"
    )

    # Authentication & Security
    authentication_changes: List[str] = Field(
        default_factory=list,
        description="Authentication and authorization modifications",
    )
    security_implementations: List[str] = Field(
        default_factory=list, description="Security measures implemented"
    )

    # Performance & Optimization
    performance_optimizations: List[str] = Field(
        default_factory=list, description="Performance improvements implemented"
    )
    caching_strategy: str = Field(
        default="", description="Caching approach and implementation"
    )
    query_optimizations: List[str] = Field(
        default_factory=list, description="Database query optimizations"
    )

    # Integration & Communication
    integration_patterns: List[str] = Field(
        default_factory=list, description="Integration patterns implemented"
    )
    message_queue_usage: List[str] = Field(
        default_factory=list, description="Message queue implementations"
    )
    external_api_integrations: List[str] = Field(
        default_factory=list, description="Third-party API integrations"
    )

    # Testing & Quality Assurance
    test_implementations: List[str] = Field(
        default_factory=list, description="Tests created or modified"
    )
    test_coverage_estimate: float = Field(
        ge=0.0, le=100.0, default=0.0, description="Estimated test coverage percentage"
    )
    error_handling_improvements: List[str] = Field(
        default_factory=list, description="Error handling enhancements"
    )

    # Deployment & Operations
    deployment_considerations: List[str] = Field(
        default_factory=list, description="Deployment and operational considerations"
    )
    monitoring_implementations: List[str] = Field(
        default_factory=list, description="Monitoring and logging implementations"
    )
    configuration_changes: List[str] = Field(
        default_factory=list, description="Configuration and environment changes"
    )

    # Overall Assessment
    backend_quality_score: float = Field(
        ge=0.0,
        le=10.0,
        default=5.0,
        description="Overall backend implementation quality",
    )
    scalability_readiness: float = Field(
        ge=0.0, le=10.0, default=5.0, description="Backend scalability readiness rating"
    )
    maintenance_complexity: Literal["low", "medium", "high"] = Field(
        default="medium", description="Ongoing maintenance complexity"
    )
