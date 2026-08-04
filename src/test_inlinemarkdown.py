import unittest
from inline_markdown import split_nodes_delimiter, split_nodes_image, split_nodes_link, extract_markdown_links, extract_markdown_images, text_to_textnodes
from textnode import *


class Test_InlineMarkdown(unittest.TestCase):

    def test_extract_markdown_no_images(self):
        matches = extract_markdown_images(
            "This is text without an image"
        )
        self.assertListEqual([], matches)

    def test_extract_markdown_uncomplete_image(self):
            matches = extract_markdown_images(
                "This is text with an ![image]"
            )
            self.assertListEqual([], matches)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images_with_link_text(self):
        matches = extract_markdown_images(
            "This is text with a link [to boot dev](https://www.boot.dev)"
        )
        self.assertListEqual([], matches)

    def test_extract_markdown_multiple_images(self):
            matches = extract_markdown_images(
                "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
            )
            self.assertListEqual([("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")], matches)



    
    def test_extract_markdown_no_links(self):
        matches = extract_markdown_links(
            "This is text without link"
        )
        self.assertListEqual([], matches)

    def test_extract_markdown_uncomplete_link(self):
        matches = extract_markdown_links(
            "This is text with a uncomplete link (https://www.boot.dev)"
        )
        self.assertListEqual([], matches)        

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev")], matches)

    def test_extract_markdown_links_with_image_text(self):
        matches = extract_markdown_links(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([], matches)

    def test_extract_markdown_multiple_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)


    ################################################################3

    def test_split_delimiter_no_text_type(self):
        
        node = TextNode("**This is a bold Text**", TextType.BOLD)

        self.assertEqual(
            split_nodes_delimiter([node], "`", TextType.CODE),
            [TextNode("**This is a bold Text**", TextType.BOLD)]
        )

    def test_split_delimiter_text_type(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)

        self.assertEqual(
            split_nodes_delimiter([node], "`", TextType.CODE),
            [
                TextNode("This is text with a " , TextType.TEXT), 
                TextNode("code block", TextType.CODE), 
                TextNode(" word", TextType.TEXT)
            ]
        )

    def test_split_delimiter_multiple_nodes_mixed(self):
        node1 = TextNode("This is text with a `code block` word", TextType.TEXT)
        node2 = TextNode("**This is a bold Text**", TextType.BOLD)

        self.assertEqual(
            split_nodes_delimiter([node1, node2], "`", TextType.CODE),
            [
                TextNode("This is text with a " , TextType.TEXT), 
                TextNode("code block", TextType.CODE), 
                TextNode(" word", TextType.TEXT), 
                TextNode("**This is a bold Text**", TextType.BOLD)
            ]
        )

    def test_split_delimiter_multiple_nodes_mixed_second_call(self):
            node1 = TextNode("This is text with a " , TextType.TEXT) 
            node2 = TextNode("code block", TextType.CODE) 
            node3 = TextNode(" word", TextType.TEXT)
            node4 = TextNode("This is text with a **bold** word", TextType.TEXT)
    
            self.assertEqual(
                split_nodes_delimiter([node1, node2, node3, node4], "**", TextType.BOLD),
                [
                    TextNode("This is text with a " , TextType.TEXT), 
                    TextNode("code block", TextType.CODE), 
                    TextNode(" word", TextType.TEXT),
                    TextNode("This is text with a " , TextType.TEXT),
                    TextNode("bold", TextType.BOLD), 
                    TextNode(" word", TextType.TEXT)
                ]
            )

    def test_split_delimiter_invalid_sintax(self):
        node = TextNode("This is text with a `code block word", TextType.TEXT)

        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "`", TextType.CODE)


#############################################################3

    def test_split_images_no_image(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_images_only_image(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_images_one_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )        

    def test_split_images_multiple_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_images_multiple_images_no_empty_nodes(self):
            node = TextNode(
                "![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
                TextType.TEXT,
            )
            new_nodes = split_nodes_image([node])
            self.assertListEqual(
                [
                    TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                    TextNode(" and another ", TextType.TEXT),
                    TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
                ],
                new_nodes,
            )

    def test_split_images_image_and_link(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and a link [to boot dev](https://www.boot.dev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and a link [to boot dev](https://www.boot.dev)", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_images_multiple_nodes(self):
            node = TextNode(
                "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and a link [to boot dev](https://www.boot.dev)",
                TextType.TEXT,
            )
            node2 = TextNode(
                            "**This is a bold text**",
                            TextType.BOLD,
                        )
            new_nodes = split_nodes_image([node, node2])
            self.assertListEqual(
                [
                    TextNode("This is text with an ", TextType.TEXT),
                    TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                    TextNode(" and a link [to boot dev](https://www.boot.dev)", TextType.TEXT),
                    TextNode("**This is a bold text**", TextType.BOLD),
                ],
                new_nodes,
            )


#####################################################

    def test_split_links_no_link(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_links_only_link(self):
        node = TextNode(
            "[to boot dev](https://www.boot.dev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            ],
            new_nodes,
        )

    def test_split_links_one_link(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            ],
            new_nodes,
        )        

    def test_split_links_multiple_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
            ],
            new_nodes,
        )

    def test_split_linkss_multiple_links_no_empty_nodes(self):
            node = TextNode(
                "[to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
                TextType.TEXT,
            )
            new_nodes = split_nodes_link([node])
            self.assertListEqual(
                [
                    TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                    TextNode(" and ", TextType.TEXT),
                    TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
                ],
                new_nodes,
            )

    def test_split_links_image_and_link(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and a link [to boot dev](https://www.boot.dev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            ],
            new_nodes,
        )

    def test_split_links_multiple_nodes(self):
            node = TextNode(
                "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and a link [to boot dev](https://www.boot.dev)",
                TextType.TEXT,
            )
            node2 = TextNode(
                            "**This is a bold text**",
                            TextType.BOLD,
                        )
            new_nodes = split_nodes_link([node, node2])
            self.assertListEqual(
                [
                    TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and a link ", TextType.TEXT),
                    TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                    TextNode("**This is a bold text**", TextType.BOLD),
                ],
                new_nodes,
            )


####################################################3

    def test_text_to_textnodes_text_with_all_nodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"

        new_nodes = text_to_textnodes(text)

        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            new_nodes,
        )

    def test_text_to_textnodes_text_with_newline_character(self):
        text = "This is **text** with an _italic_ word \n and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"

        new_nodes = text_to_textnodes(text)

        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word \n and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            new_nodes,
        )

    def test_text_to_textnodes_text_with_incorrect_markdown_syntax(self):
        text = "This is **text** with an _italic word \n and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"

        with self.assertRaises(ValueError):
            text_to_textnodes(text)

    def test_text_to_textnodes_no_mark_down(self):
        text = "Just plain text"

        new_nodes = text_to_textnodes(text)

        self.assertListEqual(
            [
                TextNode("Just plain text", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_text_to_textnodes_empty_text(self):
        text = ""

        new_nodes = text_to_textnodes(text)

        self.assertListEqual(
            [ ],
            new_nodes,
        )

    def test_text_to_textnodes_format_begin_and_end(self):
        text = "**bold** and _italic_"

        new_nodes = text_to_textnodes(text)

        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )

    def test_text_to_textnodes_only_format(self):
        text = "**bold**"

        new_nodes = text_to_textnodes(text)

        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
            ],
            new_nodes,
        )

    
    def test_text_to_textnodes_repeated_format(self):
        text = "**one** and **two**"

        new_nodes = text_to_textnodes(text)

        self.assertListEqual(
            [
                TextNode("one", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("two", TextType.BOLD),
            ],
            new_nodes,
        )

        
    def test_text_to_textnodes_consecutive_formats(self):
        text = "**bold**_italic_`code`"

        new_nodes = text_to_textnodes(text)

        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode("italic", TextType.ITALIC),
                TextNode("code", TextType.CODE),
            ],
            new_nodes,
        )

    def test_text_to_textnodes_multiple_images(self):
        text = "![one](https://i.imgur.com/fJRm4Vk.jpeg) ![two](https://i.imgur.com/fJRm4Vk2.jpeg)"

        new_nodes = text_to_textnodes(text)

        self.assertListEqual(
            [
                TextNode("one", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" ", TextType.TEXT),
                TextNode("two", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk2.jpeg"),
            ],
            new_nodes,
        )

    def test_text_to_textnodes_consecutive_image_link(self):
        text = "![image](https://i.imgur.com/fJRm4Vk.jpeg)[link](https://i.imgur.com/fJRm4Vk2.jpeg)"

        new_nodes = text_to_textnodes(text)

        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode("link", TextType.LINK, "https://i.imgur.com/fJRm4Vk2.jpeg"),
            ],
            new_nodes,
        )