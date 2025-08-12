import html_helpers
from element_components import custom_button, custom_nav
from html_helpers import div, h1, h2, p, span, textarea
from pyscript import document, when, window
from pyscript.web import Element


def _evaluate_solution(source: str = "", output_area: Element = None, error_area: Element = None) -> None:
    if source.strip() == "" or output_area is None or error_area is None:
        print("Error, invalid inputs")

    output_area.innerHTML = ""
    error_area.innerHTML = ""

    is_invalid_html = False

    # Attempt to generate HTML
    result = None
    try:
        result = eval(source, globals=html_helpers.__dict__)
    except Exception:  # noqa: BLE001
        is_invalid_html = True
    finally:
        if result is None:
            is_invalid_html = True

    # Check if result is a valid HTML element (duck-type)
    if getattr(result, "classList", None) is None:
        is_invalid_html = True

    if isinstance(result, str):
        is_invalid_html = False

    if is_invalid_html:
        error_area.append(div("The code did not produce valid HTML element."))
        return

    # TODO: Here we should check whether the given HTML fits the required structure and produce an error message
    # if it does not.

    output_area.append(div(result))


def _main() -> None:
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
        h1("About Page"),
        p("This is the about page."),
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
                    output_area := div(style="margin-top: 1em;"),
                    error_area := div(style="margin-top: 1em; color: red;"),
                    style="flex: 1; overflow: auto; padding: 0.5em;",
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
