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

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"
    NORMAL = "normal"

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
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        if delimiter not in old_node.text:
            new_nodes.append(old_node)
            continue

        parts = old_node.text.split(delimiter)

        if len(parts) % 2 == 0:
            raise ValueError("malformed markdown")

        for i in range(len(parts)):
            if parts[i] == "":
                continue

            if i % 2 == 0:
                new_nodes.append(TextNode(parts[i], TextType.TEXT))
            else:
                new_nodes.append(TextNode(parts[i], text_type))
       
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

def text_to_textnodes(text):
    raw_node = TextNode(text, TextType.TEXT)
    raw_nodes = [raw_node]
    new_nodes = split_nodes_delimiter(raw_nodes, "**", TextType.BOLD)
    print(f"After BOLD: {new_nodes}")  # Should be a list
    new_nodes = split_nodes_delimiter(new_nodes, "`",  TextType.CODE)
    print(f"After Code: {new_nodes}")  # Should be a list
    new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
    print(f"After italic: {new_nodes}")  # Should be a list
    new_nodes = split_nodes_image(new_nodes)
    new_nodes = split_nodes_link(new_nodes) 
    return new_nodes

def markdown_to_blocks(markdown):
    large_blocks = markdown.split("\n\n").strip()
    answer = []
    for i in large_blocks:
        if i is not None:
            answer.append(i)
    return answer

def block_to_block_type(markdown):
    #headings
    if re.match(r"^#{1,6}\s", markdown):
        return BlockType.HEADING
    #code blocks
    if markdown.startswith("```\n") and markdown.endswith("```"):
        return BlockType.CODE
    #quote block
    if markdown.startswith(">"):
        return BlockType.QUOTE
    #unordered list
    if markdown.startswith("-"):
        return BlockType.UNORDERED_LIST
    #ordered list
    lines = [line for line in markdown.splitlines()]
    for index, line in enumerate(lines):
        expected_number = index + 1
        pattern = rf"^{expected_number}\.\s"

        if not re.match(pattern, line):
            pass
        else:
            return BlockType.ORDERED_LIST
    #normal paragraph
    return BlockType.NORMAL
