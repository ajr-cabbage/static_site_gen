import unittest

from src.functions import split_nodes_delimiter
from src.textnode import TextNode, TextType


class TestSplitNodesDelimiter(unittest.TestCase):
    # test code block
    def test_1(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    # test italics
    def test_2(self):
        node = TextNode("This is text with _italics_ in it", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        expected = [
            TextNode("This is text with ", TextType.TEXT),
            TextNode("italics", TextType.ITALIC),
            TextNode(" in it", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    # test bold
    def test_3(self):
        node = TextNode("This is text with **bold** in it", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("This is text with ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" in it", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    # test bad syntax
    def test_4(self):
        node = TextNode("This is text with **bad syntax_ in it", TextType.TEXT)
        with self.assertRaises(Exception):
            new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)

    # test multiple tags
    def test_5(self):
        node = TextNode("**This** is text with **bold** in it", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("This", TextType.BOLD),
            TextNode(" is text with ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" in it", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)
