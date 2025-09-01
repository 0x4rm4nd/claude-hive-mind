"""
Architect Worker Output Models
==============================
Pydantic models defining structured output formats for system architecture analysis and design recommendations.
"""

from typing import List, Dict, Any, Literal
from pydantic import BaseModel, Field

from shared.models import WorkerOutput


class ArchitecturalRecommendation(BaseModel):
    """Individual architectural recommendation or design decision.
    
    Represents a specific architectural improvement with implementation
    guidance, priority assessment, and risk analysis.
    """
    category: str = Field(description="Architecture domain (e.g., 'microservices', 'data_architecture', 'security')")
    recommendation: str = Field(description="Specific architectural recommendation")
    rationale: str = Field(description="Why this recommendation is important")
    implementation_effort: Literal["low", "medium", "high"] = Field(description="Estimated implementation complexity")
    priority: Literal["critical", "high", "medium", "low"] = Field(description="Implementation priority")
    dependencies: List[str] = Field(default_factory=list, description="Other components this depends on")
    risks: List[str] = Field(default_factory=list, description="Potential risks or trade-offs")


class TechnologyDecision(BaseModel):
    """Technology selection or evaluation decision.
    
    Represents a technology choice with alternatives analysis,
    selection criteria, and implementation complexity assessment.
    """
    decision_type: str = Field(description="Type of technology decision (e.g., 'database', 'framework', 'messaging')")
    recommended_technology: str = Field(description="Recommended technology or approach")
    alternatives_considered: List[str] = Field(default_factory=list, description="Alternative technologies evaluated")
    selection_criteria: List[str] = Field(default_factory=list, description="Key factors in decision making")
    pros: List[str] = Field(default_factory=list, description="Advantages of recommended choice")
    cons: List[str] = Field(default_factory=list, description="Disadvantages or limitations")
    migration_complexity: Literal["trivial", "moderate", "complex", "major"] = Field(description="Complexity of adopting this technology")


class ScalabilityAssessment(BaseModel):
    """Assessment of system scalability characteristics.
    
    Evaluates current and future scaling capabilities with specific
    bottleneck identification and scaling strategy recommendations.
    """
    current_architecture_pattern: str = Field(description="Current architectural pattern in use")
    scalability_bottlenecks: List[str] = Field(default_factory=list, description="Identified scaling limitations")
    horizontal_scaling_readiness: float = Field(ge=0.0, le=10.0, description="Readiness for horizontal scaling (0-10)")
    vertical_scaling_headroom: float = Field(ge=0.0, le=10.0, description="Remaining vertical scaling capacity (0-10)")
    recommended_scaling_approach: str = Field(description="Recommended scaling strategy")
    scaling_milestones: List[str] = Field(default_factory=list, description="Key scaling milestones to plan for")


class ArchitectOutput(WorkerOutput):
    """Comprehensive architectural analysis output with design recommendations and technology guidance.
    
    Extends WorkerOutput with specialized architectural assessment including maturity scoring,
    design patterns, scalability analysis, and modernization roadmap.
    """
    
    # Architecture Analysis
    current_architecture_assessment: str = Field(description="Assessment of current architectural state")
    architectural_maturity_score: float = Field(ge=0.0, le=10.0, default=5.0, description="Overall architecture maturity (0-10)")
    
    # Design Recommendations
    architectural_recommendations: List[ArchitecturalRecommendation] = Field(
        default_factory=list, 
        description="Specific architectural improvements and design decisions"
    )
    
    # Technology Decisions
    technology_decisions: List[TechnologyDecision] = Field(
        default_factory=list,
        description="Technology selection and evaluation recommendations"
    )
    
    # Scalability Analysis
    scalability_assessment: ScalabilityAssessment = Field(
        default_factory=lambda: ScalabilityAssessment(
            current_architecture_pattern="",
            recommended_scaling_approach="",
            horizontal_scaling_readiness=5.0,
            vertical_scaling_headroom=5.0
        ),
        description="Comprehensive scalability analysis"
    )
    
    # Design Patterns & Principles
    design_patterns_applied: List[str] = Field(default_factory=list, description="Design patterns currently in use")
    design_patterns_recommended: List[str] = Field(default_factory=list, description="Additional patterns to consider")
    solid_principles_adherence: Dict[str, float] = Field(
        default_factory=dict, 
        description="SOLID principles compliance scores (0-10 for each principle)"
    )
    
    # Integration & Dependencies
    integration_patterns: List[str] = Field(default_factory=list, description="Current integration approaches")
    dependency_analysis: Dict[str, Any] = Field(default_factory=dict, description="Component dependency mapping and analysis")
    api_design_assessment: str = Field(default="", description="API design quality and recommendations")
    
    # Technical Debt & Evolution
    architectural_debt: List[str] = Field(default_factory=list, description="Technical debt from architectural perspective")
    evolution_roadmap: List[str] = Field(default_factory=list, description="Recommended architectural evolution steps")
    modernization_opportunities: List[str] = Field(default_factory=list, description="Areas for architectural modernization")
    
    # Quality Gates
    architecture_quality_score: float = Field(ge=0.0, le=10.0, default=5.0, description="Overall architectural quality rating")
    maintainability_score: float = Field(ge=0.0, le=10.0, default=5.0, description="System maintainability rating")
    extensibility_score: float = Field(ge=0.0, le=10.0, default=5.0, description="System extensibility rating")
