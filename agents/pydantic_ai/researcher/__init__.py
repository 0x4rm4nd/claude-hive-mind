"""
Researcher Worker Package
========================
Technical research, best practices, and industry standards analysis specialist.
"""

from .agent import researcher_agent
from .models import ResearchFinding, TechnologyEvaluation, BestPracticeRecommendation

__all__ = [
    'researcher_agent',

    'ResearchFinding',
    'TechnologyEvaluation',
    'BestPracticeRecommendation'
]