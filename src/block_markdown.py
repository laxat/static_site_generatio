import re
from enum import Enum

from htmlnode import HTMLNode, LeafNode, ParentNode
from inline_markdown import text_node_to_html_node, text_to_textnodes
from textnode import TextNode, TextType


class BlockType(Enum):
    PARAGRAPH = "p"
    HEADING = "h"
    CODE = "c"
    QUOTE = "q"
    UNORDERED_LIST = "u"
    ORDERED_LIST = "o"


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    blocks = [x.strip() for x in blocks if x != ""]
    blocks = [s.replace("\n    ", "\n") for s in blocks]

    return blocks


def block_to_block_type(md):
    lines = md.strip().split("\n")

    if md.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].endswith("```"):
        return BlockType.CODE
    if md.startswith("> "):
        for line in lines:
            if not line.startswith("> "):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if md.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    if md.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH


def markdown_to_html(md):
    md_blocks = markdown_to_blocks(md)

    children = []

    for block in md_blocks:
        if len(block) > 0:
            type = block_to_block_type(block)
            html_node = block_type_to_html(type, block)
            children.append(html_node)
    return ParentNode("div", children, None)


def text_to_children(text):
    nodes = text_to_textnodes(text)
    node_list = []
    for node in nodes:
        node_list.append(text_node_to_html_node(node))
    return node_list


def block_type_to_html(type, block) -> HTMLNode:
    lines = block.split("\n")

    match type:
        case BlockType.PARAGRAPH:
            paragraph = " ".join(lines)
            children = text_to_children(strip_md(paragraph))
            return ParentNode("p", children)
        case BlockType.HEADING:
            i = 0
            while block[i] == "#":
                i += 1
                if block[i] != "#":
                    break
            children = text_to_children(strip_md(block))
            return ParentNode(f"h{i}", children=children)
        case BlockType.QUOTE:
            new_lines = []
            for line in lines:
                if not line.startswith(">"):
                    raise ValueError("invalid quote block")
                new_lines.append(strip_md(line))
            quote = " ".join(new_lines)
            children = text_to_children(strip_md(quote))
            return ParentNode("blockquote", children)
        case BlockType.CODE:
            text = strip_md(block)
            text_node = TextNode(text, TextType.TEXT)
            children = text_node_to_html_node(text_node)
            code_block = ParentNode("code", [children])
            return ParentNode("pre", children=[code_block])
        case BlockType.ORDERED_LIST:
            full_list = []
            for line in lines:
                if line != " ":
                    children = text_to_children(strip_md(line))
                    full_list.append(ParentNode("li", children))
            return ParentNode("ol", children=full_list)
        case BlockType.UNORDERED_LIST:
            full_list = []
            for line in lines:
                children = text_to_children(strip_md(line))
                full_list.append(ParentNode("li", children))
            return ParentNode("ul", children=full_list)
        case _:
            raise ValueError("This is not the correct node type")


def strip_md(s):
    s = re.sub(r"```(?:[^\n]*)\n?([\s\S]*?)```", r"\1", s)  # fenced code blocks
    # s = re.sub(r"`([^`]*)`", r"\1", s)  # inline code
    s = re.sub(r"^>\s?", "", s, flags=re.M)  # blockquotes
    s = re.sub(r"^#{1,6}\s*", "", s, flags=re.M)  # headings
    s = re.sub(r"^[-*+]\s+", "", s, flags=re.M)  # unordered lists
    s = re.sub(r"^\d+\.\s+", "", s, flags=re.M)  # ordered lists
    return re.sub(r"\n{3,}", "\n\n", s)  # extra newlines
