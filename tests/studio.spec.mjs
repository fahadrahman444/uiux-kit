import assert from "node:assert/strict";
import fs from "node:fs";
import http from "node:http";
import path from "node:path";
import test from "node:test";
import { fileURLToPath, pathToFileURL } from "node:url";
import AxeBuilder from "@axe-core/playwright";
import { chromium } from "playwright";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const KIT_ROOT = path.resolve(__dirname, "..");
const DOCS_DIR = path.join(KIT_ROOT, "docs");

const MIME_TYPES = {
  ".html": "text/html; charset=utf-8",
  ".css": "text/css; charset=utf-8",
  ".js": "application/javascript; charset=utf-8",
  ".json": "application/json; charset=utf-8",
};

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

let server;
let baseUrl;
let browser;

test.before(async () => {
  server = http.createServer((req, res) => {
    const cleanPath = (req.url || "/").split("?")[0];
    const rel = cleanPath === "/" ? "index.html" : cleanPath.replace(/^\/+/, "");
    const target = path.resolve(DOCS_DIR, rel);
    if (!target.startsWith(DOCS_DIR) || !fs.existsSync(target) || fs.statSync(target).isDirectory()) {
      res.writeHead(404);
      res.end("Not found");
      return;
    }
    const ext = path.extname(target).toLowerCase();
    res.writeHead(200, { "Content-Type": MIME_TYPES[ext] || "application/octet-stream" });
    fs.createReadStream(target).pipe(res);
  });

  await new Promise((resolve) => server.listen(0, "127.0.0.1", resolve));
  const addr = server.address();
  baseUrl = `http://127.0.0.1:${addr.port}/`;

  const pwExec = chromium.executablePath();
  const executablePath = pwExec && fs.existsSync(pwExec) ? pwExec : resolveChromePath();
  browser = await chromium.launch({
    ...(executablePath ? { executablePath } : {}),
    headless: true,
  });
});

test.after(async () => {
  if (browser) await browser.close();
  if (server) server.close();
});

test("Vanilla Studio works over HTTP (GitHub Pages mode) and passes WCAG 2.2 AA in Light & Dark modes", async () => {
  const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 } });
  const page = await ctx.newPage();
  const errors = [];
  page.on("pageerror", (e) => errors.push(e.message));

  await page.goto(baseUrl, { waitUntil: "networkidle" });
  await page.waitForSelector("#panel-sections .blueprint-card");
  assert.deepEqual(errors, [], `Runtime page errors: ${errors.join("; ")}`);

  // Axe scan Light
  const axeLight = await new AxeBuilder({ page }).withTags(["wcag2a", "wcag2aa", "wcag21aa", "wcag22aa"]).analyze();
  assert.deepEqual(axeLight.violations, [], `Studio light violations: ${JSON.stringify(axeLight.violations, null, 2)}`);

  // Switch preset to pricing & compile
  await page.locator('[data-preset="pricing"]').click();
  await page.locator("#project_name").fill("Apex Security Suite");
  await page.locator("#compile-btn").click();

  const statusText = await page.locator("#compile-status").textContent();
  assert.ok(statusText.includes("10 sections") && statusText.includes("Apex Security Suite"), `Unexpected status: ${statusText}`);

  // Verify bottom section panels & tab switching
  const sectionCards = await page.locator("#panel-sections .blueprint-card").count();
  assert.equal(sectionCards, 10, "Pricing page should compile 10 sections");

  await page.locator("#tab-intel").click();
  await page.locator("#panel-intel").waitFor({ state: "visible" });
  assert.ok((await page.locator("#panel-intel").textContent()).includes("Style Priority"));

  await page.locator("#tab-strategy").click();
  await page.locator("#panel-strategy").waitFor({ state: "visible" });
  assert.ok((await page.locator("#panel-strategy").textContent()).includes("05. Consolidated Project Sitemap"));

  await page.locator("#tab-stack").click();
  await page.locator("#panel-stack").waitFor({ state: "visible" });
  assert.ok((await page.locator("#panel-stack").textContent()).includes("Stack Guidelines"));

  await page.locator("#tab-markdown").click();
  await page.locator("#panel-markdown").waitFor({ state: "visible" });
  const mdText = await page.locator("#panel-markdown pre").textContent();
  assert.ok(mdText.includes("Apex Security Suite") && mdText.includes("Production Engineering & Audit Guardrails"));

  await page.locator("#tab-cli").click();
  await page.locator("#panel-cli").waitFor({ state: "visible" });
  const cliText = await page.locator("#panel-cli").textContent();
  assert.ok(cliText.includes('"page_id": "pricing"'));

  // 5-Step Wizard navigation & multi-page Sitemap compilation
  await page.locator('[data-preset="multisite"]').click();
  await page.locator("#tab-sections").click();
  await page.locator("#panel-sections").waitFor({ state: "visible" });
  const groupCount = await page.locator("#panel-sections .page-group-header").count();
  assert.equal(groupCount, 5, "Multisite preset should compile 5 page groups");

  await page.locator('#wizard-next-btn').click();
  await page.locator('.wizard-step[data-step="2"]').waitFor({ state: "visible" });
  await page.locator('#wizard-prev-btn').click();
  await page.locator('.wizard-step[data-step="1"]').waitFor({ state: "visible" });
  await page.locator('.step-pill[data-wizard-step="4"]').click();
  await page.locator('.wizard-step[data-step="4"]').waitFor({ state: "visible" });

  // Step 4 contextual Sitemap route highlighting
  assert.equal(await page.locator('details[data-route-group="about"]').getAttribute("open") !== null, true);
  assert.equal(await page.locator('details[data-route-group="about"] .route-tag').isVisible(), true);
  assert.equal(await page.locator('details[data-route-group="careers"]').getAttribute("open"), null);

  await page.locator("#sitemap-single-btn").click();
  await page.locator("#page_id").selectOption("careers");
  assert.equal(await page.locator('details[data-route-group="careers"]').getAttribute("open") !== null, true);
  assert.equal(await page.locator('details[data-route-group="about"]').getAttribute("open"), null);
  await page.locator('input[name="interview_pipeline"]').check();
  await page.locator("#compile-btn").click();
  assert.ok((await page.locator("#panel-sections").textContent()).includes("jobs-03"));

  // Required validation from Step 5 auto-returns to Step 1
  await page.locator('.step-pill[data-wizard-step="1"]').click();
  await page.locator('.wizard-step[data-step="1"]').waitFor({ state: "visible" });
  await page.locator("#project_name").fill("");
  await page.locator('.step-pill[data-wizard-step="5"]').click();
  await page.locator('.wizard-step[data-step="5"]').waitFor({ state: "visible" });
  await page.locator("#compile-btn").click();
  await page.locator('.wizard-step[data-step="1"]').waitFor({ state: "visible" });
  await page.locator("#project_name").fill("Restored Project");
  await page.locator("#compile-btn").click();

  // Toggle Dark Mode (also exercising View Transitions) and re-run Axe once transition settles
  await page.locator("#theme-toggle").click();
  await page.waitForFunction(() => document.documentElement.classList.contains("dark") && !document.documentElement.hasAttribute("data-vt"));
  const axeDark = await new AxeBuilder({ page }).withTags(["wcag2a", "wcag2aa", "wcag21aa", "wcag22aa"]).analyze();
  assert.deepEqual(axeDark.violations, [], `Studio dark violations: ${JSON.stringify(axeDark.violations, null, 2)}`);

  await ctx.close();
});

test("Vanilla Studio works directly via file:// without a backend and passes 320px mobile reflow", async () => {
  const ctx = await browser.newContext({ viewport: { width: 320, height: 740 } });
  const page = await ctx.newPage();
  const errors = [];
  page.on("pageerror", (e) => errors.push(e.message));

  const fileUrl = pathToFileURL(path.join(DOCS_DIR, "index.html")).href;
  await page.goto(fileUrl, { waitUntil: "load" });
  await page.waitForSelector("#panel-sections .blueprint-card");
  assert.deepEqual(errors, [], `file:// runtime errors: ${errors.join("; ")}`);

  const overflow = await page.evaluate(() => ({
    scrollWidth: document.documentElement.scrollWidth,
    innerWidth: window.innerWidth,
  }));
  assert.ok(overflow.scrollWidth <= overflow.innerWidth, `Mobile 320px overflow: ${overflow.scrollWidth} > ${overflow.innerWidth}`);

  await ctx.close();
});
