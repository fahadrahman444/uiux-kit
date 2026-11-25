import React from "react";
import type { PatternComparisonProps } from "./types";

export const PatternComparison: React.FC<PatternComparisonProps> = ({
  id = "comparison",
  badge = "Methodology",
  title,
  description,
  leftCard,
  rightCard,
}) => {
  return (
    <section id={id} className="scroll-mt-20 py-16 sm:py-24 border-b border-[var(--border-subtle)] bg-[var(--surface-base)]">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center max-w-2xl mx-auto mb-12 sm:mb-16">
          {badge && (
            <div className="text-xs font-mono font-semibold text-[var(--color-action-accent-text)] mb-2">
              {badge}
            </div>
          )}
          <h2 className="text-2xl sm:text-4xl font-bold text-[var(--text-primary)] tracking-tight">
            {title}
          </h2>
          {description && (
            <p className="mt-3 text-base text-[var(--text-secondary)]">
              {description}
            </p>
          )}
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 items-stretch max-w-5xl mx-auto">
          {/* Left Card: The Old / Typical Way */}
          <div className="rounded-2xl border border-[var(--color-danger-border)] bg-[var(--color-danger-surface)] p-6 sm:p-8">
            <div className="pb-4 border-b border-[var(--color-danger-border)]">
              <span className="text-xs font-mono font-bold text-[var(--color-danger-text)]">
                {leftCard.title}
              </span>
              <p className="text-sm text-[var(--text-secondary)] mt-1">
                {leftCard.subtitle}
              </p>
            </div>

            <ul className="mt-6 space-y-4">
              {leftCard.items.map((item, idx) => (
                <li key={idx} className="flex items-start gap-3 text-sm">
                  <svg className="h-4 w-4 shrink-0 text-[var(--color-danger-text)] mt-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                  <div>
                    <span className="font-semibold text-[var(--text-primary)]">{item.title}: </span>
                    <span className="text-[var(--text-secondary)]">{item.desc}</span>
                  </div>
                </li>
              ))}
            </ul>
          </div>

          {/* Right Card: The Modern Way */}
          <div className="rounded-2xl border-2 border-[var(--color-success-border)] bg-[var(--color-success-surface)] p-6 sm:p-8 relative shadow-sm">
            <div className="absolute -top-3 right-6 bg-[var(--color-success)] text-[var(--color-action-primary-text)] text-xs font-semibold px-3 py-0.5 rounded-full">
              Recommended
            </div>

            <div className="pb-4 border-b border-[var(--color-success-border)]">
              <span className="text-xs font-mono font-bold text-[var(--color-success-text)]">
                {rightCard.title}
              </span>
              <p className="text-sm text-[var(--text-secondary)] mt-1">
                {rightCard.subtitle}
              </p>
            </div>

            <ul className="mt-6 space-y-4">
              {rightCard.items.map((item, idx) => (
                <li key={idx} className="flex items-start gap-3 text-sm">
                  <svg className="h-4 w-4 shrink-0 text-[var(--color-success-text)] mt-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                  </svg>
                  <div>
                    <span className="font-semibold text-[var(--text-primary)]">{item.title}: </span>
                    <span className="text-[var(--text-secondary)]">{item.desc}</span>
                  </div>
                </li>
              ))}
            </ul>
          </div>
        </div>
      </div>
    </section>
  );
};
