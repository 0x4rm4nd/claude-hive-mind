"""
Test Worker Output Models
========================
Pydantic models for structured test worker outputs.
"""

from typing import List, Dict, Any, Literal, Optional
from pydantic import BaseModel, Field

from ..shared.models import WorkerOutput


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


class TestOutput(WorkerOutput):
    """Test worker structured output - extends base WorkerOutput"""
    
    # Test Implementations
    test_implementations: List[TestImplementation] = Field(
        default_factory=list,
        description="Tests created, modified, or recommended"
    )
    test_implementation_score: float = Field(ge=0.0, le=10.0, default=5.0, description="Test implementation quality (0-10)")
    
    # Testing Strategy
    testing_strategies: List[TestStrategy] = Field(
        default_factory=list,
        description="Testing strategies and methodologies"
    )
    testing_maturity_score: float = Field(ge=0.0, le=10.0, default=5.0, description="Testing process maturity (0-10)")
    
    # Quality Gates
    quality_gates: List[QualityGate] = Field(
        default_factory=list,
        description="Quality gates and testing checkpoints"
    )
    quality_gate_coverage: float = Field(ge=0.0, le=10.0, default=5.0, description="Quality gate coverage and effectiveness (0-10)")
    
    # Coverage Analysis
    current_coverage_analysis: Dict[str, float] = Field(default_factory=dict, description="Current coverage by test type")
    coverage_gaps: List[str] = Field(default_factory=list, description="Areas with insufficient test coverage")
    coverage_improvement_plan: List[str] = Field(default_factory=list, description="Plan to improve test coverage")
    target_coverage_metrics: Dict[str, float] = Field(default_factory=dict, description="Target coverage metrics by type")
    
    # Test Automation
    automation_implementations: List[str] = Field(default_factory=list, description="Test automation implementations")
    automation_coverage: float = Field(ge=0.0, le=100.0, default=0.0, description="Percentage of tests automated")
    ci_integration_improvements: List[str] = Field(default_factory=list, description="CI/CD testing integration improvements")
    
    # Performance Testing
    performance_test_implementations: List[str] = Field(default_factory=list, description="Performance tests implemented")
    load_testing_strategy: str = Field(default="", description="Load and stress testing approach")
    performance_benchmarks: List[str] = Field(default_factory=list, description="Performance benchmarks and targets")
    
    # Security Testing
    security_test_implementations: List[str] = Field(default_factory=list, description="Security tests implemented")
    vulnerability_testing_approach: str = Field(default="", description="Vulnerability and penetration testing strategy")
    security_automation: List[str] = Field(default_factory=list, description="Automated security testing implementations")
    
    # Accessibility Testing
    accessibility_test_implementations: List[str] = Field(default_factory=list, description="Accessibility tests implemented")
    accessibility_testing_tools: List[str] = Field(default_factory=list, description="Accessibility testing tools and approaches")
    wcag_compliance_testing: str = Field(default="", description="WCAG compliance testing strategy")
    
    # Test Data & Fixtures
    test_data_strategies: List[str] = Field(default_factory=list, description="Test data management strategies")
    fixture_implementations: List[str] = Field(default_factory=list, description="Test fixtures and mock implementations")
    data_seeding_approach: str = Field(default="", description="Test database seeding and cleanup approach")
    
    # Testing Tools & Infrastructure
    testing_tools_recommended: List[str] = Field(default_factory=list, description="Testing tools and frameworks recommended")
    testing_infrastructure: List[str] = Field(default_factory=list, description="Testing infrastructure and environment setup")
    test_reporting_improvements: List[str] = Field(default_factory=list, description="Test reporting and visibility improvements")
    
    # Quality Metrics
    overall_test_quality_score: float = Field(ge=0.0, le=10.0, default=5.0, description="Overall testing quality rating")
    test_reliability_score: float = Field(ge=0.0, le=10.0, default=5.0, description="Test reliability and stability rating")
    test_maintainability_score: float = Field(ge=0.0, le=10.0, default=5.0, description="Test code maintainability rating")
    defect_prevention_score: float = Field(ge=0.0, le=10.0, default=5.0, description="Effectiveness at preventing defects")
    
    # Continuous Improvement
    testing_process_improvements: List[str] = Field(default_factory=list, description="Testing process and methodology improvements")
    knowledge_sharing_initiatives: List[str] = Field(default_factory=list, description="Testing knowledge sharing and training")
    testing_culture_recommendations: List[str] = Field(default_factory=list, description="Recommendations for improving testing culture")