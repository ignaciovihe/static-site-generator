import re
import os
from block_markdown import markdown_to_html_node


def extract_title(markdown: str) -> str:
    match = re.search(r"^#{1} (.+)$", markdown, re.MULTILINE)
    if match:
        return match.group(1)
    raise ValueError("No H1 header found")


def generate_page(from_path: str, template_path: str, dest_path: str):

    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r") as f:
        markdown = f.read()

    with open(template_path, "r") as f:
        template = f.read()

    html = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)

    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)

    parent_dir = os.path.dirname(dest_path)

    if parent_dir and not os.path.exists(parent_dir):
        os.makedirs(parent_dir, exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(template)
    


