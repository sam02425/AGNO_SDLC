"""
Monitoring and feedback agent implementation.
"""
from agno.tools.duckduckgo import DuckDuckGoTools
from agents.base_agent import create_base_agent

def create_monitoring_agent(storage_dir="storage/csv"):
    """Create and configure the monitoring and feedback agent."""
    return create_base_agent(
        name="Monitoring Agent",
        role="Monitor application performance and collect feedback",
        instructions=[
            "Track key performance metrics",
            "Log and analyze errors",
            "Collect user feedback",
            "Generate performance reports",
            "Identify potential improvement areas",
            "Format output as actionable insights"
        ],
        model_provider="groq",
        model_id="mixtral-8x7b-32768",
        tools=[DuckDuckGoTools()],
        storage_dir=storage_dir
    )