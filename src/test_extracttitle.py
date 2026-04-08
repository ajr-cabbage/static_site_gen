import unittest

from src.functions import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_simple_header(self):
        md = "# This is the header"
        result = extract_title(md)
        self.assertEqual(result, "This is the header")

    def test_multi_line(self):
        md = """
## Not the header
### Still not the header
# header
"""
        result = extract_title(md)
        self.assertEqual(result, "header")

    def test_no_header(self):
        md = """
## No headers
- to be

- found

**here**
"""

        with self.assertRaises(Exception):
            result = extract_title(md)
