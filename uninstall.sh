#!/usr/bin/env bash
# SlopGuard / Gemini UI/UX Kit - Uninstaller
set -e

INSTALL_DIR="${HOME}/.gemini/uiux-kit"

echo "==> Uninstalling SlopGuard (Gemini UI/UX Kit)..."
rm -f "${HOME}/.local/bin/slopguard" "${HOME}/.local/bin/gemini-uiux"
rm -rf "$INSTALL_DIR"

echo "✓ SlopGuard (Gemini UI/UX Kit) successfully removed."
