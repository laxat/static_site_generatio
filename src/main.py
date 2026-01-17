from sys import argv

from static_gen import (
    copy_static_to_public,
    extract_title,
    generate_page,
    generate_pages_recursive,
)


def main():
    basepath = argv[1]

    copy_static_to_public("static", "docs")

    # print(extract_title("# Hello"))  # "Hello"
    # print(extract_title("## Subheading\n# Hi"))  # "Hi"
    # print(extract_title("No title here"))
    # generate_page("content/index.md", "template.html", "public/car/index.html")
    generate_pages_recursive("content", "template.html", "docs", basepath)


main()
