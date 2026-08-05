import unittest
import textwrap
from generate_page import extract_title

class TestGeneratePage(unittest.TestCase):

    def test_extract_title_only_heading(self):
        md = textwrap.dedent(
            """
            # Heading 1
            """
        )

        heading = extract_title(md)
        self.assertEqual(
            "Heading 1",
            heading
        )


    def test_extract_title_two_level_headings(self):
        md = textwrap.dedent(
            """
            # Heading 1
            ## Heading 2
            """
        )

        heading = extract_title(md)
        self.assertEqual(
            "Heading 1",
            heading
        )

    def test_extract_title_two_headings_level_one(self):
        md = textwrap.dedent(
            """
            # Heading 2

            # Heading 1
            """
        )

        heading = extract_title(md)
        self.assertEqual(
            "Heading 2",
            heading
        )


    def test_extract_title_heading_second_place(self):
        md = textwrap.dedent(
            """
            This is a paragraph.

            # Heading 1

            This is a second paragraph
            """
        )

        heading = extract_title(md)
        self.assertEqual(
            "Heading 1",
            heading
        )

def test_extract_title_complete_markdown(self):
    md = textwrap.dedent(
        """
        # My Awesome Document

        This is the introduction paragraph with **bold**, _italic_, `inline code`, a [link](https://example.com) and an ![image](https://example.com/image.png).

        ## Section One

        This is another paragraph.

        > This is a quote.
        > It has two lines.

        ### Unordered List

        - First item
        - Second item
        - Third item

        ### Ordered List

        1. First step
        2. Second step
        3. Third step

        ```python
        def hello():
            print("Hello, world!")
        ```

        ## Final Section

        Final paragraph.
        """
    )

    heading = extract_title(md)
    self.assertEqual(
        "My Awesome Document",
        heading
    )