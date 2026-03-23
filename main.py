#!/usr/bin/env python3
"""
Main entry point for the Agentic AI Security System.
Provides a CLI interface for secure AI interactions using LangGraph workflow.
"""

import sys
from workflow import process_input

def main():
    """
    Main function to run the CLI loop using LangGraph workflow.
    """
    print("Initializing Agentic AI Security System with LangGraph...")
    print("Loading model... (This may take a moment)")

    # The workflow will initialize components on first use
    print("System ready! Type 'quit' or 'exit' to stop.")
    print("-" * 50)

    try:
        while True:
            # Get user input
            user_input = input("You: ").strip()

            if user_input.lower() in ['quit', 'exit']:
                print("Goodbye!")
                break

            if not user_input:
                continue

            # Process through LangGraph workflow
            print("Processing input through security workflow...")
            response = process_input(user_input)
            print(response)

            print("-" * 50)

    except KeyboardInterrupt:
        print("\nGoodbye!")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()