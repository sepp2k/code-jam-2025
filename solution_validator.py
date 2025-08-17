import re
from xml.etree import ElementTree as ET

from html_helpers import div
from pyscript.web import Element


def validate_solution(expected: str, actual: Element) -> Element:
    """Validate HTML output against expected template.

    The template should be a string containing the expected XML structure and can contain `{{*}}` as a wildcard that
    can match any text (but not tags).
    """
    # The generated HTML will always have a plain <div> wrapped around it because of how we create it. So we likewise
    # add a <div> around the expected HTML.
    expected_tree = ET.fromstring(f"<div>{expected}</div>")
    actual_tree = ET.fromstring(actual.outerHTML)
    error = _matches_xml_template(expected_tree, actual_tree)
    if error is None:
        return div("✅ Output matches", style="color:green; font-weight:bold;")
    return error


# The following methods return None if there was no error, otherwise an HTML element displaying the error message
type _Result = Element | None


def _test_failure_div(message: str) -> Element:
    return div(f"❌ {message}", style="color:red; font-weight:bold;")


def _matches_xml_template(expected: ET.Element, actual: ET.Element) -> _Result:
    if expected.tag != actual.tag:
        return _test_failure_div(f"Expected a <{expected.tag}> tag, but got <{actual.tag}>")
    error = _compare_attributes(expected, actual)
    if error is not None:
        return error
    error = _compare_children(expected, actual)
    if error is not None:
        return error
    return None


def _compare_attributes(expected: ET.Element, actual: ET.Element) -> _Result:
    for attribute_name, attribute_value in actual.attrib.items():
        if attribute_name not in expected.attrib:
            return _test_failure_div(f"Unexpected attribute {attribute_name}")
        expected_value = expected.attrib[attribute_name]
        if attribute_value != expected_value:
            return _test_failure_div(
                f"Attribute {attribute_name} is set to {attribute_value}, expected {expected_value}",
            )
    for attribute_name in expected.attrib:
        if attribute_name not in actual.attrib:
            return _test_failure_div(f"Missing attribute {attribute_name}")
    return None


def _compare_children(expected: ET.Element, actual: ET.Element) -> _Result:
    error = _matches_text(expected.text, actual.text)
    if error is not None:
        return error
    for expected_child, actual_child in zip(expected, actual, strict=False):
        error = _matches_xml_template(expected_child, actual_child)
        if error is not None:
            return error
        error = _matches_text(expected_child.tail, actual_child.tail)
        if error is not None:
            return error
    if len(actual) > len(expected):
        extra_element = actual[len(expected)]
        return _test_failure_div(f"Unexpected <{extra_element.tag}> element")
    if len(expected) > len(actual):
        missing_element = expected[len(actual)]
        return _test_failure_div(f"Missing <{missing_element.tag}> element")
    return None


def _matches_text(expected: str | None, actual: str | None) -> _Result:
    if expected is None and actual is None:
        return None
    if expected is None:
        return _test_failure_div(f"Unexpected text '{actual}'")
    if actual is None:
        return _test_failure_div(f"Missing text '{expected}'")
    expected_regex = expected.replace("{{*}}", ".*")
    if re.fullmatch(expected_regex, actual) is None:
        return _test_failure_div(f"Text '{actual}' did not match the expected pattern '{expected}'")
    return None
