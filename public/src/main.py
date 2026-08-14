from textnode import TextNode, TextType

def main():
    node1 = TextNode("sup", TextType.type_italic, "www.yahoo.com")
    node2 = TextNode("larry", TextType.type_bold, "www.google.com")
    node3 = TextNode("small people", TextType.type_links, "www.reddit.com")
    # print(node1.eq.node3)
    print(node2.__repr__())
    print(f"is node 1 equal to node 2, {node1 == node2}")
    # node4 = TextNode("smart people", "blaze", "www.cookies.com")
    print(node2)
    
if __name__ == "__main__":
    main()