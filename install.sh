#!/usr/bin/env bash
# Gemini UI/UX Kit - Local / Global Installer
set -e

INSTALL_DIR="${HOME}/.gemini/uiux-kit"
BIN_DEST="${HOME}/.local/bin"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "==> Installing Gemini UI/UX Kit..."
mkdir -p "$INSTALL_DIR" "$BIN_DEST"

# Sync files
cp -r "${SCRIPT_DIR}/"* "$INSTALL_DIR/"

# Permissions
chmod +x "$INSTALL_DIR/bin/gemini-uiux" "$INSTALL_DIR/scripts/"*.sh

# Symlink CLI
ln -sf "$INSTALL_DIR/bin/gemini-uiux" "$BIN_DEST/gemini-uiux"

echo "==> CLI installed to $BIN_DEST/gemini-uiux"
echo "✓ Run 'gemini-uiux help' or 'gemini-uiux doctor' to get started."
