import React from "react";
import type { PatternStepperProps } from "./types";

export const PatternStepper: React.FC<PatternStepperProps> = ({
  id = "roadmap",
  badge = "Process",
  title,
  description,
  steps,
}) => {
  return (
    <section id={id} className="scroll-mt-20 py-16 sm:py-24 border-b border-[var(--border-subtle)] bg-[var(--surface-base)]">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="max-w-2xl mb-12">
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

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {steps.map((step, idx) => (
            <div
              key={idx}
              className="relative rounded-2xl border border-[var(--border-subtle)] bg-[var(--surface-raised)] p-6 flex flex-col justify-between"
            >
              <div>
                <div className="flex items-center justify-between pb-3 border-b border-[var(--border-subtle)]">
                  <span className="text-xs font-mono font-bold text-[var(--color-action-accent-text)]">
                    {step.step}
                  </span>
                  {step.duration && (
                    <span className="text-xs font-mono text-[var(--text-secondary)]">
                      {step.duration}
                    </span>
                  )}
                </div>

                <h3 className="mt-4 text-base font-bold text-[var(--text-primary)]">
                  {step.title}
                </h3>
                <p className="mt-2 text-xs sm:text-sm text-[var(--text-secondary)] leading-relaxed">
                  {step.description}
                </p>
              </div>

              {step.deliverables && step.deliverables.length > 0 && (
                <div className="mt-6 pt-4 border-t border-[var(--border-subtle)]">
                  <span className="text-xs font-semibold text-[var(--text-secondary)]">Deliverables</span>
                  <div className="flex flex-wrap gap-1 mt-2">
                    {step.deliverables.map((d, dIdx) => (
                      <span key={dIdx} className="text-xs px-2 py-0.5 rounded bg-[var(--surface-subtle)] text-[var(--text-primary)]">
                        {d}
                      </span>
                    ))}
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};
