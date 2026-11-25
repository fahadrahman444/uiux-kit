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
    <section id={id} className="py-16 sm:py-24 border-b border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center max-w-2xl mx-auto mb-12 sm:mb-16">
          {badge && (
            <div className="text-xs font-mono font-semibold text-blue-600 dark:text-blue-400 mb-2">
              {badge}
            </div>
          )}
          <h2 className="text-2xl sm:text-4xl font-bold text-slate-900 dark:text-white tracking-tight">
            {title}
          </h2>
          {description && (
            <p className="mt-3 text-base text-slate-600 dark:text-slate-400">
              {description}
            </p>
          )}
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 items-stretch max-w-5xl mx-auto">
          {/* Left Card: The Old / Typical Way */}
          <div className="rounded-2xl border border-rose-200 dark:border-rose-950/60 bg-rose-50/40 dark:bg-rose-950/20 p-6 sm:p-8">
            <div className="pb-4 border-b border-rose-200/60 dark:border-rose-900/40">
              <span className="text-xs font-mono font-bold text-rose-700 dark:text-rose-400">
                {leftCard.title}
              </span>
              <p className="text-sm text-slate-600 dark:text-slate-400 mt-1">
                {leftCard.subtitle}
              </p>
            </div>

            <ul className="mt-6 space-y-4">
              {leftCard.items.map((item, idx) => (
                <li key={idx} className="flex items-start gap-3 text-sm">
                  <svg className="h-4 w-4 shrink-0 text-rose-600 dark:text-rose-400 mt-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                  <div>
                    <span className="font-semibold text-slate-900 dark:text-slate-100">{item.title}: </span>
                    <span className="text-slate-600 dark:text-slate-400">{item.desc}</span>
                  </div>
                </li>
              ))}
            </ul>
          </div>

          {/* Right Card: The Modern Way */}
          <div className="rounded-2xl border-2 border-emerald-500/80 bg-emerald-50/30 dark:bg-emerald-950/20 p-6 sm:p-8 relative shadow-sm">
            <div className="absolute -top-3 right-6 bg-emerald-700 text-white text-xs font-semibold px-3 py-0.5 rounded-full">
              Recommended
            </div>

            <div className="pb-4 border-b border-emerald-200/60 dark:border-emerald-900/40">
              <span className="text-xs font-mono font-bold text-emerald-700 dark:text-emerald-400">
                {rightCard.title}
              </span>
              <p className="text-sm text-slate-600 dark:text-slate-400 mt-1">
                {rightCard.subtitle}
              </p>
            </div>

            <ul className="mt-6 space-y-4">
              {rightCard.items.map((item, idx) => (
                <li key={idx} className="flex items-start gap-3 text-sm">
                  <svg className="h-4 w-4 shrink-0 text-emerald-600 dark:text-emerald-400 mt-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                  </svg>
                  <div>
                    <span className="font-semibold text-slate-900 dark:text-slate-100">{item.title}: </span>
                    <span className="text-slate-600 dark:text-slate-400">{item.desc}</span>
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
