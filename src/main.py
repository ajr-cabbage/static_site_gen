import os
import shutil

from textnode import TextNode, TextType


def copy_dir_contents(source_path, dest_path):
    if os.path.exists(dest_path):
        shutil.rmtree(dest_path)
    os.mkdir(dest_path)
    dir_contents = os.listdir(source_path)
    copied_files = []
    for content in dir_contents:
        content_path = os.path.join(source_path, content)
        if os.path.isfile(content_path):
            copied_files.append(shutil.copy(content_path, dest_path))
        else:
            new_dest = os.path.join(dest_path, content)
            copy_dir_contents(content_path, new_dest)


def main():
    source_dir = os.path.abspath("./static")
    target_dir = os.path.abspath("./public")
    copy_dir_contents(source_dir, target_dir)


if __name__ == "__main__":
    main()
