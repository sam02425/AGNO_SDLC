"""
Interactive playground for working with agents individually or as part of the workflow.
"""
from agno.playground import Playground, serve_playground_app

# Import all agent creation functions
from agents.requirements_agent import create_requirements_agent
from agents.user_story_agent import create_user_story_agent
from agents.product_owner_agent import create_product_owner_agent
from agents.design_agent import create_design_document_agent
from agents.code_agent import create_code_generator_agent
from agents.review_agents import (
    create_code_review_agent,
    create_design_review_agent,
    create_security_review_agent
)
from agents.testing_agents import (
    create_test_case_agent,
    create_test_review_agent,
    create_qa_agent
)
from agents.deployment_agent import create_deployment_agent
from agents.monitoring_agent import create_monitoring_agent
from agents.maintenance_agent import create_maintenance_agent

def create_playground_app(storage_dir="storage/csv"):
    """
    Create the playground application with all agents.

    Args:
        storage_dir: Directory for CSV storage

    Returns:
        Playground application instance
    """
    # Create all agents
    agents = [
        create_requirements_agent(storage_dir),
        create_user_story_agent(storage_dir),
        create_product_owner_agent(storage_dir),
        create_design_document_agent(None, storage_dir),
        create_design_review_agent(None, storage_dir),
        create_code_generator_agent(None, storage_dir),
        create_code_review_agent(None, storage_dir),
        create_security_review_agent(None, storage_dir),
        create_test_case_agent(storage_dir),
        create_test_review_agent(storage_dir),
        create_qa_agent(storage_dir),
        create_deployment_agent(storage_dir),
        create_monitoring_agent(storage_dir),
        create_maintenance_agent(None, storage_dir)
    ]

    # Create and return the playground app
    return Playground(agents=agents).get_app()

def serve_playground(app=None):
    """
    Serve the playground application.

    Args:
        app: Optional Playground application instance
    """
    if app is None:
        app = create_playground_app()

    serve_playground_app("ui.playground:app", reload=True)

# Create a default app instance
app = create_playground_app()