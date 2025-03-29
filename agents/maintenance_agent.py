"""
Maintenance and updates agent implementation.
"""
from agno.tools.github import GitHubTools
from agno.tools.duckduckgo import DuckDuckGoTools
from agents.base_agent import create_base_agent

def create_maintenance_agent(knowledge_base=None, storage_dir="storage/csv"):
    """Create and configure the maintenance and updates agent."""
    return create_base_agent(
        name="Maintenance Agent",
        role="Plan and implement system updates and improvements",
        instructions=[
            "Analyze monitoring data and feedback",
            "Prioritize issues and enhancement requests",
            "Plan bug fixes and feature updates",
            "Suggest optimizations based on usage patterns",
            "Create maintenance schedules",
            "Format output as actionable plan with priorities"
        ],
        model_provider="openai",
        model_id="gpt-4o",
        tools=[GitHubTools(), DuckDuckGoTools()],
        knowledge=knowledge_base,
        storage_dir=storage_dir
    )