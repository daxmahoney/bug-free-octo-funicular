from enum import Enum
from htmlnode import LeafNode
import re


class TextType(Enum):
        TEXT = "plain"
        BOLD = "bold"
        ITALIC = "italic"
        CODE = "code"
        LINK = "link"
        IMAGE = "image"

class TextNode():
    def __init__(self, text, text_type, url=None):
        self.text = text
        if not isinstance(text_type, TextType):
            raise TypeError("text_type must be a valid member of TextType enum")
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if self.text == other.text and self.text_type == other.text_type and self.url == other.url:
            return True
        return False

    def __repr__(self):
        return (f"TextNode({self.text}, {self.text_type}, {self.url})")

def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    if not isinstance(text_node.text_type, TextType):
        raise TypeError("text_type must be a valid member of TextType enum")

    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", None, {"src": text_node.url, "alt": text_node.text})
        case _:
            raise ValueError("outside the enum class")

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    """
    node = TextNode("This is text with a `code block` word", TextType.TEXT)
    new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
    """
    for node in old_nodes:
        the_string = node.text.split(delimiter)
        first_node = TextNode(the_string[0], TextType.TEXT)
        if delimiter == "**":
            second_node_type = TextType.BOLD
        elif delimiter == "`":
            second_node_type = TextType.CODE
        elif delimiter == "_":
            second_node_type = TextType.ITALIC
        else:
            second_node_type = TextType.TEXT

        second_node = TextNode(the_string[1], second_node_type)
        third_node = TextNode(the_string[2], TextType.TEXT)
        new_nodes = [first_node, second_node, third_node]
        # this is just placeholder
        return new_nodes

def extract_markdown_images(text):
        #returns list of tuples and images
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    # returns list of tuples and links
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        current_text = old_node.text
        images = extract_markdown_images(current_text)

        # keep intact if no images
        if not images:
            new_nodes.append(old_node)
            continue

    for image_alt, image_link in images:
        markdown_str = f"![{image_alt}]({image_link})"
        sections = current_text.split(markdown_str, 1)

        if len(sections) !=2:
            continue

        before, after = sections
        if before:
            new_nodes.append(TextNode(before, TextType.TEXT))
        new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))
        current_text = after

    if current_text:
        new_nodes.append(TextNode(current_text, TextType.TEXT))

    return new_nodes

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
    
        current_text = old_node.text
        links = extract_markdown_links(current_text)
    
            # keep intact if no images
        if not links:
            new_nodes.append(old_node)
            continue
    
        for alt_text, link in links:
            markdown_str = f"[{alt_text}]({link})"
            sections = current_text.split(markdown_str, 1)
    
            if len(sections) !=2:
                continue
    
            before, after = sections
            if before:
                new_nodes.append(TextNode(before, TextType.TEXT))
            new_nodes.append(TextNode(alt_text, TextType.LINK, link))
            current_text = after
    
        if current_text:
            new_nodes.append(TextNode(current_text, TextType.TEXT))
    
        return new_nodes