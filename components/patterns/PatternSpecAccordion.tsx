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
    <section id={id} className="scroll-mt-20 py-16 sm:py-24 border-b border-[var(--border-subtle)] bg-[var(--surface-raised)]">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-12">
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

        <div className="space-y-3">
          {items.map((item) => {
            const isOpen = openId === item.id;
            const triggerId = `${baseId}-trigger-${item.id}`;
            const panelId = `${baseId}-panel-${item.id}`;
            return (
              <div
                key={item.id}
                className="rounded-xl border border-[var(--border-subtle)] bg-[var(--surface-base)] overflow-hidden transition-colors"
              >
                <button
                  id={triggerId}
                  type="button"
                  onClick={() => toggle(item.id)}
                  aria-expanded={isOpen}
                  aria-controls={panelId}
                  className="w-full flex items-center justify-between p-5 sm:p-6 text-left min-h-[44px] cursor-pointer hover:bg-[var(--surface-subtle)] transition-colors focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--color-focus-ring)] forced-colors:focus-visible:outline-[Highlight]"
                >
                  <span className="font-semibold text-[var(--text-primary)] text-base sm:text-lg pr-4">
                    {item.question}
                  </span>
                  <span
                    aria-hidden="true"
                    className={`h-6 w-6 rounded-full flex items-center justify-center shrink-0 border border-[var(--border-strong)] text-[var(--text-secondary)] transition-transform duration-200 motion-reduce:transition-none ${
                      isOpen ? "rotate-180 bg-[var(--surface-subtle)]" : ""
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
                  aria-hidden={!isOpen}
                  inert={!isOpen ? true : undefined}
                  className={`grid transition-[grid-template-rows,visibility] duration-200 motion-reduce:transition-none ${
                    isOpen ? "grid-rows-[1fr] visible" : "grid-rows-[0fr] invisible"
                  }`}
                >
                  <div className="overflow-hidden">
                    <div className="px-5 pb-5 sm:px-6 sm:pb-6 pt-1 text-sm sm:text-base text-[var(--text-secondary)] leading-relaxed border-t border-[var(--border-subtle)]">
                      <p>{item.answer}</p>
                      {item.tags && item.tags.length > 0 && (
                        <div className="flex flex-wrap gap-1.5 mt-4 pt-3 border-t border-[var(--border-subtle)]">
                          {item.tags.map((tag, idx) => (
                            <span
                              key={idx}
                              className="text-xs font-mono px-2 py-0.5 rounded bg-[var(--surface-subtle)] text-[var(--text-primary)]"
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
