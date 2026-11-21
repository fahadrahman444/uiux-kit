import React from "react";
import type { PatternTieredPricingProps } from "./types";

export const PatternTieredPricing: React.FC<PatternTieredPricingProps> = ({
  id = "pricing",
  badge = "INVESTMENT",
  title,
  description,
  plans,
}) => {
  return (
    <section id={id} className="py-16 sm:py-24 border-b border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center max-w-2xl mx-auto mb-12 sm:mb-16">
          {badge && (
            <div className="text-xs font-mono font-semibold uppercase tracking-wider text-blue-600 dark:text-blue-400 mb-2">
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

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 items-stretch max-w-6xl mx-auto">
          {plans.map((plan, idx) => (
            <div
              key={idx}
              className={`rounded-2xl p-7 sm:p-8 flex flex-col justify-between transition-all duration-200 ${
                plan.popular
                  ? "border-2 border-blue-600 bg-blue-50/20 dark:bg-blue-950/20 shadow-md relative"
                  : "border border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-950"
              }`}
            >
              {plan.popular && (
                <div className="absolute -top-3 left-1/2 -translate-x-1/2 bg-blue-600 text-white text-[11px] font-bold px-3 py-0.5 rounded-full uppercase tracking-wider">
                  Most Popular
                </div>
              )}

              <div>
                <h3 className="text-lg font-bold text-slate-900 dark:text-white">
                  {plan.name}
                </h3>
                <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">
                  {plan.description}
                </p>

                <div className="mt-6 flex items-baseline gap-1">
                  <span className="text-3xl sm:text-4xl font-extrabold text-slate-900 dark:text-white font-mono">
                    {plan.price}
                  </span>
                  {plan.period && (
                    <span className="text-xs text-slate-500 font-mono">/{plan.period}</span>
                  )}
                </div>

                <ul className="mt-6 space-y-3 pt-6 border-t border-slate-200 dark:border-slate-800">
                  {plan.features.map((f, fIdx) => (
                    <li key={fIdx} className="flex items-start gap-2.5 text-xs sm:text-sm text-slate-700 dark:text-slate-300">
                      <span className="text-blue-600 dark:text-blue-400 font-bold">✓</span>
                      <span>{f}</span>
                    </li>
                  ))}
                </ul>
              </div>

              <div className="mt-8 pt-6">
                <a
                  href={plan.cta.href || "#"}
                  onClick={plan.cta.onClick}
                  className={`w-full inline-flex items-center justify-center min-h-[44px] px-5 py-2.5 rounded-lg text-sm font-semibold transition-all duration-150 active:scale-[0.98] cursor-pointer ${
                    plan.popular
                      ? "bg-blue-600 hover:bg-blue-700 text-white shadow-sm"
                      : "border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-900 text-slate-800 dark:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-800"
                  }`}
                >
                  {plan.cta.label}
                </a>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};
