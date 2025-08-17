from string import Template

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
        ${RESULT}
    </body>
</html>
"""


def _update_iframe(frame: Element, content: str) -> None:
    """Update the contents of a given iframe.

    :param frame: an iframe element
    :type frame: Element
    :param content: the HTML content to display in the iframe's body
    :type content: str
    """
    iframe_contents = Template(IFRAME_TEMPLATE).safe_substitute(RESULT=content)
    frame.setAttribute("srcdoc", iframe_contents)


def _display_result(output_area: Element, result: Element) -> None:
    """Display the result in the output area.

    :param output_area: The output area to display the result in
    :type output_area: Element
    :param result: The HTML to display
    :type result: Element
    """
    if isinstance(result, str):
        result_html = result
    elif hasattr(result, "getHTML"):
        result_html = result.getHTML()
    else:
        result_html = str(result)

    _update_iframe(output_area, result_html)


def _evaluate_solution(source: str = "", output_area: Element = None, error_area: Element = None) -> None:
    if output_area is None or error_area is None:
        print("Error, invalid inputs")
    if source.strip() == "":
        error_area.append(div("Please enter some code to evaluate.", style="color: initial;"))
        return

    output_area.innerHTML = ""
    error_area.innerHTML = ""

    is_invalid_html = False

    # Attempt to generate HTML
    result = None
    err = None
    try:
        result = eval(source, globals=html_helpers.__dict__)
    except Exception as e:  # noqa: BLE001
        print(f"Exception occurred: {e}")
        is_invalid_html = True
        err = e

    if is_invalid_html or result is None or result == "":
        print("Invalid HTML")
        error_area.append(div("The code did not produce valid HTML element.", br(), b("Error"), f": {err!s}"))
        _update_iframe(output_area, "")
        return

    # TODO: Before displaying the result we should check that the code actually produced an HTML element and display
    # a user-readable error message instead of crashing if it did not.
    _display_result(output_area, result)



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
                    style="border-bottom: 1px solid #ccc;padding: 0.5em;flex: 1;",
                ),
                div(
                    h2("Output:"),
                    error_area := div(style="color: red;"),
                    output_area := iframe(style="border: none;"),
                    style="flex: 1; padding: 0.5em; height:50%;",
                ),
                style="flex: 1;",
            ),
            style="display: flex; width:99vw; height: 95vh; border: 1px solid #ccc;",
        ),
    )

    editor = window.CodeMirror.fromTextArea(
        code_area,
        {
            "lineNumbers": True,
            "mode": "python",
            "theme": "zenburn",
        },
    )
    when("click", submit_button, handler=lambda _: _evaluate_solution(editor.getValue(), output_area, error_area))


_main()
