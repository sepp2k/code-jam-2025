from pyscript import document
from pyscript.web import Element


def _tag(tag_name: str, *children: Element | str, **attributes: str) -> Element:
    node = document.createElement(tag_name)
    if "className" in attributes:
        node.setAttribute("class", attributes["className"])
    for key, value in attributes.items():
        node.setAttribute(key, value)
    for child in children:
        node.append(child)
    return node


def h1(*children: Element | str, **attributes: str) -> Element:
    """Create an top level heading."""
    return _tag("h1", *children, **attributes)


def h2(*children: Element | str, **attributes: str) -> Element:
    """Create a second level heading."""
    return _tag("h2", *children, **attributes)


def div(*children: Element | str, **attributes: str) -> Element:
    """Create a div element."""
    return _tag("div", *children, **attributes)


def p(*children: Element | str, **attributes: str) -> Element:
    """Create a paragraph."""
    return _tag("p", *children, **attributes)


def br() -> Element:
    """Create a line break that does not start a new paragraph."""
    return _tag("br")


def em(*children: Element | str, **attributes: str) -> Element:
    """Create an em element."""
    return _tag("em", *children, **attributes)


def textarea(*children: Element | str, **attributes: str) -> Element:
    """Create a text area."""
    return _tag("textarea", *children, **attributes)


def button(*children: Element | str, **attributes: str) -> Element:
    """Create a button."""
    return _tag("button", *children, **attributes)


def iframe(*children: Element | str, **attributes: str) -> Element:
    """Create an iframe."""
    return _tag("iframe", *children, **attributes)


def nav(*children: Element | str, **attributes: str) -> Element:
    """Create a nav element."""
    return _tag("nav", *children, **attributes)


def a(*children: Element | str, **attributes: str) -> Element:
    """Create an anchor element."""
    return _tag("a", *children, **attributes)


def code(*children: Element | str, **attributes: str) -> Element:
    """Create a code element."""
    return _tag("code", *children, **attributes)


def span(*children: Element | str, **attributes: str) -> Element:
    """Create a span element."""
    return _tag("span", *children, **attributes)


def b(*children: Element | str, **attributes: str) -> Element:
    """Create a bold element."""
    return _tag("b", *children, **attributes)


def i(*children: Element | str, **attributes: str) -> Element:
    """Create an italic element."""
    return _tag("i", *children, **attributes)


def img(*children: Element | str, **attributes: str) -> Element:
    """Create an image element."""
    return _tag("img", *children, **attributes)


def hr(**attributes: str) -> Element:
    """Create a horizontal rule."""
    default_style = "border: none; border-top: 1px solid #ccc; margin: .1em 0;"
    if "style" in attributes:
        attributes["style"] += default_style
    else:
        attributes["style"] = default_style
    return _tag("hr", **attributes)
