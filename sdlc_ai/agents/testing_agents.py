"""
Testing agent implementations for test case writing, review, and QA testing.
"""
from agno.tools.filesystem import FilesystemTools
from agents.base_agent import create_base_agent

def create_test_case_agent(storage_dir="storage/csv"):
    """Create and configure the test case writing agent."""
    return create_base_agent(
        name="Test Case Writer",
        role="Create comprehensive test cases for the developed code",
        instructions=[
            "Write detailed test cases based on user stories and code",
            "Include preconditions, steps, and expected results",
            "Cover happy path and error scenarios",
            "Add edge cases and boundary testing",
            "Ensure all requirements and acceptance criteria are covered",
            "Format output as JSON for easy processing"
        ],
        model_provider="groq",
        model_id="mixtral-8x7b-32768",
        tools=[FilesystemTools()],
        storage_dir=storage_dir
    )

def create_test_review_agent(storage_dir="storage/csv"):
    """Create and configure the test case review agent."""
    return create_base_agent(
        name="Test Case Reviewer",
        role="Review test cases for completeness and quality",
        instructions=[
            "Evaluate test coverage of requirements",
            "Check clarity of test steps",
            "Verify test cases cover edge cases",
            "Assess testability of each case",
            "Begin your response with APPROVED if test cases meet standards",
            "Otherwise, begin with FEEDBACK and list issues to address"
        ],
        model_provider="groq",
        model_id="mixtral-8x7b-32768",
        storage_dir=storage_dir
    )

def create_qa_agent(storage_dir="storage/csv"):
    """Create and configure the QA testing agent."""
    return create_base_agent(
        name="QA Tester",
        role="Execute test cases and report results",
        instructions=[
            "Execute test cases against provided code",
            "Document detailed test results",
            "Report any issues found with reproducible steps",
            "Provide pass/fail status for each test",
            "Begin your response with PASSED if all tests pass",
            "Otherwise, begin with FAILED and list failed tests"
        ],
        model_provider="groq",
        model_id="mixtral-8x7b-32768",
        tools=[FilesystemTools()],
        storage_dir=storage_dir
    )