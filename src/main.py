from textnode import TextNode, TextType

import os
import shutil


def copy_dir_contents(source_path, dest_path):
    if not os.path.exists(dest_path):
        os.mkdir(dest_path)
    dir_contents = os.listdir(source_path)
    copied_files = []
    for content in dir_contents:
        content_path = os.path.join(source_path, content)
        if os.path.isfile(content_path):
            copied_files.append(shiutil.copy(content_path, dest_path))
        else:
            new_dest = os.path.join(dest_path, content)
            copy_dir_contents(content_path, new_dest)
    
    
    


def main():
    
    copy_dir_contents("../static", "../public")


if __name__ == "__main__":
    main()
