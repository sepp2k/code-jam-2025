import html_helpers
from html_helpers import div
from pyscript import document, when
from pyscript.web import Element


def _evaluate_solution(source: str = "", output_area: Element = None, error_area: Element = None) -> None:
    if source.strip() == "" or output_area is None or error_area is None:
        print("Error, invalid inputs")

    code = str(source)

    output_area.innerHTML = ""
    error_area.innerHTML = ""

    is_invalid_html = False

    # Attempt to generate HTML
    result = None
    try:
        result = eval(code, globals=html_helpers.__dict__)
    except Exception:  # noqa: BLE001
        is_invalid_html = True
    finally:  # Allow support for input like a plain string (ex. "hello")
        if result is None:
            result = str(code)

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
    code_area: Element = Element(document.querySelector("textarea#code-area"))
    button: Element = Element(document.querySelector("button#submit-button"))
    output_area: Element = Element(document.querySelector("div#output-area"))
    error_area: Element = Element(document.querySelector("div#error-area"))

    when("click", button, handler=lambda _: _evaluate_solution(code_area.value, output_area, error_area))


_main()
