"""
Frontend Worker Package
======================
UI/UX implementation, component architecture, and state management specialist.
"""

from .agent import frontend_agent
from .models import FrontendOutput, ComponentImplementation, StateManagementChange, UIOptimization

__all__ = [
    'frontend_agent',
    'FrontendOutput',
    'ComponentImplementation',
    'StateManagementChange',
    'UIOptimization'
]