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
    <section id={id} className="py-16 sm:py-24 bg-slate-900 text-white relative overflow-hidden">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center relative z-10">
        <h2 className="text-3xl sm:text-5xl font-extrabold tracking-tight">
          {title}
        </h2>
        <p className="mt-4 text-base sm:text-lg text-slate-300 max-w-2xl mx-auto leading-relaxed">
          {description}
        </p>

        <div className="mt-8 flex flex-wrap items-center justify-center gap-4">
          <CtaButton
            cta={primaryCta}
            className="inline-flex items-center justify-center min-h-[44px] px-7 py-3.5 rounded-lg text-sm font-semibold bg-blue-600 hover:bg-blue-500 text-white shadow-md transition-all duration-150 active:scale-[0.98] cursor-pointer"
          />

          {secondaryCta && (
            <CtaButton
              cta={secondaryCta}
              className="inline-flex items-center justify-center min-h-[44px] px-7 py-3.5 rounded-lg text-sm font-semibold border border-slate-700 bg-slate-800/80 hover:bg-slate-800 text-slate-200 transition-all duration-150 active:scale-[0.98] cursor-pointer"
            />
          )}
        </div>

        {guaranteeNote && (
          <p className="mt-6 text-xs text-slate-300">
            {guaranteeNote}
          </p>
        )}
      </div>
    </section>
  );
};
