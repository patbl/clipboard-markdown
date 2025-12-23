import pytest
import subprocess
from pathlib import Path
from AppKit import NSPasteboard


def run_script(script_name, input_text=None):
    """Run a script from the bin directory."""
    script_path = Path(__file__).parent / "bin" / script_name
    if input_text is not None:
        result = subprocess.run(
            [str(script_path)],
            input=input_text,
            capture_output=True,
            text=True
        )
    else:
        result = subprocess.run(
            [str(script_path)],
            capture_output=True,
            text=True
        )
    return result


def put_html_on_clipboard(html):
    pasteboard = NSPasteboard.generalPasteboard()
    pasteboard.clearContents()
    pasteboard.setString_forType_(html, "public.html")


def get_html_from_clipboard():
    return NSPasteboard.generalPasteboard().stringForType_("public.html")


@pytest.fixture
def example_full_html():
    with open("examples/example.html") as inf:
        return inf.read()


@pytest.fixture
def example_markdown():
    with open("examples/example.md") as inf:
        return inf.read()


@pytest.fixture
def example_normalized():
    with open("examples/example_normalized.html") as inf:
        return inf.read()


def test_clipboard_to_markdown(example_full_html, example_markdown):
    """Test clipboard-to-markdown conversion."""
    put_html_on_clipboard(example_full_html)
    result = run_script("clipboard-to-markdown")
    assert result.returncode == 0, \
        f"clipboard-to-markdown failed: {result.stderr}"
    assert result.stdout == example_markdown, \
        "clipboard-to-markdown output doesn't match expected markdown"


def test_markdown_to_clipboard(example_markdown, example_normalized):
    """Test markdown-to-clipboard conversion."""
    result = run_script("markdown-to-clipboard", input_text=example_markdown)
    assert result.returncode == 0, \
        f"markdown-to-clipboard failed: {result.stderr}"
    assert get_html_from_clipboard() == example_normalized, \
        "markdown-to-clipboard output doesn't match expected HTML"


def test_markdownify_clipboard(example_full_html, example_markdown):
    """Test markdownify-clipboard."""
    put_html_on_clipboard(example_full_html)
    result = run_script("markdownify-clipboard")
    assert result.returncode == 0, \
        f"markdownify-clipboard failed: {result.stderr}"
    assert subprocess.run(['pbpaste'], capture_output=True, text=True).stdout \
        == example_markdown, \
        "markdownify-clipboard output doesn't match expected markdown"


def test_normalize_clipboard(example_full_html, example_normalized):
    """Test normalize-clipboard."""
    put_html_on_clipboard(example_full_html)
    result = run_script("normalize-clipboard")
    assert result.returncode == 0, f"normalize-clipboard failed: {result.stderr}"
    assert get_html_from_clipboard() == example_normalized, \
        "normalize-clipboard output doesn't match expected HTML"
