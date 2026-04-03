from src.htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, value=None, children=children, props=props)

    def to_html(self):
        if not self.tag:
            raise ValueError("Parent nodes require tags")
        if not self.children:
            raise ValueError("Parent nodes require child(ren)")
        children_str = ""
        for child in self.children:
            children_str = children_str + child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{children_str}</{self.tag}>"
