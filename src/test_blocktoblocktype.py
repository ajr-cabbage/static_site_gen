import unittest

from src.blocktype import BlockType
from src.functions import block_to_blocktype


class TestBlockToBlockType(unittest.TestCase):
    heading_test = "### This is a heading!!!"
    code_test = """```
def function_name():
    this = "test"
```"""
    quote_block_test = """> This is some multi-line quote shenanigans.
>This line doesn't have a space after the symbol.
>  This one has two spaces."""
    unordered_list_test = """- unordered
- list
- example"""
    ordered_list_test = """1. This
2. should
3. be a properly
4. properly formatted
5. ordered list case"""
    paragraph_test = """> this should
2. return as a
- paragraph"""

    def test_heading(self):
        self.assertEqual(block_to_blocktype(self.heading_test), BlockType.HEADING)

    def test_code(self):
        self.assertEqual(block_to_blocktype(self.code_test), BlockType.CODE)

    def test_quote(self):
        self.assertEqual(block_to_blocktype(self.quote_block_test), BlockType.QUOTE)

    def test_unordered_list(self):
        self.assertEqual(
            block_to_blocktype(self.unordered_list_test), BlockType.UNORDERED_LIST
        )

    def test_ordered_list(self):
        self.assertEqual(
            block_to_blocktype(self.ordered_list_test), BlockType.ORDERED_LIST
        )

    def test_paragraph(self):
        self.assertEqual(block_to_blocktype(self.paragraph_test), BlockType.PARAGRAPH)
