import React from "react";
import type { PatternSocialProofProps } from "./types";

export const PatternSocialProof: React.FC<PatternSocialProofProps> = ({
  id = "social-proof",
  badge = "Track record",
  title,
  metrics,
  footnote,
  clientLogos,
}) => {
  return (
    <section id={id} className="scroll-mt-20 py-14 sm:py-20 border-b border-[var(--border-subtle)] bg-[var(--surface-raised)]">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {(badge || title) && (
          <div className="text-center max-w-xl mx-auto mb-10">
            {badge && (
              <div className="text-xs font-mono font-semibold text-[var(--color-action-accent-text)] mb-2">
                {badge}
              </div>
            )}
            {title && (
              <h2 className="text-xl sm:text-3xl font-bold text-[var(--text-primary)]">
                {title}
              </h2>
            )}
          </div>
        )}

        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 sm:gap-6">
          {metrics.map((metric, idx) => (
            <div
              key={idx}
              className="rounded-xl border border-[var(--border-subtle)] bg-[var(--surface-base)] p-5 sm:p-6 text-center shadow-xs"
            >
              <div className="text-3xl sm:text-4xl font-extrabold text-[var(--text-primary)] font-mono tabular-nums">
                {metric.value}
              </div>
              <div className="text-xs sm:text-sm font-semibold text-[var(--text-secondary)] mt-1">
                {metric.label}
              </div>
              {metric.growth && (
                <div className="mt-2 text-xs font-mono font-medium text-[var(--color-success-text)]">
                  {metric.growth}
                </div>
              )}
            </div>
          ))}
        </div>

        {footnote && (
          <p className="mt-4 text-center text-xs text-[var(--text-secondary)]">
            {footnote}
          </p>
        )}

        {clientLogos && clientLogos.length > 0 && (
          <div className="mt-12 pt-8 border-t border-[var(--border-subtle)] flex flex-wrap items-center justify-center gap-8">
            {clientLogos.map((client, idx) => (
              <span key={idx} className="text-sm font-semibold text-[var(--text-secondary)] tracking-wider font-mono">
                {client.name}
              </span>
            ))}
          </div>
        )}
      </div>
    </section>
  );
};
