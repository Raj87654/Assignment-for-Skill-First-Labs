import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "milestone2-ai-agent"))
from tools import search_knowledge, calculate, classify_question, extract_math_expression, run_agent


SAMPLE_KNOWLEDGE = {
    "college_name": "TechVista Institute of Technology",
    "location": "Bangalore, India",
    "founded": 2015,
    "programs": [
        {"name": "B.Tech Computer Science", "duration": "4 years", "annual_fee": 150000},
        {"name": "M.Tech AI and ML", "duration": "2 years", "annual_fee": 200000},
    ],
    "internship_partners": ["Google", "Microsoft", "Amazon", "Infosys"],
    "total_students": 5000,
    "placement_rate": "92%",
    "highest_package": "45 LPA",
    "average_package": "12 LPA",
    "campus_facilities": ["Library", "Sports Complex", "AI Research Lab", "Hostel"],
}


class TestKnowledgeSearch(unittest.TestCase):

    def test_answer_from_knowledge(self):
        result = search_knowledge("What is the placement rate?", SAMPLE_KNOWLEDGE)
        self.assertIsNotNone(result)
        self.assertIn("92%", result)

    def test_internship_partners(self):
        result = search_knowledge("Which companies are internship partners?", SAMPLE_KNOWLEDGE)
        self.assertIsNotNone(result)
        self.assertIn("Google", result)
        self.assertIn("Microsoft", result)

    def test_missing_information(self):
        result = search_knowledge("What is the hostel fee?", SAMPLE_KNOWLEDGE)
        self.assertIsNone(result)

    def test_location_query(self):
        result = search_knowledge("Where is the college located?", SAMPLE_KNOWLEDGE)
        self.assertIsNotNone(result)
        self.assertIn("Bangalore", result)


class TestCalculator(unittest.TestCase):

    def test_addition(self):
        self.assertEqual(calculate("25 + 37"), "62")

    def test_subtraction(self):
        self.assertEqual(calculate("100 - 45"), "55")

    def test_multiplication(self):
        self.assertEqual(calculate("150000 * 4"), "600000")

    def test_division(self):
        self.assertEqual(calculate("100 / 4"), "25")

    def test_division_by_zero(self):
        result = calculate("100 / 0")
        self.assertIn("Division by zero", result)

    def test_invalid_expression(self):
        result = calculate("hello + world")
        self.assertIn("Error", result)

    def test_decimal_result(self):
        self.assertEqual(calculate("10 / 3"), "3.333333")

    def test_negative_numbers(self):
        self.assertEqual(calculate("-5 + 3"), "-2")


class TestQuestionClassifier(unittest.TestCase):

    def test_math_question(self):
        self.assertEqual(classify_question("What is 25 + 37?"), "calculator")

    def test_knowledge_question(self):
        self.assertEqual(classify_question("What is the placement rate?"), "knowledge")

    def test_calculate_keyword(self):
        self.assertEqual(classify_question("Calculate 5 * 10"), "calculator")

    def test_general_question(self):
        self.assertEqual(classify_question("Tell me about the college"), "knowledge")


class TestAgentConsistency(unittest.TestCase):

    def test_same_question_twice(self):
        result1 = run_agent("What is the placement rate?", SAMPLE_KNOWLEDGE)
        result2 = run_agent("What is the placement rate?", SAMPLE_KNOWLEDGE)
        self.assertEqual(result1["answer"], result2["answer"])

    def test_math_consistency(self):
        result1 = run_agent("What is 25 + 37?", SAMPLE_KNOWLEDGE)
        result2 = run_agent("What is 25 + 37?", SAMPLE_KNOWLEDGE)
        self.assertEqual(result1["answer"], result2["answer"])
        self.assertEqual(result1["answer"], "62")


class TestToolRouting(unittest.TestCase):

    def test_routes_to_calculator(self):
        result = run_agent("What is 10 + 20?", SAMPLE_KNOWLEDGE)
        self.assertEqual(result["tool_used"], "calculator")

    def test_routes_to_knowledge(self):
        result = run_agent("What is the placement rate?", SAMPLE_KNOWLEDGE)
        self.assertEqual(result["tool_used"], "knowledge_search")

    def test_missing_info_response(self):
        result = run_agent("What is the principal's name?", SAMPLE_KNOWLEDGE)
        self.assertEqual(result["answer"], "I don't have enough information to answer that.")


if __name__ == "__main__":
    unittest.main()
