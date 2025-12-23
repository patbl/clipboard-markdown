# Clipboard Markdown

Mac utilities for interacting with the system clipboard as HTML and Markdown.

## Overview

This toolkit provides four scripts for working with clipboard content:

- **clipboard-to-markdown** - Extract HTML from clipboard as Markdown
- **markdown-to-clipboard** - Convert Markdown to HTML and put on clipboard
  as rich text
- **markdownify-clipboard** - Convert HTML on clipboard to Markdown text
- **normalize-clipboard** - Normalize HTML formatting on clipboard by
  round-tripping through Markdown

## Requirements

- macOS
- Python 3
- [Pandoc](https://pandoc.org/)

## Installation

1. Install Pandoc:
   ```bash
   brew install pandoc
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### clipboard-to-markdown

Reads HTML from the clipboard and outputs Markdown to stdout.

```bash
clipboard-to-markdown
```

**Example:**
1. Copy some rich text from a web page
2. Run `clipboard-to-markdown`
3. See the Markdown representation

### markdown-to-clipboard

Reads Markdown from stdin and puts the rendered HTML on the clipboard as rich
text.

```bash
echo "# Hello World" | markdown-to-clipboard
```

**Example:**
1. Run `cat document.md | markdown-to-clipboard`
2. Paste into any application, where it will appear as formatted rich text.

### markdownify-clipboard

Converts the clipboard from HTML to plain Markdown text.

```bash
markdownify-clipboard
```

**Example:**
1. Copy formatted text from a web page
2. Run `markdownify-clipboard`
3. Paste.  You'll get plain Markdown text

### normalize-clipboard

Normalizes HTML formatting by converting clipboard HTML to Markdown and back to
HTML, removing unnecessary formatting.

```bash
normalize-clipboard
```

**Example:**
1. Copy formatted HTML from a document
2. Run `normalize-clipboard`
3. Paste.  The HTML will be cleaner and simplified

## Adding to PATH

To run these scripts from anywhere, add the bin directory to your PATH. For
example, add to your `~/.bashrc` or `~/.zshrc`:

```bash
export PATH="$PATH:/path/to/clipboard-markdown/bin"
```

## Testing

Run the test suite with pytest:

```bash
pytest
```

Note that this will interact with your real system clipboard, so make sure you
don't have anything in there you want to keep when running tests!
