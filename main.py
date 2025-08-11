import html_helpers
from html_helpers import br, button, div, h1, h2, p, textarea
from pyscript import document, when
from pyscript.web import Element


def _evaluate_solution(source: str, output_area: Element, error_area: Element) -> None:
    output_area.innerHTML = ""
    error_area.innerHTML = ""
    try:
        result = eval(source, globals=html_helpers.__dict__)
    except Exception as e:  # noqa: BLE001
        error_area.append(str(e))
        return

    # TODO: Before displaying the result we should check that the code actually produced an HTML element and display
    # a user-readable error message instead of crashing if it did not.
    output_area.append(result)
    # TODO: Here we should check whether the given HTML fits the required structure and produce an error message
    # if it does not.


def exercise_template() -> None:
    """Create the exercise template for the HTML tutorial from which all exercises will be derived."""
    document.body.append(
        h1("HTML Tutorial"),
        *exercise_p(),  # placeholder
        code_area := textarea(),
        br(),
        submit_button := button("Submit"),
        output_area := div(),
        error_area := div(),
    )
    when("click", submit_button, handler=lambda _: _evaluate_solution(code_area.value, output_area, error_area))


def exercise_p() -> Element:
    """Create the exercise content for the <p> tag."""
    return [
        h2("The <p> element"),
        p("The <p> element is used to define a paragraph like this one you're reading!"),
        p("Example: <p>This is how you use the tag.<p>"),
        p("Create a paragraph containing whatever you want!"),
    ]


def _main() -> None:
    exercise_template()


_main()
