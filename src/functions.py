import re

from src.blocktype import BlockType
from src.leafnode import LeafNode
from src.parentnode import ParentNode
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


# Takes raw Markdown string and returns list of "block" strings.
def markdown_to_blocks(markdown):
    blocks = []
    md_blocks = markdown.split("\n\n")
    for md_block in md_blocks:
        if md_block:
            blocks.append(md_block.strip())
    return blocks


# inspect block (str) of markdown text and return correct BlockType
def block_to_blocktype(block):
    # simple cases
    if re.match(r"[#]{1,6} ", block):
        return BlockType.HEADING
    if block.startswith("```\n") and block.endswith("```"):
        return BlockType.CODE
    # multi-line cases
    lines = block.split("\n")
    quote_block = False
    unordered_list = False
    ordered_list = False
    if lines[0].startswith(">"):
        quote_block = True
        for line in lines:
            if not line.startswith(">"):
                quote_block = False
                break
    if lines[0].startswith("- "):
        unordered_list = True
        for line in lines:
            if not line.startswith("- "):
                unordered_list = False
                break
    if lines[0].startswith("1. "):
        ordered_list = True
        for i in range(len(lines)):
            if not lines[i].startswith(f"{i + 1}. "):
                ordered_list = False
    if quote_block:
        return BlockType.QUOTE
    elif unordered_list:
        return BlockType.UNORDERED_LIST
    elif ordered_list:
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH


# takes MD text and returns a list of child html nodes
def text_to_children(block_text):
    html_nodes = []
    text_nodes = text_to_textnodes(block_text)
    for text_node in text_nodes:
        html_nodes.append(text_node_to_html_node(text_node))
    if len(html_nodes) > 1:
        return html_nodes
    else:
        return []


def get_list_item_html_nodes(list_text):
    line_html_nodes = []
    lines = list_text.split("\n")
    for line in lines:
        split_line = line.split()
        cleaned_text = " ".join(split_line[1:])
        children = text_to_children(cleaned_text)
        if not children:
            line_html_nodes.append(LeafNode("li", cleaned_text))
        else:
            line_html_nodes.append(ParentNode("li", children))
    return line_html_nodes


def create_block_node(block_text, block_type):
    if block_type == BlockType.CODE:
        split_block = block_text.split("\n")
        cleaned_text = "\n".join(split_block[1:-1]) + "\n"
        plain_txt_node = text_node_to_html_node(TextNode(cleaned_text, TextType.TEXT))
        inner_node = ParentNode("code", [plain_txt_node])
        return ParentNode("pre", [inner_node])
    match block_type:
        case BlockType.PARAGRAPH:
            split_block = block_text.split()
            cleaned_text = " ".join(split_block)
            children = text_to_children(cleaned_text)
            if not children:
                return LeafNode("p", cleaned_text)
            else:
                return ParentNode("p", children)
        case BlockType.HEADING:
            hash_count = 0
            for char in block_text[0:6]:
                if char == "#":
                    hash_count += 1
            split_block = block_text[hash_count:].split()
            cleaned_text = " ".join(split_block)
            children = text_to_children(cleaned_text)
            if not children:
                return LeafNode(f"h{hash_count}", cleaned_text)
            else:
                return ParentNode(f"h{hash_count}", children)
        case BlockType.QUOTE:
            lines = block_text.split("\n")
            for i in range(len(lines)):
                lines[i] = lines[i].lstrip(">").strip()
            cleaned_text = " ".join(lines)
            children = text_to_children(cleaned_text)
            if not children:
                return LeafNode("blockquote", cleaned_text)
            else:
                return ParentNode("blockquote", children)
        case BlockType.UNORDERED_LIST:
            return ParentNode("ul", get_list_item_html_nodes(block_text))
        case BlockType.ORDERED_LIST:
            return ParentNode("ol", get_list_item_html_nodes(block_text))
        case _:
            raise Exception("Bad BlockType")


def markdown_to_html_node(markdown):
    block_html_nodes = []
    md_blocks = markdown_to_blocks(markdown)
    for i in range(len(md_blocks)):
        # print(type(create_block_node(md_blocks[i], block_to_blocktype(md_blocks[i]))))
        block_html_nodes.append(
            create_block_node(md_blocks[i], block_to_blocktype(md_blocks[i]))
        )
    return ParentNode("div", block_html_nodes)
