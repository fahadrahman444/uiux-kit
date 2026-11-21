import React, { useState } from "react";
import type { PatternSpecAccordionProps } from "./types";

export const PatternSpecAccordion: React.FC<PatternSpecAccordionProps> = ({
  id = "specs",
  badge = "SPECIFICATIONS",
  title,
  description,
  items,
}) => {
  const [openId, setOpenId] = useState<string | null>(items[0]?.id || null);

  const toggle = (id: string) => {
    setOpenId((prev) => (prev === id ? null : id));
  };

  return (
    <section id={id} className="py-16 sm:py-24 border-b border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-950">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-12">
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

        <div className="space-y-3">
          {items.map((item) => {
            const isOpen = openId === item.id;
            return (
              <div
                key={item.id}
                className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 overflow-hidden transition-colors"
              >
                <button
                  type="button"
                  onClick={() => toggle(item.id)}
                  aria-expanded={isOpen}
                  className="w-full flex items-center justify-between p-5 sm:p-6 text-left min-h-[44px] cursor-pointer hover:bg-slate-50 dark:hover:bg-slate-800/50 transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500"
                >
                  <span className="font-semibold text-slate-900 dark:text-white text-base sm:text-lg pr-4">
                    {item.question}
                  </span>
                  <span
                    className={`h-6 w-6 rounded-full flex items-center justify-center shrink-0 border border-slate-300 dark:border-slate-700 text-xs font-bold transition-transform duration-200 ${
                      isOpen ? "rotate-180 bg-slate-100 dark:bg-slate-800" : ""
                    }`}
                  >
                    ▼
                  </span>
                </button>

                {isOpen && (
                  <div className="px-5 pb-5 sm:px-6 sm:pb-6 pt-1 text-sm sm:text-base text-slate-600 dark:text-slate-400 leading-relaxed border-t border-slate-100 dark:border-slate-800/80">
                    <p>{item.answer}</p>
                    {item.tags && item.tags.length > 0 && (
                      <div className="flex flex-wrap gap-1.5 mt-4 pt-3 border-t border-slate-100 dark:border-slate-800/60">
                        {item.tags.map((tag, idx) => (
                          <span
                            key={idx}
                            className="text-xs font-mono px-2 py-0.5 rounded bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300"
                          >
                            {tag}
                          </span>
                        ))}
                      </div>
                    )}
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
};
