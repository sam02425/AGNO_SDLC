"""
User story generation agent implementation.
"""
from agents.base_agent import create_base_agent

def create_user_story_agent(storage_dir="storage/csv"):
    """
    Create and configure the user story generation agent.

    Args:
        storage_dir: Directory for CSV storage

    Returns:
        Configured user story agent
    """
    return create_base_agent(
        name="User Story Generator",
        role="Generate comprehensive user stories from requirements",
        instructions=[
            "Create user stories in 'As a [user], I want to [action] so that [benefit]' format",
            "Include acceptance criteria for each story",
            "Assign priority (High/Medium/Low) and effort estimates (1-5) to each story",
            "Ensure stories are testable and valuable",
            "Format output as JSON for easy processing"
        ],
        model_provider="groq",
        model_id="mixtral-8x7b-32768",
        storage_dir=storage_dir
    )