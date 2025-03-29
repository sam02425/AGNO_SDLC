"""
Main entry point for the AI-driven software development workflow application.
"""
import os
import json
import argparse
from dotenv import load_dotenv

from workflow.sdlc_workflow import SDLCWorkflow
from ui.playground import create_playground_app, serve_playground

# Load environment variables
load_dotenv()

def run_workflow(requirements_text):
    """Run the complete SDLC workflow with the given requirements"""
    workflow = SDLCWorkflow()
    result = workflow.run_workflow(requirements_text)
    return result

def run_playground():
    """Launch the interactive playground"""
    app = create_playground_app()
    serve_playground(app)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AI-Driven SDLC Application")
    parser.add_argument("--playground", action="store_true", help="Launch the playground interface")
    parser.add_argument("--requirements", type=str, help="Requirements text to start workflow")
    parser.add_argument("--output", type=str, help="Output file for workflow results")

    args = parser.parse_args()

    if args.playground:
        run_playground()
    elif args.requirements:
        result = run_workflow(args.requirements)

        if args.output:
            with open(args.output, 'w') as f:
                json.dump(result, f, indent=2)
        else:
            print(json.dumps(result, indent=2))
    else:
        parser.print_help()