class HtmlNode():
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children :list[HtmlNode] = children 
        self.props: dict = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if self.props is None:
            return ""
        html_props = ""
        for prop, value in self.props.items():
            html_props += f' {prop}="{value}"'
        return html_props


    def __repr__(self):
        return f"Htmlnode({self.tag}, {self.value}, {self.children}, {self.props})"
    

class LeafNode(HtmlNode):

    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("All leaf nodes must have a value")
        
        if self.tag is None:
            return self.value
        
        if self.tag == "img":
            return f"<img{self.props_to_html()}>"
        
        if not self.props:
            return f"<{self.tag}>{self.value}</{self.tag}>"
        
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
    def __repr__(self):
        return f"Htmlnode({self.tag}, {self.value}, {self.props})"


class ParentNode(HtmlNode):

    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):

        if not self.tag:
            raise ValueError("All parent nodes must have a tag")
        if not self.children:
            raise ValueError("All parent nodes must have children")
        html_text=""
        if not self.props:
            html_text += f"<{self.tag}>"
        else: 
            html_text += f"<{self.tag}{self.props_to_html()}>"

        for node in self.children:
            html_text += node.to_html()

        html_text += f"</{self.tag}>"

        return html_text