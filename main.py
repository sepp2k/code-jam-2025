import ast
from dataclasses import dataclass
from string import Template
from typing import Final
from xml.etree import ElementTree as ET

import html_helpers
from element_components import custom_button, custom_nav
from html_helpers import _tag, b, br, div, h1, h2, iframe, li, p, span, textarea, ul
from pyscript import document, when, window
from pyscript.web import Element


class InvalidInputError(Exception):
    """Exception raised when the input is invalid."""


@dataclass()
class AppState:
    """Application state."""

    MAX_ERRORS_BEFORE_HINT: Final[int] = 3
    error_count: int = 0

    def reset_error_count(self) -> None:
        """Reset the error count to zero."""
        self.error_count = 0

    def increment_error_count(self) -> None:
        """Increment the error count by one."""
        self.error_count += 1

    def should_show_hint(self) -> bool:
        """Check if the hint should be shown based on the error count."""
        return self.error_count >= self.MAX_ERRORS_BEFORE_HINT

    def __str__(self) -> str:
        return f"{self.error_count=}"


@dataclass
class XPathValidator:
    """XPath expression validator."""

    xpath: str  # XPath expression to check
    count: int | None = None  # Expected number of occurrences
    message: str | None = None  # Error message if validation fails

    def validate(self, xml: str) -> bool:
        """Validate the XPath expression against the provided HTML."""
        try:
            tree = ET.ElementTree(ET.fromstring(xml))
            elements = tree.findall(self.xpath)
            return self.count is not None and len(elements) == self.count
        except ET.ParseError as e:
            self.message = f"Invalid HTML: {e}"
            return False


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

LocalAppState = AppState()


def _update_iframe(frame: Element, content: str | Element) -> None:
    """Update the contents of a given iframe.

    Args:
        frame (Element): The iframe element to update.
        content (str | Element): The HTML content to display in the iframe's body.

    """
    content = content.outerHTML
    iframe_contents = Template(IFRAME_TEMPLATE).safe_substitute(RESULT=content)
    frame.setAttribute("srcdoc", iframe_contents)


def _display_result(output_area: Element, result: Element | str) -> None:
    """Display the result in the output area.

    Args:
        output_area (Element): The element to update with the result.
        result (Element | str): The result to display.

    """
    if isinstance(result, str) or hasattr(result, "getHTML"):
        result_html = result
    else:
        result_html = str(result)

    _update_iframe(output_area, result_html)


def _update_error(error_area: Element, title: str, message_type: str, message: str | Element) -> None:
    error_area.append(div(title, br(), b(message_type), f": {message}", br()))


def _update_info(info_area: Element, title: str | Element | None, info: list[str | Element] | None) -> None:
    if title is None:
        title = ""

    if info is None or len(info) == 0:
        info_area.append(div(title))
    elif len(info) == 1:
        info_area.append(div(b(title), f" {info[0]}"))
    else:
        info_area.append(div(ul(b(title), *[li(i) for i in info])))


def _validate_user_input(source: str = "") -> Element:
    # Attempt to generate HTML
    output = div()
    err = None
    is_invalid_html = False
    environment = {name: value for name, value in html_helpers.__dict__.items() if not name.startswith("_")}

    try:
        tree = ast.parse(source)
        for statement in tree.body:
            match statement:
                case ast.Expr():
                    result = eval(compile(ast.Expression(statement.value), "", mode="eval"), globals=environment)
                    if hasattr(result, "classList") or isinstance(result, str):
                        output.append(result)
                    else:
                        is_invalid_html = True
                        err = f"""
                        Expression returned {result} (of type {type(result)}), instead of an HTML element or string
                        """.strip()
                case ast.FunctionDef() | ast.Assign():
                    exec(compile(ast.Module([statement]), "", mode="exec"), globals=environment)
    except Exception as e:
        if err is None:
            err = str(e)
        raise InvalidInputError(err) from e

    if is_invalid_html:
        raise InvalidInputError(err)

    return output


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

    # validate user input
    try:
        output = _validate_user_input(source)
    except InvalidInputError as e:
        _update_error(error_area, "An error occurred while evaluating the code.", "Error", str(e))
        _update_iframe(output_area, "")
        return

    # validate generated HTML
    matched, msg = _matches_expected([XPathValidator(".//p", 2, "Expected 2 paragraph elements")], output)
    if matched:
        _update_info(info_area, b("Good job!"), ["You produced the expected HTML."])
        LocalAppState.reset_error_count()

    else:
        LocalAppState.increment_error_count()
        if LocalAppState.should_show_hint():
            # display hints
            _update_info(
                info_area,
                b("Hints"),
                ["Did you use the correct tag?", "Try wrapping the two paragraphs in a div?"],
            )
        _update_error(error_area, "The code did not produce the expected HTML.", "Error", msg)

    _display_result(output_area, output)
    print(LocalAppState)


def _matches_expected(expected: list[XPathValidator], actual: Element) -> tuple[bool, str | Element]:
    """Validate HTML output against expected XPath validators."""
    # Normalize actual HTML
    if hasattr(actual, "outerHTML"):
        actual_html = actual.outerHTML
    else:
        actual_html = str(actual).strip()

    # Run validators
    for validator in expected:
        if not validator.validate(actual_html):
            msg = div(
                validator.message or "Validation failed.",
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
                    h2("Exercise 1: Create two paragraphs"),
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
