from html_helpers import _tag, a, button, div, img, nav, span
from pyscript.web import Element


def custom_nav() -> Element:
    """Create a custom navigation element."""
    a_style = "color: white; text-decoration: none; margin-right: 1em;"
    a_onmouseover = "this.style.textDecoration = 'underline';"
    a_onmouseleave = "this.style.textDecoration = 'none';"
    return nav(
        div(
            a(img(src="/assets/icon.png", alt="Logo", style="width: 3em"), href="/"),
            a("Home", href="/", style=a_style, onmouseover=a_onmouseover, onmouseleave=a_onmouseleave),
            a(
                "Exercises",
                href="/exercises.html",
                style=a_style,
                onmouseover=a_onmouseover,
                onmouseleave=a_onmouseleave,
            ),
            style="display: flex; align-items: center; justify-items: center; gap: 1em;",
        ),
        style="background-color: #333;color: white;padding: 0.5em 1em;"
        "box-shadow: rgba(60, 64, 67, 0.3) 0px 1px 2px 0px, rgba(60, 64, 67, 0.15) 0px 2px 6px 2px;",
    )


def custom_button(text: str) -> Element:
    """Create a custom button element."""
    button_style = "background-color: #4CAF50; color: white; border: none; padding: 0.5em 1em; cursor: pointer;"
    return button(text, style=button_style)


def custom_code_block(text: str, *children: str | Element, **attributes: str) -> Element:
    """Create a custom code block element."""
    if children:
        text = "\n".join([text, *list(children)])

    pre = _tag(
        "pre",
        text,
        style='margin: 1em 0em 0 0; font-family: "Google Sans Code", serif;',
    )

    language_tip = None
    language_style = "position: absolute; top: .2em; left: .2em; color:white; font-size: 0.8rem"
    if attributes.get("language"):
        language_tip = span(attributes["language"], style=language_style)
    language_tip = language_tip or span("text", style=language_style)

    make_copy = attributes.get("copy_tip", "copy")
    copy_tip = a(
        span("📄 copy"),
        onclick=f"copyToClipboard(`{text}`, () => {{ this.querySelector('span').textContent = '✔ copied';"
        "setTimeout(() => this.querySelector('span').textContent = '📄 copy', 2000); })",
        style=f"{language_style}; text-decoration: none; left: initial; right: .2em;",
        onmouseover="this.querySelector('span').style.textDecoration = 'underline';",
        onmouseleave="this.querySelector('span').style.textDecoration = 'none';",
    )

    return div(
        pre,
        language_tip,
        (copy_tip if make_copy!="none" else ""),
        style="position: relative; border-bottom: 4px solid #0065d7; padding: 0.5em; border: 2px solid #4f4f4f;"
        "background-color: #1f1f1f; color: #f8f8f2;",
    )
