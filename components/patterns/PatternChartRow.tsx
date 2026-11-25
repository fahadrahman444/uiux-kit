import React, { useId } from "react";
import type { PatternChartRowProps } from "./types";

export const PatternChartRow: React.FC<PatternChartRowProps> = ({
  id = "telemetry-charts",
  badge = "Verified Telemetry",
  title,
  description,
  sourceNote,
  charts,
}) => {
  const baseId = useId();

  const buildPolyline = (values: number[], width: number, height: number, pad = 6) => {
    if (values.length === 0) return { line: "", area: "" };
    const min = Math.min(...values);
    const max = Math.max(...values);
    const span = max - min || 1;
    const stepX = values.length > 1 ? (width - pad * 2) / (values.length - 1) : 0;

    const coords = values.map((v, i) => {
      const x = pad + i * stepX;
      const y = height - pad - ((v - min) / span) * (height - pad * 2);
      return [Number(x.toFixed(1)), Number(y.toFixed(1))] as const;
    });

    const line = coords.map(([x, y]) => `${x},${y}`).join(" ");
    const firstX = coords[0][0];
    const lastX = coords[coords.length - 1][0];
    const baseY = height - pad;
    const area = `M ${firstX} ${baseY} L ${coords.map(([x, y]) => `${x} ${y}`).join(" L ")} L ${lastX} ${baseY} Z`;
    return { line, area };
  };

  return (
    <section id={id} className="scroll-mt-20 py-14 sm:py-20 border-b border-[var(--border-subtle)] bg-[var(--surface-base)]">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="max-w-2xl mb-10">
          {badge && (
            <div className="text-xs font-mono font-semibold text-[var(--color-action-accent-text)] mb-2">
              {badge}
            </div>
          )}
          <h2 className="text-2xl sm:text-3xl font-bold text-[var(--text-primary)] tracking-tight">
            {title}
          </h2>
          {description && (
            <p className="mt-2 text-sm sm:text-base text-[var(--text-secondary)]">
              {description}
            </p>
          )}
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {charts.map((chart) => {
            const values = chart.points.map((pt) => pt.value);
            const { line, area } = buildPolyline(values, 280, 92);
            const chartTitleId = `${baseId}-${chart.id}-title`;
            const minVal = values.length ? Math.min(...values) : 0;
            const maxVal = values.length ? Math.max(...values) : 0;

            const deltaToneClass =
              chart.deltaTone === "negative"
                ? "text-[var(--color-danger-text)] bg-[var(--color-danger-surface)] border-[var(--color-danger-border)]"
                : chart.deltaTone === "positive"
                ? "text-[var(--color-success-text)] bg-[var(--color-success-surface)] border-[var(--color-success-border)]"
                : "text-[var(--text-secondary)] bg-[var(--surface-subtle)] border-[var(--border-subtle)]";

            return (
              <article
                key={chart.id}
                className="rounded-2xl border border-[var(--border-subtle)] bg-[var(--surface-raised)] p-6 flex flex-col justify-between gap-4"
              >
                <div className="flex items-start justify-between gap-3">
                  <div>
                    <h3 className="text-sm font-semibold text-[var(--text-secondary)]">
                      {chart.title}
                    </h3>
                    <div className="mt-1 text-3xl font-extrabold text-[var(--text-primary)] font-mono tabular-nums">
                      {chart.metricValue}
                    </div>
                  </div>
                  <span className={`px-2.5 py-1 rounded-md border text-xs font-mono font-semibold ${deltaToneClass}`}>
                    {chart.deltaLabel}
                  </span>
                </div>

                <div className="rounded-xl border border-[var(--border-subtle)] bg-[var(--surface-base)] p-3">
                  <svg
                    viewBox="0 0 280 92"
                    role="img"
                    aria-labelledby={chartTitleId}
                    className="w-full h-24 text-[var(--color-action-primary)] overflow-visible"
                  >
                    <title id={chartTitleId}>
                      {`${chart.title} trend (${chart.dateRange}): ${chart.metricValue}, range ${minVal} to ${maxVal}`}
                    </title>
                    {area && (
                      <path d={area} fill="currentColor" opacity="0.14" />
                    )}
                    {line && (
                      <polyline
                        fill="none"
                        stroke="currentColor"
                        strokeWidth="2.5"
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        points={line}
                      />
                    )}
                  </svg>
                  <div className="mt-2 flex items-center justify-between text-xs font-mono text-[var(--text-secondary)]">
                    <span>{chart.points[0]?.label ?? chart.dateRange}</span>
                    <span>{`min ${minVal} · max ${maxVal}`}</span>
                    <span>{chart.points[chart.points.length - 1]?.label ?? ""}</span>
                  </div>
                </div>

                <div className="text-xs font-mono text-[var(--text-secondary)]">
                  Window: {chart.dateRange}
                </div>
              </article>
            );
          })}
        </div>

        <p className="mt-5 text-xs font-mono text-[var(--text-secondary)]">
          Source: {sourceNote}
        </p>
      </div>
    </section>
  );
};
