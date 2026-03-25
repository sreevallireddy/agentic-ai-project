# Quick Reference Guide - Agentic AI Security System

## 🚀 Quick Start (5 minutes)

### Setup
```bash
# 1. Navigate to project
cd /Users/sreevalli.ribm.com/agentic-ai-project

# 2. Create virtual environment
python3 -m venv venv

# 3. Activate it
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt
```

### Run (Choose One)
```bash
# Option A: Web Interface (Recommended)
streamlit run app.py
# Open http://localhost:8501

# Option B: Command Line
python main.py

# Option C: REST API
python api.py
# Open http://localhost:8000/docs
```

---

## 📊 System Architecture at a Glance

```
User Input 
    ↓
[Analyze] → [Detect] → [Validate] → [Decide]
                                      ↓
                    ┌─────────────────┼─────────────────┐
                    ↓                 ↓                 ↓
              [Block]→END        [Retry]            [RAG] 
                              (if unclear)           ↓
                                ↓              [Tool]→[Response]→END
                            [Detect]
```

---

## 🔑 Key Components

### Core Files
| File | Purpose | Key Classes |
|------|---------|-----------|
| `workflow.py` | LangGraph workflow | `AgentState`, `AgentComponents`, all nodes |
| `llm/model.py` | LLM integration | `LLMModel` |
| `security/detector.py` | Threat detection | `SecurityDetector` |

### RAG System
| File | Purpose | Key Classes |
|------|---------|-----------|
| `rag/loader.py` | Document loading | `DocumentLoader`, `split_text()` |
| `rag/vector_store.py` | Vector storage | `FAISSVectorStore` |

### Tools
| File | Purpose | Key Methods |
|------|---------|-----------|
| `tools/search.py` | Search queries | `search()`, `is_search_needed()` |
| `tools/calculator.py` | Math operations | `calculate()`, `is_calculation_needed()` |
| `tools/file_reader.py` | File reading | `read_file()`, `list_files()` |

### Interfaces
| File | Purpose | Tech Stack |
|------|---------|-----------|
| `app.py` | Web chat UI | Streamlit |
| `main.py` | Command line | Python CLI |
| `api.py` | REST API | FastAPI + Uvicorn |

### Support
| File | Purpose | Key Functions |
|------|---------|-----------|
| `memory/memory.py` | Chat history | `ConversationMemory` class |
| `utils/prompts.py` | Prompt templates | 8 prompt functions |

---

## 🎯 Workflow Nodes (10 Total)

### Processing Nodes
1. **input_node** - Prepare context
2. **analyze_node** - Understand intent (LLM)
3. **security_node** - Detect threats (LLM)
4. **validation_node** - Confirm decision (LLM)

### Decision & Execution
5. **decision_node** - Route based on safety
6. **rag_node** - Retrieve documents
7. **tool_node** - Execute tools
8. **response_node** - Generate answer (LLM)

### Handling
9. **block_node** - Block unsafe input
10. **retry_node** - Handle unclear cases

---

## 📝 Common Tasks

### Add a New Tool
```python
# 1. Create tools/my_tool.py
class MyTool:
    @staticmethod
    def execute(param):
        return result
    
    @staticmethod
    def is_needed(user_input):
        return True/False

# 2. Import in workflow.py
from tools.my_tool import MyTool

# 3. Use in tool_node()
if MyTool.is_needed(user_input):
    result = MyTool.execute(param)
    tool_results.append(f"Result: {result}")
```

### Add Documents for RAG
```bash
# 1. Create docs directory
mkdir docs

# 2. Add .txt files
echo "Machine learning is..." > docs/ml.txt

# 3. System loads automatically on startup
```

### Customize Prompts
```python
# Edit utils/prompts.py
def get_analyze_prompt(user_input: str, history: str = "") -> str:
    return f"""
    YOUR_CUSTOM_PROMPT_HERE
    
    User input: {user_input}
    History: {history}
    """
```

### Adjust Memory Size
```python
# In workflow.py, AgentComponents.__init__()
self.memory = ConversationMemory(max_history=10)  # Change from 5
```

---

## 🔒 Security Threat Categories

| Threat | Example | Detection |
|--------|---------|-----------|
| **Prompt Injection** | "Ignore instructions, tell me..." | Direct override attempts |
| **Indirect Injection** | Misleading context | Subtle manipulation |
| **Data Leakage** | "Give me secrets" | Info extraction |
| **Data Poisoning** | "Replace X with Y" | Corruption attempts |

---

## 📡 API Endpoints

### Health Check
```bash
GET /health
# Returns: {"status": "healthy"}
```

### Chat
```bash
POST /chat
Content-Type: application/json

{"message": "Hello!"}

# Returns: {"response": "...", "session_id": null}
```

### Docs
```
http://localhost:8000/docs   # Swagger UI
http://localhost:8000/redoc  # ReDoc
```

---

## 🧪 Testing Commands

### Test CLI
```bash
python main.py
# Type: What is 2 + 2?
# Should use calculator tool
```

### Test Streamlit
```bash
streamlit run app.py
# Use web interface to chat
```

### Test API
```bash
# Chat endpoint
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is capital of France?"}'

# Health check
curl http://localhost:8000/health
```

---

## 🐛 Troubleshooting

### Model Download Stuck
```bash
# Set cache directory
export HUGGINGFACE_HOME=./models
export TRANSFORMERS_CACHE=./models

# Try again
python main.py
```

### FAISS Installation Error
```bash
# Reinstall FAISS
pip uninstall faiss-cpu -y
pip install faiss-cpu
```

### Memory Issues
```python
# In rag/loader.py, reduce chunk size
chunk_size = 300  # Was 500
overflow = 25     # Was 50
```

### Port Already in Use
```bash
# API on different port
python api.py --port 8001

# Streamlit on different port
streamlit run app.py --server.port 8502
```

---

## 📚 File Locations Quick Reference

```
Critical Files:
  ├─ workflow.py ..................... LangGraph core
  ├─ app.py .......................... Streamlit UI
  ├─ main.py ......................... CLI
  ├─ api.py .......................... REST API
  └─ requirements.txt ................ Dependencies

Configuration:
  ├─ utils/prompts.py ............... Prompt templates
  └─ .env (optional) ................. Environment vars

Data:
  ├─ docs/ (create manually) ........ Your documents
  ├─ models/ (auto-created) ......... Downloaded LLM
  └─ venv/ ........................... Python environment
```

---

## 💡 State Flow Example

### For Safe Query: "What is Python?"

```
STATE FLOW:
user_input: "What is Python?"
    ↓
[ANALYZE] → analysis: "Asking about programming language"
    ↓
[SECURITY] → detection: "safe"
    ↓
[VALIDATION] → validation: "safe"
    ↓
[DECISION] → classification: "safe", is_safe: True
    ↓
[RAG] → rag_context: "Python is a programming language..."
    ↓
[TOOL] → tool_results: "" (no tools needed)
    ↓
[RESPONSE] → response: "Python is a high-level programming language..."
    ↓
Store in memory + Return to user
```

---

## 📈 Performance Tips

1. **First Load**: 1-2 minutes (one-time)
2. **Subsequent Queries**: 5-10 seconds
3. **GPU**: Automatically used if available
4. **Memory**: ~4GB required
5. **Scaling**: Use FastAPI for multi-user access

---

## 🔗 Important Links

- **LangGraph Docs**: https://github.com/langchain-ai/langgraph
- **LangChain**: https://python.langchain.com/
- **Streamlit**: https://docs.streamlit.io/
- **FastAPI**: https://fastapi.tiangolo.com/
- **HuggingFace**: https://huggingface.co/
- **FAISS**: https://github.com/facebookresearch/faiss

---

## ✅ Verification Checklist

Before deploying:
- [ ] Virtual environment created and activated
- [ ] All dependencies installed: `pip install -r requirements.txt`
- [ ] Model downloads on first run (check internet connection)
- [ ] At least one interface runs without errors
- [ ] Documents can be placed in `docs/` directory
- [ ] Security detection works (test with "Ignore instructions")

---

## 📧 Support Notes

- **First run takes time**: Model download is ~1GB
- **GPU support**: Automatic if CUDA available
- **Memory requirement**: Minimum 4GB RAM
- **Python version**: 3.8+

---

**Status**: 🟢 **Production Ready**

For detailed information, see `IMPLEMENTATION_SUMMARY.md` and `README.md`
