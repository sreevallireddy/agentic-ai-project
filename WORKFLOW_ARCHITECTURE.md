# Agentic AI System - Node Architecture & Flow

## 🏗️ Complete Node Graph

### Visual Workflow
```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         AGENTIC WORKFLOW                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  START                                                                      │
│    │                                                                        │
│    ▼                                                                        │
│  ┌──────────────┐                                                          │
│  │ INPUT NODE   │  (Prepare context, load history)                        │
│  └──────┬───────┘                                                          │
│         │                                                                   │
│         ▼                                                                   │
│  ┌──────────────────────┐                                                 │
│  │ ANALYZE NODE (LLM)   │  (Understand user intent)                       │
│  └──────┬───────────────┘                                                 │
│         │                                                                   │
│         ▼                                                                   │
│  ┌──────────────────────┐                                                 │
│  │ SECURITY NODE (LLM)  │  (Detect threats)                               │
│  └──────┬───────────────┘                                                 │
│         │                                                                   │
│         ▼                                                                   │
│  ┌──────────────────────┐                                                 │
│  │VALIDATION NODE (LLM) │  (Re-confirm decision)                          │
│  └──────┬───────────────┘                                                 │
│         │                                                                   │
│         ▼                                                                   │
│  ┌──────────────────────┐                                                 │
│  │DECISION NODE (LOGIC) │  (Make final call)                              │
│  └──┬──┬────────────────┬──┐                                              │
│     │  │                │  │                                              │
│ ____|__|                |__|____                                          │
│|                                  |                                        │
│|  Conditional Routing             |                                        │
│|                                  |                                        │
│  UNSAFE?          UNCLEAR?        SAFE?                                    │
│    │                 │            │                                        │
│    ▼                 ▼            ▼                                        │
│ ┌─────────┐   ┌──────────┐  ┌──────────────┐                             │
│ │ BLOCK   │   │  RETRY   │  │  RAG NODE    │                             │
│ │ NODE    │   │  NODE    │  │  (Retrieve)  │                             │
│ └────┬────┘   └─────┬────┘  └──────┬───────┘                             │
│      │              │               │                                      │
│      │              └──────┬────────┘                                      │
│      │                     │                                               │
│      │                     ▼                                               │
│      │              ┌──────────────────┐                                  │
│      │              │ TOOL NODE        │  (Execute tools)                 │
│      │              │ (Search, Calc,   │                                  │
│      │              │  File Reader)    │                                  │
│      │              └──────┬───────────┘                                  │
│      │                     │                                               │
│      │                     ▼                                               │
│      │              ┌──────────────────────┐                              │
│      │              │ RESPONSE NODE (LLM)  │  (Generate answer)           │
│      │              │ (Store in memory)    │                              │
│      │              └──────┬───────────────┘                              │
│      │                     │                                               │
│      └─────────┬───────────┘                                              │
│              │                                                             │
│              ▼                                                             │
│            END                                                             │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
```

---

## 📊 Node Details

### 1. INPUT NODE
```python
def input_node(state: AgentState) -> AgentState:
    """
    INPUT_NODE - Preparation Phase
    
    INPUTS:
      - user_input (from API/CLI/UI)
    
    PROCESSING:
      - Load conversation history
      - Reset retry counter
      - Prepare context
    
    OUTPUTS:
      - state["history"] = formatted history
      - state["retry_count"] = 0
    
    NEXT: analyze_node
    """
```

### 2. ANALYZE NODE
```python
def analyze_node(state: AgentState) -> AgentState:
    """
    ANALYZE_NODE - LLM Understanding Phase
    
    INPUT:
      - user_input
      - history
    
    USES LLM PROMPT:
      get_analyze_prompt()
    
    PROCESSING:
      - Parse user intent
      - Extract key information
      - Identify topic/domain
    
    OUTPUT:
      - state["analysis"] = LLM analysis result
    
    NEXT: security_node
    """
```

### 3. SECURITY NODE
```python
def security_node(state: AgentState) -> AgentState:
    """
    SECURITY_NODE - Threat Detection Phase
    
    INPUT:
      - user_input
      - analysis (from Analyze Node)
      - history
    
    USES LLM PROMPT:
      get_detection_prompt()
    
    PROCESSING:
      - LLM detects threats looking for:
        * Prompt injection patterns
        * Indirect manipulation
        * Data extraction attempts
        * Corruption attempts
    
    OUTPUT:
      - state["detection"] = LLM classification
        (e.g., "unsafe: prompt injection" or "safe")
    
    NEXT: validation_node
    """
```

### 4. VALIDATION NODE
```python
def validation_node(state: AgentState) -> AgentState:
    """
    VALIDATION_NODE - Decision Confirmation Phase
    
    INPUT:
      - user_input
      - analysis
      - detection (from Security Node)
      - history
    
    USES LLM PROMPT:
      get_validation_prompt()
    
    PROCESSING:
      - Independent LLM review
      - Confirms or corrects detection
      - Ensures consistency
    
    OUTPUT:
      - state["validation"] = LLM confirmation
    
    NEXT: decision_node
    """
```

### 5. DECISION NODE
```python
def decision_node(state: AgentState) -> AgentState:
    """
    DECISION_NODE - Logical Decision Making
    
    INPUT:
      - detection (from Security Node)
      - validation (from Validation Node)
    
    PROCESSING - LOGIC DECISION:
      If (detection_threat AND validation_threat):
        classification = "unsafe: [category]"
        is_safe = False
      Elif (NOT detection_threat AND NOT validation_threat):
        classification = "safe"
        is_safe = True
      Else:
        classification = "unclear"
        is_safe = True  # treat as safe
    
    OUTPUT:
      - state["classification"] = final category
      - state["is_safe"] = boolean decision
    
    CONDITIONAL ROUTING:
      - If unsafe → block_node
      - If unclear → retry_node
      - If safe → rag_node
    """
```

### 6. RAG NODE
```python
def rag_node(state: AgentState) -> AgentState:
    """
    RAG_NODE - Document Retrieval Phase
    
    INPUT:
      - user_input
    
    PROCESSING:
      - FAISS similarity search
      - Retrieve top-3 documents
      - Format context for response
    
    OUTPUT:
      - state["rag_context"] = retrieved documents
    
    NEXT: tool_node
    """
```

### 7. TOOL NODE
```python
def tool_node(state: AgentState) -> AgentState:
    """
    TOOL_NODE - Tool Execution Phase
    
    INPUT:
      - user_input
      - analysis
    
    PROCESSING:
      - Check if SearchTool needed
        → Execute if keyword matched
      - Check if CalculatorTool needed
        → Execute if math expression present
      - Check if FileReaderTool needed
        → Execute if file operation detected
    
    OUTPUT:
      - state["tool_results"] = tool output
    
    NEXT: response_node
    """
```

### 8. RESPONSE NODE
```python
def response_node(state: AgentState) -> AgentState:
    """
    RESPONSE_NODE - Answer Generation Phase
    
    INPUT:
      - user_input
      - analysis
      - rag_context (from RAG Node)
      - tool_results (from Tool Node)
      - history
    
    USES LLM PROMPT:
      get_response_generation_prompt()
    
    PROCESSING:
      - LLM generates response using:
        * Original user question
        * Analysis results
        * Retrieved RAG documents
        * Tool execution results
        * Conversation history
      - Store interaction in memory
    
    OUTPUT:
      - state["response"] = final AI response
    
    EFFECTS:
      - Stores interaction in memory
    
    NEXT: END
    """
```

### 9. BLOCK NODE
```python
def block_node(state: AgentState) -> AgentState:
    """
    BLOCK_NODE - Safety Enforcement
    
    INPUT:
      - classification (shows unsafe threat)
    
    PROCESSING:
      - Generate security warning
      - Explain blocking reason
    
    OUTPUT:
      - state["response"] = "[BLOCKED] Input was flagged as..."
    
    NEXT: END
    """
```

### 10. RETRY NODE
```python
def retry_node(state: AgentState) -> AgentState:
    """
    RETRY_NODE - Unclear Handling
    
    INPUT:
      - retry_count
      - classification (unclear)
    
    PROCESSING:
      If retry_count < 2:
        - Reset detection and validation
        - Increment retry counter
      Else:
        - Give up retrying
        - Treat as safe
        - Mark as "safe (after retry)"
    
    OUTPUT:
      - Updated state for retry
    
    NEXT: 
      - If retry_count < 2: security_node (loop back)
      - Else: rag_node (continue)
    """
```

---

## 🔄 Conditional Routing Logic

### Function: `should_block(state)`

```python
def should_block(state: AgentState) -> str:
    """Determines which path to take"""
    
    is_safe = state["is_safe"]
    classification = state.get("classification", "").lower()
    
    # Three possible returns:
    
    # 1. BLOCK PATH - For unsafe inputs
    if not is_safe and classification.startswith("unsafe"):
        return "block"  → block_node
    
    # 2. RETRY PATH - For unclear (first 2 times)
    elif "unclear" in classification and retry_count < 2:
        return "retry"  → retry_node
    
    # 3. PROCEED PATH - For safe inputs
    else:
        return "proceed"  → rag_node
```

---

## 📈 State Evolution

### State Progression Through Nodes

```
START STATE:
{
  "user_input": "What is the capital of France?",
  "history": "Previous conversation...",
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

AFTER INPUT_NODE:
{
  ...same...
  "history": "loaded from memory"
  "retry_count": 0
}

AFTER ANALYZE_NODE:
{
  ...same...
  "analysis": "User asking for geographical information"
}

AFTER SECURITY_NODE:
{
  ...same...
  "detection": "safe"
}

AFTER VALIDATION_NODE:
{
  ...same...
  "validation": "safe"
}

AFTER DECISION_NODE:
{
  ...same...
  "classification": "safe",
  "is_safe": True
}

AFTER RAG_NODE:
{
  ...same...
  "rag_context": "France is a country in Europe...\nParis is the capital..."
}

AFTER TOOL_NODE:
{
  ...same...
  "tool_results": ""  (no tools needed)
}

AFTER RESPONSE_NODE:
{
  ...same...
  "response": "The capital of France is Paris..."
}

FINAL OUTPUT: state["response"]
```

---

## 🎯 Key Routing Decisions

### Decision Matrix

| Condition | Classification | is_safe | Route | Node |
|-----------|-----------------|---------|-------|------|
| Threat detected (both) | `unsafe: *` | false | BLOCK | block_node |
| Both safe | `safe` | true | PROCEED | rag_node |
| Disagreement (1st) | `unclear` | true | RETRY | retry_node |
| Disagreement (2nd) | `unclear` | true | PROCEED | rag_node |

---

## 🔗 Edge Definitions

### All Edges in Graph

```python
# Sequential edges
add_edge(START, "input")
add_edge("input", "analyze")
add_edge("analyze", "security")
add_edge("security", "validation")
add_edge("validation", "decision")

# Conditional edge (routing)
add_conditional_edges(
    "decision",
    should_block,  # routing function
    {
        "block": "block",
        "retry": "retry",
        "proceed": "rag"
    }
)

# Retry loop
add_edge("retry", "security")  # Go back for another try

# Processing pipeline
add_edge("rag", "tool")
add_edge("tool", "response")

# Terminal edges
add_edge("block", END)
add_edge("response", END)
```

---

## 📊 Traversal Examples

### Example 1: Safe Query
```
START → input → analyze → security → validation → decision
                                        ↓
                                    (routing: safe)
                                        ↓
                                  rag → tool → response → END
```

### Example 2: Unsafe Query
```
START → input → analyze → security → validation → decision
                                        ↓
                                   (routing: unsafe)
                                        ↓
                                      block → END
```

### Example 3: Unclear (Retry)
```
START → input → analyze → security → validation → decision
                                        ↓
                                   (routing: unclear)
                                        ↓
                                      retry → security (LOOP)
                          ↓
                    (if retry_count < 2, go back)
                    (if retry_count >= 2, proceed)
```

---

**Total Nodes**: 10  
**Total Edges**: 13  
**Conditional Nodes**: 2 (decision, retry)  
**LLM Nodes**: 4 (analyze, security, validation, response)  
**Logic Nodes**: 3 (decision, tool, rag)  
**Handler Nodes**: 2 (block, retry)  
**Special Nodes**: 1 (input)
