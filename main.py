from string import Template

import html_helpers
from html_helpers import br, button, div, em, h1, h2, iframe, p, textarea
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
    result_html = result.getHTML()
    _update_iframe(output_area, result_html)


def _evaluate_solution(source: str, output_area: Element, error_area: Element) -> None:
    error_area.innerHTML = ""
    try:
        result = eval(source, globals=html_helpers.__dict__)
    except Exception as e:  # noqa: BLE001
        error_area.append(str(e))
        return

    # TODO: Before displaying the result we should check that the code actually produced an HTML element and display
    # a user-readable error message instead of crashing if it did not.
    _display_result(output_area, result)
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
        output_area := iframe(id="output-area"),
        error_area := div(),
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
