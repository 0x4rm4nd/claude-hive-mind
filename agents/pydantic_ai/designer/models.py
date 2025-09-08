"""
Designer Worker Output Models
============================
Pydantic models for structured designer worker outputs.
"""

from typing import List, Dict, Any, Literal, Optional
from pydantic import BaseModel, Field

from shared.models import WorkerOutput


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


