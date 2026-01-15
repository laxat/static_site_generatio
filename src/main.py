from inline_markdown import split_nodes_delimiter, text_to_textnodes
from textnode import TextNode, TextType


def main():
    # new = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")

    # new1 = TextNode("This is **bold** text used", TextType.TEXT)
    # new2 = TextNode("This is **sparta on it**", TextType.TEXT)

    # new1m = split_nodes_delimiter([new1, new2], "**", TextType.BOLD)
    # new2m = split_nodes_delimiter([new2], "*", TextType.ITALIC)
    # new_html = text_node_to_html_node(new)
    # print(new_html)

    # print(new1m)
    # print(new2m)
    # text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
    # text_image = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"

    # text_img1 = (
    #     "This is text with a link ![to boot dev](https://www.boot.dev) and other folks"
    # )
    # new3 = TextNode(text_image, TextType.TEXT)
    # new4 = TextNode(text_img1, TextType.TEXT)
    # print(split_nodes_image([new4, new3]))

    # node = TextNode("This is text with a **bolded** word", TextType.TEXT)
    # new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
    # self.assertListEqual(
    #     [
    #         TextNode("This is text with a ", TextType.TEXT),
    #         TextNode("bolded", TextType.BOLD),
    #         TextNode(" word", TextType.TEXT),
    #     ],
    #     new_nodes,
    # )
    node = TextNode("**bold** and _italic_", TextType.TEXT)
    new_nodes_old = split_nodes_delimiter([node], "**", TextType.BOLD)
    new_nodes = split_nodes_delimiter(new_nodes_old, "_", TextType.ITALIC)

    print(new_nodes_old)
    print(new_nodes)


main()
