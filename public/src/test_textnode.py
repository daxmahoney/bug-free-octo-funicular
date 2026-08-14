import unittest
from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.type_bold)
        node2 = TextNode("This is a text node", TextType.type_bold)
        self.assertEqual(node, node2)

    def test_url(self):
        node = TextNode("This is a text node", TextType.type_bold)
        node2 = TextNode("This is a text node", TextType.type_bold)
        self.assertEqual(node, node2)

    def test_None_url(self):
        node2 = TextNode("This is a text node", TextType.type_bold)
        self.assertEqual(None, node2.url)

    def test_text_type_property(self):
        node3 = TextNode("some_text", TextType.type_italic)
        node4 = TextNode("some_text", TextType.type_italic)
        self.asserEqual(node3.text_type, node4.text_type)


if __name__ == "__main__":
    unittest.main()