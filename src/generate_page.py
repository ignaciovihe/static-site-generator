import re
import os
import shutil
from block_markdown import markdown_to_html_node


def extract_title(markdown: str) -> str:
    match = re.search(r"^#{1} (.+)$", markdown, re.MULTILINE)
    if match:
        return match.group(1)
    raise ValueError("No H1 header found")


def generate_page(from_path: str, template_path: str, dest_path: str, basepath: str):

    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r") as f:
        markdown = f.read()

    with open(template_path, "r") as f:
        template = f.read()

    html = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)

    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)
    template = template.replace('href="/', f'href="{basepath}')
    template = template.replace('src="/', f'src="{basepath}')


    parent_dir = os.path.dirname(dest_path)

    if parent_dir and not os.path.exists(parent_dir):
        os.makedirs(parent_dir, exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(template)


def generate_pages_recursive(dir_path_content: str, template_path: str, dest_dir_path: str, basepath: str):


    if  not os.path.exists(dest_dir_path):
        print(f"Creating {dest_dir_path}")
        os.makedirs(dest_dir_path, exist_ok= True)

    for item in os.listdir(dir_path_content):
        src_path = os.path.join(dir_path_content, item)
        dst_path = os.path.join(dest_dir_path, item)
        if os.path.isfile(src_path) and os.path.splitext(src_path)[1] == ".md":
            dst_path = dst_path.removesuffix(".md") + ".html"
            generate_page(src_path, template_path, dst_path, basepath)
        if os.path.isdir(src_path):
            generate_pages_recursive(src_path, template_path, dst_path, basepath)



