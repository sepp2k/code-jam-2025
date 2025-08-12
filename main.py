import html_helpers
from element_components import custom_nav
from html_helpers import br, button, div, em, h1, h2, p, textarea
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
    finally:  # Allow support for input like a plain string (ex. "hello")
        if result is None:
            result = str(source)

    # Check if result is a valid HTML element (duck-type)
    try:
        print(result.classList)
    except Exception:  # noqa: BLE001
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
        h1("Exercises Page"),
        p("This is the exercises page."),
    )

    editor = window.CodeMirror.fromTextArea(
        code_area,
        {
            "lineNumbers": True,
            "mode": "python",
        },
    )
    when("click", submit_button, handler=lambda _: _evaluate_solution(editor.getValue(), output_area, error_area))


_main()
