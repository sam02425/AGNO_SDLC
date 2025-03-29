"""
Code generation agent implementation.
"""
from agno.tools.github import GithubTools
from agno.tools.filesystem import FilesystemTools
from agents.base_agent import create_base_agent

def create_code_generator_agent(knowledge_base=None, storage_dir="storage/csv"):
    """
    Create and configure the code generation agent.

    Args:
        knowledge_base: Optional knowledge base
        storage_dir: Directory for CSV storage

    Returns:
        Configured code generator agent
    """
    return create_base_agent(
        name="Code Generator",
        role="Generate high-quality code based on design documents",
        instructions=[
            "Generate code that implements the approved design",
            "Follow language-specific best practices and coding standards",
            "Include proper error handling and logging",
            "Add appropriate comments and documentation",
            "Organize code in a modular, maintainable structure",
            "Format output with clear file structure"
        ],
        model_id="gpt-4o",
        tools=[GithubTools(), FilesystemTools()],
        knowledge=knowledge_base,
        storage_dir=storage_dir
    )