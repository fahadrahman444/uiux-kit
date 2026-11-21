#!/usr/bin/env bash
# Gemini UI/UX Kit - Uninstaller
set -e

INSTALL_DIR="${HOME}/.gemini/uiux-kit"
BIN_LINK="${HOME}/.local/bin/gemini-uiux"

echo "==> Uninstalling Gemini UI/UX Kit..."
rm -f "$BIN_LINK"
rm -rf "$INSTALL_DIR"

echo "✓ Gemini UI/UX Kit successfully removed."
