# Milestone 1: CSS Parser

## What This Project Does

This program reads a CSS file and extracts structured information from it. Instead of just displaying the raw CSS text, it parses the file and pulls out:

- **Selectors** (e.g., `body`, `h1`, `.container`)
- **Property names** (e.g., `background-color`, `font-size`)
- **Property values** (e.g., `#f0f0f0`, `24px`)

The extracted data is displayed as a Python dictionary and also printed as formatted JSON.

## How It Works

1. The program reads the CSS file (defaults to `sample.css` in the same folder).
2. It uses the `tinycss2` library to parse the CSS into tokens.
3. It loops through each CSS rule, extracts the selector and declarations.
4. Each declaration is split into a property name and value.
5. The result is stored as a list of dictionaries and printed in a readable format.

## Dependencies

- Python 3.8+
- `tinycss2` library

## Installation

```bash
pip install tinycss2
```

## How to Run

```bash
# Run with the default sample.css file
python css_parser.py

# Run with a custom CSS file
python css_parser.py path/to/your/file.css
```

## Sample Output

```
==================================================
PARSED CSS RULES
==================================================

Rule 1: body
------------------------------
  background-color: #f0f0f0
  font-family: Arial, sans-serif
  margin: 0

Rule 2: h1
------------------------------
  color: #333333
  font-size: 24px

Rule 3: .container
------------------------------
  width: 80%
  margin: 0 auto
  padding: 20px

==================================================
JSON OUTPUT
==================================================
[
  {
    "selector": "body",
    "properties": {
      "background-color": "#f0f0f0",
      "font-family": "Arial, sans-serif",
      "margin": "0"
    }
  },
  {
    "selector": "h1",
    "properties": {
      "color": "#333333",
      "font-size": "24px"
    }
  },
  {
    "selector": ".container",
    "properties": {
      "width": "80%",
      "margin": "0 auto",
      "padding": "20px"
    }
  }
]
```

## Edge Cases Handled

- **Empty CSS file**: Prints a message and exits gracefully.
- **CSS comments**: Comments are skipped during parsing.
- **Multiple rules**: All rules are extracted and displayed.
- **File not found**: Shows an error message.
