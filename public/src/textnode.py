from enum import Enum


class TextType(Enum):
        type_plain = "plain"
        type_bold = "bold"
        type_italic = "italic"
        type_code = "code"
        type_links = "links"
        type_images = "images"

class TextNode():
    def __init__(self, text, text_type, url=None):
        self.text = text
        if not isinstance(text_type, TextType):
            raise TypeError("text_type must be a valid member of TextType enum")
        self.text_type= text_type
        self.url = url

    def __eq__(self, other):
        if self.text == other.text and self.text_type == other.text_type and self.url == other.url:
            return True
        return False

    def __repr__(self):
        return (f"TextNode({self.text}, {self.text_type}, {self.url})")
