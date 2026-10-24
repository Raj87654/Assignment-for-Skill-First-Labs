import unittest
import sys
import os
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "milestone1-css-parser"))
from css_parser import parse_css, read_css_file


class TestCSSParser(unittest.TestCase):

    def test_multiple_selectors(self):
        css_text = """
        body {
            background-color: #fff;
            margin: 0;
        }
        h1 {
            color: red;
        }
        .main {
            padding: 10px;
        }
        """
        result = parse_css(css_text)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0]["selector"], "body")
        self.assertEqual(result[0]["properties"]["background-color"], "#fff")
        self.assertEqual(result[0]["properties"]["margin"], "0")
        self.assertEqual(result[1]["selector"], "h1")
        self.assertEqual(result[1]["properties"]["color"], "red")
        self.assertEqual(result[2]["selector"], ".main")
        self.assertEqual(result[2]["properties"]["padding"], "10px")

    def test_empty_css(self):
        css_text = ""
        result = parse_css(css_text)
        self.assertEqual(result, [])

    def test_whitespace_only_css(self):
        css_text = "   \n\n   \t  "
        result = parse_css(css_text)
        self.assertEqual(result, [])

    def test_css_with_comments(self):
        css_text = """
        /* This is a comment */
        p {
            font-size: 16px;
        }
        /* Another comment */
        """
        result = parse_css(css_text)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["selector"], "p")
        self.assertEqual(result[0]["properties"]["font-size"], "16px")

    def test_correct_property_extraction(self):
        css_text = """
        div {
            width: 100%;
            height: 50px;
            border: 1px solid black;
        }
        """
        result = parse_css(css_text)
        self.assertEqual(len(result), 1)
        props = result[0]["properties"]
        self.assertEqual(props["width"], "100%")
        self.assertEqual(props["height"], "50px")
        self.assertEqual(props["border"], "1px solid black")

    def test_read_css_file(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".css", delete=False) as f:
            f.write("a { color: blue; }")
            temp_path = f.name
        try:
            content = read_css_file(temp_path)
            self.assertEqual(content, "a { color: blue; }")
        finally:
            os.unlink(temp_path)


if __name__ == "__main__":
    unittest.main()
