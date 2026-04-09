import os

from functions import copy_dir_contents, generate_page_recursive


def main():
    source_dir = os.path.abspath("./static")
    target_dir = os.path.abspath("./public")
    copy_dir_contents(source_dir, target_dir)
    generate_page_recursive("./content", "./template.html", "./public")


if __name__ == "__main__":
    main()
