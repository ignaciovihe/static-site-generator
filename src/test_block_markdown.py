import unittest
import textwrap

from block_markdown import markdown_to_blocks, block_to_block_type, markdown_to_html_node, BlockType

class Test_BlockMarkdown(unittest.TestCase):

    def test_markdown_to_blocks_one_new_line(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_two_new_lines(self):
            md = """
This is **bolded** paragraph


This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
            blocks = markdown_to_blocks(md)
            self.assertEqual(
                blocks,
                [
                    "This is **bolded** paragraph",
                    "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                    "- This is a list\n- with items",
                ],
            )

    def test_markdown_to_blocks_three_new_lines(self):
            md = """
This is **bolded** paragraph



This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
            blocks = markdown_to_blocks(md)
            self.assertEqual(
                blocks,
                [
                    "This is **bolded** paragraph",
                    "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                    "- This is a list\n- with items",
                ],
            )

    def test_markdown_to_blocks_multiple_new_lines_with_spaces(self):
            md = """
This is **bolded** paragraph


    
This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
            blocks = markdown_to_blocks(md)
            self.assertEqual(
                blocks,
                [
                    "This is **bolded** paragraph",
                    "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                    "- This is a list\n- with items",
                ],
            )

    def test_markdown_to_blocks_multiple_new_lines_with_spaces(self):
            md = """
This is **bolded** paragraph
This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line
- This is a list
- with items
"""
            blocks = markdown_to_blocks(md)
            self.assertEqual(
                blocks,
                [
                    "This is **bolded** paragraph\nThis is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line\n- This is a list\n- with items",
                ],
            )

    def test_markdown_to_blocks_multiple_spaces_start_end(self):
            md = """   
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
            blocks = markdown_to_blocks(md)
            self.assertEqual(
                blocks,
                [
                    "This is **bolded** paragraph",
                    "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                    "- This is a list\n- with items",
                ],
            )

    def test_markdown_to_blocks_multiple_new_lines_start_end(self):
            md = """



This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items


"""
            blocks = markdown_to_blocks(md)
            self.assertEqual(
                blocks,
                [
                    "This is **bolded** paragraph",
                    "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                    "- This is a list\n- with items",
                ],
            )

##############################################3

    def test_block_to_block_type_heading(self):
        valid_blocks = [
            "# Title1",
            "## Title2",
            "### Title3",
            "#### Title4",
            "##### Title5",
            "###### Title6",
        ]

        for block in valid_blocks:
            block_type = block_to_block_type(block)
            self.assertEqual(
                block_type, BlockType.HEADING
            )   

    def test_block_to_block_type_heading_sintax_error(self):
        valid_blocks = [
            "#Title1",
            "####### Title6",
            "Title",
        ]

        for block in valid_blocks:
            block_type = block_to_block_type(block)
            self.assertEqual(
                block_type, BlockType.PARAGRAPH
            )

    def test_block_to_block_type_code(self):
        blocks = [
"```\n Code line 1```",
"```\n Code line 1\nCode line 2```",
"```\n Code line 1\nCode `line 2```",
"```\n Code line 1\nCode line 2\n```",
"```\n Code line 1\nCode``` line 2```",

        ]

        for block in blocks:
            block_type = block_to_block_type(block)
            self.assertEqual(
                block_type, BlockType.CODE
            )

    def test_block_to_block_type_code_syntax_error(self):
        blocks = [
"``\n Code line 1```",
"```\n Code line 1``",
"``` Code line 1```",

        ]

        for block in blocks:
            block_type = block_to_block_type(block)
            self.assertEqual(
                block_type, BlockType.PARAGRAPH
            )

    def test_block_to_block_type_quote(self):
        blocks = [
"> Quote 1",
">Quote 1",
""">Quote 1
>Quote 2""",
"""> Quote 1
> Quote 2""",
""">Quote 1
> Quote 2""",
""">Quote 1
>Quote 2
>Quote 3""",

        ]

        for block in blocks:
            block_type = block_to_block_type(block)
            self.assertEqual(
                block_type, BlockType.QUOTE
            )

    def test_block_to_block_type_quote_syntax_error(self):
        blocks = [
"Quote 1",
" Quote 1",
">  Quote 1",
"""> Quote 1
Quote 2""",
""">Quote 1
> Quote 2\n""",
""">Quote 1
>Quote 2
>  Quote 3""",
" > Quote 1",
">> Quote 1",


        ]

        for block in blocks:
            block_type = block_to_block_type(block)
            self.assertEqual(
                block_type, BlockType.PARAGRAPH
            )

    def test_block_to_block_type_uolist(self):
        blocks = [
"- Element 1",
"""- Element 1
- Element 2""",
"""- Element 1
- Element 2
- Element 3""",


        ]

        for block in blocks:
            block_type = block_to_block_type(block)
            self.assertEqual(
                block_type, BlockType.UOLIST
            )

    def test_block_to_block_type_uolist_syntax_error(self):
        blocks = [
" Element 1",
"-Element 1",
"-  Element 1",
" - Element 1",
"-- Element 1",
"""- Element 1
Element 2""",

        ]

        for block in blocks:
            block_type = block_to_block_type(block)
            self.assertEqual(
                block_type, BlockType.PARAGRAPH
            )

    def test_block_to_block_type_olist(self):
        blocks = [
"1. Element 1",
"""1. Element 1
2. Element 2""",
"""1. Element 1
2. Element 2
3. Element 3""",

        ]

        for block in blocks:
            block_type = block_to_block_type(block)
            self.assertEqual(
                block_type, BlockType.OLIST
            )

    def test_block_to_block_type_olist_syntax_error(self):
        blocks = [
" Element 1",
"1 Element 1",
"1.Element 1",
"1 .Element 1",
"1.. Element 1",
"1- Element 1",
"""1. Element 1
3. Element 2""",
"""0. Element 1
1. Element 2""",

        ]

        for block in blocks:
            block_type = block_to_block_type(block)
            self.assertEqual(
                block_type, BlockType.PARAGRAPH
            )


    def test_block_to_block_type_paragraph(self):
        blocks = [
"""
This is **bolded** paragraph
This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line
- This is a list
- with items
""",

        ]

        for block in blocks:
            block_type = block_to_block_type(block)
            self.assertEqual(
                block_type, BlockType.PARAGRAPH
            )


#######################################

    def test_markdown_to_html_node_paragraphs(self):
        md = textwrap.dedent("""
            This is **bolded** paragraph
            text in a p
            tag here

            This is another paragraph with _italic_ text and `code` here

        """)

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )


    def test_markdown_to_html_node_codeblock(self):
        md = textwrap.dedent("""
            ```
            This is text that _should_ remain
            the **same** even with inline stuff
            ```
        """)

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_markdown_to_html_node_heading(self):
        md = textwrap.dedent("""
            # Heading 1

            ## Heading 2

            ### Heading 3

            #### Heading 4

            ##### Heading 5

            ###### Heading 6

        """)

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading 1</h1><h2>Heading 2</h2><h3>Heading 3</h3><h4>Heading 4</h4><h5>Heading 5</h5><h6>Heading 6</h6></div>",
        )

    def test_markdown_to_html_node_quote(self):
        md = textwrap.dedent("""
            > Quote 1
            >Quote 2

        """)

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>Quote 1\nQuote 2</blockquote></div>",
        )

    def test_markdown_to_html_node_uolist(self):
        md = textwrap.dedent("""
            - Item 1
            - Item 2

        """)

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>Item 1</li><li>Item 2</li></ul></div>",
        )


    def test_markdown_to_html_node_olist(self):
        md = textwrap.dedent("""
            1. Item 1
            2. Item 2

        """)

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>Item 1</li><li>Item 2</li></ol></div>",
        )

    def test_markdown_to_html_node_multiple_block_types(self):

        md = textwrap.dedent("""\
            # Heading 1

            This is a **bold** paragraph with _italic_, `inline code`, a [link](https://example.com) and an ![image](image.png).

            > This is a quote.
            > It has two lines.

            - First item
            - Second item with **bold**
            - Third item

            1. Ordered item one
            2. Ordered item two

            ```
            def hello():
                print("Hello, world!")
            ```
        """)

        expected_html = (
            "<div>"
            "<h1>Heading 1</h1>"
            '<p>This is a <b>bold</b> paragraph with <i>italic</i>, '
            '<code>inline code</code>, a <a href="https://example.com">link</a> '
            'and an <img src="image.png" alt="image">.</p>'
            "<blockquote>This is a quote.\n"
            "It has two lines.</blockquote>"
            "<ul>"
            "<li>First item</li>"
            "<li>Second item with <b>bold</b></li>"
            "<li>Third item</li>"
            "</ul>"
            "<ol>"
            "<li>Ordered item one</li>"
            "<li>Ordered item two</li>"
            "</ol>"
            "<pre><code>def hello():\n"
            '    print("Hello, world!")\n'
            "</code></pre>"
            "</div>"
        )

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            expected_html        
        )