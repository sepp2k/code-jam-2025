import ast
from functools import partial
from pathlib import Path
from string import Template
from typing import Final

import html_helpers
from element_components import custom_button, custom_code_block, custom_nav
from exercises import Exercise, ExerciseGroup, load_exercises_from_json
from html_helpers import (
    _tag,
    a,
    b,
    br,
    details,
    div,
    h1,
    h2,
    hr,
    i,
    iframe,
    li,
    p,
    span,
    summary,
    textarea,
    ul,
)
from pyodide.ffi.wrappers import add_event_listener
from pyscript import document, when, window
from pyscript.web import Element
from solution_validator import validate_solution

EXERCISES_JSON_FILE: Final[Path] = Path("exercises.json")

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


class AppStorage:
    """Application's local storage."""

    EXERCISES: list[ExerciseGroup] = load_exercises_from_json(EXERCISES_JSON_FILE)
    current_exercise: Exercise = EXERCISES[0].exercises[0]

    def get_current_exercise(self) -> Exercise:
        """Get current exercise that's being worked on."""
        return self.current_exercise

    def set_current_exercise_by_index(self, group_index: int, exercise_index: int) -> None:
        """Set current exercise that's being worked on."""
        self.current_exercise = self.EXERCISES[group_index].exercises[exercise_index]


AppState: AppStorage = AppStorage()


def _update_iframe(frame: Element, content: Element) -> None:
    """Update the contents of a given iframe.

    Args:
        frame (Element): The iframe element to update.
        content (str | Element): The HTML content to display in the iframe's body.

    """
    content = content.outerHTML
    iframe_contents = Template(IFRAME_TEMPLATE).safe_substitute(RESULT=content)
    frame.setAttribute("srcdoc", iframe_contents)


def _display_result(output_area: Element, result: Element) -> None:
    """Display the result in the output area.

    Args:
        output_area (Element): The element to update with the result.
        result (Element): The result to display.

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
    output = div()
    err = None
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
        is_invalid_html = True
        err = e

    if is_invalid_html:
        error_area.append(div("The code did not produce valid HTML element.", br(), b("Error"), f": {err!s}"))
        _update_iframe(output_area, "")
        return

    msg = validate_solution("<p>{{*}}</p>", output)
    info_area.append(msg)

    _display_result(output_area, output)


def _main() -> None:
    document.head.append(
        _tag(
            "style",
            "@import url('https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,200..800&family"
            "=Google+Sans"
            "+Code:ital,wght@0,300..800;1,300..800&display=swap');"
            "body {font-family: 'Bricolage Grotesque', sans-serif;}"
            ".cm-editor, .CodeMirror {font-family: 'Google Sans Code', monospace;}",
        ),
        _tag(
            "script",
            """
function copyToClipboard(text, callback=()=>{}) {
    navigator.clipboard.writeText(text).then(() => {
        if (callback) callback();
    });
}
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
        case "exercises":
            _exercises_page()
        case _:
            _404_page()


def _404_page() -> None:
    document.body.append(
        div(
            h1("404 Not Found"),
            p("The page you are looking for does not exist."),
            a(
                "Go back to Home",
                href="/index.html",
                style="color: blue; text-decoration: none;",
                onmouseover="this.style.textDecoration = 'underline';",
                onmouseleave="this.style.textDecoration = 'none';",
            ),
            style="text-align: center; margin-top: 2em;",
        ),
    )


def _home_page() -> None:
    document.body.append(
        div(
            h1("About this Project", style="margin:0;"),
            p(
                "This project was created as part of ",
                b("Python Code Jam 2025"),
                ", where the theme was ",
                i("Wrong Tool for the Job"),
                ".",
                style="margin: 0.5em 0 1em 0;",
            ),
            hr(),
            h2("The Idea", style="margin:1em 0 0 0;"),
            p(
                "Our entry takes the form of an ",
                b("HTML Tutorial"),
                " but with a twist. Instead of writing HTML, user write ",
                b("Python code"),
                " to complete each exercise. For example, rather than typing:",
                style="margin: 0.5em 0 1em 0;",
            ),
            custom_code_block("<div>Hello <em>World</em>!</div>", language="html"),
            p("the user writes:"),
            custom_code_block('div("Hello ", em("World"), "!")', language="python"),
            p(
                "The Python is then executed directly in the browser to generate the HTML, which is "
                "displayed alongside the code editor. Each chapter introduces a new HTML concept, "
                "followed by exercises that can only be solved by writing Python that outputs the "
                "correct HTML structure.",
            ),
            hr(),
            h2("Why This Fits the Theme", style="margin:1em 0 0 0;"),
            p(
                "At its core, the project is about teaching HTML, but we're doing it with Python, arguably the "
                "wrong tool for the job. This mismatch captures the spirit of the Code Jam's theme while also "
                'making for an engaging, "playful" learning experience.',
                style="margin: 0.5em 0 0.5em 0;",
            ),
            p(
                "It's also a fun exploration of ",
                b('"Python in the browser"'),
                ". Everything-tutorial logic, code execution, and validation-is written in Python. The user writes "
                "Python, the site runs Python, and all of it ultimately produces HTML (Plus CSS and JavaScript).",
                style="margin: 0.5em 0 1em 0;",
            ),
            hr(),
            custom_code_block(
                "• @psyklopps42 (Sebastian)",
                "• @kcatloaf (Granth)",
                "• @0w3n (Owen)",
                "• @AMK (Amen Ellah)",
                "• @kuro (Mohammad)",
                language="authors",
                copy_tip="none",
            ),
            style="display:flex; flex-direction:column; max-width: 70vw; margin: 2em auto 2em auto;"
            "background-color:#eeeeee; padding: 2em; border-radius: 1em; "
            "box-shadow: rgba(60, 64, 67, 0.3) 0px 1px 2px 0px, rgba(60, 64, 67, 0.15) 0px 2px 6px 2px;",
        ),
    )


def _exercise_link_listener(group_index: int, exercise_index: int, *args, **kwargs) -> None:  # noqa: ARG001, ANN002, ANN003
    AppState.set_current_exercise_by_index(group_index, exercise_index)
    _main()


def _create_exercise_group(exercise_group: ExerciseGroup, group_index: int) -> Element:
    """Create a collapsible exercise group."""
    # create links for each exercise
    exercise_links = [
        a(
            f"{index + 1}. {exercise.title}",
            href="#",
            style="text-decoration: none;",
            onmouseover="this.style.textDecoration = 'underline';",
            onmouseleave="this.style.textDecoration = 'none';",
        )
        for index, exercise in enumerate(exercise_group.exercises)
    ]

    # add callback for each link
    for index, link in enumerate(exercise_links):
        add_event_listener(
            link,
            "click",
            partial(
                _exercise_link_listener,
                group_index,
                index,
            ),
        )

    # create exercise list
    exercise_list = ul(
        *[li(exercise_link, style="margin: 0.5em 0;") for exercise_link in exercise_links],
        style="list-style-type: none; margin: 0; padding: 0; cursor: pointer;",
    )

    # create collapsible exercise group
    group = details(
        summary(
            b(f"{group_index + 1}. {exercise_group.title}"),
            style="cursor: pointer; margin: 0; border: 1px solid #eee;",
        ),
        exercise_list,
    )

    if AppState.current_exercise in exercise_group.exercises:
        group.open = True

    return group


def list_exercises() -> list[Element]:
    """List exercises as a collapsible list of exercise groups."""
    return [_create_exercise_group(exercise_group, index) for index, exercise_group in enumerate(AppState.EXERCISES)]


def _exercises_page(exercise: Exercise = AppState.current_exercise) -> None:
    document.body.append(
        div(
            div(
                h1("Exercises"),
                *list_exercises(),
                style="""
resize: horizontal; overflow: auto; min-width: 25%; max-width:75%;
border-right: 1px solid #ccc; padding: 0.5em;
""",
            ),
            div(
                div(
                    h2(exercise.title),
                    p(exercise.description, style="margin: 0.5em 0;"),
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
