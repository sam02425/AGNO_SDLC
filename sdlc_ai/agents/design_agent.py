"""
Design document creation agent implementation.
"""
from agno.tools.duckduckgo import DuckDuckGoTools
from agents.base_agent import create_base_agent
from knowledge.loaders import FAISSKnowledgeBase

def create_design_document_agent(knowledge_base=None, storage_dir="storage/csv"):
    """
    Create and configure the design document creation agent.

    Args:
        knowledge_base: Optional knowledge base
        storage_dir: Directory for CSV storage

    Returns:
        Configured design document agent
    """
    return create_base_agent(
        name="Design Document Creator",
        role="Create functional and technical design documents",
        instructions=[
            "Create comprehensive design documents based on approved user stories",
            "Include architecture overview, data models, and API specifications",
            "Document UI/UX design guidelines",
            "Outline security considerations and compliance requirements",
            "Structure documents clearly with references to diagrams",
            "Format the output as JSON with functional and technical sections"
        ],
        model_provider="openai",
        model_id="gpt-4o",
        tools=[DuckDuckGoTools()],
        knowledge=knowledge_base,
        storage_dir=storage_dir
    )