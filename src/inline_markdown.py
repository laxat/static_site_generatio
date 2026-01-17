import re

from htmlnode import LeafNode
from textnode import TextNode, TextType


def extract_markdown_images(text):
    if text is None:
        return ""
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches


def extract_markdown_links(text):
    if text is None:
        return ""

    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    node_list = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            node_list.extend([TextNode(node.text, node.text_type, node.url)])
        else:
            nodes = []
            text_blocks = node.text.split(delimiter)
            if len(text_blocks) % 2 == 0:
                raise ValueError("Improper use of delimiter detected")
            for i in range(0, len(text_blocks)):
                if text_blocks[i] != "":
                    if i % 2 != 0:
                        nodes.append(TextNode(text_blocks[i], text_type))
                    else:
                        nodes.append(TextNode(text_blocks[i], TextType.TEXT))
            node_list.extend(nodes)
    return node_list


def split_nodes_image(old_nodes):
    node_list = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            node_list.extend([node])
            continue

        images = extract_markdown_images(node.text)

        if len(images) <= 0:
            node_list.append(TextNode(node.text, TextType.TEXT))
            continue
        else:
            n = []
            current_text = node.text
            for alt, url in images:
                text_blocks = current_text.split(f"![{alt}]({url})", 1)

                if len(text_blocks) != 2:
                    raise ValueError("Improper use of the delimiter.")
                if text_blocks[0] != "":
                    n.append(TextNode(text_blocks[0], TextType.TEXT))
                n.append(TextNode(alt, TextType.IMAGE, url))

                current_text = text_blocks[1]

            if current_text != "":
                n.append(TextNode(current_text, TextType.TEXT))

            node_list.extend(n)
    return node_list


def split_nodes_link(old_nodes):
    node_list = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            node_list.extend([node])
            continue

        images = extract_markdown_links(node.text)

        if len(images) <= 0:
            node_list.append(TextNode(node.text, TextType.TEXT))
            continue
        else:
            n = []
            current_text = node.text
            for alt, url in images:
                text_blocks = current_text.split(f"[{alt}]({url})", 1)

                if len(text_blocks) != 2:
                    raise ValueError("Improper use of the delimiter.")
                if text_blocks[0] != "":
                    n.append(TextNode(text_blocks[0], TextType.TEXT))
                n.append(TextNode(alt, TextType.LINK, url))

                current_text = text_blocks[1]

            if current_text != "":
                n.append(TextNode(current_text, TextType.TEXT))

            node_list.extend(n)
    return node_list


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes


def text_node_to_html_node(text_node):
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
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise ValueError("Not a valid text type option")
