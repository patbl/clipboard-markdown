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


def test_html_clipboard_get(example_full_html):
    """Test html-clipboard get."""
    put_html_on_clipboard(example_full_html)
    bin_dir = Path(__file__).parent / "bin"
    html_clipboard = bin_dir / "html-clipboard"
    result = subprocess.run(
        [str(html_clipboard), "get"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"html-clipboard get failed: {result.stderr}"
    assert result.stdout == example_full_html, \
        "html-clipboard get output doesn't match clipboard contents"


def test_html_clipboard_set(example_full_html):
    """Test html-clipboard set."""
    bin_dir = Path(__file__).parent / "bin"
    html_clipboard = bin_dir / "html-clipboard"
    result = subprocess.run(
        [str(html_clipboard), "set"],
        input=example_full_html,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"html-clipboard set failed: {result.stderr}"
    assert get_html_from_clipboard() == example_full_html, \
        "html-clipboard set didn't put correct HTML on clipboard"


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


def test_unescape_dollar():
    """Test that $ is unescaped."""
    result = run_script("unescape-markdown", r"\$foo")
    assert result.stdout == "$foo", "Failed to unescape $"


def test_unescape_pipe():
    """Test that | is unescaped."""
    result = run_script("unescape-markdown", r"\| bar")
    assert result.stdout == "| bar", "Failed to unescape |"


def test_unescape_brackets():
    """Test that [ and ] are unescaped."""
    result = run_script("unescape-markdown", r"\[1\]")
    assert result.stdout == "[1]", "Failed to unescape [ and ]"


def test_unescape_underscore_in_word():
    """Test that underscores inside words are unescaped."""
    result = run_script("unescape-markdown", r"file\_name")
    assert result.stdout == "file_name", "Failed to unescape underscore in word"


def test_keep_underscore_at_boundary():
    """Test that underscores at word boundaries stay escaped."""
    result = run_script("unescape-markdown", r"\_italic\_")
    assert result.stdout == r"\_italic\_", "Incorrectly unescaped underscore at boundary"


def test_unescape_asterisk_with_spaces():
    """Test that asterisks with spaces are unescaped."""
    result = run_script("unescape-markdown", r"3 \* 4")
    assert result.stdout == "3 * 4", "Failed to unescape asterisk with spaces"


def test_keep_asterisk_without_spaces():
    """Test that asterisks without spaces stay escaped."""
    result = run_script("unescape-markdown", r"\*bold\*")
    assert result.stdout == r"\*bold\*", "Incorrectly unescaped asterisk without spaces"


def test_combined_escapes():
    """Test multiple escapes in one line."""
    result = run_script("unescape-markdown", r"\$foo \| bar \[1\] file\_name 3 \* 4")
    assert result.stdout == "$foo | bar [1] file_name 3 * 4", \
        "Failed to handle combined escapes"


def test_asterisk_leading_space_only():
    """Test asterisk with leading space but no trailing space."""
    result = run_script("unescape-markdown", r"3 \*4")
    assert result.stdout == r"3 \*4", "Should keep escaped without trailing space"


def test_asterisk_trailing_space_only():
    """Test asterisk with trailing space but no leading space."""
    result = run_script("unescape-markdown", r"3\* 4")
    assert result.stdout == r"3\* 4", "Should keep escaped without leading space"


def test_dollar_math():
    """Test dollar signs used for math expressions."""
    result = run_script("unescape-markdown", r"\$x\$")
    assert result.stdout == "$x$", "Current behavior: unescapes all dollars"


def test_multiple_underscores():
    """Test multiple underscores in a word."""
    result = run_script("unescape-markdown", r"foo\_bar\_baz")
    assert result.stdout == "foo_bar_baz", "Current behavior: unescapes all underscores in words"


def test_asterisk_emphasis():
    """Test asterisks used for emphasis/italic."""
    result = run_script("unescape-markdown", r"foo \*bar\* baz")
    assert result.stdout == r"foo \*bar\* baz", "Should keep escaped to preserve emphasis markup"


def test_asterisk_start_of_line():
    """Test asterisk at start of line (like a list item)."""
    result = run_script("unescape-markdown", r"\* foo")
    assert result.stdout == r"\* foo", "Should keep escaped at start of line"


def test_asterisk_end_of_line():
    """Test asterisk at end of line."""
    result = run_script("unescape-markdown", r"foo \*")
    assert result.stdout == r"foo \*", "Should keep escaped at end of line"


def test_asterisk_both_ends():
    """Test asterisks at both start and end of line."""
    result = run_script("unescape-markdown", r"\* foo \*")
    assert result.stdout == r"\* foo \*", "Should keep escaped at line boundaries"


def test_asterisk_start_of_multiline():
    """Test asterisk at start of line in multiline text."""
    result = run_script("unescape-markdown", "foo\n\\* bar")
    assert result.stdout == "foo\n\\* bar", "Should keep escaped at start of line after newline"


def test_underscore_with_spaces():
    """Test underscore with spaces on both sides."""
    result = run_script("unescape-markdown", r"foo \_ bar")
    assert result.stdout == "foo _ bar", "Should unescape when surrounded by spaces"


def test_underscore_space_before_only():
    """Test underscore with space before but not after (emphasis marker)."""
    result = run_script("unescape-markdown", r"foo \_bar")
    assert result.stdout == r"foo \_bar", "Should keep escaped with only leading space"


def test_underscore_space_after_only():
    """Test underscore with space after but not before (emphasis marker)."""
    result = run_script("unescape-markdown", r"foo\_ bar")
    assert result.stdout == r"foo\_ bar", "Should keep escaped with only trailing space"
