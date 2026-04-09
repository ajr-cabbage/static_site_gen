import os
import sys

from functions import copy_dir_contents, generate_page_recursive


def main():
    basepath = "/"
    args = sys.argv
    if len(args) > 1:
        basepath = args[1]
    print(f"BASEPATH: {basepath}")
    source_dir = os.path.abspath("./static")
    target_dir = os.path.abspath("./docs")
    copy_dir_contents(source_dir, target_dir)
    generate_page_recursive("./content", "./template.html", "./docs", basepath)


if __name__ == "__main__":
    main()
