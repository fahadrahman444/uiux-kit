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

  const spanClass = (colSpan?: 1 | 2 | 3) => {
    if (colSpan === 3) return "md:col-span-2 lg:col-span-3";
    if (colSpan === 2) return "md:col-span-2";
    return "";
  };

  return (
    <section id={id} className="scroll-mt-20 py-16 sm:py-24 border-b border-[var(--border-subtle)] bg-[var(--surface-raised)]">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="max-w-2xl mb-12">
          {badge && (
            <div className="text-xs font-mono font-medium text-[var(--color-action-accent-text)] mb-2">
              {badge}
            </div>
          )}
          <h2 className="text-2xl sm:text-4xl font-bold text-[var(--text-primary)] tracking-tight">
            {title}
          </h2>
          {description && (
            <p className="mt-3 text-base sm:text-lg text-[var(--text-secondary)]">
              {description}
            </p>
          )}
        </div>

        <div className={`grid ${colClass} gap-6`}>
          {items.map((item, idx) => {
            const Icon = item.icon;
            const span = spanClass(item.colSpan);
            const sharedClasses = `group rounded-2xl border border-[var(--border-subtle)] bg-[var(--surface-base)] p-6 sm:p-7 flex flex-col justify-between transition-all duration-200 ${span}`;
            const content = (
              <>
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <div className="h-10 w-10 rounded-lg bg-[var(--color-action-accent-surface)] text-[var(--color-action-accent-text)] flex items-center justify-center font-bold text-lg">
                      {Icon ? <Icon className="h-5 w-5" /> : idx + 1}
                    </div>
                    {item.caption && (
                      <span className="text-xs font-mono font-medium text-[var(--text-secondary)]">
                        {item.caption}
                      </span>
                    )}
                  </div>

                  <div>
                    <h3 className="text-base sm:text-lg font-semibold text-[var(--text-primary)] group-hover:text-[var(--color-action-accent-text)] transition-colors">
                      {item.title}
                    </h3>
                    <p className="mt-1.5 text-sm text-[var(--text-secondary)] leading-relaxed">
                      {item.description}
                    </p>
                  </div>
                </div>

                {item.href && (
                  <div className="mt-4 pt-3 border-t border-[var(--border-subtle)] flex items-center gap-1 text-xs font-semibold text-[var(--color-action-accent-text)]">
                    <span>Learn more</span>
                    <span aria-hidden="true">→</span>
                  </div>
                )}
              </>
            );

            return item.href ? (
              <a
                key={idx}
                href={item.href}
                className={`${sharedClasses} min-h-[44px] hover:border-[var(--color-action-primary)] hover:shadow-md hover:-translate-y-0.5 active:translate-y-0 cursor-pointer focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--color-focus-ring)] forced-colors:focus-visible:outline-[Highlight]`}
              >
                {content}
              </a>
            ) : (
              <div key={idx} className={`${sharedClasses} hover:border-[var(--border-strong)]`}>
                {content}
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
};
