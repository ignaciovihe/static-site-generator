import unittest
from htmlnode import HtmlNode, LeafNode, ParentNode
class TestHtmlNode(unittest.TestCase):
        
    def test_init(self):
        node = HtmlNode("p", "Hello")

        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "Hello")
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

    def test_props_to_html_no_props(self):
        node = HtmlNode()

        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_one_prop(self):
        node = HtmlNode(props={"href": "https://google.com"})

        self.assertEqual(node.props_to_html(), ' href="https://google.com"')

    def test_props_to_html_two_props(self):
        node = HtmlNode(props={
            "href": "https://google.com",
            "target": "_blank"
        })

        self.assertEqual(node.props_to_html(), ' href="https://google.com" target="_blank"')

    def test_to_html(self):
        node = HtmlNode()

        with self.assertRaises(NotImplementedError):
            node.to_html()


    def test_repr(self):
        node = HtmlNode("p", "Hello",)
        self.assertEqual(
            repr(node),
            "Htmlnode(p, Hello, None, None)"
        )

class TestLeafNode(unittest.TestCase):
        
    def test_leaf_init(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})

        self.assertEqual(node.tag, "a")
        self.assertEqual(node.value, "Click me!")
        self.assertIsNone(node.children)
        self.assertEqual(node.props, {"href": "https://www.google.com"})


    def test_leaf_to_html_raw(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_leaf_to_html_img(self):
        node = LeafNode("img", "", {"src":"image.png", "alt":"image"})
        self.assertEqual(node.to_html(), '<img src="image.png" alt="image">')

    def test_leaf_to_html_not_value(self):
        node = LeafNode("p", None)

        with self.assertRaises(ValueError):
            node.to_html()


class TestParentNode(unittest.TestCase):

    def test_parent_init(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])

        self.assertEqual(parent_node.tag, "div")
        self.assertIsNone(parent_node.value)
        self.assertEqual(parent_node.children, [child_node])
        self.assertEqual(parent_node.props, None)

    def test_parent_init_with_props(self):
        child_node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        parent_node = ParentNode("div", [child_node], {"id": "container"})

        self.assertEqual(parent_node.tag, "div")
        self.assertIsNone(parent_node.value, None)
        self.assertEqual(parent_node.children, [child_node])
        self.assertEqual(parent_node.props, {"id": "container"})

    def test_to_html_with_no_children(self):
        parent_node = ParentNode("div", None)

        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_multiple_children(self):   
        grandchild_node = LeafNode("b", "grandchild")
        child_node_leaf = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node, child_node_leaf])
        self.assertEqual(
            parent_node.to_html(),
            '<div><span><b>grandchild</b></span><a href="https://www.google.com">Click me!</a></div>',
        )

if __name__ == "__main__":
    unittest.main()