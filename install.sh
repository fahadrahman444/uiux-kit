#!/usr/bin/env bash
# SlopGuard / Gemini UI/UX Kit - Idempotent Installer & Sync
set -e

INSTALL_DIR="${HOME}/.gemini/uiux-kit"
REPO_URL="https://github.com/fahadrahman444/uiux-kit.git"
BIN_DEST="${HOME}/.local/bin"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "==> SlopGuard (Gemini UI/UX Kit) Installer"
echo "──────────────────────────────────────────"

mkdir -p "$INSTALL_DIR" "$BIN_DEST"

if [ "$SCRIPT_DIR" != "$INSTALL_DIR" ] && [ -f "$SCRIPT_DIR/bin/gemini-uiux" ]; then
    echo "==> Syncing from local source ($SCRIPT_DIR) to $INSTALL_DIR..."
    cp -r "${SCRIPT_DIR}/." "$INSTALL_DIR/"
elif [ -d "$INSTALL_DIR/.git" ]; then
    echo "==> Repository exists. Pulling latest updates..."
    cd "$INSTALL_DIR"
    git pull origin main || echo "Local modifications found. Preserving current state."
else
    echo "==> Fetching UI/UX kit into $INSTALL_DIR..."
    git clone "$REPO_URL" "$INSTALL_DIR" 2>/dev/null || (
        TMP_DIR=$(mktemp -d)
        git clone "$REPO_URL" "$TMP_DIR"
        cp -r "$TMP_DIR/." "$INSTALL_DIR/"
        rm -rf "$TMP_DIR"
    )
fi

# Permissions & Symlink both slopguard (primary) and gemini-uiux (legacy alias)
chmod +x "$INSTALL_DIR/bin/slopguard" "$INSTALL_DIR/bin/gemini-uiux" "$INSTALL_DIR/scripts/"*.sh "$INSTALL_DIR/scripts/"*.py "$INSTALL_DIR/install.sh" "$INSTALL_DIR/uninstall.sh" 2>/dev/null || true
ln -sf "$INSTALL_DIR/bin/slopguard" "$BIN_DEST/slopguard"
ln -sf "$INSTALL_DIR/bin/gemini-uiux" "$BIN_DEST/gemini-uiux"

echo "==> CLI installed to $BIN_DEST/slopguard (alias: gemini-uiux)"
"$INSTALL_DIR/scripts/doctor.sh"

echo "──────────────────────────────────────────"
echo "✓ Installation complete! Run 'slopguard help' or 'slopguard doctor' to start."
