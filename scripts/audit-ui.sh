#!/usr/bin/env bash
# Gemini UI/UX Kit - Automated Design & Accessibility Audit Script
set -e

DIR="${1:-.}"
OUTPUT_FILE="${2:-}"
cd "$DIR"

CYAN="\033[0;36m"
GREEN="\033[0;32m"
RED="\033[0;31m"
YELLOW="\033[0;33m"
BOLD="\033[1m"
RESET="\033[0m"

echo -e "${BOLD}${CYAN}Gemini UI/UX Audit Engine${RESET}"
echo -e "${CYAN}Target:${RESET} $(pwd)"
echo -e "${CYAN}──────────────────────────────────────────────────${RESET}"

WARNINGS=0
ERRORS=0

# 1. Check for animated opacity on backdrop blur (compositor performance lag)
echo -ne "Checking for backdrop-blur opacity animation antipattern... "
BLUR_ANIM=$(grep -rnE "(backdrop-blur.*animate-fade|animate-fade.*backdrop-blur|motion\.div.*backdrop-blur.*opacity)" . \
    --exclude-dir={.git,node_modules,dist,build,.gemini,.design,scripts} 2>/dev/null || true)
if [ -n "$BLUR_ANIM" ]; then
    echo -e "${RED}FOUND${RESET}"
    echo -e "${YELLOW}  ⚠ Warning: Animating opacity on backdrop-filter elements drops FPS significantly on mobile.${RESET}"
    WARNINGS=$((WARNINGS + 1))
else
    echo -e "${GREEN}PASS${RESET}"
fi

# 2. Check for sub-44px touch targets on buttons
echo -ne "Scanning for sub-44px buttons (< 44x44px footprint)... "
TINY_BUTTONS=$(grep -rnE "className=.*(h-[4-8]|p-[0-1])\b" . \
    --include="*.tsx" --include="*.jsx" --exclude-dir={.git,node_modules,dist,build} 2>/dev/null | grep -E "(<button|<a)" | head -n 5 || true)
if [ -n "$TINY_BUTTONS" ]; then
    echo -e "${YELLOW}POTENTIAL ISSUES${RESET}"
    echo -e "${YELLOW}  Ensure buttons and touch triggers have min-h-[44px] min-w-[44px] for mobile finger reachability.${RESET}"
    WARNINGS=$((WARNINGS + 1))
else
    echo -e "${GREEN}PASS${RESET}"
fi

# 3. Check for static 100vh on mobile layouts
echo -ne "Checking for rigid 100vh viewport bug... "
RIGID_VH=$(grep -rnE "\b(h-screen|h-\[100vh\]|min-h-screen)\b" . \
    --include="*.tsx" --include="*.jsx" --include="*.css" --exclude-dir={.git,node_modules,dist,build} 2>/dev/null | head -n 5 || true)
if [ -n "$RIGID_VH" ]; then
    echo -e "${YELLOW}NOTICE${RESET}"
    echo -e "${YELLOW}  Consider migrating 'h-screen' / '100vh' to 'min-h-[100dvh]' to prevent mobile URL bar layout jump.${RESET}"
    WARNINGS=$((WARNINGS + 1))
else
    echo -e "${GREEN}PASS${RESET}"
fi

# 4. Check for unlabelled icon buttons (missing aria-label)
echo -ne "Scanning for icon-only buttons missing aria-label... "
UNLABELLED=$(grep -rnE "<button[^>]*>[[:space:]]*<svg" . \
    --include="*.tsx" --include="*.jsx" --exclude-dir={.git,node_modules,dist,build} 2>/dev/null | grep -v "aria-label" | head -n 5 || true)
if [ -n "$UNLABELLED" ]; then
    echo -e "${YELLOW}NOTICE${RESET}"
    echo -e "${YELLOW}  Found icon-only buttons without explicit aria-label attribute (WCAG 2.1 AA requirement).${RESET}"
    WARNINGS=$((WARNINGS + 1))
else
    echo -e "${GREEN}PASS${RESET}"
fi

# 5. Check for non-tokenized arbitrary hex classes (e.g. bg-[#...], text-[#...])
echo -ne "Scanning for non-tokenized arbitrary hex utilities... "
ARBITRARY_HEX=$(grep -rnE "(bg|text|border|ring)-\[#[0-9a-fA-F]{3,8}\]" . \
    --include="*.tsx" --include="*.jsx" --exclude-dir={.git,node_modules,dist,build} 2>/dev/null | head -n 5 || true)
if [ -n "$ARBITRARY_HEX" ]; then
    echo -e "${YELLOW}FOUND${RESET}"
    echo -e "${YELLOW}  Found arbitrary hex classes (e.g. bg-[#...]). Centralize them in tailwind.config or CSS variables.${RESET}"
    WARNINGS=$((WARNINGS + 1))
else
    echo -e "${GREEN}PASS${RESET}"
fi

# 6. Check for React state updates on mousemove (laggy cursor effects)
echo -ne "Scanning for unaccelerated onMouseMove state updates... "
MOUSE_STATE=$(grep -rnE "onMouseMove=\{.*set[A-Z]" . \
    --include="*.tsx" --include="*.jsx" --exclude-dir={.git,node_modules,dist,build} 2>/dev/null | head -n 5 || true)
if [ -n "$MOUSE_STATE" ]; then
    echo -e "${RED}FOUND${RESET}"
    echo -e "${YELLOW}  Detected React state updates inside onMouseMove. Offload cursor coords to CSS custom properties.${RESET}"
    WARNINGS=$((WARNINGS + 1))
else
    echo -e "${GREEN}PASS${RESET}"
fi

echo -e "${CYAN}──────────────────────────────────────────────────${RESET}"
if [ $ERRORS -eq 0 ] && [ $WARNINGS -eq 0 ]; then
    echo -e "Audit Result: ${GREEN}${BOLD}CLEAN & ACCESSIBLE${RESET}"
    exit 0
else
    echo -e "Audit Result: ${YELLOW}${BOLD}${WARNINGS} advisory items / ${ERRORS} errors${RESET}"
    exit 0
fi
