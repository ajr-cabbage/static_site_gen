import os
import sys

from functions import copy_dir_contents, generate_page_recursive


def main():
    basepath = "/"
    args = sys.argv
    if args[0]:
        basepath = args[0]
    source_dir = os.path.abspath("./static")
    target_dir = os.path.abspath("./docs")
    copy_dir_contents(source_dir, target_dir)
    generate_page_recursive("./content", "./template.html", "./docs", basepath)


if __name__ == "__main__":
    main()
