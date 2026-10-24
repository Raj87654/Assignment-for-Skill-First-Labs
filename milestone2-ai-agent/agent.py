import os
import sys

try:
    from langgraph.graph import StateGraph, END
    from typing import TypedDict
    LANGGRAPH_AVAILABLE = True
except ImportError:
    LANGGRAPH_AVAILABLE = False

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tools import (
    load_knowledge,
    search_knowledge,
    calculate,
    classify_question,
    extract_math_expression,
    run_agent,
)


LLM_MODE = False
try:
    from dotenv import load_dotenv
    load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env"))
    api_key = os.environ.get("OPENAI_API_KEY", "")
    if api_key and api_key.strip():
        LLM_MODE = True
except ImportError:
    pass


def build_langgraph_agent(knowledge_data):

    class AgentState(TypedDict):
        question: str
        tool_choice: str
        expression: str
        answer: str

    def router_node(state):
        tool = classify_question(state["question"])
        expression = ""
        if tool == "calculator":
            expression = extract_math_expression(state["question"]) or ""
        return {"tool_choice": tool, "expression": expression}

    def knowledge_node(state):
        result = search_knowledge(state["question"], knowledge_data)
        if result:
            return {"answer": result}
        return {"answer": "I don't have enough information to answer that."}

    def calculator_node(state):
        expression = state.get("expression", "")
        if not expression:
            return {"answer": "Error: Could not extract a valid math expression from your question."}
        result = calculate(expression)
        return {"answer": result}

    def route_decision(state):
        if state["tool_choice"] == "calculator":
            return "calculator"
        return "knowledge"

    graph = StateGraph(AgentState)
    graph.add_node("router", router_node)
    graph.add_node("knowledge", knowledge_node)
    graph.add_node("calculator", calculator_node)

    graph.set_entry_point("router")
    graph.add_conditional_edges("router", route_decision, {
        "calculator": "calculator",
        "knowledge": "knowledge",
    })
    graph.add_edge("knowledge", END)
    graph.add_edge("calculator", END)

    return graph.compile()


def ask_agent(question, knowledge_data=None, agent_app=None):
    if knowledge_data is None:
        knowledge_data = load_knowledge()

    if LANGGRAPH_AVAILABLE and agent_app is not None:
        result = agent_app.invoke({
            "question": question,
            "tool_choice": "",
            "expression": "",
            "answer": "",
        })
        return {
            "question": question,
            "tool_used": result["tool_choice"] + ("_search" if result["tool_choice"] == "knowledge" else ""),
            "answer": result["answer"],
        }

    return run_agent(question, knowledge_data)


def main():
    knowledge_data = load_knowledge()

    if LANGGRAPH_AVAILABLE:
        print("=" * 60)
        print("AI AGENT (LangGraph Mode - Fallback / No LLM)")
        print("=" * 60)
        print("Using LangGraph for workflow routing.")
        if not LLM_MODE:
            print("No API key found. Running in FALLBACK mode.")
            print("(This uses rule-based routing, not an LLM.)")
        print()
        agent_app = build_langgraph_agent(knowledge_data)
    else:
        print("=" * 60)
        print("AI AGENT (Simple Python Mode - Fallback / No LLM)")
        print("=" * 60)
        print("LangGraph not installed. Using simple Python routing.")
        print("(This uses rule-based routing, not an LLM.)")
        print()
        agent_app = None

    sample_questions = [
        "What is the placement rate?",
        "What is 150000 * 4?",
        "Which companies are internship partners?",
        "What is 25 + 37?",
        "What is the hostel fee?",
        "What is 100 / 0?",
        "What is the location of the college?",
        "What programs are offered?",
    ]

    for question in sample_questions:
        result = ask_agent(question, knowledge_data, agent_app)
        print(f"Q: {result['question']}")
        print(f"Tool: {result['tool_used']}")
        print(f"A: {result['answer']}")
        print("-" * 40)

    print("\n" + "=" * 60)
    print("CONSISTENCY TEST")
    print("=" * 60)
    test_question = "What is the placement rate?"
    result1 = ask_agent(test_question, knowledge_data, agent_app)
    result2 = ask_agent(test_question, knowledge_data, agent_app)
    print(f"Q: {test_question}")
    print(f"Answer 1: {result1['answer']}")
    print(f"Answer 2: {result2['answer']}")
    if result1["answer"] == result2["answer"]:
        print("[PASS] Answers are consistent.")
    else:
        print("[FAIL] Answers differ!")

    print("\n" + "=" * 60)
    print("INTERACTIVE MODE")
    print("=" * 60)
    print("Type your question (or 'quit' to exit):\n")

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if user_input.lower() in ("quit", "exit", "q"):
            print("Goodbye!")
            break

        if not user_input:
            continue

        result = ask_agent(user_input, knowledge_data, agent_app)
        print(f"Tool: {result['tool_used']}")
        print(f"Agent: {result['answer']}")
        print()


if __name__ == "__main__":
    main()
