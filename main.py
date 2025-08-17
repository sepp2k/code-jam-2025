import re
from string import Template
from xml.etree import ElementTree as ET

import html_helpers
from element_components import custom_button, custom_nav
from html_helpers import _tag, b, br, div, h1, h2, iframe, p, span, textarea
from pyscript import document, when, window
from pyscript.web import Element

IFRAME_TEMPLATE: str = """<html>
    <head>
        <title>HTML Tutorial</title>
    </head>
    <body>
        <div id="result">
        ${RESULT}
        </div>
    </body>
</html>
"""


def _update_iframe(frame: Element, content: str | Element) -> None:
    """Update the contents of a given iframe.

    Args:
        frame (Element): The iframe element to update.
        content (str | Element): The HTML content to display in the iframe's body.

    """
    if hasattr(content, "getHTML"):
        content = content.outerHTML
    iframe_contents = Template(IFRAME_TEMPLATE).safe_substitute(RESULT=content)
    frame.setAttribute("srcdoc", iframe_contents)


def _display_result(output_area: Element, result: Element) -> None:
    """Display the result in the output area.

    :param output_area: The output area to display the result in
    :type output_area: Element
    :param result: The HTML to display
    :type result: Element
    """
    if isinstance(result, str) or hasattr(result, "getHTML"):
        result_html = result
    else:
        result_html = str(result)

    _update_iframe(output_area, result_html)


def _evaluate_solution(
    source: str = "",
    output_area: Element = None,
    error_area: Element = None,
    info_area: Element = None,
) -> None:
    if output_area is None or error_area is None or info_area is None:
        print("Error, invalid inputs")
        return

    if source.strip() == "":
        error_area.append(div("Please enter some code to evaluate.", style="color: initial;"))
        return

    output_area.innerHTML = ""
    error_area.innerHTML = ""
    info_area.innerHTML = ""

    is_invalid_html = False

    # Attempt to generate HTML
    result = None
    err = None
    try:
        result = eval(source, globals=html_helpers.__dict__)
    except Exception as e:
        print(f"Exception occurred: {e}")
        is_invalid_html = True
        err = e

    if is_invalid_html or result is None or result == "":
        print("Invalid HTML")
        error_area.append(div("The code did not produce valid HTML element.", br(), b("Error"), f": {err!s}"))
        _update_iframe(output_area, "")
        return

    matched, msg = _matches_expected({"answer": "{{*}}", "validators": []}, result)
    info_area.append(msg)

    _display_result(output_area, result)


def _matches_expected(expected: dict, actual: str | object) -> tuple[bool, str | Element]:
    """Validate HTML output against expected pattern and validators."""
    # Normalize actual HTML
    if hasattr(actual, "outerHTML"):
        actual_html = actual.outerHTML
    else:
        actual_html = str(actual).strip()

    # --- 1) Wildcard pattern check ---
    expected_answer = expected.get("answer", "")
    answer_pattern = re.escape(expected_answer).replace(r"\{\{\*\}\}", ".*?")
    if not re.fullmatch(answer_pattern, actual_html, re.DOTALL):
        msg = div("Not quite right")
        return False, msg

    # --- 2) Parse for validators ---
    try:
        wrapped_html = f"<root>{actual_html}</root>"  # single root for parsing
        tree = ET.fromstring(wrapped_html)
    except Exception as e:
        msg = div(f"Error parsing HTML: {e}", style="color:red; font-weight:bold;")
        return False, msg

    for validator in expected.get("validators", []):
        xpath_expr = validator.get("xpath")
        error_msg = validator.get("error", "Validation failed.")
        expected_count = validator.get("count")  # optional exact count

        try:
            matches = tree.findall(xpath_expr)
        except Exception:
            msg = div(f"Unsupported XPath in validator: {xpath_expr}", style="color:red; font-weight:bold;")
            return False, msg

        if expected_count is not None:
            if len(matches) != expected_count:
                msg = div(
                    f"{error_msg} Expected exactly {expected_count}, found {len(matches)}.",
                    style="color:red; font-weight:bold;",
                )
                return False, msg
        elif not matches:
            msg = div(error_msg, style="color:red; font-weight:bold;")
            return False, msg

    # --- 3) Style enforcement ---
    def parse_style(style_str: str) -> dict:
        """Parse style string into dict using last occurrence of each key."""
        style_dict = {}
        for part in style_str.split(";"):
            if ":" in part:
                key, value = part.split(":", 1)
                style_dict[key.strip()] = value.strip()  # last occurrence wins
        return style_dict

    style_match = re.search(r'style="([^"]*)"', expected_answer)
    expected_style = style_match.group(1) if style_match else None

    if expected_style:
        # Extract actual style attribute
        tag_match = re.match(r"<(\w+)([^>]*)>", actual_html)
        if tag_match:
            actual_attrs = tag_match.group(2)
            actual_style_match = re.search(r'style="([^"]*)"', actual_attrs)
            actual_style = actual_style_match.group(1) if actual_style_match else ""
        else:
            actual_style = ""

        expected_style_dict = parse_style(expected_style)
        actual_style_dict = parse_style(actual_style)

        # Compare each expected key against the final value in actual
        for key, val in expected_style_dict.items():
            if key not in actual_style_dict:
                msg = div(f"Missing expected style '{key}: {val}'.", style="color:red; font-weight:bold;")
                return False, msg
            if actual_style_dict[key] != val:
                msg = div(
                    f"Style mismatch for '{key}': expected '{val}', found '{actual_style_dict[key]}'.",
                    style="color:red; font-weight:bold;",
                )
                return False, msg

    return True, div("Output matches ✅", style="color:green; font-weight:bold;")


def _main() -> None:
    document.head.append(
        _tag(
            "style",
            """
@import url('https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,200..800&display=swap');
body {font-family: 'Bricolage Grotesque', sans-serif;}
        """,
        ),
    )

    document.body.append(
        custom_nav(),
    )

    page_name = document.querySelector("meta[name='page-name']").content
    match page_name:
        case "home":
            _home_page()
        case "about":
            _about_page()
        case "exercises":
            _exercises_page()


def _home_page() -> None:
    document.body.append(
        h1("Home Page"),
        p("This is the home page."),
    )


def _about_page() -> None:
    document.body.append(
        h1("HTML Tutorial"),
    )


def _exercises_page() -> None:
    document.body.append(
        div(
            div(
                h1("Exercises"),
                h2(
                    "Create a ",
                    span("paragraph", style="text-decoration:underline;"),
                    " tag",
                ),
                style="""
resize: horizontal; overflow: auto; min-width: 25%; max-width:75%;
border-right: 1px solid #ccc; padding: 0.5em;
""",
            ),
            div(
                div(
                    h2("Exercise 1: Create a Custom HTML Element"),
                    code_area := textarea(""),
                    submit_button := custom_button("Submit"),
                    span("Or press Ctrl/Cmd+Enter", style="margin-left: 1em; color: #aaa"),
                    style="border-bottom: 1px solid #ccc;padding: 0.5em;flex: 1;",
                ),
                div(
                    h2("Output:"),
                    info_area := div(),
                    error_area := div(style="color: red;"),
                    output_area := iframe(style="border: none; width: 95%; height: 85%;"),
                    style="flex: 1; padding: 0.5em; height:50%;",
                ),
                style="flex: 1;",
            ),
            style="display: flex; width:99vw; height: 90vh; border: 1px solid #ccc;",
        ),
    )

    editor = window.CodeMirror.fromTextArea(
        code_area,
        {
            "lineNumbers": True,
            "mode": "python",
            "theme": "zenburn",
            "extraKeys": {
                "Ctrl-Enter": lambda _: _evaluate_solution(editor.getValue(), output_area, error_area, info_area),
                "Cmd-Enter": lambda _: _evaluate_solution(editor.getValue(), output_area, error_area, info_area),
            },
        },
    )
    when(
        "click",
        submit_button,
        handler=lambda _: _evaluate_solution(editor.getValue(), output_area, error_area, info_area),
    )


_main()
