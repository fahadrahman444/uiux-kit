import React, { useEffect, useState } from "react";
import { ActionButton } from "../../../components/feedback/ActionButton";
import { SkeletonLoader } from "../../../components/feedback/SkeletonLoader";
import { SpotlightCard } from "../../../components/feedback/SpotlightCard";
import { BottomTabBar } from "../../../components/navigation/BottomTabBar";
import { ResponsiveHeader } from "../../../components/navigation/ResponsiveHeader";
import { BottomSheet } from "../../../components/overlays/BottomSheet";
import { ModalDialog } from "../../../components/overlays/ModalDialog";
import {
  PatternAppShell,
  PatternBentoGrid,
  PatternChartRow,
  PatternComparison,
  PatternCtaBand,
  PatternDataTable,
  PatternFormEngine,
  PatternSocialProof,
  PatternSpecAccordion,
  PatternSplitHero,
  PatternStepper,
  PatternTieredPricing,
  type FormTelemetryEvent,
} from "../../../components/patterns";

export const App: React.FC = () => {
  const [darkMode, setDarkMode] = useState(false);
  const [viewMode, setViewMode] = useState<"marketing" | "workspace">("marketing");
  const [modalOpen, setModalOpen] = useState(false);
  const [sheetOpen, setSheetOpen] = useState(false);
  const [actionLoading, setActionLoading] = useState(false);
  const [selectedRowId, setSelectedRowId] = useState<string | null>(null);
  const [lastTelemetry, setLastTelemetry] = useState<FormTelemetryEvent | null>(null);

  useEffect(() => {
    document.documentElement.classList.toggle("dark", darkMode);
  }, [darkMode]);

  const handleSimulatedAction = () => {
    setActionLoading(true);
    window.setTimeout(() => setActionLoading(false), 350);
  };

  const navLinks = [
    { label: "Features", href: "#features" },
    { label: "Comparison", href: "#comparison" },
    { label: "Specs", href: "#specs" },
    { label: "Pricing", href: "#pricing" },
    { label: "Contact", href: "#cta-band" },
  ];

  const themeAndModeControls = (
    <div className="flex items-center gap-2">
      <button
        type="button"
        data-testid="view-toggle"
        onClick={() => setViewMode((v) => (v === "marketing" ? "workspace" : "marketing"))}
        className="min-h-[44px] inline-flex items-center justify-center rounded-lg border border-[var(--border-strong)] bg-[var(--surface-raised)] px-3 py-2 text-xs font-semibold text-[var(--text-primary)] hover:bg-[var(--surface-subtle)] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--color-focus-ring)] forced-colors:focus-visible:outline-[Highlight] cursor-pointer"
      >
        {viewMode === "marketing" ? "Workspace View" : "Marketing View"}
      </button>
      <button
        type="button"
        data-testid="theme-toggle"
        aria-pressed={darkMode}
        onClick={() => setDarkMode((d) => !d)}
        className="min-h-[44px] inline-flex items-center justify-center rounded-lg border border-[var(--border-strong)] bg-[var(--surface-base)] px-3 py-2 text-xs font-semibold text-[var(--text-primary)] hover:bg-[var(--surface-subtle)] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--color-focus-ring)] forced-colors:focus-visible:outline-[Highlight] cursor-pointer"
      >
        {darkMode ? "Light Mode" : "Dark Mode"}
      </button>
    </div>
  );

  if (viewMode === "workspace") {
    return (
      <PatternAppShell
        brandName="SlopGuard Ops"
        navItems={[
          { id: "overview", label: "Telemetry", href: "#telemetry-charts", active: true, badge: "Live" },
          { id: "inventory", label: "Component Ledger", href: "#data-table", badge: "23" },
          { id: "intake", label: "Audit Intake", href: "#intake-form" },
        ]}
        breadcrumbs={[
          { label: "Console", href: "#telemetry-charts" },
          { label: "Verification Gate" },
        ]}
        user={{ name: "Ada Lovelace", role: "Staff A11y Lead", initials: "AL" }}
        notifications={[
          { id: "n1", title: "Static AST audit passed (100/100)", time: "2m ago", unread: true },
          { id: "n2", title: "WCAG 2.2 AA token check verified", time: "14m ago" },
        ]}
        headerActions={themeAndModeControls}
      >
        <PatternChartRow
          badge="Verified Telemetry"
          title="Accessibility & Performance Gate History"
          description="Live verification counters bound exclusively to CSS semantic tokens and currentColor SVG primitives."
          sourceNote="Internal Playwright + Axe-Core CI benchmark across 23 kit components (Q4 2026)."
          charts={[
            {
              id: "anti-slop",
              title: "Static Anti-Slop Score",
              metricValue: "100 / 100",
              deltaLabel: "+0 blockers",
              deltaTone: "positive",
              dateRange: "Nov 18 – Nov 25, 2026",
              points: [
                { label: "Nov 18", value: 84 },
                { label: "Nov 20", value: 92 },
                { label: "Nov 22", value: 96 },
                { label: "Nov 24", value: 100 },
                { label: "Nov 25", value: 100 },
              ],
            },
            {
              id: "contrast",
              title: "AAA Palette Compliance",
              metricValue: "96 / 96",
              deltaLabel: "100% pass",
              deltaTone: "positive",
              dateRange: "Nov 18 – Nov 25, 2026",
              points: [
                { label: "Nov 18", value: 89 },
                { label: "Nov 20", value: 91 },
                { label: "Nov 22", value: 96 },
                { label: "Nov 24", value: 96 },
                { label: "Nov 25", value: 96 },
              ],
            },
          ]}
        />

        <PatternDataTable
          title="Component Verification Ledger"
          description="Sortable and searchable audit matrix for all production UI primitives."
          caption="Component verification ledger"
          columns={[
            { key: "component", label: "Component", sortable: true },
            { key: "category", label: "Category", sortable: true },
            { key: "targetPx", label: "Min Target (px)", sortable: true, numeric: true },
            { key: "score", label: "Score", sortable: true, numeric: true },
          ]}
          rows={[
            {
              id: "row-hero",
              status: "healthy",
              cells: { component: "PatternSplitHero", category: "Landing", targetPx: 44, score: 100 },
            },
            {
              id: "row-accordion",
              status: "healthy",
              cells: { component: "PatternSpecAccordion", category: "Disclosure", targetPx: 44, score: 100 },
            },
            {
              id: "row-table",
              status: "healthy",
              cells: { component: "PatternDataTable", category: "Enterprise", targetPx: 44, score: 100 },
            },
            {
              id: "row-form",
              status: "warning",
              cells: { component: "PatternFormEngine", category: "Enterprise", targetPx: 44, score: 98 },
            },
          ]}
          onRowAction={(row) => setSelectedRowId(row.id)}
          rowActionLabel="Select"
        />

        {selectedRowId && (
          <div role="status" className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-3 text-xs font-mono text-[var(--text-secondary)]">
            Selected row: {selectedRowId}
          </div>
        )}

        <PatternFormEngine
          title="Enterprise Security & Accessibility Waiver Intake"
          description="Demonstrates inline validation, role=alert error summary, honeypot discard, and zero-PII telemetry."
          minSubmitMs={150}
          fields={[
            {
              name: "ownerName",
              label: "Engineering owner",
              type: "text",
              required: true,
              autoComplete: "name",
              placeholder: "Ada Lovelace",
              helperText: "Use your full team contact name.",
            },
            {
              name: "ownerEmail",
              label: "Work email",
              type: "email",
              required: true,
              autoComplete: "email",
              placeholder: "ada@example.com",
            },
            {
              name: "severityTier",
              label: "Waiver severity",
              type: "select",
              required: true,
              options: [
                { label: "Minor (Peer Sign-Off)", value: "minor" },
                { label: "Major (System Lead)", value: "major" },
              ],
            },
            {
              name: "justification",
              label: "Technical justification",
              type: "textarea",
              required: true,
              minLength: 10,
              placeholder: "Explain why domain parity requires a 90-day waiver.",
            },
          ]}
          onTelemetry={(ev) => setLastTelemetry(ev)}
          onSubmitData={async () => {
            await new Promise((r) => setTimeout(r, 120));
          }}
        />

        {lastTelemetry && (
          <div data-testid="telemetry-log" className="max-w-3xl mx-auto px-4 pb-10 text-xs font-mono text-[var(--text-secondary)]">
            {JSON.stringify(lastTelemetry)}
          </div>
        )}
      </PatternAppShell>
    );
  }

  return (
    <div className="min-h-[100dvh] bg-[var(--surface-base)] text-[var(--text-primary)] pb-20 sm:pb-0">
      <ResponsiveHeader
        logo={<span className="font-bold text-lg tracking-tight">SlopGuard</span>}
        navLinks={navLinks}
        actions={themeAndModeControls}
        onMenuToggle={() => setSheetOpen(true)}
      />

      <main id="main-content">
        <PatternSplitHero
          badge="WCAG 2.2 AA Verified Kit"
          title="Token-Wired UI Primitives Built for Real Verification"
          subhead="Every section, overlay, and enterprise pattern resolves to CSS custom properties, preserves dual-ring keyboard focus, and passes automated Axe + AST gates."
          primaryCta={{ label: "Open Dialog", onClick: () => setModalOpen(true) }}
          secondaryCta={{ label: "Inspect Specs", href: "#specs" }}
          proofCard={{
            title: "Static & Runtime Gates",
            liveStatus: "Verified",
            stats: [
              { value: "100/100", label: "Anti-Slop Score", sublabel: "23 files scanned" },
              { value: "96/96", label: "AAA Palettes", sublabel: "Zero failures" },
              { value: "19", label: "Active AST Rules", sublabel: "TS Compiler API" },
              { value: ">=44px", label: "Touch Targets", sublabel: "Mobile enforced" },
            ],
            techChips: ["CSS Tokens", "TS AST", "Axe-Core", "Playwright"],
            footnote: "Measured on local kit audit suite; host-app CWV metrics verified in Playwright.",
          }}
          trustBadges={[
            { text: "Zero hardcoded hexes in TSX" },
            { text: "Windows Forced Colors support" },
            { text: "prefers-reduced-motion safe" },
          ]}
        />

        <PatternBentoGrid
          title="Architectural Primitives"
          description="Asymmetric bento cards powered by semantic CSS variables."
          items={[
            {
              title: "AST-Backed Static Scanner",
              description: "Walks TypeScript JSX syntax trees and multi-file CSS rules instead of brittle single-line regexes.",
              caption: "19 rules",
              colSpan: 2,
              href: "#specs",
            },
            {
              title: "Zero-PII Forms",
              description: "Built-in honeypot, time-trap, role=alert error summaries, and progressive enhancement.",
              caption: "WCAG 3.3.7",
              colSpan: 1,
              href: "#comparison",
            },
          ]}
        />

        {/* Feedback Component Showcase (ActionButton, SkeletonLoader, SpotlightCard) */}
        <section aria-label="Interactive feedback primitives" className="scroll-mt-20 py-14 border-b border-[var(--border-subtle)] bg-[var(--surface-base)]">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 grid grid-cols-1 md:grid-cols-2 gap-6">
            <SpotlightCard interactive className="p-6">
              <h2 className="text-lg font-bold text-[var(--text-primary)]">ActionButton & Loading Lock</h2>
              <p className="mt-1 text-sm text-[var(--text-secondary)]">
                Maintains accessible label and disables duplicate submissions via aria-disabled and aria-busy.
              </p>
              <div className="mt-4 flex flex-wrap gap-3">
                <ActionButton loading={actionLoading} onClick={handleSimulatedAction}>
                  {actionLoading ? "Saving..." : "Run Safe Mutation"}
                </ActionButton>
                <ActionButton variant="secondary" onClick={() => setSheetOpen(true)}>
                  Open Mobile Sheet
                </ActionButton>
              </div>
            </SpotlightCard>

            <div className="rounded-2xl border border-[var(--border-subtle)] bg-[var(--surface-raised)] p-6">
              <h2 className="text-lg font-bold text-[var(--text-primary)]">Reduced-Motion Skeleton Loader</h2>
              <p className="mt-1 text-sm text-[var(--text-secondary)]">
                Reserves layout geometry cleanly to hold CLS near zero.
              </p>
              <div className="mt-4 space-y-3">
                <SkeletonLoader className="h-5 w-2/3" />
                <SkeletonLoader className="h-4 w-full" />
                <SkeletonLoader className="h-4 w-4/5" />
              </div>
            </div>
          </div>
        </section>

        <PatternComparison
          title="Before vs. After Remediation"
          description="Concrete engineering upgrades applied across tokens, overlays, and datasets."
          leftCard={{
            title: "Legacy Draft",
            subtitle: "Common AI-generated traps",
            items: [
              { title: "Hardcoded classes", desc: "Components ignored tokens.css overrides." },
              { title: "Broken accordion height", desc: "hidden={!isOpen} forced display:none immediately." },
            ],
          }}
          rightCard={{
            title: "SlopGuard v1.6.1",
            subtitle: "Verified production contract",
            items: [
              { title: "Semantic CSS vars", desc: "All surfaces, borders, and focus rings respond to tokens.css." },
              { title: "Inert grid disclosure", desc: "Smooth 0fr/1fr transition with inert collapsed panels." },
            ],
          }}
        />

        <PatternSpecAccordion
          title="Technical Specifications"
          description="Expand rows to inspect smooth grid height transitions and inert collapsed DOM behavior."
          items={[
            {
              id: "spec-tokens",
              question: "How do components consume design tokens?",
              answer: "Every surface, text, border, and action token maps to CSS custom properties defined in styles/tokens.css.",
              tags: ["tokens.css", "light/dark", "forced-colors"],
            },
            {
              id: "spec-accordion",
              question: "Why does collapsed content remain non-focusable?",
              answer: "Collapsed panels set inert, aria-hidden='true', and visibility:hidden so CSS grid transitions run smoothly without exposing hidden tab stops.",
              tags: ["grid-rows", "inert", "WCAG 2.2"],
            },
          ]}
        />

        <PatternStepper
          title="Verification Pipeline"
          description="Four deterministic stages before deployment."
          steps={[
            { step: "01", title: "Token Audit", description: "Verify zero raw hexes in TSX.", duration: "2s", deliverables: ["tokens.css"] },
            { step: "02", title: "AST Scan", description: "Analyze JSX wrappers & styles.", duration: "3s", deliverables: ["audit-v1.json"] },
            { step: "03", title: "Golden Eval", description: "Score 30 prompt briefs >= 95.", duration: "4s", deliverables: ["rubric.json"] },
            { step: "04", title: "Playwright + Axe", description: "Verify live browser DOM & reflow.", duration: "12s", deliverables: ["e2e report"] },
          ]}
        />

        <PatternSocialProof
          title="Dataset & Audit Coverage"
          metrics={[
            { value: "40", label: "Page Sections" },
            { value: "173", label: "Archetypes" },
            { value: "96", label: "Normalized Products" },
            { value: "19", label: "Static Rules" },
          ]}
          footnote="Verified via system_audit.py and audit_engine.py across kit datasets."
          clientLogos={[{ name: "ACME CORP" }, { name: "NORTHSTAR" }, { name: "VERDANT LABS" }]}
        />

        <PatternTieredPricing
          title="Deployment Profiles"
          description="Identical parity cards reserved strictly for tier comparison."
          plans={[
            {
              name: "Starter",
              price: "$0",
              period: "month",
              description: "Local static audits & tokens",
              features: ["19 static AST rules", "CSS token baseline"],
              cta: { label: "Inspect Starter", href: "#specs" },
            },
            {
              name: "Growth",
              price: "$49",
              period: "month",
              popular: true,
              description: "Multi-page prompt & Playwright CI",
              features: ["All 9 page templates", "Axe + Playwright suite", "Enterprise components"],
              cta: { label: "Open Workspace", onClick: () => setViewMode("workspace") },
            },
            {
              name: "Enterprise",
              price: "$199",
              period: "month",
              description: "Custom governance & waivers",
              features: ["90-day baseline waivers", "Dedicated a11y sign-off"],
              cta: { label: "Book Review", onClick: () => setModalOpen(true) },
            },
          ]}
        />

        <PatternCtaBand
          title="Ready to Inspect the Enterprise Workspace?"
          description="Switch to the Workspace view to verify PatternAppShell, PatternChartRow, PatternDataTable, and PatternFormEngine."
          primaryCta={{ label: "Switch to Workspace View", onClick: () => setViewMode("workspace") }}
          secondaryCta={{ label: "Open Modal Dialog", onClick: () => setModalOpen(true) }}
          guaranteeNote="All interactive controls verified at >= 44px touch target footprint."
        />
      </main>

      <ModalDialog isOpen={modalOpen} onClose={() => setModalOpen(false)} title="Accessibility Focus Trap">
        <p className="text-sm text-[var(--text-secondary)]">
          Tab and Shift+Tab wrap inside this dialog; pressing Escape returns focus to the initiating button.
        </p>
        <div className="mt-5 flex justify-end gap-3">
          <ActionButton variant="secondary" onClick={() => setModalOpen(false)}>
            Dismiss
          </ActionButton>
          <ActionButton
            onClick={() => {
              setModalOpen(false);
              setViewMode("workspace");
            }}
          >
            Go to Workspace
          </ActionButton>
        </div>
      </ModalDialog>

      <BottomSheet isOpen={sheetOpen} onClose={() => setSheetOpen(false)} title="Mobile Navigation Sheet">
        <div className="space-y-3">
          {navLinks.map((link) => (
            <a
              key={link.href}
              href={link.href}
              onClick={() => setSheetOpen(false)}
              className="min-h-[44px] flex items-center rounded-lg px-3 text-sm font-medium text-[var(--text-primary)] hover:bg-[var(--surface-subtle)] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--color-focus-ring)]"
            >
              {link.label}
            </a>
          ))}
        </div>
      </BottomSheet>

      <BottomTabBar
        tabs={[
          { id: "home", label: "Home", isActive: true, icon: <span>H</span>, onClick: () => window.scrollTo({ top: 0 }) },
          { id: "specs", label: "Specs", icon: <span>S</span>, onClick: () => document.getElementById("specs")?.scrollIntoView() },
          { id: "ops", label: "Ops", icon: <span>O</span>, onClick: () => setViewMode("workspace") },
        ]}
      />
    </div>
  );
};
