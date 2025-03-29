"""
Review agent implementations for code, design, and security reviews.
"""
from agno.tools.github import GitHubTools
from agents.base_agent import create_base_agent

def create_code_review_agent(knowledge_base=None, storage_dir="storage/csv"):
    """Create and configure the code review agent."""
    return create_base_agent(
        name="Code Reviewer",
        role="Review code for quality, bugs, and adherence to design",
        instructions=[
            "Evaluate code quality and readability",
            "Check adherence to design specifications",
            "Identify potential bugs or edge cases",
            "Review performance considerations",
            "Assess test coverage",
            "Begin your response with APPROVED if code meets standards",
            "Otherwise, begin with FEEDBACK and list issues to address"
        ],
        model_provider="openai",
        model_id="gpt-4o",
        tools=[GitHubTools()],
        knowledge=knowledge_base,
        storage_dir=storage_dir
    )

def create_design_review_agent(knowledge_base=None, storage_dir="storage/csv"):
    """Create and configure the design review agent."""
    return create_base_agent(
        name="Design Reviewer",
        role="Review design documents for technical feasibility and best practices",
        instructions=[
            "Evaluate design for alignment with requirements and user stories",
            "Assess technical feasibility of proposed solutions",
            "Check scalability considerations",
            "Review security aspects against best practices",
            "Begin your response with APPROVED if design meets standards",
            "Otherwise, begin with FEEDBACK and list issues to address"
        ],
        model_provider="openai",
        model_id="gpt-4o",
        knowledge=knowledge_base,
        storage_dir=storage_dir
    )

def create_security_review_agent(knowledge_base=None, storage_dir="storage/csv"):
    """Create and configure the security review agent."""
    return create_base_agent(
        name="Security Reviewer",
        role="Perform security review of code to identify vulnerabilities",
        instructions=[
            "Check for injection vulnerabilities",
            "Review authentication and authorization mechanisms",
            "Identify potential data exposure risks",
            "Check for security misconfigurations",
            "Assess cross-site scripting (XSS) vulnerabilities",
            "Verify proper handling of sensitive data",
            "Begin your response with APPROVED if code meets security standards",
            "Otherwise, begin with FEEDBACK and list vulnerabilities to address"
        ],
        model_provider="openai",
        model_id="gpt-4o",
        knowledge=knowledge_base,
        storage_dir=storage_dir
    )