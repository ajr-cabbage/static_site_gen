import re

from src.leafnode import LeafNode
from src.textnode import TextNode, TextType


# Takes a Markdown TextNode and returns an HTML LeafNode
def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(tag=None, value=text_node.text)
        case TextType.BOLD:
            return LeafNode(tag="b", value=text_node.text)
        case TextType.ITALIC:
            return LeafNode(tag="i", value=text_node.text)
        case TextType.CODE:
            return LeafNode(tag="code", value=text_node.text)
        case TextType.LINK:
            return LeafNode(
                tag="a", value=text_node.text, props={"href": text_node.url}
            )
        case TextType.IMAGE:
            return LeafNode(
                tag="img", value="", props={"src": text_node.url, "alt": text_node.text}
            )
        case _:
            raise ValueError("Invalid TextType")


# convert a lits of TextNodes that may have inline formatting and
# return separate nodes with correct TextType
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            split_node = node.text.split(delimiter)
            if len(split_node) % 2 == 0:
                raise Exception("That's invalid Markdown syntax.")
            for i in range(len(split_node)):
                if split_node[i] and i % 2 == 0:
                    new_node = TextNode(split_node[i], TextType.TEXT)
                    new_nodes.append(new_node)
                elif split_node[i] and i % 2 != 0:
                    match text_type:
                        case TextType.CODE:
                            new_node = TextNode(split_node[i], TextType.CODE)
                            new_nodes.append(new_node)
                        case TextType.ITALIC:
                            new_node = TextNode(split_node[i], TextType.ITALIC)
                            new_nodes.append(new_node)
                        case TextType.BOLD:
                            new_node = TextNode(split_node[i], TextType.BOLD)
                            new_nodes.append(new_node)
                        case _:
                            raise ValueError("Invalid TextType")
    return new_nodes


# takes a string with markdown images and returns a
# list of (text, url) tuples
def extract_markdown_images(text):
    if not text:
        return []
    img_list = []
    matches = re.findall(r"!\[(.*?)]\((.*?)\)", text)
    for match in matches:
        img_list.append(match)
    return img_list


# takes a string with markdown links and returns a
# list of (text, url) tuples
def extract_markdown_links(text):
    if not text:
        return []
    link_list = []
    matches = re.findall(r"\[(.*?)]\((.*?)\)", text)
    for match in matches:
        link_list.append(match)
    return link_list


# Takes a list of TextNodes with inline images and
# returns separate nodes with correct TextType
def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            img_list = extract_markdown_images(node.text)
            if len(img_list) == 0:
                new_nodes.append(node)
                continue
            img_list_index = 0
            subbed_text = re.sub(r"!\[(.*?)]\((.*?)\)", "\x00&\x00", node.text)
            split_node = subbed_text.split("\x00")
            for i in range(len(split_node)):
                if split_node[i] and i % 2 == 0:
                    new_node = TextNode(split_node[i], TextType.TEXT)
                    new_nodes.append(new_node)
                elif split_node[i] and i % 2 != 0:
                    new_node = TextNode(
                        img_list[img_list_index][0],
                        TextType.IMAGE,
                        img_list[img_list_index][1],
                    )
                    new_nodes.append(new_node)
                    img_list_index += 1
    return new_nodes


# Takes a list of TextNodes with inline links and
# returns separate nodes with correct TextType
def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            link_list = extract_markdown_links(node.text)
            if len(link_list) == 0:
                new_nodes.append(node)
                continue
            link_list_index = 0
            subbed_text = re.sub(r"\[(.*?)]\((.*?)\)", "\x00&\x00", node.text)
            split_node = subbed_text.split("\x00")
            for i in range(len(split_node)):
                if split_node[i] and i % 2 == 0:
                    new_node = TextNode(split_node[i], TextType.TEXT)
                    new_nodes.append(new_node)
                elif split_node[i] and i % 2 != 0:
                    new_node = TextNode(
                        link_list[link_list_index][0],
                        TextType.LINK,
                        link_list[link_list_index][1],
                    )
                    new_nodes.append(new_node)
                    link_list_index += 1
    return new_nodes


# Take a raw string of markdown textr and return a list of TextNodes
def text_to_textnodes(text):
    raw_node = TextNode(text, TextType.TEXT)
    return split_nodes_link(
        split_nodes_image(
            split_nodes_delimiter(
                split_nodes_delimiter(
                    split_nodes_delimiter([raw_node], "**", TextType.BOLD),
                    "_",
                    TextType.ITALIC,
                ),
                "`",
                TextType.CODE,
            )
        )
    )
