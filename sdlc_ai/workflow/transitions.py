"""
Stage transition logic for the SDLC workflow.
"""
from typing import Dict, Any

def get_next_stage(current_stage: str, result: Any, state: Dict[str, Any]) -> str:
    """
    Determine the next stage based on the current stage and result.

    Args:
        current_stage: Current workflow stage
        result: Result from the current stage
        state: Current workflow state

    Returns:
        Next stage name
    """
    # Convert result to string if it's not already
    result_str = str(result) if result else ""

    # Define transitions based on current stage
    transitions = {
        "requirements": "user_stories",
        "user_stories": "product_review",
        "product_review": "create_design_documents" if result_str.startswith("APPROVED") else "revise_user_stories",
        "revise_user_stories": "product_review",
        "create_design_documents": "design_review",
        "design_review": "generate_code" if result_str.startswith("APPROVED") else "revise_design_documents",
        "revise_design_documents": "design_review",
        "generate_code": "code_review",
        "code_review": "security_review" if result_str.startswith("APPROVED") else "fix_code_after_review",
        "fix_code_after_review": "code_review",
        "security_review": "write_test_cases" if result_str.startswith("APPROVED") else "fix_code_after_security",
        "fix_code_after_security": "security_review",
        "write_test_cases": "test_cases_review",
        "test_cases_review": "qa_testing" if result_str.startswith("APPROVED") else "fix_test_cases",
        "fix_test_cases": "test_cases_review",
        "qa_testing": "deployment" if result_str.startswith("PASSED") else "fix_code_after_qa",
        "fix_code_after_qa": "qa_testing",
        "deployment": "monitoring",
        "monitoring": "maintenance",
        "maintenance": "complete"
    }

    return transitions.get(current_stage, "requirements")