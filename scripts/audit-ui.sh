#!/usr/bin/env bash
# SlopGuard / Gemini UI/UX Kit - Automated Design & Accessibility Audit Wrapper
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

find_python() {
    for cand in python3 python py; do
        if command -v "$cand" >/dev/null 2>&1 && "$cand" -c "import sys" >/dev/null 2>&1; then
            echo "$cand"
            return 0
        fi
    done
    return 1
}

PYTHON_BIN="$(find_python || true)"
if [ -z "$PYTHON_BIN" ]; then
    echo "Error: Working Python 3 interpreter is required to run the SlopGuard audit engine." >&2
    exit 2
fi

exec "$PYTHON_BIN" "${SCRIPT_DIR}/audit_engine.py" "$@"
