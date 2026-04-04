import unittest
from cmath import exp

from src.functions import text_to_textnodes
from src.textnode import TextNode, TextType


class TestTextToTextNodes(unittest.TestCase):
    def test_1(self):
        test_str = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        result = text_to_textnodes(test_str)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode(
                "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
            ),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertListEqual(expected, result)

    def test_2(self):
        test_str = "This has bad **markdown__ syntax in it."
        with self.assertRaises(Exception):
            result = text_to_textnodes(test_str)

    def test_3(self):
        test_str = "![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg)![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg)![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg)"
        result = text_to_textnodes(test_str)
        expected = [
            TextNode(
                "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
            ),
            TextNode(
                "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
            ),
            TextNode(
                "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
            ),
        ]
        self.assertListEqual(result, expected)
