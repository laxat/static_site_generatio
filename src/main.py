from block_markdown import block_to_block_type, block_type_to_html, markdown_to_html


def main():
    block = "# heading"

    type = block_to_block_type(block)
    html_node = block_type_to_html(type, block)

    block1 = "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line"
    type1 = block_to_block_type(block1)

    html_node_0 = block_type_to_html(type1, block1)

    # print(html_node)
    # print(html_node_0.value)
    md = """```
This is text that _should_ remain
the **same** even with inline stuff
```"""

    ans = markdown_to_html(md)
    # print(repr(ans.to_html()))

    md = """
    - This is a list
    - with items
    - and _more_ items

    1. This is an `ordered` list
    2. with items
    3. and more items

    """

    node = markdown_to_html(md)
    # html = node.to_html()

    print(node.to_html())


main()
