"""
State management for the SDLC workflow.
"""
import json
import os
from typing import Dict, List, Any, Optional

class WorkflowState:
    """
    Manages the state of the SDLC workflow, tracking progress and artifacts.
    """
    def __init__(self, state_file: Optional[str] = None):
        """
        Initialize the workflow state.

        Args:
            state_file: Optional path to save state to disk
        """
        self.state_file = state_file
        self.state = {
            "current_stage": "requirements",
            "requirements": {},
            "user_stories": [],
            "design_documents": {
                "functional": {},
                "technical": {}
            },
            "code": {},
            "test_cases": [],
            "feedback": {},
            "review_status": {},
            "test_results": {},
            "deployment": {},
            "monitoring": {},
            "maintenance": {},
            "history": []
        }

        # Load state from file if it exists
        if state_file and os.path.exists(state_file):
            with open(state_file, 'r') as f:
                self.state = json.load(f)

    def get_current_stage(self) -> str:
        """Get the current workflow stage."""
        return self.state["current_stage"]

    def set_stage(self, stage: str) -> None:
        """Set the current workflow stage."""
        self.state["current_stage"] = stage
        self._save_state()

    def update(self, key: str, value: Any) -> None:
        """
        Update a value in the state.

        Args:
            key: State key to update
            value: New value
        """
        keys = key.split('.')
        current = self.state

        for k in keys[:-1]:
            if k not in current:
                current[k] = {}
            current = current[k]

        current[keys[-1]] = value
        self._save_state()

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a value from the state.

        Args:
            key: State key to retrieve
            default: Default value if key not found

        Returns:
            The value or default
        """
        keys = key.split('.')
        current = self.state

        for k in keys:
            if k not in current:
                return default
            current = current[k]

        return current

    def add_to_history(self, stage: str, data: Dict[str, Any]) -> None:
        """
        Add an entry to the workflow history.

        Args:
            stage: Stage name
            data: Data to add to history
        """
        self.state["history"].append({
            "stage": stage,
            "data": data
        })
        self._save_state()

    def is_complete(self) -> bool:
        """Check if the workflow is complete."""
        return self.state["current_stage"] == "complete"

    def get_full_state(self) -> Dict[str, Any]:
        """Get the complete state dictionary."""
        return self.state

    def _save_state(self) -> None:
        """Save the state to disk if a state file is specified."""
        if self.state_file:
            os.makedirs(os.path.dirname(self.state_file), exist_ok=True)
            with open(self.state_file, 'w') as f:
                json.dump(self.state, f, indent=2)