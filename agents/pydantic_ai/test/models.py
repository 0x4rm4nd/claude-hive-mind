"""
Test Worker Output Models
========================
Pydantic models for structured test worker outputs.
"""

from typing import List, Dict, Any, Literal, Optional
from pydantic import BaseModel, Field

from shared.models import WorkerOutput


class TestImplementation(BaseModel):
    """Individual test implementation or modification"""
    test_type: Literal["unit", "integration", "e2e", "performance", "security", "accessibility"] = Field(description="Type of test")
    test_name: str = Field(description="Name or description of the test")
    target_component: str = Field(description="Component or functionality being tested")
    test_framework: str = Field(description="Testing framework used (Jest, Pytest, Cypress, etc.)")
    test_scope: str = Field(description="Scope and boundaries of the test")
    assertions: List[str] = Field(default_factory=list, description="Key assertions and test conditions")
    test_data_requirements: List[str] = Field(default_factory=list, description="Test data and fixtures needed")
    expected_coverage: float = Field(ge=0.0, le=100.0, description="Expected code coverage percentage")
    implementation_effort: Literal["low", "medium", "high"] = Field(description="Effort required to implement")


class TestStrategy(BaseModel):
    """Testing strategy and approach definition"""
    strategy_name: str = Field(description="Name of the testing strategy")
    testing_levels: List[str] = Field(default_factory=list, description="Testing levels included (unit, integration, e2e)")
    testing_frameworks: List[str] = Field(default_factory=list, description="Testing frameworks and tools used")
    coverage_targets: Dict[str, float] = Field(default_factory=dict, description="Coverage targets by test type")
    automation_level: float = Field(ge=0.0, le=10.0, description="Level of test automation (0-10)")
    ci_integration: str = Field(description="CI/CD pipeline integration approach")
    testing_environments: List[str] = Field(default_factory=list, description="Testing environments and configurations")
    quality_gates: List[str] = Field(default_factory=list, description="Quality gates and blocking conditions")


class QualityGate(BaseModel):
    """Quality gate or testing checkpoint"""
    gate_name: str = Field(description="Name of the quality gate")
    gate_type: Literal["coverage", "performance", "security", "accessibility", "code_quality"] = Field(description="Type of quality gate")
    criteria: List[str] = Field(default_factory=list, description="Specific criteria that must be met")
    threshold_values: Dict[str, float] = Field(default_factory=dict, description="Numerical thresholds for pass/fail")
    blocking_behavior: Literal["blocking", "warning", "informational"] = Field(description="Whether gate blocks deployment")
    automation_status: Literal["automated", "manual", "planned"] = Field(description="Automation level of this gate")
    escalation_procedure: str = Field(default="", description="Procedure when gate fails")


