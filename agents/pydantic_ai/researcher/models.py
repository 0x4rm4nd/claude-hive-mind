"""
Researcher Worker Output Models
==============================
Pydantic models for structured researcher worker outputs.
"""

from typing import List, Dict, Any, Literal, Optional
from pydantic import BaseModel, Field

from ..shared.models import WorkerOutput


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


class ResearcherOutput(WorkerOutput):
    """Researcher worker structured output - extends base WorkerOutput"""
    
    # Research Findings
    research_findings: List[ResearchFinding] = Field(
        default_factory=list,
        description="Research findings and insights discovered"
    )
    research_scope: List[str] = Field(default_factory=list, description="Areas of research conducted")
    
    # Technology Evaluations
    technology_evaluations: List[TechnologyEvaluation] = Field(
        default_factory=list,
        description="Technology assessments and comparisons"
    )
    technology_recommendations: List[str] = Field(default_factory=list, description="Top technology recommendations")
    
    # Best Practices
    best_practice_recommendations: List[BestPracticeRecommendation] = Field(
        default_factory=list,
        description="Industry best practices and standards"
    )
    compliance_requirements: List[str] = Field(default_factory=list, description="Compliance and regulatory requirements")
    
    # Industry Analysis
    industry_trends: List[str] = Field(default_factory=list, description="Relevant industry trends and developments")
    competitive_analysis: List[str] = Field(default_factory=list, description="Competitive landscape insights")
    market_insights: List[str] = Field(default_factory=list, description="Market trends and opportunities")
    
    # Risk Assessment
    technology_risks: List[str] = Field(default_factory=list, description="Technology and implementation risks")
    security_considerations: List[str] = Field(default_factory=list, description="Security implications and considerations")
    regulatory_considerations: List[str] = Field(default_factory=list, description="Regulatory and compliance considerations")
    
    # Implementation Guidance
    adoption_roadmap: List[str] = Field(default_factory=list, description="Recommended adoption and implementation roadmap")
    migration_strategies: List[str] = Field(default_factory=list, description="Migration approaches for current technologies")
    training_requirements: List[str] = Field(default_factory=list, description="Team training and skill development needs")
    
    # Quality Metrics
    research_depth_score: float = Field(ge=0.0, le=10.0, default=5.0, description="Depth and thoroughness of research (0-10)")
    source_credibility_score: float = Field(ge=0.0, le=10.0, default=5.0, description="Overall source credibility rating (0-10)")
    relevance_score: float = Field(ge=0.0, le=10.0, default=5.0, description="Research relevance to project needs (0-10)")
    
    # Knowledge Management
    knowledge_gaps_identified: List[str] = Field(default_factory=list, description="Areas requiring additional research")
    follow_up_research_topics: List[str] = Field(default_factory=list, description="Topics for future research")
    research_methodology: str = Field(default="", description="Research approach and methodology used")
    
    # Overall Assessment
    research_quality_score: float = Field(ge=0.0, le=10.0, default=5.0, description="Overall research quality rating")
    actionability_score: float = Field(ge=0.0, le=10.0, default=5.0, description="How actionable the research findings are")
    strategic_value: float = Field(ge=0.0, le=10.0, default=5.0, description="Strategic value of research insights")