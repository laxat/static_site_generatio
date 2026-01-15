from enum import Enum


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
    lines = md.split("\n")

    if md.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
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
