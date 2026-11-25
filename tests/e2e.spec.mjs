import assert from "node:assert/strict";
import { spawn } from "node:child_process";
import fs from "node:fs";
import path from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";
import AxeBuilder from "@axe-core/playwright";
import { chromium } from "playwright";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const KIT_ROOT = path.resolve(__dirname, "..");
const PORT = 4179;
const BASE_URL = `http://127.0.0.1:${PORT}`;

function resolveChromePath() {
  const candidates = [
    process.env.CHROME_PATH,
    "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
    "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe",
    "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe",
    "/usr/bin/google-chrome",
    "/usr/bin/chromium",
    "/usr/bin/chromium-browser",
  ].filter(Boolean);
  for (const p of candidates) {
    if (fs.existsSync(p)) return p;
  }
  return undefined;
}

async function waitForServer(url, timeoutMs = 20000) {
  const start = Date.now();
  while (Date.now() - start < timeoutMs) {
    try {
      const res = await fetch(url);
      if (res.ok) return;
    } catch {
      // retry
    }
    await new Promise((r) => setTimeout(r, 200));
  }
  throw new Error(`Timed out waiting for Vite server at ${url}`);
}

let serverProc;
let browser;

test.before(async () => {
  const viteBin = path.join(KIT_ROOT, "node_modules", "vite", "bin", "vite.js");
  serverProc = spawn(
    process.execPath,
    [viteBin, "--config", "apps/demo/vite.config.ts", "--port", String(PORT), "--strictPort", "--host", "127.0.0.1"],
    { cwd: KIT_ROOT, stdio: ["ignore", "pipe", "pipe"] }
  );
  await waitForServer(BASE_URL);

  const pwExec = chromium.executablePath();
  const executablePath = pwExec && fs.existsSync(pwExec) ? pwExec : resolveChromePath();
  browser = await chromium.launch({
    ...(executablePath ? { executablePath } : {}),
    headless: true,
  });
});

test.after(async () => {
  if (browser) await browser.close();
  if (serverProc && !serverProc.killed) {
    serverProc.kill();
  }
});

test("WCAG 2.2 AA Axe-Core passes in Light & Dark modes across Marketing and Workspace views", async () => {
  const context = await browser.newContext({ viewport: { width: 1440, height: 900 } });
  const page = await context.newPage();
  await page.goto(BASE_URL, { waitUntil: "networkidle" });

  // 1. Marketing Light
  const mLight = await new AxeBuilder({ page }).withTags(["wcag2a", "wcag2aa", "wcag21aa", "wcag22aa"]).analyze();
  assert.deepEqual(mLight.violations, [], `Marketing light violations: ${JSON.stringify(mLight.violations, null, 2)}`);

  // 2. Marketing Dark (also verify CSS tokens actually drive computed styles!)
  const bgBefore = await page.evaluate(() => getComputedStyle(document.body).backgroundColor);
  await page.getByTestId("theme-toggle").click();
  await page.waitForTimeout(100);
  const bgAfter = await page.evaluate(() => getComputedStyle(document.body).backgroundColor);
  assert.notEqual(bgBefore, bgAfter, "Toggling .dark should change CSS token computed background color");

  const mDark = await new AxeBuilder({ page }).withTags(["wcag2a", "wcag2aa", "wcag21aa", "wcag22aa"]).analyze();
  assert.deepEqual(mDark.violations, [], `Marketing dark violations: ${JSON.stringify(mDark.violations, null, 2)}`);

  // 3. Workspace Dark + Light
  await page.getByTestId("view-toggle").click();
  await page.waitForTimeout(100);
  const wDark = await new AxeBuilder({ page }).withTags(["wcag2a", "wcag2aa", "wcag21aa", "wcag22aa"]).analyze();
  assert.deepEqual(wDark.violations, [], `Workspace dark violations: ${JSON.stringify(wDark.violations, null, 2)}`);

  await page.getByTestId("theme-toggle").click();
  await page.waitForTimeout(100);
  const wLight = await new AxeBuilder({ page }).withTags(["wcag2a", "wcag2aa", "wcag21aa", "wcag22aa"]).analyze();
  assert.deepEqual(wLight.violations, [], `Workspace light violations: ${JSON.stringify(wLight.violations, null, 2)}`);

  await context.close();
});

test("PatternSpecAccordion uses inert grid transition (no display:none hidden bug)", async () => {
  const context = await browser.newContext({ viewport: { width: 1280, height: 900 } });
  const page = await context.newPage();
  await page.goto(BASE_URL, { waitUntil: "networkidle" });

  const triggers = page.locator("#specs button[aria-expanded]");
  assert.equal(await triggers.count(), 2);

  // Second panel starts collapsed
  const secondTrigger = triggers.nth(1);
  const panelId = await secondTrigger.getAttribute("aria-controls");
  const secondPanel = page.locator(`#${panelId}`);

  assert.equal(await secondTrigger.getAttribute("aria-expanded"), "false");
  assert.equal(await secondPanel.getAttribute("aria-hidden"), "true");
  assert.notEqual(await secondPanel.getAttribute("inert"), null, "Collapsed panel must have inert attribute");

  const collapsedStyles = await secondPanel.evaluate((el) => {
    const cs = getComputedStyle(el);
    return {
      display: cs.display,
      visibility: cs.visibility,
      gridTemplateRows: cs.gridTemplateRows,
      hasHiddenAttr: el.hasAttribute("hidden"),
    };
  });
  assert.equal(collapsedStyles.hasHiddenAttr, false, "Collapsed panel must NOT use HTML hidden attribute");
  assert.equal(collapsedStyles.display, "grid", "Panel must stay display:grid so height transitions animate");
  assert.equal(collapsedStyles.visibility, "hidden");
  assert.equal(collapsedStyles.gridTemplateRows, "0px");

  // Click to expand and verify open state
  await secondTrigger.click();
  await page.waitForTimeout(250);
  assert.equal(await secondTrigger.getAttribute("aria-expanded"), "true");
  assert.equal(await secondPanel.getAttribute("aria-hidden"), "false");
  assert.equal(await secondPanel.getAttribute("inert"), null, "Expanded panel must remove inert");

  const expandedStyles = await secondPanel.evaluate((el) => {
    const cs = getComputedStyle(el);
    return { visibility: cs.visibility, height: el.getBoundingClientRect().height };
  });
  assert.equal(expandedStyles.visibility, "visible");
  assert.ok(expandedStyles.height > 20, `Expanded accordion panel should have height > 20px, got ${expandedStyles.height}`);

  await context.close();
});

test("Target sizes (>= 24px / >= 44px), 320px reflow, Focus Not Obscured (2.4.11), and SLOP-004 viewport budget", async () => {
  for (const vp of [
    { width: 320, height: 700 },
    { width: 390, height: 844 },
    { width: 768, height: 1024 },
    { width: 1440, height: 900 },
  ]) {
    const context = await browser.newContext({ viewport: vp });
    const page = await context.newPage();
    await page.goto(BASE_URL, { waitUntil: "networkidle" });

    // Reflow: zero horizontal overflow
    const overflow = await page.evaluate(() => ({
      scrollWidth: document.documentElement.scrollWidth,
      innerWidth: window.innerWidth,
    }));
    assert.ok(
      overflow.scrollWidth <= overflow.innerWidth,
      `Horizontal overflow at ${vp.width}px: scrollWidth=${overflow.scrollWidth} > innerWidth=${overflow.innerWidth}`
    );

    // Target sizes & SLOP-004 uppercase count
    const checks = await page.evaluate(() => {
      const tinyTargets = [];
      const els = document.querySelectorAll("a, button, input, select, textarea");
      for (const el of els) {
        const cs = getComputedStyle(el);
        if (cs.display === "none" || cs.visibility === "hidden" || el.closest("[inert]")) continue;
        const r = el.getBoundingClientRect();
        if (r.width === 0 && r.height === 0) continue;
        if (r.width < 24 || r.height < 24) {
          tinyTargets.push({ tag: el.tagName, text: el.textContent?.trim(), w: r.width, h: r.height });
        }
      }
      const uppercaseEls = Array.from(document.querySelectorAll("*")).filter((el) => {
        const cs = getComputedStyle(el);
        return cs.display !== "none" && cs.visibility !== "hidden" && cs.textTransform === "uppercase";
      });
      return { tinyTargets, uppercaseCount: uppercaseEls.length };
    });

    assert.deepEqual(checks.tinyTargets, [], `Targets < 24x24px at ${vp.width}px: ${JSON.stringify(checks.tinyTargets)}`);
    assert.ok(checks.uppercaseCount <= 1, `Too many uppercase labels (${checks.uppercaseCount}) at ${vp.width}px`);

    await context.close();
  }

  // Focus Not Obscured (WCAG 2.4.11) while tabbing at mobile 390x844
  const mobileCtx = await browser.newContext({ viewport: { width: 390, height: 844 } });
  const mobilePage = await mobileCtx.newPage();
  await mobilePage.goto(BASE_URL, { waitUntil: "networkidle" });

  for (let i = 0; i < 8; i++) {
    await mobilePage.keyboard.press("Tab");
    const obscured = await mobilePage.evaluate(() => {
      const el = document.activeElement;
      if (!el || el === document.body) return null;
      el.scrollIntoView({ block: "center", inline: "nearest" });
      const r = el.getBoundingClientRect();
      if (r.width === 0 || r.height === 0) return null;
      const cx = r.left + r.width / 2;
      const cy = r.top + r.height / 2;
      const hit = document.elementFromPoint(cx, cy);
      const ok = hit && (el === hit || el.contains(hit) || hit.contains(el));
      return ok ? null : { activeTag: el.tagName, text: el.textContent?.trim(), hitTag: hit?.tagName };
    });
    assert.equal(obscured, null, `Focused element obscured: ${JSON.stringify(obscured)}`);
  }
  await mobileCtx.close();
});

test("ModalDialog & BottomSheet trap focus, close on Escape, and restore focus to trigger", async () => {
  const context = await browser.newContext({ viewport: { width: 390, height: 844 } });
  const page = await context.newPage();
  await page.goto(BASE_URL, { waitUntil: "networkidle" });

  const openDialogBtn = page.getByRole("button", { name: "Open Dialog" });
  await openDialogBtn.focus();
  await openDialogBtn.click();

  const dialog = page.getByRole("dialog", { name: "Accessibility Focus Trap" });
  await dialog.waitFor({ state: "visible" });
  await page.waitForTimeout(150);

  // Focus stays inside dialog while tabbing
  for (let i = 0; i < 5; i++) {
    await page.keyboard.press("Tab");
    const inside = await page.evaluate(() => {
      const d = document.querySelector('[role="dialog"]');
      return Boolean(d && d.contains(document.activeElement));
    });
    assert.equal(inside, true, "Focus escaped ModalDialog during Tab navigation");
  }

  await page.keyboard.press("Escape");
  await dialog.waitFor({ state: "hidden" });
  const restoredText = await page.evaluate(() => document.activeElement?.textContent?.trim());
  assert.equal(restoredText, "Open Dialog", "Focus must restore to initiating trigger after Escape");

  // Mobile BottomSheet open + Escape restore
  const sheetTrigger = page.getByRole("button", { name: "Open Mobile Sheet" });
  await sheetTrigger.focus();
  await sheetTrigger.click();
  const sheet = page.getByRole("dialog", { name: "Mobile Navigation Sheet" });
  await sheet.waitFor({ state: "visible" });
  await page.keyboard.press("Escape");
  await sheet.waitFor({ state: "hidden" });

  await context.close();
});

test("Enterprise Workspace components (AppShell, ChartRow, DataTable, FormEngine) work interactively", async () => {
  const context = await browser.newContext({ viewport: { width: 1280, height: 900 } });
  const page = await context.newPage();
  await page.goto(BASE_URL, { waitUntil: "networkidle" });
  await page.getByTestId("view-toggle").click();

  // AppShell sidebar toggle & notification Escape dismiss
  const sidebarBtn = page.getByRole("button", { name: /Collapse sidebar/i });
  assert.equal(await sidebarBtn.getAttribute("aria-expanded"), "true");
  await sidebarBtn.click();
  assert.equal(await page.getByRole("button", { name: /Expand sidebar/i }).getAttribute("aria-expanded"), "false");

  const notifBtn = page.getByRole("button", { name: /Notifications/i });
  await notifBtn.click();
  await page.getByRole("region", { name: "Recent notifications" }).waitFor({ state: "visible" });
  await page.keyboard.press("Escape");
  await page.getByRole("region", { name: "Recent notifications" }).waitFor({ state: "hidden" });

  // ChartRow SVG role=img
  const svgs = page.locator("#telemetry-charts svg[role='img']");
  assert.equal(await svgs.count(), 2);

  // DataTable sorting + search filtering + empty reset
  const compSortBtn = page.locator("#data-table th button", { hasText: "Component" });
  await compSortBtn.click();
  const th = page.locator("#data-table th", { hasText: "Component" });
  assert.equal(await th.getAttribute("aria-sort"), "ascending");

  const searchInput = page.getByLabel("Search table");
  await searchInput.fill("nonexistent-query");
  await page.getByText("No matching records found.").waitFor({ state: "visible" });
  await page.getByRole("button", { name: "Reset filter" }).click();
  assert.equal(await page.locator("#data-table tbody tr").count(), 4);

  // FormEngine: wait > 150ms time-trap, trigger empty validation alert, then fill & submit cleanly
  await page.waitForTimeout(200);
  await page.getByRole("button", { name: "Submit request" }).click();
  const alertBox = page.locator("#intake-form [role='alert']");
  await alertBox.waitFor({ state: "visible" });
  assert.equal(await page.getByLabel(/Engineering owner/i).getAttribute("aria-invalid"), "true");

  await page.getByLabel(/Engineering owner/i).fill("Grace Hopper");
  await page.getByLabel(/Work email/i).fill("grace@example.com");
  await page.getByLabel(/Waiver severity/i).selectOption("minor");
  await page.getByLabel(/Technical justification/i).fill("Tier comparison parity verified in review.");
  await page.getByRole("button", { name: "Submit request" }).click();

  await page.locator("#intake-form [role='status']").waitFor({ state: "visible" });
  const telemetryJson = await page.getByTestId("telemetry-log").textContent();
  assert.ok(telemetryJson && !telemetryJson.includes("grace@example.com"), "Zero-PII telemetry must not log email");

  await context.close();
});
