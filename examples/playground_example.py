"""
Example of running the playground application.
"""
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ui.playground import create_playground_app, serve_playground

if __name__ == "__main__":
    # Create and serve the playground
    app = create_playground_app()
    serve_playground(app)