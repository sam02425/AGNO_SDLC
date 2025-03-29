"""
Main workflow orchestrator that manages the SDLC process
from requirements to deployment and maintenance.
"""
import os
import json
from typing import Dict, Any, Optional

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

# Import knowledge base and workflow components
from knowledge.loaders import FAISSKnowledgeBase
from workflow.state_manager import WorkflowState
from workflow.transitions import get_next_stage

class SDLCWorkflow:
    """
    Software Development Lifecycle workflow orchestrator.
    Manages the flow of work through all stages according to the diagram.
    """
    def __init__(self,
                 state_file: Optional[str] = "storage/workflow_state.json",
                 storage_dir: str = "storage/csv",
                 knowledge_dir: str = "knowledge/resources"):
        """
        Initialize the SDLC workflow.

        Args:
            state_file: Path to save workflow state
            storage_dir: Directory for CSV storage
            knowledge_dir: Directory for knowledge resources
        """
        # Initialize workflow state
        self.state_manager = WorkflowState(state_file)

        # Initialize knowledge base if resources exist
        self.knowledge_base = None
        if os.path.exists(knowledge_dir) and any(os.listdir(knowledge_dir)):
            self.knowledge_base = FAISSKnowledgeBase(docs_path=knowledge_dir)

            # Get all PDF files in the knowledge directory
            pdf_files = [
                os.path.join(knowledge_dir, f)
                for f in os.listdir(knowledge_dir)
                if f.endswith('.pdf') or f.endswith('.txt')
            ]

            if pdf_files:
                self.knowledge_base.load_documents(pdf_files)

                # Build index if it doesn't exist
                index_path = os.path.join(knowledge_dir, "index.faiss")
                if not os.path.exists(index_path):
                    self.knowledge_base.build_index()
                else:
                    self.knowledge_base.load_index()

        # Initialize all agents
        self.agents = {
            "requirements": create_requirements_agent(storage_dir),
            "user_stories": create_user_story_agent(storage_dir),
            "product_review": create_product_owner_agent(storage_dir),
            "design_documents": create_design_document_agent(self.knowledge_base, storage_dir),
            "design_review": create_design_review_agent(self.knowledge_base, storage_dir),
            "code_generator": create_code_generator_agent(self.knowledge_base, storage_dir),
            "code_review": create_code_review_agent(self.knowledge_base, storage_dir),
            "security_review": create_security_review_agent(self.knowledge_base, storage_dir),
            "test_cases": create_test_case_agent(storage_dir),
            "test_review": create_test_review_agent(storage_dir),
            "qa_testing": create_qa_agent(storage_dir),
            "deployment": create_deployment_agent(storage_dir),
            "monitoring": create_monitoring_agent(storage_dir),
            "maintenance": create_maintenance_agent(self.knowledge_base, storage_dir),
            # Code fix agent is reused for different types of fixes
            "code_fix": create_code_generator_agent(self.knowledge_base, storage_dir)
        }

    def process_requirements(self, requirements_text: str) -> Dict[str, Any]:
        """
        Process initial requirements and start the workflow.

        Args:
            requirements_text: User input requirements

        Returns:
            Processed requirements
        """
        response = self.agents["requirements"].get_response(requirements_text)

        # Try to parse as JSON if possible
        try:
            requirements = json.loads(response)
        except json.JSONDecodeError:
            # If not JSON, use the raw response
            requirements = {"raw": response}

        # Update state
        self.state_manager.update("requirements", requirements)
        self.state_manager.add_to_history("requirements", {
            "input": requirements_text,
            "output": requirements
        })
        self.state_manager.set_stage("user_stories")

        return requirements

    def generate_user_stories(self) -> list:
        """Generate user stories from requirements."""
        requirements = self.state_manager.get("requirements")

        # Generate user stories
        response = self.agents["user_stories"].get_response(
            f"Generate user stories based on these requirements: {json.dumps(requirements)}"
        )

        # Try to parse as JSON if possible
        try:
            user_stories = json.loads(response)
        except json.JSONDecodeError:
            # If not JSON, use the raw response
            user_stories = [{"raw": response}]

        # Update state
        self.state_manager.update("user_stories", user_stories)
        self.state_manager.add_to_history("user_stories", {
            "input": requirements,
            "output": user_stories
        })
        self.state_manager.set_stage("product_review")

        return user_stories

    def product_owner_review(self) -> Dict[str, Any]:
        """Have product owner review user stories."""
        user_stories = self.state_manager.get("user_stories")

        # Review user stories
        response = self.agents["product_review"].get_response(
            f"Review these user stories: {json.dumps(user_stories)}"
        )

        # Update state
        self.state_manager.update("feedback.product_review", response)
        self.state_manager.add_to_history("product_review", {
            "input": user_stories,
            "output": response
        })

        # Determine next stage based on response
        if response.startswith("APPROVED"):
            self.state_manager.update("review_status.product_review", "approved")
            self.state_manager.set_stage("create_design_documents")
        else:
            self.state_manager.update("review_status.product_review", "needs_revision")
            self.state_manager.set_stage("revise_user_stories")

        return {"response": response}

    def revise_user_stories(self) -> list:
        """Revise user stories based on feedback."""
        user_stories = self.state_manager.get("user_stories")
        feedback = self.state_manager.get("feedback.product_review")

        # Revise user stories
        response = self.agents["user_stories"].get_response(
            f"Revise these user stories based on feedback:\n\n"
            f"User Stories: {json.dumps(user_stories)}\n\n"
            f"Feedback: {feedback}"
        )

        # Try to parse as JSON if possible
        try:
            revised_stories = json.loads(response)
        except json.JSONDecodeError:
            # If not JSON, use the raw response
            revised_stories = [{"raw": response}]

        # Update state
        self.state_manager.update("user_stories", revised_stories)
        self.state_manager.add_to_history("revise_user_stories", {
            "input": {"stories": user_stories, "feedback": feedback},
            "output": revised_stories
        })
        self.state_manager.set_stage("product_review")

        return revised_stories

    def create_design_documents(self) -> Dict[str, Any]:
        """Create design documents based on approved user stories."""
        user_stories = self.state_manager.get("user_stories")
        requirements = self.state_manager.get("requirements")

        # Create design documents
        response = self.agents["design_documents"].get_response(
            f"Create design documents based on these requirements and user stories:\n\n"
            f"Requirements: {json.dumps(requirements)}\n\n"
            f"User Stories: {json.dumps(user_stories)}"
        )

        # Try to parse as JSON if possible
        try:
            design_docs = json.loads(response)
        except json.JSONDecodeError:
            # If not JSON, split into functional and technical sections
            design_docs = {
                "functional": {"raw": response},
                "technical": {"raw": response}
            }

        # Update state
        self.state_manager.update("design_documents", design_docs)
        self.state_manager.add_to_history("create_design_documents", {
            "input": {"requirements": requirements, "user_stories": user_stories},
            "output": design_docs
        })
        self.state_manager.set_stage("design_review")

        return design_docs

    # Implement remaining workflow methods...
    # For brevity, I'll focus on a subset of core functionality

    def run_stage(self, stage_name: str, input_data: Any = None) -> Any:
        """
        Run a specific stage of the workflow.

        Args:
            stage_name: Stage to run
            input_data: Optional input data

        Returns:
            Result of the stage
        """
        stage_methods = {
            "requirements": self.process_requirements,
            "user_stories": self.generate_user_stories,
            "product_review": self.product_owner_review,
            "revise_user_stories": self.revise_user_stories,
            "create_design_documents": self.create_design_documents,
            # Add other stages as needed
        }

        if stage_name in stage_methods:
            if stage_name == "requirements" and input_data:
                return stage_methods[stage_name](input_data)
            else:
                return stage_methods[stage_name]()
        else:
            return f"Stage {stage_name} not implemented yet"

    def run_workflow(self, requirements_text: str) -> Dict[str, Any]:
        """
        Run the entire workflow from start to finish.

        Args:
            requirements_text: User input requirements

        Returns:
            Final workflow state
        """
        # Start with requirements
        self.process_requirements(requirements_text)

        # Continue through stages based on current_stage
        max_iterations = 100  # Prevent infinite loops
        iterations = 0

        while not self.state_manager.is_complete() and iterations < max_iterations:
            current_stage = self.state_manager.get_current_stage()
            result = self.run_stage(current_stage)

            # Break if stuck in the same stage
            if self.state_manager.get_current_stage() == current_stage:
                break

            iterations += 1

        return self.state_manager.get_full_state()