# Skill First Labs Assignment

## Milestone 1: CSS Parser

Reads a CSS file and extracts selectors, property names, and values into structured Python dictionaries and JSON. Uses the `tinycss2` library for parsing.

See [milestone1-css-parser/README.md](milestone1-css-parser/README.md) for details.

## Milestone 2: Simple AI Agent with Tools

A command-line AI agent that routes questions to the appropriate tool:
- **Knowledge Search** — Looks up facts from a JSON knowledge base.
- **Calculator** — Performs safe arithmetic operations.

Uses LangGraph for workflow routing (with a simple Python fallback).

See [milestone2-ai-agent/README.md](milestone2-ai-agent/README.md) for details.

## Dependencies

| Package | Purpose |
|---|---|
| `tinycss2` | CSS parsing library |
| `langgraph` | Graph-based workflow routing |
| `python-dotenv` | Load environment variables from `.env` |

## Project Structure

```
skill-first-labs-assignment/
├── milestone1-css-parser/       # Project 1: CSS Parser
│   ├── css_parser.py            # Main parser program
│   ├── sample.css               # Sample CSS input file
│   └── README.md                # Project documentation
├── milestone2-ai-agent/         # Project 2: Simple AI Agent
│   ├── agent.py                 # Main agent program
│   ├── tools.py                 # Tool functions (search, calculate)
│   ├── knowledge.json           # Knowledge base (fictional college data)
│   └── README.md                # Project documentation
├── tests/                       # Automated test cases
│   ├── test_css_parser.py       # Tests for the CSS parser
│   └── test_ai_agent.py         # Tests for the AI agent
├── requirements.txt             # Python dependencies
├── .gitignore                   # Git ignore rules
└── README.md                    # This file
```

## Quick Start

### 1. Create a Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate       # Windows
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the CSS Parser

```bash
cd milestone1-css-parser
python css_parser.py
```

### 4. Run the AI Agent

```bash
cd milestone2-ai-agent
python agent.py
```

### 5. Run All Tests

```bash
python -m pytest tests/ -v
```

Or using unittest:

```bash
python -m unittest discover -s tests -v
```


## Author
Rajkumar M
