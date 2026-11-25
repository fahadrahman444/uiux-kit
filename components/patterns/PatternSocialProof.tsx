import React from "react";
import type { PatternSocialProofProps } from "./types";

export const PatternSocialProof: React.FC<PatternSocialProofProps> = ({
  id = "social-proof",
  badge = "Track record",
  title,
  metrics,
  clientLogos,
}) => {
  return (
    <section id={id} className="py-14 sm:py-20 border-b border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-950">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {(badge || title) && (
          <div className="text-center max-w-xl mx-auto mb-10">
            {badge && (
              <div className="text-xs font-mono font-semibold text-blue-600 dark:text-blue-400 mb-2">
                {badge}
              </div>
            )}
            {title && (
              <h2 className="text-xl sm:text-3xl font-bold text-slate-900 dark:text-white">
                {title}
              </h2>
            )}
          </div>
        )}

        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 sm:gap-6">
          {metrics.map((metric, idx) => (
            <div
              key={idx}
              className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 p-5 sm:p-6 text-center shadow-xs"
            >
              <div className="text-3xl sm:text-4xl font-extrabold text-slate-900 dark:text-white font-mono">
                {metric.value}
              </div>
              <div className="text-xs sm:text-sm font-semibold text-slate-600 dark:text-slate-400 mt-1">
                {metric.label}
              </div>
              {metric.growth && (
                <div className="mt-2 text-xs font-mono font-medium text-emerald-700 dark:text-emerald-400">
                  {metric.growth}
                </div>
              )}
            </div>
          ))}
        </div>

        {clientLogos && clientLogos.length > 0 && (
          <div className="mt-12 pt-8 border-t border-slate-200 dark:border-slate-800 flex flex-wrap items-center justify-center gap-8">
            {clientLogos.map((client, idx) => (
              <span key={idx} className="text-sm font-semibold text-slate-600 dark:text-slate-400 tracking-wider font-mono">
                {client.name}
              </span>
            ))}
          </div>
        )}
      </div>
    </section>
  );
};
