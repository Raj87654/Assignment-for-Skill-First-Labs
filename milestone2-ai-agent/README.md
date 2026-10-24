# Milestone 2: Simple AI Agent with Tools

## What This Project Does

This is a simple AI agent that answers questions using two tools:

1. **Knowledge Search** — Looks up facts about a fictional college from a JSON file.
2. **Calculator** — Performs basic arithmetic (add, subtract, multiply, divide) safely.

The agent decides which tool to use based on the user's question, runs the tool, and returns the answer.

## How It Works

### Agent Workflow

1. User asks a question.
2. The **router** analyzes the question to decide which tool to use:
   - If the question contains numbers and math operators → use the **calculator**.
   - Otherwise → use **knowledge search**.
3. The selected tool processes the question and returns the answer.
4. If the knowledge search finds no relevant data, it returns: "I don't have enough information to answer that."

### LangGraph Integration

If `langgraph` is installed, the agent uses a LangGraph StateGraph to route questions:

```
[Start] → [Router Node] → (calculator?) → [Calculator Node] → [End]
                        → (knowledge?) → [Knowledge Node] → [End]
```

- **State**: Holds the question, tool choice, math expression, and answer.
- **Router Node**: Classifies the question and picks a tool.
- **Conditional Edge**: Routes to the correct tool node.
- **Tool Nodes**: Execute the tool and update the answer in the state.

If LangGraph is not installed, the agent uses a simple Python function to do the same routing.

### Fallback Mode

When no API key is configured (which is the default), the agent runs in **fallback mode**:
- It uses rule-based keyword matching to classify questions.
- This is clearly labelled as a fallback and not a full LLM-based agent.
- The fallback mode is fully functional and testable without any external services.

## Files

- `knowledge.json` — Sample data about a fictional college.
- `tools.py` — Contains `search_knowledge()`, `calculate()`, and routing logic.
- `agent.py` — Main entry point with LangGraph workflow, sample questions, and interactive mode.

## Dependencies

- Python 3.8+
- `langgraph` (optional, for graph-based routing)
- `python-dotenv` (optional, for loading API keys)

## Installation

```bash
pip install langgraph python-dotenv
```

## How to Run

```bash
python agent.py
```

The program will:
1. Run through sample questions and show results.
2. Perform a consistency test (same question asked twice).
3. Enter interactive mode where you can type your own questions.

## Sample Questions and Expected Answers

| Question | Tool Used | Expected Answer |
|---|---|---|
| What is the placement rate? | knowledge_search | Placement Rate: 92% |
| What is 150000 * 4? | calculator | 600000 |
| Which companies are internship partners? | knowledge_search | Internship Partners: Google, Microsoft, Amazon, Infosys |
| What is 25 + 37? | calculator | 62 |
| What is the hostel fee? | knowledge_search | I don't have enough information to answer that. |
| What is 100 / 0? | calculator | Error: Division by zero is not allowed. |

## API Key (Optional)

If you want to use an LLM for smarter routing, create a `.env` file in the project root:

```
OPENAI_API_KEY=your-key-here
```

Without an API key, the agent works perfectly in fallback mode using keyword-based routing.
