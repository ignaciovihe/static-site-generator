import unittest
from textnode import *

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq_text(self):
        node = TextNode("Hello", TextType.BOLD)
        node2 = TextNode("Bye", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_not_eq_type(self):
        node = TextNode("Hello", TextType.BOLD)
        node2 = TextNode("Hello", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_not_eq_url(self):
        node = TextNode("Hello", TextType.BOLD, "http://google.com")
        node2 = TextNode("Hello", TextType.BOLD, "http://bootdev.com")
        self.assertNotEqual(node, node2)

    def test_not_eq_url_none(self):
        node = TextNode("Hello", TextType.BOLD)
        node2 = TextNode("Hello", TextType.BOLD, "http://bootdev.com")
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = TextNode("Hola", TextType.TEXT)
        self.assertEqual(
            repr(node),
            "TextNode(Hola, TextType.TEXT, None)"
        )


    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a bold text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold text node")

    def test_italic(self):
        node = TextNode("This is a italic text node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is a italic text node")

    def test_code(self):
        node = TextNode("This is code", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is code")

    def test_link(self):
        node = TextNode("Click here!", TextType.LINK, "http://google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Click here!")
        self.assertEqual(html_node.props, {"href": "http://google.com"})

    def test_image(self):
        node = TextNode("Image description", TextType.IMAGE, "http://img.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "http://img.com", "alt": "Image description"})        


if __name__ == "__main__":
    unittest.main()