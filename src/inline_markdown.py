import re
from textnode import TextNode, TextType



def extract_markdown_images(text: str)->list[tuple[str, str]]:

    pattern = r"!\[([^\]]*)\]\(([^)\s]+)\)"
    return re.findall(pattern, text)


def extract_markdown_links(text: str)->list[tuple[str, str]]:

    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(pattern, text)


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            splited_node = node.text.split(delimiter)
            if len(splited_node) % 2 == 0:
                raise ValueError(f"Missing closing delimiter: {delimiter}")
            for index, part in enumerate(splited_node):
                if part == "":
                    continue

                if index % 2 == 0:
                    new_node = TextNode(part, TextType.TEXT)
                else:
                    new_node = TextNode(part, text_type)
                new_nodes.append(new_node)
    return new_nodes


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            images = extract_markdown_images(node.text)
            if not images:
                new_nodes.append(node)
            else:
                current_text = node.text
                for image in images:
                    text, url = image
                    separator = f"![{text}]({url})"
                    splitted_node = current_text.split(separator, 1)
                    before_image = splitted_node[0]
                    after_image = splitted_node [1]
                    if before_image == "":
                        new_node = TextNode(text, TextType.IMAGE, url)
                        new_nodes.append(new_node)
                        current_text = after_image 
                    else:
                        new_node = TextNode(before_image, TextType.TEXT)
                        new_nodes.append(new_node)
                        new_node = TextNode(text, TextType.IMAGE, url)
                        new_nodes.append(new_node)
                        current_text = after_image
                if current_text != "":
                    new_node = TextNode(current_text, TextType.TEXT)
                    new_nodes.append(new_node)
    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            links = extract_markdown_links(node.text)
            if not links:
                new_nodes.append(node)
            else:
                current_text = node.text
                for link in links:
                    text, url = link
                    separator = f"[{text}]({url})"
                    splitted_node = current_text.split(separator, 1)
                    before_link = splitted_node[0]
                    after_link = splitted_node [1]
                    if before_link == "":
                        new_node = TextNode(text, TextType.LINK, url)
                        new_nodes.append(new_node)
                        current_text = after_link 
                    else:
                        new_node = TextNode(before_link, TextType.TEXT)
                        new_nodes.append(new_node)
                        new_node = TextNode(text, TextType.LINK, url)
                        new_nodes.append(new_node)
                        current_text = after_link
                if current_text != "":
                    new_node = TextNode(current_text, TextType.TEXT)
                    new_nodes.append(new_node)
    return new_nodes


def text_to_textnodes(text) -> list[TextNode]:

    node_splitters = [split_nodes_image, split_nodes_link]
    delimiters = {
        TextType.BOLD: "**",
        TextType.ITALIC: "_",
        TextType.CODE: "`"
    }

    result = [TextNode(text, TextType.TEXT)]

    for delimiter_type, delimiter in delimiters.items():
        result = split_nodes_delimiter(result, delimiter, delimiter_type)

    for func in node_splitters:
        result = func(result)

    return result