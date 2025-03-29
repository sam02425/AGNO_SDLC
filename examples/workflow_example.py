"""
Example of running the complete SDLC workflow.
"""
import json
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from workflow.sdlc_workflow import SDLCWorkflow

# Example requirements
requirements_text = """
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

if __name__ == "__main__":
    # Create and run the workflow
    workflow = SDLCWorkflow()
    result = workflow.run_workflow(requirements_text)

    # Print the final state
    print(json.dumps(result, indent=2))