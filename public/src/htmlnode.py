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