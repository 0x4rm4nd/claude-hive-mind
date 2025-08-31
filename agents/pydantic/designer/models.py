"""
Designer Worker Output Models
============================
Pydantic models for structured designer worker outputs.
"""

from typing import List, Dict, Any, Literal, Optional
from pydantic import BaseModel, Field

from ..shared.models import WorkerOutput


class DesignRecommendation(BaseModel):
    """Individual design recommendation or improvement"""
    category: Literal["visual_design", "user_experience", "accessibility", "interaction_design", "information_architecture"] = Field(description="Design recommendation category")
    recommendation: str = Field(description="Specific design recommendation")
    rationale: str = Field(description="Why this design improvement is important")
    implementation_effort: Literal["low", "medium", "high"] = Field(description="Estimated implementation complexity")
    priority: Literal["critical", "high", "medium", "low"] = Field(description="Implementation priority")
    user_impact: Literal["high", "medium", "low"] = Field(description="Expected user experience impact")
    design_principles: List[str] = Field(default_factory=list, description="Design principles this addresses")


class AccessibilityFinding(BaseModel):
    """Accessibility compliance issue or improvement"""
    wcag_level: Literal["A", "AA", "AAA"] = Field(description="WCAG compliance level")
    guideline: str = Field(description="Specific WCAG guideline reference")
    description: str = Field(description="Accessibility issue description")
    severity: Literal["critical", "high", "medium", "low"] = Field(description="Accessibility issue severity")
    affected_components: List[str] = Field(default_factory=list, description="UI components affected")
    remediation_steps: List[str] = Field(default_factory=list, description="Steps to fix accessibility issue")
    testing_instructions: str = Field(description="How to test the accessibility improvement")


class DesignSystemComponent(BaseModel):
    """Design system component specification"""
    component_name: str = Field(description="Name of the design system component")
    component_type: Literal["atom", "molecule", "organism", "template", "page"] = Field(description="Atomic design hierarchy level")
    description: str = Field(description="Component purpose and usage")
    design_tokens: Dict[str, str] = Field(default_factory=dict, description="Design tokens used (colors, typography, spacing)")
    states: List[str] = Field(default_factory=list, description="Component states (default, hover, active, disabled)")
    variants: List[str] = Field(default_factory=list, description="Component variants or sizes")
    accessibility_features: List[str] = Field(default_factory=list, description="Built-in accessibility features")
    implementation_notes: str = Field(default="", description="Technical implementation guidance")


class DesignerOutput(WorkerOutput):
    """Designer worker structured output - extends base WorkerOutput"""
    
    # Design Analysis
    current_design_assessment: str = Field(description="Assessment of current design state")
    design_maturity_score: float = Field(ge=0.0, le=10.0, default=5.0, description="Overall design system maturity (0-10)")
    
    # Design Recommendations
    design_recommendations: List[DesignRecommendation] = Field(
        default_factory=list,
        description="Specific design improvements and recommendations"
    )
    
    # Accessibility Assessment
    accessibility_findings: List[AccessibilityFinding] = Field(
        default_factory=list,
        description="Accessibility compliance issues and improvements"
    )
    accessibility_score: float = Field(ge=0.0, le=10.0, default=5.0, description="Overall accessibility compliance (0-10)")
    
    # Design System
    design_system_components: List[DesignSystemComponent] = Field(
        default_factory=list,
        description="Design system components and specifications"
    )
    design_system_completeness: float = Field(ge=0.0, le=10.0, default=5.0, description="Design system completeness rating")
    
    # User Experience
    user_experience_issues: List[str] = Field(default_factory=list, description="UX problems identified")
    user_journey_improvements: List[str] = Field(default_factory=list, description="User journey optimization opportunities")
    usability_score: float = Field(ge=0.0, le=10.0, default=5.0, description="Overall usability rating (0-10)")
    
    # Visual Design
    visual_consistency_issues: List[str] = Field(default_factory=list, description="Visual inconsistency problems")
    brand_alignment_assessment: str = Field(default="", description="Brand consistency and alignment evaluation")
    visual_hierarchy_improvements: List[str] = Field(default_factory=list, description="Visual hierarchy enhancement opportunities")
    
    # Design Tokens & Standards
    design_tokens_audit: Dict[str, Any] = Field(default_factory=dict, description="Design tokens consistency analysis")
    typography_recommendations: List[str] = Field(default_factory=list, description="Typography system improvements")
    color_system_recommendations: List[str] = Field(default_factory=list, description="Color system enhancements")
    spacing_system_recommendations: List[str] = Field(default_factory=list, description="Spacing system improvements")
    
    # Responsive Design
    responsive_design_issues: List[str] = Field(default_factory=list, description="Responsive design problems")
    mobile_experience_score: float = Field(ge=0.0, le=10.0, default=5.0, description="Mobile experience quality (0-10)")
    cross_platform_consistency: float = Field(ge=0.0, le=10.0, default=5.0, description="Cross-platform design consistency")
    
    # Overall Quality Assessment
    design_quality_score: float = Field(ge=0.0, le=10.0, default=5.0, description="Overall design quality rating")
    user_satisfaction_estimate: float = Field(ge=0.0, le=10.0, default=5.0, description="Estimated user satisfaction impact")
    design_debt_estimate: str = Field(default="", description="Estimated effort to address design debt")