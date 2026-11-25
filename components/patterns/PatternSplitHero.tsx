import React from "react";
import type { PatternSplitHeroProps } from "./types";
import { CtaButton } from "./CtaButton";

export const PatternSplitHero: React.FC<PatternSplitHeroProps> = ({
  id = "hero",
  badge,
  title,
  subhead,
  primaryCta,
  secondaryCta,
  proofCard,
  trustBadges,
  mediaSlot,
}) => {
  return (
    <section id={id} className="relative pt-8 pb-16 sm:pt-14 sm:pb-24 lg:pt-20 lg:pb-28 border-b border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-950">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-10 lg:gap-14 items-center">
          {/* Left Column (7 cols): Copy + CTAs */}
          <div className="lg:col-span-7 space-y-6">
            {badge && (
              <div className="inline-flex items-center gap-2 rounded-full border border-blue-500/30 bg-blue-50 dark:bg-blue-950/50 px-3 py-1 text-xs font-semibold tracking-wide text-blue-700 dark:text-blue-300">
                <span className="h-2 w-2 rounded-full bg-blue-600" aria-hidden="true" />
                <span>{badge}</span>
              </div>
            )}

            <h1 className="text-3xl sm:text-5xl lg:text-6xl font-extrabold text-slate-900 dark:text-white tracking-tight leading-[1.15]">
              {title}
            </h1>

            <p className="text-base sm:text-lg text-slate-600 dark:text-slate-300 leading-relaxed max-w-2xl">
              {subhead}
            </p>

            <div className="flex flex-wrap items-center gap-3 pt-2">
              <CtaButton
                cta={primaryCta}
                className="inline-flex items-center justify-center min-h-[44px] px-6 py-3 rounded-lg text-sm font-semibold bg-blue-600 hover:bg-blue-700 text-white shadow-sm hover:shadow transition-all duration-150 active:scale-[0.98] cursor-pointer"
              />

              {secondaryCta && (
                <CtaButton
                  cta={secondaryCta}
                  className="inline-flex items-center justify-center min-h-[44px] px-6 py-3 rounded-lg text-sm font-semibold border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-900 text-slate-800 dark:text-slate-200 hover:bg-slate-50 dark:hover:bg-slate-800 transition-all duration-150 active:scale-[0.98] cursor-pointer"
                />
              )}
            </div>

            {trustBadges && trustBadges.length > 0 && (
              <div className="pt-6 border-t border-slate-100 dark:border-slate-800/80 flex flex-wrap items-center gap-6">
                {trustBadges.map((item, idx) => (
                  <div key={idx} className="flex items-center gap-2 text-xs sm:text-sm font-medium text-slate-600 dark:text-slate-300">
                    <span className="h-1.5 w-1.5 rounded-full bg-emerald-600 dark:bg-emerald-400" aria-hidden="true" />
                    <span>{item.text}</span>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Right Column (5 cols): Media Slot or Proof Card */}
          <div className="lg:col-span-5 min-h-[360px]">
            {mediaSlot ? (
              mediaSlot
            ) : (
              <div className="rounded-2xl border border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-900/60 p-6 sm:p-8 shadow-sm h-full">
                <div className="flex items-center justify-between pb-4 border-b border-slate-200 dark:border-slate-800">
                  <span className="text-xs font-mono font-semibold text-slate-600 dark:text-slate-300">
                    {proofCard.title || "Live Performance"}
                  </span>
                  {proofCard.liveStatus && (
                    <span className="inline-flex items-center gap-1.5 text-xs font-medium text-emerald-700 dark:text-emerald-400">
                      <span className="h-2 w-2 rounded-full bg-emerald-600 dark:bg-emerald-400" aria-hidden="true" />
                      {proofCard.liveStatus}
                    </span>
                  )}
                </div>

                <div className="grid grid-cols-2 gap-4 py-6">
                  {proofCard.stats.map((stat, idx) => (
                    <div key={idx} className="rounded-xl border border-slate-200/80 dark:border-slate-800 bg-white dark:bg-slate-950 p-4">
                      <div className="text-2xl sm:text-3xl font-extrabold text-slate-900 dark:text-white font-mono">
                        {stat.value}
                      </div>
                      <div className="text-xs font-semibold text-slate-700 dark:text-slate-300 mt-1">
                        {stat.label}
                      </div>
                      {stat.sublabel && (
                        <div className="text-xs text-slate-600 dark:text-slate-400 mt-0.5">
                          {stat.sublabel}
                        </div>
                      )}
                    </div>
                  ))}
                </div>

                {proofCard.techChips && proofCard.techChips.length > 0 && (
                  <div className="pt-4 border-t border-slate-200 dark:border-slate-800">
                    <div className="flex flex-wrap gap-1.5">
                      {proofCard.techChips.map((chip, idx) => (
                        <span key={idx} className="px-2.5 py-1 text-xs font-medium rounded-md bg-slate-200/60 dark:bg-slate-800 text-slate-700 dark:text-slate-300">
                          {chip}
                        </span>
                      ))}
                    </div>
                  </div>
                )}

                {proofCard.footnote && (
                  <p className="mt-4 text-xs text-slate-600 dark:text-slate-400">
                    {proofCard.footnote}
                  </p>
                )}
              </div>
            )}
          </div>
        </div>
      </div>
    </section>
  );
};
