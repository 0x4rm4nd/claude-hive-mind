#!/usr/bin/env python3
"""
Scribe Agent Module Runner
==========================
Module entry point for running the Scribe agent via python -m syntax.
Maps to the actual Pydantic AI scribe implementation.
"""

if __name__ == "__main__":
    import sys
    import os
    
    # Add the .claude directory to Python path for imports
    claude_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if claude_dir not in sys.path:
        sys.path.insert(0, claude_dir)
    
    from agents.pydantic_ai.scribe.runner import main
    
    # Execute the scribe main function
    sys.exit(main())