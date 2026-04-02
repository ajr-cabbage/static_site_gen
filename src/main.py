from textnode import TextNode, TextType


def main():
    new_text_node = TextNode(
        "This is some anchor text", TextType.TEXT, "https://www.boot.dev"
    )
    print(new_text_node)


if __name__ == "__main__":
    main()
