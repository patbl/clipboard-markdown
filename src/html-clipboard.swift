import Cocoa

func addMarginZeroToTags(_ html: String) -> String {
    // Wrap HTML in a root element to ensure it's valid XML
    let wrappedHTML = "<root>\(html)</root>"

    guard let xmlDoc = try? XMLDocument(xmlString: wrappedHTML, options: [.documentTidyHTML]) else {
        // If parsing fails, return original HTML
        return html
    }

    let tags = ["p", "ol", "ul", "li"]

    for tag in tags {
        let xpath = "//\(tag)"
        guard let elements = try? xmlDoc.nodes(forXPath: xpath) as? [XMLElement] else {
            continue
        }

        for element in elements {
            if let styleAttr = element.attribute(forName: "style") {
                // Append margin:0 to existing style
                let currentStyle = styleAttr.stringValue ?? ""
                let newStyle = currentStyle.isEmpty ? "margin:0" : "margin:0;\(currentStyle)"
                element.removeAttribute(forName: "style")
                element.addAttribute(XMLNode.attribute(withName: "style", stringValue: newStyle) as! XMLNode)
            } else {
                // Add new style attribute
                element.addAttribute(XMLNode.attribute(withName: "style", stringValue: "margin:0") as! XMLNode)
            }
        }
    }

    // Extract the content without the root wrapper
    guard let rootElement = xmlDoc.rootElement(),
          let children = rootElement.children else {
        return html
    }

    return children.map { $0.xmlString }.joined()
}

let args = CommandLine.arguments

if args.count < 2 {
    print("Usage: html-clipboard [get|set]")
    exit(1)
}

let board = NSPasteboard.general

if args[1] == "get" {
    // Read HTML from clipboard and print to stdout
    if let html = board.string(forType: .html) {
        print(html, terminator: "")
    }
} else if args[1] == "set" {
    // Read from stdin and write to clipboard as HTML
    let data = FileHandle.standardInput.readDataToEndOfFile()
    if let str = String(data: data, encoding: .utf8) {
        let modifiedHTML = addMarginZeroToTags(str)
        board.clearContents()
        board.setString(modifiedHTML, forType: .html)
        // Also set plain text version so it pastes nicely in code editors
        board.setString(modifiedHTML, forType: .string)
    }
}
