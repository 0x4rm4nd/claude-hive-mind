"""
Analyzer Worker Output Models
=============================
Pydantic models defining structured output formats for security, performance, and code quality analysis.
"""

from typing import List, Literal
from pydantic import BaseModel, Field

from shared.models import WorkerOutput


class SecurityFinding(BaseModel):
    """Individual security vulnerability or configuration issue.

    Represents a specific security concern found during analysis, including
    severity assessment, location details, and remediation guidance.
    """

    severity: Literal["critical", "high", "medium", "low"] = Field(
        description="Security issue severity"
    )
    category: str = Field(
        description="OWASP category or security domain (e.g., 'injection', 'authentication')"
    )
    description: str = Field(description="Detailed finding description")
    location: str = Field(description="File path and line number where issue was found")
    recommendation: str = Field(description="Specific remediation steps")
    confidence: float = Field(
        ge=0.0, le=1.0, description="Confidence in finding accuracy"
    )


class PerformanceIssue(BaseModel):
    """Performance bottleneck or optimization opportunity.

    Represents a specific performance concern with impact assessment
    and optimization recommendations.
    """

    severity: Literal["critical", "high", "medium", "low"] = Field(
        description="Performance impact level"
    )
    category: str = Field(
        description="Performance domain (e.g., 'database', 'algorithm', 'network')"
    )
    description: str = Field(description="Detailed performance issue description")
    location: str = Field(description="Code location where issue occurs")
    impact: str = Field(description="Expected performance impact and metrics")
    optimization: str = Field(description="Recommended optimization approach")
    effort_estimate: str = Field(
        description="Estimated effort to fix (e.g., '2-4h', '1-2d')"
    )


class QualityMetric(BaseModel):
    """Code quality measurement and assessment.

    Quantifies specific aspects of code quality with current values,
    target thresholds, and improvement recommendations.
    """

    metric_name: str = Field(
        description="Quality metric name (e.g., 'cyclomatic_complexity', 'test_coverage')"
    )
    current_value: float = Field(description="Current measured value")
    target_value: float = Field(description="Recommended target value")
    assessment: Literal["excellent", "good", "needs_improvement", "critical"] = Field(
        description="Quality assessment"
    )
    improvement_actions: List[str] = Field(
        description="Specific actions to improve this metric"
    )


