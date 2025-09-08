"""
Frontend Worker Output Models
============================
Pydantic models for structured frontend worker outputs.
"""

from typing import List, Dict, Any, Literal, Optional
from pydantic import BaseModel, Field

from shared.models import WorkerOutput


class ComponentImplementation(BaseModel):
    """Frontend component implementation details"""
    component_name: str = Field(description="Name of the component")
    component_type: Literal["page", "layout", "feature", "ui", "utility"] = Field(description="Component category")
    description: str = Field(description="Component purpose and functionality")
    framework_specific: Dict[str, Any] = Field(default_factory=dict, description="Framework-specific implementation details")
    props_interface: Dict[str, str] = Field(default_factory=dict, description="Component props and their types")
    state_dependencies: List[str] = Field(default_factory=list, description="State management dependencies")
    styling_approach: str = Field(description="CSS/styling methodology used")
    accessibility_features: List[str] = Field(default_factory=list, description="Accessibility features implemented")
    testing_strategy: str = Field(description="Component testing approach")


class StateManagementChange(BaseModel):
    """State management implementation or modification"""
    change_type: Literal["store_creation", "reducer_update", "action_creation", "selector_update", "middleware"] = Field(description="Type of state change")
    description: str = Field(description="State management change description")
    affected_components: List[str] = Field(default_factory=list, description="Components affected by this state change")
    state_pattern: str = Field(description="State management pattern used (Redux, Zustand, Context, etc.)")
    implementation_details: str = Field(description="Technical implementation approach")
    performance_impact: Literal["positive", "neutral", "negative"] = Field(description="Expected performance impact")
    testing_requirements: List[str] = Field(default_factory=list, description="Testing needed for state changes")


class UIOptimization(BaseModel):
    """UI performance or user experience optimization"""
    optimization_type: Literal["performance", "bundle_size", "rendering", "loading", "interaction", "accessibility"] = Field(description="Type of optimization")
    description: str = Field(description="Optimization description and benefits")
    implementation_approach: str = Field(description="Technical approach for optimization")
    expected_improvement: str = Field(description="Expected performance or UX improvement")
    measurement_metrics: List[str] = Field(default_factory=list, description="Metrics to measure optimization success")
    implementation_effort: Literal["low", "medium", "high"] = Field(description="Estimated implementation effort")
    user_impact: Literal["high", "medium", "low"] = Field(description="Expected user experience impact")


