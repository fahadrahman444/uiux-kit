import React, { useId, useState } from "react";
import type { PatternSpecAccordionProps } from "./types";

export const PatternSpecAccordion: React.FC<PatternSpecAccordionProps> = ({
  id = "specs",
  badge = "Specifications",
  title,
  description,
  items,
}) => {
  const [openId, setOpenId] = useState<string | null>(items[0]?.id || null);
  const baseId = useId();

  const toggle = (itemId: string) => {
    setOpenId((prev) => (prev === itemId ? null : itemId));
  };

  return (
    <section id={id} className="py-16 sm:py-24 border-b border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-950">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-12">
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

        <div className="space-y-3">
          {items.map((item) => {
            const isOpen = openId === item.id;
            const triggerId = `${baseId}-trigger-${item.id}`;
            const panelId = `${baseId}-panel-${item.id}`;
            return (
              <div
                key={item.id}
                className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 overflow-hidden transition-colors"
              >
                <button
                  id={triggerId}
                  type="button"
                  onClick={() => toggle(item.id)}
                  aria-expanded={isOpen}
                  aria-controls={panelId}
                  className="w-full flex items-center justify-between p-5 sm:p-6 text-left min-h-[44px] cursor-pointer hover:bg-slate-50 dark:hover:bg-slate-800/50 transition-colors focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-blue-600 forced-colors:focus-visible:outline-[Highlight] focus-visible:ring-2 focus-visible:ring-blue-500"
                >
                  <span className="font-semibold text-slate-900 dark:text-white text-base sm:text-lg pr-4">
                    {item.question}
                  </span>
                  <span
                    aria-hidden="true"
                    className={`h-6 w-6 rounded-full flex items-center justify-center shrink-0 border border-slate-300 dark:border-slate-700 text-slate-700 dark:text-slate-300 transition-transform duration-200 motion-reduce:transition-none ${
                      isOpen ? "rotate-180 bg-slate-100 dark:bg-slate-800" : ""
                    }`}
                  >
                    <svg className="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                    </svg>
                  </span>
                </button>

                <div
                  id={panelId}
                  role="region"
                  aria-labelledby={triggerId}
                  hidden={!isOpen}
                  className={`grid transition-[grid-template-rows] duration-200 motion-reduce:transition-none ${
                    isOpen ? "grid-rows-[1fr]" : "grid-rows-[0fr]"
                  }`}
                >
                  <div className="overflow-hidden">
                    <div className="px-5 pb-5 sm:px-6 sm:pb-6 pt-1 text-sm sm:text-base text-slate-600 dark:text-slate-400 leading-relaxed border-t border-slate-100 dark:border-slate-800/80">
                      <p>{item.answer}</p>
                      {item.tags && item.tags.length > 0 && (
                        <div className="flex flex-wrap gap-1.5 mt-4 pt-3 border-t border-slate-100 dark:border-slate-800/60">
                          {item.tags.map((tag, idx) => (
                            <span
                              key={idx}
                              className="text-xs font-mono px-2 py-0.5 rounded bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300"
                            >
                              {tag}
                            </span>
                          ))}
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
};
