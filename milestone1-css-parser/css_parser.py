import tinycss2
import json
import sys
import os


def read_css_file(file_path):
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found.")
        sys.exit(1)
    with open(file_path, "r") as f:
        return f.read()


def parse_css(css_text):
    rules = tinycss2.parse_stylesheet(css_text, skip_comments=True, skip_whitespace=True)
    parsed_rules = []

    for rule in rules:
        if rule.type == "qualified-rule":
            selector = tinycss2.serialize(rule.prelude).strip()
            declarations = tinycss2.parse_declaration_list(rule.content, skip_comments=True, skip_whitespace=True)
            properties = {}
            for declaration in declarations:
                if declaration.type == "declaration":
                    property_name = declaration.lower_name
                    property_value = tinycss2.serialize(declaration.value).strip()
                    properties[property_name] = property_value
            parsed_rules.append({
                "selector": selector,
                "properties": properties
            })

    return parsed_rules


def display_results(parsed_rules):
    if not parsed_rules:
        print("No CSS rules found.")
        return

    print("=" * 50)
    print("PARSED CSS RULES")
    print("=" * 50)

    for i, rule in enumerate(parsed_rules, 1):
        print(f"\nRule {i}: {rule['selector']}")
        print("-" * 30)
        for prop, value in rule["properties"].items():
            print(f"  {prop}: {value}")

    print("\n" + "=" * 50)
    print("JSON OUTPUT")
    print("=" * 50)
    print(json.dumps(parsed_rules, indent=2))


def main():
    if len(sys.argv) > 1:
        css_file = sys.argv[1]
    else:
        css_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sample.css")

    css_text = read_css_file(css_file)

    if not css_text.strip():
        print("The CSS file is empty. No rules to parse.")
        return

    parsed_rules = parse_css(css_text)
    display_results(parsed_rules)

    return parsed_rules


if __name__ == "__main__":
    main()
