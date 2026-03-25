"""
Complete LangGraph workflow for the Agentic AI Security System.
Defines nodes, edges, and the complete agentic workflow.
"""

from typing import TypedDict, List
from langgraph.graph import StateGraph, START, END
from llm.model import LLMModel
from security.detector import SecurityDetector
from rag.loader import DocumentLoader, split_text
from rag.vector_store import FAISSVectorStore
from tools.search import SearchTool
from tools.calculator import CalculatorTool
from tools.file_reader import FileReaderTool
from memory.memory import ConversationMemory
from utils.prompts import (
    get_analyze_prompt,
    get_detection_prompt,
    get_validation_prompt,
    get_rag_context_prompt,
    get_response_generation_prompt,
    get_tool_decision_prompt
)


# Define the state
class AgentState(TypedDict):
    """State object for the LangGraph workflow."""
    user_input: str
    history: str
    analysis: str
    detection: str
    validation: str
    is_safe: bool
    classification: str
    rag_context: str
    tool_results: str
    response: str
    retry_count: int


# Global components
class AgentComponents:
    """Singleton for shared components."""
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        print("Initializing Agent Components...")
        self.llm_model = LLMModel()
        self.detector = SecurityDetector(self.llm_model)
        self.memory = ConversationMemory(max_history=5)
        
        # Initialize RAG components
        self.vector_store = FAISSVectorStore(embeddings_model=None)
        self._load_documents()
        
        self._initialized = True
    
    def _load_documents(self):
        """Load documents for RAG."""
        try:
            loader = DocumentLoader()
            docs = loader.load_documents("./docs")
            if docs:
                for doc in docs:
                    chunks = split_text(doc["content"])
                    for chunk in chunks:
                        self.vector_store.add_documents([{"content": chunk}])
        except Exception as e:
            print(f"Note: Could not load documents: {str(e)}")


def get_components() -> AgentComponents:
    """Get or initialize shared components."""
    return AgentComponents()


# Node functions
def input_node(state: AgentState) -> AgentState:
    """Input Node: Accept and prepare user input."""
    state["retry_count"] = 0
    history = get_components().memory.get_context()
    state["history"] = history
    return state


def analyze_node(state: AgentState) -> AgentState:
    """Analyze Node: Understand user input intent."""
    components = get_components()
    user_input = state["user_input"]
    history = state["history"]
    
    prompt = get_analyze_prompt(user_input, history)
    analysis = components.llm_model.generate_response(prompt)
    
    return {
        **state,
        "analysis": analysis
    }


def security_node(state: AgentState) -> AgentState:
    """Security Node: Detect threats using LLM classification."""
    components = get_components()
    user_input = state["user_input"]
    analysis = state["analysis"]
    history = state["history"]
    
    prompt = get_detection_prompt(user_input, analysis, history)
    detection = components.llm_model.generate_response(prompt)
    
    return {
        **state,
        "detection": detection
    }


def validation_node(state: AgentState) -> AgentState:
    """Validation Node: Re-check security decision."""
    components = get_components()
    user_input = state["user_input"]
    analysis = state["analysis"]
    detection = state["detection"]
    history = state["history"]
    
    prompt = get_validation_prompt(user_input, analysis, detection, history)
    validation = components.llm_model.generate_response(prompt)
    
    return {
        **state,
        "validation": validation
    }


def decision_node(state: AgentState) -> AgentState:
    """Decision Node: Make final security decision (logic-based)."""
    detection = state["detection"].strip().lower()
    validation = state["validation"].strip().lower()
    
    # Check for threat keywords
    threat_keywords = ["prompt injection", "indirect prompt injection", "data leakage", "data poisoning"]
    
    detection_threat = any(keyword in detection for keyword in threat_keywords)
    validation_threat = any(keyword in validation for keyword in threat_keywords)
    
    # Both agree on threat = unsafe
    if detection_threat and validation_threat:
        for keyword in threat_keywords:
            if keyword in detection or keyword in validation:
                classification = f"unsafe: {keyword}"
                break
        else:
            classification = "unsafe: unknown"
        is_safe = False
    # Both agree it's safe = safe
    elif not detection_threat and not validation_threat:
        classification = "safe"
        is_safe = True
    # Disagreement = unclear (retry or proceed cautiously)
    else:
        classification = "unclear"
        is_safe = True  # Treat as safe for now
    
    return {
        **state,
        "classification": classification,
        "is_safe": is_safe
    }


def rag_node(state: AgentState) -> AgentState:
    """RAG Node: Retrieve relevant documents from vector store."""
    components = get_components()
    user_input = state["user_input"]
    
    # Get similar documents
    results = components.vector_store.similarity_search(user_input, k=3)
    
    if results:
        context_parts = [result[0] for result in results]
        rag_context = "\n\n".join(context_parts)
    else:
        rag_context = "No relevant documents found in knowledge base."
    
    return {
        **state,
        "rag_context": rag_context
    }


def tool_node(state: AgentState) -> AgentState:
    """Tool Node: Decide and execute needed tools."""
    user_input = state["user_input"]
    analysis = state["analysis"]
    
    tool_results = []
    
    # Check if search is needed
    if SearchTool.is_search_needed(user_input):
        search_results = SearchTool.search(user_input, num_results=3)
        tool_results.append(f"Search results:\n" + "\n".join(search_results))
    
    # Check if calculator is needed
    if CalculatorTool.is_calculation_needed(user_input):
        # Extract expression (simple heuristic)
        import re
        expr_match = re.search(r'[\d\+\-\*/\(\)\.]', user_input)
        if expr_match:
            calc_result = CalculatorTool.calculate(user_input)
            tool_results.append(f"Calculation result: {calc_result}")
    
    # Check if file reading is needed
    if FileReaderTool.is_file_read_needed(user_input):
        # Extract filename (simple heuristic)
        words = user_input.split()
        for word in words:
            if word.endswith(('.txt', '.py', '.json', '.md')):
                content = FileReaderTool.read_file(word)
                tool_results.append(f"File content:\n{content}")
                break
    
    tool_output = "\n".join(tool_results) if tool_results else ""
    
    return {
        **state,
        "tool_results": tool_output
    }


def response_node(state: AgentState) -> AgentState:
    """Response Node: Generate final response using LLM."""
    components = get_components()
    user_input = state["user_input"]
    analysis = state["analysis"]
    rag_context = state["rag_context"]
    tool_results = state["tool_results"]
    history = state["history"]
    
    prompt = get_response_generation_prompt(
        user_input,
        analysis,
        rag_context,
        tool_results,
        history
    )
    
    response = components.llm_model.generate_response(prompt)
    
    # Store in memory
    components.memory.add_interaction(user_input, response)
    
    return {
        **state,
        "response": response
    }


def block_node(state: AgentState) -> AgentState:
    """Block unsafe input."""
    classification = state["classification"]
    state["response"] = f"[BLOCKED] This input was flagged as potentially unsafe ({classification}). Please rephrase your question."
    return state


def retry_node(state: AgentState) -> AgentState:
    """Retry unclear classification."""
    state["retry_count"] = state.get("retry_count", 0) + 1
    if state["retry_count"] < 2:
        # Reset detection and validation
        state["detection"] = ""
        state["validation"] = ""
        return state
    else:
        # After max retries, treat as safe
        state["is_safe"] = True
        state["classification"] = "safe (after retry)"
        return state


def should_block(state: AgentState) -> str:
    """Determine if input should be blocked."""
    is_safe = state["is_safe"]
    classification = state.get("classification", "").lower()
    
    if not is_safe and classification.startswith("unsafe"):
        return "block"
    elif "unclear" in classification and state.get("retry_count", 0) < 2:
        return "retry"
    else:
        return "proceed"


# Build the graph
def build_workflow() -> StateGraph:
    """Build and return the LangGraph workflow."""
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("input", input_node)
    workflow.add_node("analyze", analyze_node)
    workflow.add_node("security", security_node)
    workflow.add_node("validation", validation_node)
    workflow.add_node("decision", decision_node)
    workflow.add_node("rag", rag_node)
    workflow.add_node("tool", tool_node)
    workflow.add_node("response", response_node)
    workflow.add_node("block", block_node)
    workflow.add_node("retry", retry_node)
    
    # Add edges
    workflow.add_edge(START, "input")
    workflow.add_edge("input", "analyze")
    workflow.add_edge("analyze", "security")
    workflow.add_edge("security", "validation")
    workflow.add_edge("validation", "decision")
    
    # Conditional edge based on safety decision
    workflow.add_conditional_edges(
        "decision",
        should_block,
        {
            "block": "block",
            "retry": "retry",
            "proceed": "rag"
        }
    )
    
    workflow.add_edge("retry", "security")  # Retry goes back to security node
    
    workflow.add_edge("rag", "tool")
    workflow.add_edge("tool", "response")
    workflow.add_edge("block", END)
    workflow.add_edge("response", END)
    
    return workflow


# Create global workflow instance
_workflow_instance = None


def get_workflow():
    """Get or create the workflow instance."""
    global _workflow_instance
    if _workflow_instance is None:
        _workflow_instance = build_workflow().compile()
    return _workflow_instance


def process_input(user_input: str) -> str:
    """
    Process user input through the entire workflow.
    
    Args:
        user_input (str): User's input text.
    
    Returns:
        str: The final response.
    """
    workflow = get_workflow()
    
    # Initial state
    initial_state = {
        "user_input": user_input,
        "history": "",
        "analysis": "",
        "detection": "",
        "validation": "",
        "is_safe": True,
        "classification": "",
        "rag_context": "",
        "tool_results": "",
        "response": "",
        "retry_count": 0
    }
    
    # Execute workflow
    result = workflow.invoke(initial_state)
    
    return result["response"]