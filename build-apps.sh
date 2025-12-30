#!/bin/bash
set -e

PLATYPUS="/Applications/Platypus.app/Contents/Resources/platypus_clt"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Check if Platypus is installed
if [ ! -f "$PLATYPUS" ]; then
    echo "Error: Platypus not found at $PLATYPUS"
    echo "Please install Platypus from https://sveinbjorn.org/platypus"
    exit 1
fi

# Check if Platypus CLI tools are installed
if [ ! -f "/usr/local/share/platypus/ScriptExec" ]; then
    echo "Platypus command-line tools not installed."
    echo "Installing now (requires sudo)..."
    sudo /Applications/Platypus.app/Contents/Resources/InstallCommandLineTool.sh \
        /Applications/Platypus.app/Contents/Resources
    echo "CLI tools installed successfully"
fi

echo "Building Markdownify Clipboard.app..."
"$PLATYPUS" \
  --overwrite \
  --name "Markdownify Clipboard" \
  --interface-type "Status Menu" \
  --interpreter /bin/bash \
  --app-version "1.0" \
  --bundle-identifier "com.jefftk.MarkdownifyClipboard" \
  --author "Jeff Kaufman" \
  --app-icon "$SCRIPT_DIR/logos/clipboard-md.icns" \
  --status-item-kind "Icon" \
  --status-item-icon "$SCRIPT_DIR/logos/clipboard-md.icns" \
  --status-item-template-icon \
  --background \
  --bundled-file "$SCRIPT_DIR/bin/html-clipboard" \
  "$SCRIPT_DIR/bin/markdownify-clipboard" \
  "$SCRIPT_DIR/Markdownify Clipboard.app"

echo "Building Normalize Clipboard.app..."
"$PLATYPUS" \
  --overwrite \
  --name "Normalize Clipboard" \
  --interface-type "Status Menu" \
  --interpreter /bin/bash \
  --app-version "1.0" \
  --bundle-identifier "com.jefftk.NormalizeClipboard" \
  --author "Jeff Kaufman" \
  --app-icon "$SCRIPT_DIR/logos/clipboard-n.icns" \
  --status-item-kind "Icon" \
  --status-item-icon "$SCRIPT_DIR/logos/clipboard-n.icns" \
  --status-item-template-icon \
  --background \
  --bundled-file "$SCRIPT_DIR/bin/html-clipboard" \
  "$SCRIPT_DIR/bin/normalize-clipboard" \
  "$SCRIPT_DIR/Normalize Clipboard.app"

echo ""
echo "Successfully built both apps!"
echo "- Markdownify Clipboard.app"
echo "- Normalize Clipboard.app"
