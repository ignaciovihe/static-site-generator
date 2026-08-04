from textnode import *
from htmlnode import *

def main():

    new_node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    new_node2 = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.deva")
    print(new_node)
    print(new_node == new_node2)

    node = ParentNode(
        "p",
        [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            ParentNode("p", [
                LeafNode("a", "Click me!", {"href": "https://www.google.com"}),
            ],),
            LeafNode(None, "Normal text"),
        ],
    )

    print(node.to_html())

main()
