"""
Backend Worker Output Models
============================
Pydantic models defining structured output formats for API development and database design analysis.
"""

from typing import List, Dict, Any, Literal, Optional
from pydantic import BaseModel, Field


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
