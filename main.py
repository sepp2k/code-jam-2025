import html_helpers
from html_helpers import br, button, div, em, h1, h2, p, textarea
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


def _main() -> None:
    document.body.append(
        h1("HTML Tutorial"),
        h2("The em element"),
        p("The <em> element can be used to emphasized parts of a text ", em("like this"), "."),
        p("Please create a paragraph (<p> tag) that contains at least two words, exactly one of which is emphasized."),
        code_area := textarea(),
        br(),
        submit_button := button("Submit"),
        output_area := div(),
        error_area := div(),
    )
    when("click", submit_button, handler=lambda _: _evaluate_solution(code_area.value, output_area, error_area))


_main()
