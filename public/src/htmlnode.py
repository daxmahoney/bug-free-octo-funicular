from textnode import block_to_block_type, text_node_to_html_node, \
                     text_to_textnodes, markdown_to_blocks, BlockType


class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplemented

    def props_to_html(self):
        if self.props is None:
            return ""
        composed_string = []
        for k,v in self.props:
            composed_string.append(f"{k}={v}")
        return " ".join(composed_string)

    def __repr__(self):
        return f"{self.tag} {self.value} {self.children} {self.props}"

class LeafNode(HTMLNode):
    def __init__(self, tag,  value=None, props=None):
        super().__init__(tag=tag, value=value,  children=None, props=props)

    def __repr__(self):
        return f"{self.tag} {self.value} {self.props}"

    def to_html(self):
        if not self.value:
            raise ValueError
        if not self.tag:
            return self.value
        if self.tag == "a":
            return f'<{self.tag} href="{self.props["href"]}">{self.value}</{self.tag}>'
        else:
            return f"<{self.tag}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode): 
    def __init__(self, tag, children, props=None):
        super().__init__(tag, value=None, children=children, props=props)

    def to_html(self):
        if not self.tag:
            raise ValueError("ain't got no tag")
        if not self.children:
            raise ValueError("no children")
        if self.tag == "a":
            parent = f'<{self.tag} href="{self.props["href"]}">{self.value}</{self.tag}>'
            return parent and self.child.to_html()
        else:
            parent = f"<{self.tag}>{self.value}</{self.tag}>"
            return parent and self.child.to_html()

def markdown_to_html_node(markdown):
    some_blocks = markdown_to_blocks(markdown)

    for block in some_blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.PARAGRAPH:
            lines = block.split("\n")
            text = " ".join(lines)
            lots_of_nodes = text_to_textnodes(text)
            result_nodes = []
            for lot in lots_of_nodes:
                result_nodes.append(text_node_to_html_node(lot))
            return ParentNode("p", result_nodes)

        if block_type == BlockType.HEADING:
            lines = block.split("\n")
            first_line = lines[0]
            count_level = len(first_line) - len(first_line.lstrip('#')) #whole - part_minus_heading = level

            text = " ".join(lines)
            clean_text = text[count_level:].strip()

            lots_of_nodes = text_to_textnodes(clean_text)
            result_nodes = []
            for lot in lots_of_nodes:
                result_nodes.append(text_node_to_html_node(lot))
            return ParentNode(f"h{count_level}", result_nodes)


        # Block text → child HTML nodes
        # Block nodes → one parent <div>
"""Next:
- Finish heading: count only leading # characters
- Remove "#... " before inline parsing
- Append each block node to an outer list
- Return ParentNode("div", block_nodes)
"""
