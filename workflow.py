"""
Workflow module using LangGraph for the Agentic AI Security System.
Defines the graph with nodes and edges for processing user inputs.
"""

from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from llm.model import LLMModel
from security.detector import SecurityDetector
from utils.prompts import get_response_generation_prompt

# Define the state
class AgentState(TypedDict):
    user_input: str
    is_safe: bool
    classification: str
    response: str

# Initialize shared components (loaded only once)
_llm_model = None
_detector = None

def get_components():
    """Get or initialize the LLM model and detector (lazy loading)."""
    global _llm_model, _detector
    if _llm_model is None:
        _llm_model = LLMModel()
        _detector = SecurityDetector(_llm_model)
    return _llm_model, _detector

# Node functions
def security_check(state: AgentState) -> AgentState:
    """Node to perform security classification."""
    llm_model, detector = get_components()
    user_input = state["user_input"]
    is_safe = detector.is_safe(user_input)
    classification = detector.get_classification(user_input)
    return {
        **state,
        "is_safe": is_safe,
        "classification": classification
    }

def generate_response(state: AgentState) -> AgentState:
    """Node to generate AI response for safe inputs."""
    llm_model, detector = get_components()
    user_input = state["user_input"]
    prompt = get_response_generation_prompt(user_input)
    response = llm_model.generate_response(prompt)
    
    # Format response with security status
    formatted_response = f"✅ **Safe** - No security threats detected\n\n{response}"
    
    return {
        **state,
        "response": formatted_response
    }

def security_response(state: AgentState) -> AgentState:
    """Node to generate security warning for unsafe inputs."""
    classification = state["classification"]
    warning = f"⚠️ **Security Alert** - {classification.upper()}\n\nI cannot process this request due to detected security threats. Please rephrase your question to ensure it doesn't contain:\n- Prompt injection attempts\n- Data extraction requests\n- Unauthorized instructions"
    return {
        **state,
        "response": warning
    }

# Create the graph
def create_workflow():
    """Create and compile the LangGraph workflow."""
    workflow = StateGraph(AgentState)

    # Add nodes
    workflow.add_node("security_check", security_check)
    workflow.add_node("generate_response", generate_response)
    workflow.add_node("security_response", security_response)

    # Add edges
    workflow.add_edge(START, "security_check")

    # Conditional edges based on safety
    workflow.add_conditional_edges(
        "security_check",
        lambda state: "safe" if state["is_safe"] else "unsafe",
        {
            "safe": "generate_response",
            "unsafe": "security_response"
        }
    )

    workflow.add_edge("generate_response", END)
    workflow.add_edge("security_response", END)

    return workflow.compile()

# Global workflow instance (created once)
_agent_workflow = None

def get_workflow():
    """Get the compiled workflow, initializing if necessary."""
    global _agent_workflow
    if _agent_workflow is None:
        _agent_workflow = create_workflow()
    return _agent_workflow

def process_input(user_input: str) -> str:
    """
    Process user input through the workflow.

    Args:
        user_input (str): The user's input text.

    Returns:
        str: The final response.
    """
    workflow = get_workflow()
    initial_state = AgentState(
        user_input=user_input,
        is_safe=False,
        classification="",
        response=""
    )
    final_state = workflow.invoke(initial_state)
    return final_state["response"]