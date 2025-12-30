#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "Quitting running apps if any..."
killall "Markdownify Clipboard" 2>/dev/null || true
killall "Normalize Clipboard" 2>/dev/null || true
sleep 0.5

echo "Removing old apps from /Applications/..."
rm -rf "/Applications/Markdownify Clipboard.app" || true
rm -rf "/Applications/Normalize Clipboard.app" || true

echo "Installing apps to /Applications/..."
cp -r "$SCRIPT_DIR/Markdownify Clipboard.app" /Applications/
cp -r "$SCRIPT_DIR/Normalize Clipboard.app" /Applications/

echo ""
echo "Apps installed to /Applications/"
echo "Launching apps..."
open "/Applications/Markdownify Clipboard.app"
open "/Applications/Normalize Clipboard.app"

