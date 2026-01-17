import os
import shutil as sh
from pathlib import Path

from block_markdown import markdown_to_html


def copy_static_to_public(src_path, dest_path):
    try:
        if os.path.exists(dest_path):
            sh.rmtree(dest_path)
        os.mkdir(dest_path)
        for i in os.listdir(src_path):
            curr_path = os.path.join(src_path, i)
            if os.path.isfile(curr_path):
                sh.copy(curr_path, dest_path)
            else:
                new_dest_path = os.path.join(dest_path, i)
                copy_static_to_public(curr_path, new_dest_path)

        # sh.copytree(src_path, dest_path)
    except Exception as e:
        print(e)


def extract_title(md):
    for line in md.splitlines():
        line = line.strip()
        if line.startswith("# ") and not line.startswith("##"):
            return line[2:].strip()
        if line == "#":  # edge case: "#" alone
            return ""
    raise Exception("No h1 header found")


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r") as f:
        md_contents = f.read()

    with open(template_path, "r") as h:
        html_contents = h.read()

    md_html = markdown_to_html(md_contents).to_html()
    title = extract_title(md_contents)

    html_contents = html_contents.replace("{{ Title }}", title)
    html_contents = html_contents.replace("{{ Content }}", md_html)

    if not os.path.exists(dest_path):
        dest_path = Path(dest_path)
        dest_path.parent.mkdir(exist_ok=True, parents=True)

    with open(dest_path, "w") as f:
        f.write(html_contents)


def generate_pages_recursive(dir_path_content, template_path, dest_path):
    try:
        if not os.path.exists(dir_path_content) and not dest_path.info.exists():
            raise FileNotFoundError("This file path does not exist")

        for i in os.listdir(dir_path_content):
            curr_path = os.path.join(dir_path_content, i)
            if os.path.isfile(curr_path) and ".md" in curr_path:
                index_path = Path(f"{dest_path}/index.html")
                generate_page(curr_path, template_path, index_path)
            else:
                new_dest_path = os.path.join(dest_path, i)
                dest_path_folder = Path(new_dest_path)
                generate_pages_recursive(curr_path, template_path, dest_path_folder)
    except Exception as e:
        print(e)
