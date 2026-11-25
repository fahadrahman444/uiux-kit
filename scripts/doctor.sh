#!/usr/bin/env bash
# Gemini UI/UX Kit - Doctor Diagnostic Script
set -e

GREEN="\033[0;32m"
YELLOW="\033[0;33m"
CYAN="\033[0;36m"
BOLD="\033[1m"
RESET="\033[0m"

echo -e "${BOLD}${CYAN}Gemini UI/UX Kit — Doctor${RESET}"
echo -e "${CYAN}──────────────────────────────────────────${RESET}"

check_tool() {
    local name="$1"
    local cmd="$2"
    if command -v "$cmd" >/dev/null 2>&1; then
        echo -e "  ${GREEN}✓${RESET} ${name} (${cmd} available)"
    else
        echo -e "  ${YELLOW}⚠${RESET} ${name} (${cmd} not detected)"
    fi
}

echo -e "\n${BOLD}Frontend & Audit Runtime Tooling:${RESET}"
check_tool "Python 3" "python3"
check_tool "Python" "python"
check_tool "Node.js" "node"
check_tool "npm / npx" "npm"
check_tool "Git" "git"
check_tool "Tailwind CSS CLI" "tailwindcss"

echo -e "\n${BOLD}Package Managers (Optional):${RESET}"
check_tool "pnpm" "pnpm"
check_tool "yarn" "yarn"
check_tool "bun" "bun"

echo -e "\n${CYAN}──────────────────────────────────────────${RESET}"
echo -e "Status: ${GREEN}${BOLD}OPERATIONAL${RESET}"
