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
    if all(re.fullmatch(r"> ?[^>\s].+", line) for line in markdown_block.split("\n")):
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



def text_to_children(text:str):
    text_nodes = text_to_textnodes(text)
    html_children= []

    for text_node in text_nodes:
        html_children.append(text_node_to_html_node(text_node))
    return html_children

def markdown_to_html_node(markdown:str)-> HtmlNode:
    root_children = []
    markdown_blocks = markdown_to_blocks(markdown)
    for md_block in markdown_blocks:
        block_type = block_to_block_type(md_block)

        match block_type:
            case BlockType.PARAGRAPH:
                content = md_block.replace("\n", " ")
                html_children = text_to_children(content)
                paragraph_node = ParentNode("p", html_children)
                root_children.append(paragraph_node)
            case BlockType.HEADING:
                level, content = md_block.split(" ", 1)
                level = len(level)
                html_children = text_to_children(content)
                heading_node = ParentNode(f"h{level}",html_children)
                root_children.append(heading_node)
            case BlockType.QUOTE:
                quote_lines = md_block.split("\n")
                content = "\n".join([line.removeprefix(">").removeprefix(" ") for line in quote_lines])
                html_children = text_to_children(content)
                quote_node = ParentNode("blockquote",html_children)
                root_children.append(quote_node)
            case BlockType.UOLIST:
                list_items = []
                lines = md_block.split("\n")
                for line in lines:
                    content = line.removeprefix("- ")
                    html_children = text_to_children(content)
                    list_item_node = ParentNode("li",html_children)
                    list_items.append(list_item_node)
                ul_node = ParentNode("ul", list_items)
                root_children.append(ul_node)
            case BlockType.OLIST:
                list_items = []
                lines = md_block.split("\n")
                for line in lines:
                    content = line.split(". ", 1)[1]
                    html_children = text_to_children(content)
                    list_item_node = ParentNode("li",html_children)
                    list_items.append(list_item_node)
                ol_node = ParentNode("ol", list_items)
                root_children.append(ol_node)
            case BlockType.CODE:
                content = md_block.removeprefix("```\n").removesuffix("```")
                code_text_node = TextNode(content, TextType.CODE)
                code_node = text_node_to_html_node(code_text_node)
                pre_node = ParentNode("pre",[code_node])
                root_children.append(pre_node)

    root_node = ParentNode("div", root_children)
    return root_node
