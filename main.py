#!/usr/bin/env python3
"""
Main CLI entry point for the Agentic AI Security System.
Provides a command-line interface for secure AI interactions using LangGraph workflow.
"""

import sys
from workflow import process_input


def main():
    """
    Main function to run the CLI interface using LangGraph workflow.
    
    Features:
    - Input processing through complete agentic workflow
    - Security analysis with multi-step validation
    - RAG-based context retrieval
    - Tool integration (search, calculator, file reader)
    - Conversation memory management
    """
    print("=" * 60)
    print("     AGENTIC AI SECURITY SYSTEM - CLI Interface")
    print("=" * 60)
    print("\nInitializing Agentic AI Security System with LangGraph...")
    print("Loading LLM model and supporting components...")
    print("(This may take a moment on first run)")
    print()

    try:
        print("System ready! Type 'quit' or 'exit' to exit.")
        print("The system uses an agentic workflow with:")
        print("  • Analyze Node - Input understanding")
        print("  • Security Node - Threat detection")
        print("  • Validation Node - Decision confirmation")
        print("  • RAG Node - Context retrieval")
        print("  • Tool Node - Tool integration")
        print("  • Response Node - Answer generation")
        print("-" * 60)
        print()

        while True:
            # Get user input
            user_input = input("You: ").strip()

            if user_input.lower() in ['quit', 'exit']:
                print("\nGoodbye! Thank you for using Agentic AI Security System.")
                break

            if not user_input:
                continue

            # Process through LangGraph workflow
            print("\nProcessing through agentic workflow...")
            print("  → Analyzing input")
            print("  → Checking security")
            print("  → Validating decision")
            print("  → Retrieving context (RAG)")
            print("  → Executing tools if needed")
            print("  → Generating response")
            print()

            response = process_input(user_input)
            print(f"Assistant: {response}\n")
            print("-" * 60)
            print()

    except KeyboardInterrupt:
        print("\n\nInterrupted by user. Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\nAn error occurred: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
