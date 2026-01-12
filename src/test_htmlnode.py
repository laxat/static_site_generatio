import unittest

from htmlnode import HTMLNode, LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        my_props = {"onhover": "show"}
        node = HTMLNode("button", "Click me", props=my_props)
        solution = ' onhover="show"'

        self.assertEqual(node.props_to_html(), solution)

    def test_prop_to_html2(self):
        node = HTMLNode("button", "Click me")
        solution = " onhover=show"

        self.assertNotEqual(node.props_to_html(), solution)

    def test_prop_to_html3(self):
        test_props = {"onhover": "show", "color": "red"}

        node = HTMLNode("button", "Click me", props=test_props)

        solution = ' onhover="show" color="red"'

        self.assertEqual(node.props_to_html(), solution)

    def test_html_node(self):
        node = HTMLNode("button", "Click me")

        solution = "<button>Click me</button>"

        self.assertEqual(repr(node), solution)

    def test_html_node2(self):
        test_props = {"onhover": "show"}
        node = HTMLNode("button", "Click me", props=test_props)

        solution = '<button onhover="show">Click me</button>'

        self.assertEqual(repr(node), solution)

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")


if __name__ == "__main__":
    unittest.main()
