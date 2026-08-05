from enum import Enum
import re
from htmlnode import HtmlNode, ParentNode
from inline_markdown import text_to_textnodes
from textnode import TextNode, TextType, text_node_to_html_node


class BlockType(Enum):
    PARAGRAPH= "paragraph"
    HEADING= "heading"
    CODE= "code"
    QUOTE= "quote"
    UOLIST= "uolist"
    OLIST= "olist"


def markdown_to_blocks(markdown: str)-> list[str]:
    blocks = markdown.split("\n\n")
    clean_blocks = []
    for block in blocks:
        clean = block.strip("\n ")
        if clean:
            clean_blocks.append(clean)
    return clean_blocks


def block_to_block_type(markdown_block: str)-> BlockType:

    if (re.search(r"^#{1,6} .+$",markdown_block)):
        return BlockType.HEADING
    if (re.search(r"^```\n[\s\S]+```$", markdown_block)):
        return BlockType.CODE
    if all(re.fullmatch(r">(?: ?[^>\s].*)?", line) for line in markdown_block.split("\n")):
        return BlockType.QUOTE
    if all(re.fullmatch(r"- \S.+", line) for line in markdown_block.split("\n")):
        return BlockType.UOLIST
    
    lines = markdown_block.split("\n")

    for expected, line in enumerate(lines, start=1):
        match = re.fullmatch(r"(\d+)\. .+", line)

        if not match:
            return BlockType.PARAGRAPH

        if expected != int(match.group(1)):
            return BlockType.PARAGRAPH
        
    return BlockType.OLIST



def text_to_children(text:str) -> list[HtmlNode]:
    text_nodes = text_to_textnodes(text)
    html_children= []

    for text_node in text_nodes:
        html_children.append(text_node_to_html_node(text_node))
    return html_children

def markdown_to_html_node(markdown: str)-> HtmlNode:
    root_children = []
    markdown_blocks = markdown_to_blocks(markdown)
    for md_block in markdown_blocks:
        html_node = block_to_html_node(md_block)
        root_children.append(html_node)
    root_node = ParentNode("div", root_children)
    return root_node

def block_to_html_node(md_block: str) -> ParentNode:
    block_type = block_to_block_type(md_block)
    match block_type:
        case BlockType.PARAGRAPH:
            return paragraph_to_html_node(md_block)
        case BlockType.HEADING:
            return heading_to_html_node(md_block)
        case BlockType.QUOTE:
            return quote_to_html_node(md_block)
        case BlockType.UOLIST:
            return uolist_to_html_node(md_block)
        case BlockType.OLIST:
            return olist_to_html_node(md_block)
        case BlockType.CODE:
            return code_to_html_node(md_block)


def paragraph_to_html_node(md_block: str) -> ParentNode:
    content = md_block.replace("\n", " ")
    html_children = text_to_children(content)
    return ParentNode("p", html_children)

def heading_to_html_node(md_block: str) -> ParentNode:
    level, content = md_block.split(" ", 1)
    level = len(level)
    html_children = text_to_children(content)
    return ParentNode(f"h{level}",html_children)

def quote_to_html_node(md_block: str) -> ParentNode:
    quote_lines = md_block.split("\n")
    content = "\n".join([line.removeprefix(">").removeprefix(" ") for line in quote_lines])
    html_children = text_to_children(content)
    return ParentNode("blockquote",html_children)

def uolist_to_html_node(md_block: str) -> ParentNode:
    list_items = []
    lines = md_block.split("\n")
    for line in lines:
        content = line.removeprefix("- ")
        html_children = text_to_children(content)
        list_item_node = ParentNode("li",html_children)
        list_items.append(list_item_node)
    return ParentNode("ul", list_items)

def olist_to_html_node(md_block: str) -> ParentNode:
    list_items = []
    lines = md_block.split("\n")
    for line in lines:
        content = line.split(". ", 1)[1]
        html_children = text_to_children(content)
        list_item_node = ParentNode("li",html_children)
        list_items.append(list_item_node)
    return ParentNode("ol", list_items)

def code_to_html_node(md_block: str) -> ParentNode:
    content = md_block.removeprefix("```\n").removesuffix("```")
    code_text_node = TextNode(content, TextType.CODE)
    code_node = text_node_to_html_node(code_text_node)
    return ParentNode("pre",[code_node])
