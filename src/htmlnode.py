class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __repr__(self):
        if not self.tag:
            return f"{self.value}"
        return f"<{self.tag}{self.props_to_html()}>{self.value if self.value else self.children}</{self.tag}>"

    # def __repr__(self):
    #         return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"

    def to_html(self):
        raise NotImplementedError("Not implemented yet...")

    def props_to_html(self):
        if self.props is None:
            return ""
        start = ""
        for x, y in self.props.items():
            start += f' {x}="{y}"'
        return start


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, props=props)

    # def __repr__(self):
    #     return f"LeafNode({self.tag}, {self.value}, {self.props})"

    def to_html(self):
        if self.value is None:
            raise ValueError(f"All leaf nodes must have a value. Cause by {self}")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, children=children, props=props)

    def to_html(self):
        if not self.tag:
            raise ValueError

        if not self.children:
            raise ValueError("Parent node needs to have children elements")

        else:
            html_str = f"<{self.tag}{self.props_to_html()}>"
            for child in self.children:
                html_str += child.to_html()
            html_str += f"</{self.tag}>"
            return html_str
