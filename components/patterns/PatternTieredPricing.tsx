import React from "react";
import type { PatternTieredPricingProps } from "./types";
import { CtaButton } from "./CtaButton";

export const PatternTieredPricing: React.FC<PatternTieredPricingProps> = ({
  id = "pricing",
  badge = "Investment",
  title,
  description,
  plans,
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

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 items-stretch max-w-6xl mx-auto">
          {plans.map((plan, idx) => (
            <div
              key={idx}
              className={`rounded-2xl p-7 sm:p-8 flex flex-col justify-between transition-all duration-200 ${
                plan.popular
                  ? "border-2 border-[var(--color-action-primary)] bg-[var(--color-action-accent-surface)] shadow-md relative"
                  : "border border-[var(--border-subtle)] bg-[var(--surface-raised)]"
              }`}
            >
              {plan.popular && (
                <div className="absolute -top-3 left-1/2 -translate-x-1/2 bg-[var(--color-action-primary)] text-[var(--color-action-primary-text)] text-xs font-semibold px-3 py-0.5 rounded-full">
                  Most Popular
                </div>
              )}

              <div>
                <h3 className="text-lg font-bold text-[var(--text-primary)]">
                  {plan.name}
                </h3>
                <p className="text-xs text-[var(--text-secondary)] mt-1">
                  {plan.description}
                </p>

                <div className="mt-6 flex items-baseline gap-1">
                  <span className="text-3xl sm:text-4xl font-extrabold text-[var(--text-primary)] font-mono tabular-nums">
                    {plan.price}
                  </span>
                  {plan.period && (
                    <span className="text-xs text-[var(--text-secondary)] font-mono">/{plan.period}</span>
                  )}
                </div>

                <ul className="mt-6 space-y-3 pt-6 border-t border-[var(--border-subtle)]">
                  {plan.features.map((f, fIdx) => (
                    <li key={fIdx} className="flex items-start gap-2.5 text-xs sm:text-sm text-[var(--text-primary)]">
                      <svg className="h-4 w-4 shrink-0 text-[var(--color-action-accent-text)] mt-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                      </svg>
                      <span>{f}</span>
                    </li>
                  ))}
                </ul>
              </div>

              <div className="mt-8 pt-6">
                <CtaButton
                  cta={plan.cta}
                  className={`w-full inline-flex items-center justify-center px-5 py-2.5 rounded-lg text-sm font-semibold transition-all duration-150 active:scale-[0.98] cursor-pointer ${
                    plan.popular
                      ? "bg-[var(--color-action-primary)] hover:bg-[var(--color-action-primary-hover)] text-[var(--color-action-primary-text)] shadow-sm"
                      : "border border-[var(--border-strong)] bg-[var(--surface-base)] text-[var(--text-primary)] hover:bg-[var(--surface-subtle)]"
                  }`}
                />
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};
