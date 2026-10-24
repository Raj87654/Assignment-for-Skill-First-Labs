import json
import os
import re
import operator


KNOWLEDGE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "knowledge.json")


def load_knowledge(file_path=None):
    if file_path is None:
        file_path = KNOWLEDGE_FILE
    with open(file_path, "r") as f:
        return json.load(f)


def search_knowledge(query, knowledge_data=None):
    if knowledge_data is None:
        knowledge_data = load_knowledge()

    query_lower = query.lower()
    results = []

    direct_field_map = {
        "college name": "college_name",
        "name of the college": "college_name",
        "institute name": "college_name",
        "location": "location",
        "where": "location",
        "city": "location",
        "founded": "founded",
        "established": "founded",
        "when was": "founded",
        "year": "founded",
        "total students": "total_students",
        "number of students": "total_students",
        "how many students": "total_students",
        "student count": "total_students",
        "placement rate": "placement_rate",
        "placement percentage": "placement_rate",
        "highest package": "highest_package",
        "highest salary": "highest_package",
        "top package": "highest_package",
        "average package": "average_package",
        "average salary": "average_package",
        "mean package": "average_package",
    }

    for phrase, field in direct_field_map.items():
        if phrase in query_lower:
            if field in knowledge_data:
                value = knowledge_data[field]
                results.append(f"{field.replace('_', ' ').title()}: {value}")

    if any(word in query_lower for word in ["program", "course", "degree", "btech", "mtech", "b.tech", "m.tech"]):
        programs = knowledge_data.get("programs", [])
        for prog in programs:
            results.append(f"{prog['name']} - Duration: {prog['duration']}, Annual Fee: Rs.{prog['annual_fee']}")

    fee_keywords = ["fee", "cost", "tuition", "price"]
    specific_fee_items = ["hostel", "mess", "transport", "library", "exam", "lab", "registration"]
    if any(word in query_lower for word in fee_keywords):
        is_specific_unknown_fee = any(item in query_lower for item in specific_fee_items)
        if not is_specific_unknown_fee:
            programs = knowledge_data.get("programs", [])
            for prog in programs:
                results.append(f"{prog['name']} - Annual Fee: Rs.{prog['annual_fee']}")

    if any(word in query_lower for word in ["internship", "partner", "company", "companies", "recruit"]):
        partners = knowledge_data.get("internship_partners", [])
        if partners:
            results.append(f"Internship Partners: {', '.join(partners)}")

    if any(word in query_lower for word in ["facilit", "campus", "infrastructure", "ameniti"]):
        facilities = knowledge_data.get("campus_facilities", [])
        if facilities:
            results.append(f"Campus Facilities: {', '.join(facilities)}")

    if not results:
        return None

    seen = []
    for r in results:
        if r not in seen:
            seen.append(r)
    return "\n".join(seen)


SAFE_OPERATORS = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.truediv,
}


def calculate(expression):
    expression = expression.strip()
    pattern = r"^(-?\d+\.?\d*)\s*([+\-*/])\s*(-?\d+\.?\d*)$"
    match = re.match(pattern, expression)

    if not match:
        return "Error: Invalid expression. Use format: number operator number (e.g., 5 + 3)"

    num1 = float(match.group(1))
    op = match.group(2)
    num2 = float(match.group(3))

    if op == "/" and num2 == 0:
        return "Error: Division by zero is not allowed."

    operation = SAFE_OPERATORS[op]
    result = operation(num1, num2)

    if result == int(result):
        return str(int(result))
    return str(round(result, 6))


def classify_question(question):
    question_lower = question.lower()

    math_patterns = [
        r"\d+\s*[+\-*/]\s*\d+",
        r"what is \d+",
        r"calculate",
        r"compute",
        r"how much is \d+",
        r"sum of",
        r"multiply",
        r"divide",
        r"add \d+",
        r"subtract",
    ]

    for pattern in math_patterns:
        if re.search(pattern, question_lower):
            return "calculator"

    return "knowledge"


def extract_math_expression(question):
    match = re.search(r"(-?\d+\.?\d*)\s*([+\-*/])\s*(-?\d+\.?\d*)", question)
    if match:
        return match.group(0)
    return None


def run_agent(question, knowledge_data=None):
    tool_used = classify_question(question)

    if tool_used == "calculator":
        expression = extract_math_expression(question)
        if expression:
            answer = calculate(expression)
            return {
                "question": question,
                "tool_used": "calculator",
                "expression": expression,
                "answer": answer,
            }
        else:
            return {
                "question": question,
                "tool_used": "calculator",
                "answer": "Error: Could not extract a valid math expression from your question.",
            }

    result = search_knowledge(question, knowledge_data)
    if result:
        return {
            "question": question,
            "tool_used": "knowledge_search",
            "answer": result,
        }
    else:
        return {
            "question": question,
            "tool_used": "knowledge_search",
            "answer": "I don't have enough information to answer that.",
        }
