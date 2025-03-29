"""
Deployment agent implementation.
"""
from agno.tools.github import GitHubTools
from agno.tools.filesystem import FilesystemTools
from agents.base_agent import create_base_agent

def create_deployment_agent(storage_dir="storage/csv"):
    """Create and configure the deployment agent."""
    return create_base_agent(
        name="Deployment Agent",
        role="Create and execute deployment plan",
        instructions=[
            "Create a comprehensive deployment plan",
            "Include deployment steps and environment details",
            "Document rollback procedures",
            "Outline monitoring setup",
            "Configure CI/CD pipelines if applicable",
            "Format output as clear steps in markdown"
        ],
        model_provider="groq",
        model_id="mixtral-8x7b-32768",
        tools=[GitHubTools(), FilesystemTools()],
        storage_dir=storage_dir
    )