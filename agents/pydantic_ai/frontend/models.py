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


class FrontendOutput(WorkerOutput):
    """Frontend worker structured output - extends base WorkerOutput"""
    
    # Component Implementation
    component_implementations: List[ComponentImplementation] = Field(
        default_factory=list,
        description="Frontend components created or modified"
    )
    component_architecture_score: float = Field(ge=0.0, le=10.0, default=5.0, description="Component architecture quality (0-10)")
    
    # State Management
    state_management_changes: List[StateManagementChange] = Field(
        default_factory=list,
        description="State management implementations and modifications"
    )
    state_architecture_score: float = Field(ge=0.0, le=10.0, default=5.0, description="State management architecture quality (0-10)")
    
    # UI/UX Optimizations
    ui_optimizations: List[UIOptimization] = Field(
        default_factory=list,
        description="UI performance and user experience optimizations"
    )
    ui_performance_score: float = Field(ge=0.0, le=10.0, default=5.0, description="UI performance rating (0-10)")
    
    # Accessibility Implementation
    accessibility_implementations: List[str] = Field(default_factory=list, description="Accessibility features implemented")
    accessibility_score: float = Field(ge=0.0, le=10.0, default=5.0, description="Accessibility compliance rating (0-10)")
    
    # Responsive Design
    responsive_design_improvements: List[str] = Field(default_factory=list, description="Responsive design enhancements")
    mobile_optimization_score: float = Field(ge=0.0, le=10.0, default=5.0, description="Mobile experience optimization (0-10)")
    cross_browser_compatibility: float = Field(ge=0.0, le=10.0, default=5.0, description="Cross-browser compatibility rating")
    
    # Styling & Design System
    styling_implementations: List[str] = Field(default_factory=list, description="Styling and CSS implementations")
    design_system_integration: List[str] = Field(default_factory=list, description="Design system component integrations")
    styling_consistency_score: float = Field(ge=0.0, le=10.0, default=5.0, description="Styling consistency rating")
    
    # Performance & Optimization
    bundle_optimizations: List[str] = Field(default_factory=list, description="Bundle size and loading optimizations")
    rendering_optimizations: List[str] = Field(default_factory=list, description="Rendering performance improvements")
    lazy_loading_implementations: List[str] = Field(default_factory=list, description="Lazy loading strategies implemented")
    
    # Testing & Quality Assurance
    test_implementations: List[str] = Field(default_factory=list, description="Frontend tests created or modified")
    test_coverage_estimate: float = Field(ge=0.0, le=100.0, default=0.0, description="Estimated test coverage percentage")
    testing_strategy_improvements: List[str] = Field(default_factory=list, description="Testing methodology enhancements")
    
    # Developer Experience
    development_tooling: List[str] = Field(default_factory=list, description="Development tooling improvements")
    build_optimizations: List[str] = Field(default_factory=list, description="Build process optimizations")
    developer_experience_score: float = Field(ge=0.0, le=10.0, default=5.0, description="Developer experience rating")
    
    # Overall Assessment
    frontend_quality_score: float = Field(ge=0.0, le=10.0, default=5.0, description="Overall frontend implementation quality")
    user_experience_score: float = Field(ge=0.0, le=10.0, default=5.0, description="User experience quality rating")
    maintainability_score: float = Field(ge=0.0, le=10.0, default=5.0, description="Frontend code maintainability rating")