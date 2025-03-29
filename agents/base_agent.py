"""
Base agent configuration for the SDLC workflow.
"""
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from storage.csv_storage import CSVAgentStorage

def create_base_agent(
    name: str,
    role: str,
    instructions: list,
    model_id: str = "gpt-4o",
    tools: list = None,
    knowledge = None,
    storage_dir: str = "storage/csv",
):
    """
    Create a base agent with common configuration.

    Args:
        name: Agent name
        role: Agent role description
        instructions: List of instructions for the agent
        model_id: Model ID to use
        tools: List of tools for the agent
        knowledge: Knowledge base for the agent
        storage_dir: Directory for CSV storage

    Returns:
        Configured Agent instance
    """
    # Create model (currently supporting OpenAI only)
    model = OpenAIChat(id=model_id)

    # Create CSV storage
    storage = CSVAgentStorage(
        table_name=name.lower().replace(" ", "_"),
        csv_dir=storage_dir
    )

    # Create and return the agent
    return Agent(
        name=name,
        role=role,
        model=model,
        instructions=instructions,
        tools=tools or [],
        knowledge=knowledge,
        storage=storage,
        add_datetime_to_instructions=True,
        add_history_to_messages=True,
        show_tool_calls=True,
        markdown=True,
    )