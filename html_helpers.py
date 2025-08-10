from pyscript import document
from pyscript.web import Element


def _tag(tag_name: str, *children: Element | str, **attributes: str) -> Element:
    node = document.createElement(tag_name)
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
