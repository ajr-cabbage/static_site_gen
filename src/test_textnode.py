import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("This is one type", TextType.ITALIC)
        node2 = TextNode("This is another", TextType.CODE)
        self.assertNotEqual(node, node2)

    def test_text_not_eq(self):
        node = TextNode("This is one type", TextType.ITALIC)
        node2 = TextNode("Same type, different text", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_url_eq(self):
        node = TextNode("This is a text node", TextType.LINK, "google.com")
        node2 = TextNode("This is a text node", TextType.LINK, "google.com")
        self.assertEqual(node, node2)

    def test_url_not_eq(self):
        node = TextNode("This is a text node", TextType.LINK, "google.com")
        node2 = TextNode("This is a text node", TextType.LINK, "yahoo.com")
        self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()
