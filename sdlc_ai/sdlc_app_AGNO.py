#!/usr/bin/env python3
# sdlc_app.py - AI-Driven Software Development Lifecycle Application

import os
from pathlib import Path
from dotenv import load_dotenv
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.file import FileTools
from agno.playground import Playground, serve_playground_app

# Load environment variables
load_dotenv()

# Ensure file storage directory exists
file_storage = Path("tmp/sdlc_files")
file_storage.mkdir(parents=True, exist_ok=True)

# Create agents for each SDLC stage
requirements_agent = Agent(
    name="Requirements Agent",
    model=OpenAIChat(id="gpt-4o"),
    instructions=[
        "Process user input requirements and structure them",
        "Extract functional requirements, non-functional requirements, constraints, and user types",
        "Format requirements in a clear, structured JSON format for generating user stories",
        "Ask clarifying questions when requirements are ambiguous",
        "Save the structured requirements to 'requirements.json'"
    ],
    tools=[FileTools(file_storage)],
    show_tool_calls=True,
    markdown=True
)

user_story_agent = Agent(
    name="User Story Generator",
    model=OpenAIChat(id="gpt-4o"),
    instructions=[
        "Generate comprehensive user stories from requirements",
        "Create user stories in 'As a [user], I want to [action] so that [benefit]' format",
        "Include acceptance criteria for each story",
        "Assign priority (High/Medium/Low) and effort estimates (1-5) to each story",
        "Ensure stories are testable and valuable",
        "Save the user stories to 'user_stories.json'"
    ],
    tools=[FileTools(file_storage)],
    show_tool_calls=True,
    markdown=True
)

product_owner_agent = Agent(
    name="Product Owner",
    model=OpenAIChat(id="gpt-4o"),
    instructions=[
        "Review user stories for completeness and alignment with product vision",
        "Evaluate stories for alignment with product vision",
        "Check clarity and completeness of each story",
        "Verify appropriate acceptance criteria",
        "Review priority and estimates for reasonableness",
        "Begin your response with APPROVED if all stories are acceptable",
        "Otherwise, begin with FEEDBACK and list issues to address",
        "Save your review to 'product_review.json'"
    ],
    tools=[FileTools(file_storage)],
    show_tool_calls=True,
    markdown=True
)

user_story_reviser_agent = Agent(
    name="User Story Reviser",
    model=OpenAIChat(id="gpt-4o"),
    instructions=[
        "Revise user stories based on product owner feedback",
        "Address all feedback points while maintaining the user story format",
        "Keep acceptance criteria, priority, and effort estimates",
        "Save the revised user stories to 'user_stories_revised.json'"
    ],
    tools=[FileTools(file_storage)],
    show_tool_calls=True,
    markdown=True
)

design_document_agent = Agent(
    name="Design Document Creator",
    model=OpenAIChat(id="gpt-4o"),
    instructions=[
        "Create functional and technical design documents based on approved user stories",
        "Include architecture overview, data models, and API specifications",
        "Document UI/UX design guidelines",
        "Outline security considerations and compliance requirements",
        "Structure documents clearly with references to diagrams",
        "Save the design documents to 'design_documents.json'"
    ],
    tools=[DuckDuckGoTools(), FileTools(file_storage)],
    show_tool_calls=True,
    markdown=True
)

design_review_agent = Agent(
    name="Design Reviewer",
    model=OpenAIChat(id="gpt-4o"),
    instructions=[
        "Review design documents for technical feasibility and best practices",
        "Evaluate design for alignment with requirements and user stories",
        "Assess technical feasibility of proposed solutions",
        "Check scalability considerations",
        "Review security aspects against best practices",
        "Begin your response with APPROVED if design meets standards",
        "Otherwise, begin with FEEDBACK and list issues to address",
        "Save your review to 'design_review.json'"
    ],
    tools=[FileTools(file_storage)],
    show_tool_calls=True,
    markdown=True
)

design_reviser_agent = Agent(
    name="Design Document Reviser",
    model=OpenAIChat(id="gpt-4o"),
    instructions=[
        "Revise design documents based on reviewer feedback",
        "Address all feedback points while maintaining document structure",
        "Save the revised design documents to 'design_documents_revised.json'"
    ],
    tools=[FileTools(file_storage)],
    show_tool_calls=True,
    markdown=True
)

code_generator_agent = Agent(
    name="Code Generator",
    model=OpenAIChat(id="gpt-4o"),
    instructions=[
        "Generate high-quality code based on design documents",
        "Follow language-specific best practices and coding standards",
        "Include proper error handling and logging",
        "Add appropriate comments and documentation",
        "Organize code in a modular, maintainable structure",
        "Save the generated code to 'code_base.json'"
    ],
    tools=[FileTools(file_storage)],
    show_tool_calls=True,
    markdown=True
)

code_review_agent = Agent(
    name="Code Reviewer",
    model=OpenAIChat(id="gpt-4o"),
    instructions=[
        "Review code for quality, bugs, and adherence to design",
        "Evaluate code quality and readability",
        "Check adherence to design specifications",
        "Identify potential bugs or edge cases",
        "Review performance considerations",
        "Assess test coverage",
        "Begin your response with APPROVED if code meets standards",
        "Otherwise, begin with FEEDBACK and list issues to address",
        "Save your review to 'code_review.json'"
    ],
    tools=[FileTools(file_storage)],
    show_tool_calls=True,
    markdown=True
)

code_fix_agent = Agent(
    name="Code Fixer (After Review)",
    model=OpenAIChat(id="gpt-4o"),
    instructions=[
        "Fix code based on review feedback",
        "Address all issues mentioned in the review",
        "Maintain code quality and readability",
        "Save the fixed code to 'code_base_fixed.json'"
    ],
    tools=[FileTools(file_storage)],
    show_tool_calls=True,
    markdown=True
)

security_review_agent = Agent(
    name="Security Reviewer",
    model=OpenAIChat(id="gpt-4o"),
    instructions=[
        "Perform security review of code to identify vulnerabilities",
        "Check for injection vulnerabilities",
        "Review authentication and authorization mechanisms",
        "Identify potential data exposure risks",
        "Check for security misconfigurations",
        "Assess cross-site scripting (XSS) vulnerabilities",
        "Verify proper handling of sensitive data",
        "Begin your response with APPROVED if code meets security standards",
        "Otherwise, begin with FEEDBACK and list vulnerabilities to address",
        "Save your review to 'security_review.json'"
    ],
    tools=[FileTools(file_storage)],
    show_tool_calls=True,
    markdown=True
)

security_fix_agent = Agent(
    name="Code Fixer (After Security Review)",
    model=OpenAIChat(id="gpt-4o"),
    instructions=[
        "Fix code based on security review feedback",
        "Address all security vulnerabilities identified",
        "Maintain code quality and functionality",
        "Save the security-fixed code to 'code_base_secure.json'"
    ],
    tools=[FileTools(file_storage)],
    show_tool_calls=True,
    markdown=True
)

test_case_agent = Agent(
    name="Test Case Writer",
    model=OpenAIChat(id="gpt-4o"),
    instructions=[
        "Create comprehensive test cases for the developed code",
        "Write detailed test cases based on user stories and code",
        "Include preconditions, steps, and expected results",
        "Cover happy path and error scenarios",
        "Add edge cases and boundary testing",
        "Ensure all requirements and acceptance criteria are covered",
        "Save the test cases to 'test_cases.json'"
    ],
    tools=[FileTools(file_storage)],
    show_tool_calls=True,
    markdown=True
)

test_review_agent = Agent(
    name="Test Case Reviewer",
    model=OpenAIChat(id="gpt-4o"),
    instructions=[
        "Review test cases for completeness and quality",
        "Evaluate test coverage of requirements",
        "Check clarity of test steps",
        "Verify test cases cover edge cases",
        "Assess testability of each case",
        "Begin your response with APPROVED if test cases meet standards",
        "Otherwise, begin with FEEDBACK and list issues to address",
        "Save your review to 'test_review.json'"
    ],
    tools=[FileTools(file_storage)],
    show_tool_calls=True,
    markdown=True
)

test_fix_agent = Agent(
    name="Test Case Fixer",
    model=OpenAIChat(id="gpt-4o"),
    instructions=[
        "Fix test cases based on review feedback",
        "Address all issues mentioned in the review",
        "Maintain test case clarity and coverage",
        "Save the fixed test cases to 'test_cases_fixed.json'"
    ],
    tools=[FileTools(file_storage)],
    show_tool_calls=True,
    markdown=True
)

qa_agent = Agent(
    name="QA Tester",
    model=OpenAIChat(id="gpt-4o"),
    instructions=[
        "Execute test cases against provided code",
        "Document detailed test results",
        "Report any issues found with reproducible steps",
        "Provide pass/fail status for each test",
        "Begin your response with PASSED if all tests pass",
        "Otherwise, begin with FAILED and list failed tests",
        "Save your test results to 'qa_results.json'"
    ],
    tools=[FileTools(file_storage)],
    show_tool_calls=True,
    markdown=True
)

qa_fix_agent = Agent(
    name="Code Fixer (After QA)",
    model=OpenAIChat(id="gpt-4o"),
    instructions=[
        "Fix code based on QA test failures",
        "Address all issues found during testing",
        "Maintain code quality and functionality",
        "Save the fixed code to 'code_base_final.json'"
    ],
    tools=[FileTools(file_storage)],
    show_tool_calls=True,
    markdown=True
)

deployment_agent = Agent(
    name="Deployment Agent",
    model=OpenAIChat(id="gpt-4o"),
    instructions=[
        "Create and execute deployment plan",
        "Include deployment steps and environment details",
        "Document rollback procedures",
        "Outline monitoring setup",
        "Configure CI/CD pipelines if applicable",
        "Save the deployment plan to 'deployment_plan.json'"
    ],
    tools=[FileTools(file_storage)],
    show_tool_calls=True,
    markdown=True
)

monitoring_agent = Agent(
    name="Monitoring Agent",
    model=OpenAIChat(id="gpt-4o"),
    instructions=[
        "Set up monitoring for the deployed application",
        "Track key performance metrics",
        "Log and analyze errors",
        "Collect user feedback",
        "Generate performance reports",
        "Identify potential improvement areas",
        "Save the monitoring plan to 'monitoring_plan.json'"
    ],
    tools=[DuckDuckGoTools(), FileTools(file_storage)],
    show_tool_calls=True,
    markdown=True
)

maintenance_agent = Agent(
    name="Maintenance Agent",
    model=OpenAIChat(id="gpt-4o"),
    instructions=[
        "Plan and implement system updates and improvements",
        "Analyze monitoring data and feedback",
        "Prioritize issues and enhancement requests",
        "Plan bug fixes and feature updates",
        "Suggest optimizations based on usage patterns",
        "Create maintenance schedules",
        "Save the maintenance plan to 'maintenance_plan.json'"
    ],
    tools=[DuckDuckGoTools(), FileTools(file_storage)],
    show_tool_calls=True,
    markdown=True
)

# Function to run the workflow
def run_workflow(requirements_text):
    try:
        print("\n===== STEP 1: PROCESSING REQUIREMENTS =====")
        print("Sending requirements to the Requirements Agent...")
        requirements_agent.print_response(
            f"Process these requirements and save them to requirements.json:\n\n{requirements_text}",
            stream=True
        )

        print("\n===== STEP 2: GENERATING USER STORIES =====")
        print("Generating user stories based on requirements...")
        user_story_agent.print_response(
            "Read the requirements from requirements.json and generate comprehensive user stories. Save them to user_stories.json.",
            stream=True
        )

        print("\n===== STEP 3: PRODUCT OWNER REVIEW =====")
        print("Product owner reviewing user stories...")
        product_owner_agent.print_response(
            "Review the user stories in user_stories.json for completeness, clarity, and alignment with product vision. Provide approval or feedback.",
            stream=True
        )

        # Check if user stories were approved or need revision
        print("\nChecking product owner review results...")
        print("Would you like to proceed assuming user stories were APPROVED? (y/n): ")
        approval = input()

        if approval.lower() != 'y':
            print("\n===== STEP 3b: REVISING USER STORIES =====")
            print("Revising user stories based on feedback...")
            user_story_reviser_agent.print_response(
                "Read the user stories from user_stories.json and the product owner feedback from product_review.json. Revise the user stories accordingly and save to user_stories_revised.json.",
                stream=True
            )
            print("\n===== RETURNING TO PRODUCT OWNER REVIEW =====")
            print("Product owner reviewing revised user stories...")
            product_owner_agent.print_response(
                "Review the revised user stories in user_stories_revised.json for completeness, clarity, and alignment with product vision. Provide approval or feedback.",
                stream=True
            )

        print("\n===== STEP 4: CREATING DESIGN DOCUMENTS =====")
        print("Creating design documents based on approved user stories...")
        design_document_agent.print_response(
            "Read the approved user stories and create comprehensive functional and technical design documents. Save them to design_documents.json.",
            stream=True
        )

        print("\n===== STEP 5: DESIGN REVIEW =====")
        print("Reviewing design documents...")
        design_review_agent.print_response(
            "Review the design documents in design_documents.json for technical feasibility and adherence to best practices. Provide approval or feedback.",
            stream=True
        )

        # Check if design was approved or needs revision
        print("\nChecking design review results...")
        print("Would you like to proceed assuming design was APPROVED? (y/n): ")
        approval = input()

        if approval.lower() != 'y':
            print("\n===== STEP 5b: REVISING DESIGN DOCUMENTS =====")
            print("Revising design documents based on feedback...")
            design_reviser_agent.print_response(
                "Read the design documents from design_documents.json and the review feedback from design_review.json. Revise the design documents accordingly and save to design_documents_revised.json.",
                stream=True
            )
            print("\n===== RETURNING TO DESIGN REVIEW =====")
            print("Reviewing revised design documents...")
            design_review_agent.print_response(
                "Review the revised design documents in design_documents_revised.json for technical feasibility and adherence to best practices. Provide approval or feedback.",
                stream=True
            )

        print("\n===== STEP 6: GENERATING CODE =====")
        print("Generating code based on approved design...")
        code_generator_agent.print_response(
            "Read the approved design documents and generate code implementing the design. Save the code to code_base.json.",
            stream=True
        )

        print("\n===== STEP 7: CODE REVIEW =====")
        print("Reviewing generated code...")
        code_review_agent.print_response(
            "Review the code in code_base.json for quality, bugs, and adherence to design. Provide approval or feedback.",
            stream=True
        )

        # Check if code was approved or needs fixes
        print("\nChecking code review results...")
        print("Would you like to proceed assuming code was APPROVED? (y/n): ")
        approval = input()

        if approval.lower() != 'y':
            print("\n===== STEP 7b: FIXING CODE BASED ON REVIEW =====")
            print("Fixing code based on review feedback...")
            code_fix_agent.print_response(
                "Read the code from code_base.json and the review feedback from code_review.json. Fix the code accordingly and save to code_base_fixed.json.",
                stream=True
            )
            print("\n===== RETURNING TO CODE REVIEW =====")
            print("Reviewing fixed code...")
            code_review_agent.print_response(
                "Review the fixed code in code_base_fixed.json for quality, bugs, and adherence to design. Provide approval or feedback.",
                stream=True
            )

        print("\n===== STEP 8: SECURITY REVIEW =====")
        print("Performing security review on code...")
        security_review_agent.print_response(
            "Perform a security review of the code in code_base.json. Check for vulnerabilities and security issues. Provide approval or feedback.",
            stream=True
        )

        # Check if security review passed or needs fixes
        print("\nChecking security review results...")
        print("Would you like to proceed assuming security review was APPROVED? (y/n): ")
        approval = input()

        if approval.lower() != 'y':
            print("\n===== STEP 8b: FIXING SECURITY ISSUES =====")
            print("Fixing security issues in code...")
            security_fix_agent.print_response(
                "Read the code from code_base.json and the security review from security_review.json. Fix the security issues and save to code_base_secure.json.",
                stream=True
            )
            print("\n===== RETURNING TO SECURITY REVIEW =====")
            print("Reviewing code with security fixes...")
            security_review_agent.print_response(
                "Review the fixed code in code_base_secure.json for security vulnerabilities. Provide approval or feedback.",
                stream=True
            )

        print("\n===== STEP 9: WRITING TEST CASES =====")
        print("Writing test cases for the code...")
        test_case_agent.print_response(
            "Read the user stories and code. Write comprehensive test cases for the application. Save test cases to test_cases.json.",
            stream=True
        )

        print("\n===== STEP 10: TEST CASE REVIEW =====")
        print("Reviewing test cases...")
        test_review_agent.print_response(
            "Review the test cases in test_cases.json for completeness and quality. Provide approval or feedback.",
            stream=True
        )

        # Check if test cases were approved or need revision
        print("\nChecking test case review results...")
        print("Would you like to proceed assuming test cases were APPROVED? (y/n): ")
        approval = input()

        if approval.lower() != 'y':
            print("\n===== STEP 10b: FIXING TEST CASES =====")
            print("Fixing test cases based on review...")
            test_fix_agent.print_response(
                "Read the test cases from test_cases.json and the review feedback from test_review.json. Fix the test cases accordingly and save to test_cases_fixed.json.",
                stream=True
            )
            print("\n===== RETURNING TO TEST CASE REVIEW =====")
            print("Reviewing fixed test cases...")
            test_review_agent.print_response(
                "Review the fixed test cases in test_cases_fixed.json for completeness and quality. Provide approval or feedback.",
                stream=True
            )

        print("\n===== STEP 11: QA TESTING =====")
        print("Running QA tests on the code...")
        qa_agent.print_response(
            "Execute the test cases in test_cases.json against the code in code_base.json. Report test results and save to qa_results.json.",
            stream=True
        )

        # Check if QA tests passed or found issues
        print("\nChecking QA test results...")
        print("Would you like to proceed assuming QA tests PASSED? (y/n): ")
        approval = input()

        if approval.lower() != 'y':
            print("\n===== STEP 11b: FIXING CODE AFTER QA =====")
            print("Fixing code based on QA test results...")
            qa_fix_agent.print_response(
                "Read the code from code_base.json and the QA test results from qa_results.json. Fix the issues identified during testing and save to code_base_final.json.",
                stream=True
            )
            print("\n===== RETURNING TO QA TESTING =====")
            print("Re-running QA tests on fixed code...")
            qa_agent.print_response(
                "Execute the test cases in test_cases.json against the fixed code in code_base_final.json. Report test results and save to qa_results_final.json.",
                stream=True
            )

        print("\n===== STEP 12: DEPLOYMENT =====")
        print("Creating deployment plan...")
        deployment_agent.print_response(
            "Create a comprehensive deployment plan for the application. Include steps, environment details, and rollback procedures. Save to deployment_plan.json.",
            stream=True
        )

        print("\n===== STEP 13: MONITORING SETUP =====")
        print("Setting up application monitoring...")
        monitoring_agent.print_response(
            "Create a monitoring plan for the deployed application. Include metrics to track, logging, and feedback collection methods. Save to monitoring_plan.json.",
            stream=True
        )

        print("\n===== STEP 14: MAINTENANCE PLANNING =====")
        print("Creating maintenance plan...")
        maintenance_agent.print_response(
            "Create a maintenance plan for the application based on the monitoring plan. Include update schedules, issue prioritization, and optimization strategies. Save to maintenance_plan.json.",
            stream=True
        )

        print("\n===== WORKFLOW COMPLETE =====")
        print("The SDLC workflow has completed successfully!")
        print(f"All artifacts are saved in the {file_storage} directory.")

        return "SDLC Workflow completed successfully!"

    except Exception as e:
        print(f"\nERROR: {str(e)}")
        return f"Workflow failed with error: {str(e)}"

# Create the playground app with all agents
def create_playground():
    all_agents = [
        requirements_agent,
        user_story_agent,
        product_owner_agent,
        user_story_reviser_agent,
        design_document_agent,
        design_review_agent,
        design_reviser_agent,
        code_generator_agent,
        code_review_agent,
        code_fix_agent,
        security_review_agent,
        security_fix_agent,
        test_case_agent,
        test_review_agent,
        test_fix_agent,
        qa_agent,
        qa_fix_agent,
        deployment_agent,
        monitoring_agent,
        maintenance_agent
    ]

    app = Playground(agents=all_agents).get_app()
    return app

# Example usage
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="SDLC Workflow with AGNO")
    parser.add_argument("--playground", action="store_true", help="Launch the playground interface")
    parser.add_argument("--workflow", action="store_true", help="Run the complete workflow")

    args = parser.parse_args()

    if args.playground:
        print("Launching SDLC Agent Playground...")
        app = create_playground()
        serve_playground_app("sdlc_app:app", reload=True)

    elif args.workflow:
        print("Running SDLC Workflow...")
        requirements = """
        Create a task management system with the following features:
        1. User authentication (register, login, logout)
        2. Task creation, editing, and deletion
        3. Task categorization with labels
        4. Due dates and priority levels for tasks
        5. Task assignment to team members
        6. Email notifications for upcoming deadlines
        7. Dashboard with task statistics
        8. Mobile-responsive design

        Non-functional requirements:
        - The system should load pages in under 2 seconds
        - The system should be secure and protect user data
        - The system should be available 99.9% of the time
        """

        result = run_workflow(requirements)
        print(result)

    else:
        parser.print_help()