# Interactive HTML Tutorial

An interactive web-based HTML tutorial application that teaches HTML through hands-on Python coding exercises. Built with `PyScript`, this educational tool allows users to write Python code using HTML helper functions and see their HTML output.

**Key Value**: Learn HTML by writing Python code instead of raw HTML markup, with instant feedback and validation.

## Demo

Live Demo: [Coming Soon]

## Example Usage

1. Select an exercise

2. Write your solution in the editor, something like this:

    ```python
    # Write Python code like this:
    div(h1("My Title"), p("Some content"))
    ```

3. Click submit to see the HTML preview, and validation feedback.

## Features

- Interactive Code Editor with Python syntax highlighting (powered by CodeMirror).
- HTML Preview.
- Validation to check exercise requirements.
- Error Handling with helpful error messages.
- Keyboard Shortcuts (`Ctrl/Cmd+Enter` for quick submission).
- Responsive Design with resizable interface panels.
- Educational Feedback showing success/failure with specific guidance and hints.

## Installation

### Prerequisites

- A modern web browser.
- Internet connection (for PyScript and external dependencies).

### Setup Instructions

1. Clone the repository:

    ```bash
    git clone https://github.com/sepp2k/code-jam-2025.git
    cd code-jam-2025
    ```

    > No additional Python packages required - runs entirely in the browser via PyScript

2. Serve the files using a local web server:

    - using python's `http.server` (requires Python3+):

        ```bash
        python -m http.server 8000
        ```

    - or using Node.js:

        ```bash
        npx serve .
        ```

### Running the Application

1. Open your web browser.
2. Navigate to `http://localhost:8000`
3. Start with the exercises page to begin learning.

## Usage Guide

### Navigation

1. **Home**: Landing page.
2. **About**: HTML tutorial information.
3. **Exercises**: Interactive exercises.

### Available HTML Helper Functions

To pass an exercise, you ned to write Python code that mirrors the requested HTML structure request by the exercise. To do that, you should use the available Python helper functions to create HTML elements. The functions take the form: `html_tag_name(content, *children, **attributes)`.

- `content`: is the text content of the tag.
- `*children`: a list of HTML elements of tags that are appended as children to the current tag.
- `**attributes`: key-value attributes that are added to the tag.

#### Examples

- A simple HTML header tag:

    ```python
    h1("Hello World")
    ```

- A paragraph tag:

    ```python
    p("foo bar")
    ```

- An anchor tag (tag with attributes):

    ```python
    a("google", href="https://www.google.com/")
    ```

- A tag with nested children:

    ```python
    div(
        h1("HTML Tutorial"),
        div(
            p("Paragraph Tag", id="exercise-title"),
            p("Write two paragraphs, each having at least 2 words.", "exercise-description"),
            id="exercise-area-"
        ),
        id="main-container"
    )
    ```

#### Available Helper Functions

- `h1()`: Header 1 element
- `h2()`: Header 2 element
- `div()`: Div element
- `p()`: Paragraph element
- `br()`: Line break element
- `em()`: Emphasis element
- `textarea()`: Textarea element
- `button()`: Button element
- `iframe()`: Iframe element
- `nav()`: Nav element
- `a()`: Anchor element
- `code()`: Code element
- `span()`: Span element
- `b()`: Bold element
- `img()`: Image element

> check available HTML helper elements in `helper_elements.py`

## Technical Details

### Built With

- **PyScript** - Python in the browser runtime.
- **CodeMirror** - Code editor with syntax highlighting.

### Browser Compatibility

1. Chrome 90+
2. Firefox 88+
3. Safari 14+
4. Edge 90+

> Note: Requires WebAssembly support for PyScript.
> For more technical details, check the [design document](./docs/design_document.md).

## License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE.txt) file for details.

## Credits and Acknowledgments

- **Python Code Jam 2025** - This project was created as an entry for the annual Python programming contest, with Python the browser and 'the wrong tool for the job' themes.
- **Development Team:**
  - [Sebastian](https://github.com/sepp2k) - Team leader
  - [Granth](https://github.com/cat-loaf) - Developer
  - [Owen](https://github.com/owenw-28) - Developer
  - [Amen](https://github.com/AMK) - Developer
  - [Mohammad](https://github.com/ece-mohammad) - Developer
- **PyScript Team** for making Python in the browser possible
- **CodeMirror** for the excellent code editor component
- **[Python Discord](https://discord.com/invite/python)** for the amazing contest, inspiration, and collaborative spirit
