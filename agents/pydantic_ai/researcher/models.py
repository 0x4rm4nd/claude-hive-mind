"""
Researcher Worker Output Models
==============================
Pydantic models for structured researcher worker outputs.
"""

from typing import List, Dict, Any, Literal, Optional
from pydantic import BaseModel, Field

from shared.models import WorkerOutput


class ResearchFinding(BaseModel):
    """Individual research finding or insight"""
    research_area: str = Field(description="Research domain or topic area")
    finding_type: str = Field(description="Type of research finding")
    title: str = Field(description="Brief title of the finding")
    description: str = Field(description="Detailed finding description")
    source: str = Field(description="Source of information (URL, documentation, paper)")
    credibility: str = Field(description="Source credibility assessment")
    relevance_score: float = Field(ge=0.0, le=10.0, description="Relevance to current project (0-10)")
    implementation_complexity: str = Field(description="Complexity of implementing this finding")
    potential_impact: str = Field(description="Expected impact if implemented")


class TechnologyEvaluation(BaseModel):
    """Technology assessment and comparison"""
    technology_name: str = Field(description="Name of technology being evaluated")
    technology_category: str = Field(description="Technology category (e.g., 'database', 'framework', 'tool')")
    evaluation_criteria: List[str] = Field(default_factory=list, description="Criteria used for evaluation")
    pros: List[str] = Field(default_factory=list, description="Advantages and benefits")
    cons: List[str] = Field(default_factory=list, description="Disadvantages and limitations")
    alternatives: List[str] = Field(default_factory=list, description="Alternative technologies considered")
    recommendation: str = Field(description="Overall recommendation")
    adoption_complexity: str = Field(description="Complexity of adoption")
    community_support: float = Field(ge=0.0, le=10.0, description="Community support and ecosystem rating (0-10)")
    maturity_score: float = Field(ge=0.0, le=10.0, description="Technology maturity rating (0-10)")


class BestPracticeRecommendation(BaseModel):
    """Best practice or industry standard recommendation"""
    practice_category: str = Field(description="Category of best practice (e.g., 'security', 'testing', 'architecture')")
    recommendation_title: str = Field(description="Brief title of the recommendation")
    description: str = Field(description="Detailed description of the best practice")
    implementation_steps: List[str] = Field(default_factory=list, description="Steps to implement this practice")
    industry_adoption: str = Field(description="Industry adoption level")
    evidence: List[str] = Field(default_factory=list, description="Supporting evidence and references")
    implementation_effort: str = Field(description="Effort required to implement")
    priority: str = Field(description="Implementation priority")
    compliance_frameworks: List[str] = Field(default_factory=list, description="Compliance frameworks this addresses")


