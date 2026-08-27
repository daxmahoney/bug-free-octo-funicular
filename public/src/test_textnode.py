import unittest
from textnode import TextNode, TextType, text_node_to_html_node, split_nodes_delimiter, extract_markdown_images, extract_markdown_links


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_url(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_None_url(self):
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(None, node2.url)

    def test_text_type_property(self):
        node3 = TextNode("some_text", TextType.ITALIC)
        node4 = TextNode("some_text", TextType.ITALIC)
        self.assertEqual(node3.text_type, node4.text_type)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_new_node_types(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        test_node_list = [TextNode("This is text with a ", TextType.TEXT), 
                          TextNode("code block", TextType.CODE), 
                          TextNode(" word", TextType.TEXT)]
        self.assertEqual(new_nodes, test_node_list)

def test_extract_markdown_images(self):
    matches = extract_markdown_images(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
    )
    self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

def test_extract_markdown_links(self):
    matches = extract_markdown_links(
        "This is text with a link [to yahoo](https://www.yahoo.com) and [to youtube](https://www.youtube.com)"
    )
    self.assertListEqual([("to yahoo","https://www.yahoo.com" ), ("to youtube", "https://www.youtube.com")], matches)

if __name__ == "__main__":
    unittest.main()