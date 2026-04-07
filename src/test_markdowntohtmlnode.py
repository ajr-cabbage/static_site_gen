import unittest

from src.functions import markdown_to_html_node


class TestMarkdownToHTMLNode(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        # print(node)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
        """

        node = markdown_to_html_node(md)
        # print(node)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_heading(self):
        md = "#### This is a **bold** \nand _italic_ heading block."

        node = markdown_to_html_node(md)
        # print(node)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h4>This is a <b>bold</b> and <i>italic</i> heading block.</h4></div>",
        )

    def test_blockquote(self):
        md = """
> This is a
> multi line quote
> with a [link](google.com) in it.
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            '<div><blockquote>This is a multi line quote with a <a href="google.com">link</a> in it.</blockquote></div>',
        )

    def test_unordered_list(self):
        md = """
- This         is
- an _italic_ unordered
- list
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is</li><li>an <i>italic</i> unordered</li><li>list</li></ul></div>",
        )

    def test_ordered_list(self):
        md = """
1. This is
2. an ordered
3. list with an ![image](boots.png)
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            '<div><ol><li>This is</li><li>an ordered</li><li>list with an <img src="boots.png" alt="image"></img></li></ol></div>',
        )
