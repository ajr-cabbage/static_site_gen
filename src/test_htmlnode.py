import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_htmlnode_repr(self):
        htmlnode1 = HTMLNode(tag="p", value="paragraph")
        htmlnode2 = HTMLNode(tag="h1", value="header")
        children_lst = [htmlnode1, htmlnode2]
        prop_dic = {
            "href": "https://www.google.com",
            "target": "_blank",
        }
        parentnode = HTMLNode(
            tag="a", value="google.com", children=children_lst, props=prop_dic
        )
        # print(parentnode)

    def test_props_to_html(self):
        htmlnode1 = HTMLNode(tag="p", value="paragraph")
        htmlnode2 = HTMLNode(tag="h1", value="header")
        children_lst = [htmlnode1, htmlnode2]
        prop_dic = {
            "href": "https://www.google.com",
            "target": "_blank",
        }
        parentnode = HTMLNode(
            tag="a", value="google.com", children=children_lst, props=prop_dic
        )
        expected = ' href="https://www.google.com" target="_blank"'
        test_str = parentnode.props_to_html()
        self.assertEqual(expected, test_str)

    def test_props_null(self):
        htmlnode1 = HTMLNode(tag="p", value="paragraph")
        expected = ""
        test_str = htmlnode1.props_to_html()
        self.assertEqual(expected, test_str)
