import React from "react";
import type { PatternBentoGridProps } from "./types";

export const PatternBentoGrid: React.FC<PatternBentoGridProps> = ({
  id = "features",
  badge = "Capabilities",
  title,
  description,
  items,
  columns = 3,
}) => {
  const colClass =
    columns === 4
      ? "grid-cols-1 sm:grid-cols-2 lg:grid-cols-4"
      : columns === 2
      ? "grid-cols-1 md:grid-cols-2"
      : "grid-cols-1 md:grid-cols-2 lg:grid-cols-3";

  return (
    <section id={id} className="py-16 sm:py-24 border-b border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-950">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="max-w-2xl mb-12">
          {badge && (
            <div className="text-xs font-mono font-medium text-blue-600 dark:text-blue-400 mb-2">
              {badge}
            </div>
          )}
          <h2 className="text-2xl sm:text-4xl font-bold text-slate-900 dark:text-white tracking-tight">
            {title}
          </h2>
          {description && (
            <p className="mt-3 text-base sm:text-lg text-slate-600 dark:text-slate-400">
              {description}
            </p>
          )}
        </div>

        <div className={`grid ${colClass} gap-6`}>
          {items.map((item, idx) => {
            const Icon = item.icon;
            const CardWrapper = item.href ? "a" : "div";

            return (
              <CardWrapper
                key={idx}
                href={item.href}
                className={`group rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 p-6 sm:p-7 flex flex-col justify-between transition-all duration-200 ${
                  item.href
                    ? "hover:border-blue-500 hover:shadow-md hover:-translate-y-0.5 active:translate-y-0 cursor-pointer"
                    : "hover:border-slate-300 dark:hover:border-slate-700"
                }`}
              >
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <div className="h-10 w-10 rounded-lg bg-blue-50 dark:bg-blue-950/60 text-blue-600 dark:text-blue-400 flex items-center justify-center font-bold text-lg">
                      {Icon ? <Icon className="h-5 w-5" /> : idx + 1}
                    </div>
                    {item.caption && (
                      <span className="text-[11px] font-mono font-medium text-slate-400 dark:text-slate-500">
                        {item.caption}
                      </span>
                    )}
                  </div>

                  <div>
                    <h3 className="text-base sm:text-lg font-semibold text-slate-900 dark:text-white group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors">
                      {item.title}
                    </h3>
                    <p className="mt-1.5 text-sm text-slate-600 dark:text-slate-400 leading-relaxed">
                      {item.description}
                    </p>
                  </div>
                </div>

                {item.href && (
                  <div className="mt-4 pt-3 border-t border-slate-100 dark:border-slate-800/80 flex items-center gap-1 text-xs font-semibold text-blue-600 dark:text-blue-400">
                    <span>Learn more</span>
                    <span>→</span>
                  </div>
                )}
              </CardWrapper>
            );
          })}
        </div>
      </div>
    </section>
  );
};
