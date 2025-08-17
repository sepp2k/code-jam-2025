from html_helpers import a, button, nav, img, div
from pyscript.web import Element


def custom_nav() -> Element:
    """Create a custom navigation element."""
    a_style = "color: white; text-decoration: none; margin-right: 1em;"
    a_onmouseover = "this.style.textDecoration = 'underline';"
    a_onmouseleave = "this.style.textDecoration = 'none';"
    return nav(
        div(
            a(img(src="/assets/icon.png", alt="Logo", style="width: 3em"), href="/index.html"),
            a("Home", href="/index.html", style=a_style, onmouseover=a_onmouseover, onmouseleave=a_onmouseleave),
            a("About", href="/about.html", style=a_style, onmouseover=a_onmouseover, onmouseleave=a_onmouseleave),
            a("Exercises", href="/exercises.html", style=a_style, onmouseover=a_onmouseover, onmouseleave=a_onmouseleave),
            style="display: flex; align-items: center; justify-items: center; gap: 1em;"
        ),
        style="background-color: #333;color: white;padding: 0.5em 1em;",
    )


def custom_button(text: str) -> Element:
    """Create a custom button element."""
    button_style = "background-color: #4CAF50; color: white; border: none; padding: 0.5em 1em; cursor: pointer;"
    return button(text, style=button_style)
