import React from "react";
import type { PatternCtaBandProps } from "./types";
import { CtaButton } from "./CtaButton";

export const PatternCtaBand: React.FC<PatternCtaBandProps> = ({
  id = "cta-band",
  title,
  description,
  primaryCta,
  secondaryCta,
  guaranteeNote,
}) => {
  return (
    <section id={id} className="scroll-mt-20 py-16 sm:py-24 bg-[var(--surface-inverse)] text-[var(--text-inverse)] relative overflow-hidden">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center relative z-10">
        <h2 className="text-3xl sm:text-5xl font-extrabold tracking-tight text-[var(--text-inverse)]">
          {title}
        </h2>
        <p className="mt-4 text-base sm:text-lg text-[var(--text-inverse-secondary)] max-w-2xl mx-auto leading-relaxed">
          {description}
        </p>

        <div className="mt-8 flex flex-wrap items-center justify-center gap-4">
          <CtaButton
            cta={primaryCta}
            className="inline-flex items-center justify-center px-7 py-3.5 rounded-lg text-sm font-semibold bg-[var(--color-action-primary)] hover:bg-[var(--color-action-primary-hover)] text-[var(--color-action-primary-text)] shadow-md transition-all duration-150 active:scale-[0.98] cursor-pointer"
          />

          {secondaryCta && (
            <CtaButton
              cta={secondaryCta}
              className="inline-flex items-center justify-center px-7 py-3.5 rounded-lg text-sm font-semibold border border-[var(--border-strong)] bg-[var(--surface-base)] text-[var(--text-primary)] hover:bg-[var(--surface-subtle)] transition-all duration-150 active:scale-[0.98] cursor-pointer"
            />
          )}
        </div>

        {guaranteeNote && (
          <p className="mt-6 text-xs text-[var(--text-inverse-secondary)]">
            {guaranteeNote}
          </p>
        )}
      </div>
    </section>
  );
};
