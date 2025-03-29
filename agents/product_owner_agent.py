"""
Product owner review agent implementation.
"""
from agents.base_agent import create_base_agent

def create_product_owner_agent(storage_dir="storage/csv"):
    """
    Create and configure the product owner review agent.

    Args:
        storage_dir: Directory for CSV storage

    Returns:
        Configured product owner agent
    """
    return create_base_agent(
        name="Product Owner",
        role="Review user stories for completeness and alignment with product vision",
        instructions=[
            "Evaluate stories for alignment with product vision",
            "Check clarity and completeness of each story",
            "Verify appropriate acceptance criteria",
            "Review priority and estimates for reasonableness",
            "Provide explicit approval or detailed feedback",
            "Begin your response with APPROVED if all stories are acceptable",
            "Otherwise, begin with FEEDBACK and list issues to address"
        ],
        model_provider="openai",
        model_id="gpt-4o",
        storage_dir=storage_dir
    )