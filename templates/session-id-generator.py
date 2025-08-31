"""
Session ID Generator Template
Generates session IDs in the correct format: YYYY-MM-DD-HH-mm-shorttaskdescription
"""

import re
from datetime import datetime

def generate_session_id(task_description: str) -> str:
    """
    Generate a session ID in the format: YYYY-MM-DD-HH-mm-shorttaskdescription
    
    Args:
        task_description: The task description to create a slug from
        
    Returns:
        Properly formatted session ID
        
    Examples:
        "Analyze crypto-data architecture" -> "2025-08-31-14-30-analyze-crypto-data"
        "Fix authentication bug in API" -> "2025-08-31-14-30-fix-authentication-bug"
        "Implement user registration" -> "2025-08-31-14-30-implement-user-registration"
    """
    # Get current timestamp in UTC
    timestamp = datetime.utcnow().strftime('%Y-%m-%d-%H-%M')
    
    # Process task description to create meaningful slug
    # Remove special characters and normalize
    task_lower = task_description.lower()
    
    # Remove common filler words for cleaner slugs
    filler_words = {'the', 'a', 'an', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
    
    # Extract meaningful words
    words = re.findall(r'\b[a-zA-Z0-9]+\b', task_lower)
    
    # Filter out filler words and take first 4-5 meaningful words
    meaningful_words = [w for w in words if w not in filler_words][:5]
    
    # If we have less than 2 meaningful words, include some filler words
    if len(meaningful_words) < 2:
        meaningful_words = words[:4]
    
    # Join with hyphens to create slug
    task_slug = '-'.join(meaningful_words) if meaningful_words else 'task'
    
    # Truncate slug if too long (keep session IDs reasonable)
    if len(task_slug) > 50:
        task_slug = task_slug[:50].rstrip('-')
    
    # Combine timestamp and slug
    session_id = f"{timestamp}-{task_slug}"
    
    return session_id

def validate_session_id_format(session_id: str) -> bool:
    """
    Validate that a session ID follows the correct format
    
    Args:
        session_id: The session ID to validate
        
    Returns:
        True if format is correct, False otherwise
    """
    # Pattern: YYYY-MM-DD-HH-mm-shorttaskdescription
    pattern = r'^\d{4}-\d{2}-\d{2}-\d{2}-\d{2}-[a-zA-Z0-9\-]+$'
    return bool(re.match(pattern, session_id))

# Example usage for agents
if __name__ == "__main__":
    # Test examples
    test_cases = [
        "Analyze crypto-data architecture and scalability",
        "Fix authentication bug in API service",
        "Implement user registration with OAuth2",
        "Review and optimize database queries",
        "Create comprehensive test suite for payment processing",
    ]
    
    for task in test_cases:
        session_id = generate_session_id(task)
        valid = validate_session_id_format(session_id)
        print(f"Task: {task[:50]}...")
        print(f"Session ID: {session_id}")
        print(f"Valid format: {valid}")
        print()