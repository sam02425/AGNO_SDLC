"""
Requirements processing agent implementation.
"""
from agents.base_agent import create_base_agent

def create_requirements_agent(storage_dir="storage/csv"):
    """
    Create and configure the requirements processing agent.

    Args:
        storage_dir: Directory for CSV storage

    Returns:
        Configured requirements agent
    """
    return create_base_agent(
        name="Requirements Agent",
        role="Process user requirements and structure them",
        instructions=[
            "Extract functional requirements, non-functional requirements, constraints, and user types",
            "Format requirements in a clear, structured JSON format for generating user stories",
            "Ask clarifying questions when requirements are ambiguous",
            "Include all details provided by the user in your structured output"
        ],
        model_id="gpt-4o",
        storage_dir=storage_dir
    )