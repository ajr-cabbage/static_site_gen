class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag  # string - html tag name
        self.value = value  # string - what's in the tag
        self.children = children  # list - HTMLNode objects
        self.props = props  # dict - attributes ex. {"href":"https://google.com"}

    def __repr__(self):
        return f"tag: {self.tag}\nvalue: {self.value}\nchildren: {self.children}\nprops:{self.props}"

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if not self.props:
            return ""
        html_props = ""
        for key in list(self.props):
            html_props = html_props + " " + f'{key}="{self.props[key]}"'
        return html_props
