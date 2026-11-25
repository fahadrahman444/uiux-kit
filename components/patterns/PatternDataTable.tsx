import React, { useId, useMemo, useState } from "react";
import type { DataTableRow, PatternDataTableProps } from "./types";

export const PatternDataTable: React.FC<PatternDataTableProps> = ({
  id = "data-table",
  badge = "Operations",
  title,
  description,
  caption,
  columns,
  rows,
  searchable = true,
  searchPlaceholder = "Filter records...",
  emptyMessage = "No matching records found.",
  rowActionLabel = "Inspect",
  onRowAction,
}) => {
  const [query, setQuery] = useState("");
  const [sortKey, setSortKey] = useState<string | null>(null);
  const [sortDir, setSortDir] = useState<"ascending" | "descending">("ascending");
  const searchId = useId();
  const tableRegionLabelId = useId();

  const filteredRows = useMemo(() => {
    const q = query.trim().toLowerCase();
    const matched = q
      ? rows.filter((row) =>
          columns.some((col) => String(row.cells[col.key] ?? "").toLowerCase().includes(q))
        )
      : rows;

    if (!sortKey) return matched;
    const colMeta = columns.find((c) => c.key === sortKey);
    return [...matched].sort((a, b) => {
      const av = a.cells[sortKey] ?? "";
      const bv = b.cells[sortKey] ?? "";
      let cmp = 0;
      if (colMeta?.numeric || (typeof av === "number" && typeof bv === "number")) {
        cmp = Number(av) - Number(bv);
      } else {
        cmp = String(av).localeCompare(String(bv), undefined, { numeric: true, sensitivity: "base" });
      }
      return sortDir === "ascending" ? cmp : -cmp;
    });
  }, [rows, columns, query, sortKey, sortDir]);

  const toggleSort = (key: string) => {
    if (sortKey === key) {
      setSortDir((prev) => (prev === "ascending" ? "descending" : "ascending"));
    } else {
      setSortKey(key);
      setSortDir("ascending");
    }
  };

  const statusPill = (status?: DataTableRow["status"]) => {
    if (!status) return null;
    const styles = {
      healthy: "bg-[var(--color-success-surface)] text-[var(--color-success-text)] border-[var(--color-success-border)]",
      warning: "bg-[var(--color-warning-surface)] text-[var(--color-warning-text)] border-[var(--color-warning-border)]",
      critical: "bg-[var(--color-danger-surface)] text-[var(--color-danger-text)] border-[var(--color-danger-border)]",
    }[status];
    return (
      <span className={`inline-flex items-center px-2 py-0.5 rounded-md border text-xs font-mono font-medium ${styles}`}>
        {status}
      </span>
    );
  };

  return (
    <section id={id} className="scroll-mt-20 py-14 sm:py-20 border-b border-[var(--border-subtle)] bg-[var(--surface-base)]">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex flex-col md:flex-row md:items-end justify-between gap-6 mb-8">
          <div className="max-w-2xl">
            {badge && (
              <div className="text-xs font-mono font-semibold text-[var(--color-action-accent-text)] mb-2">
                {badge}
              </div>
            )}
            <h2 id={tableRegionLabelId} className="text-2xl sm:text-3xl font-bold text-[var(--text-primary)] tracking-tight">
              {title}
            </h2>
            {description && (
              <p className="mt-2 text-sm sm:text-base text-[var(--text-secondary)]">
                {description}
              </p>
            )}
          </div>

          {searchable && (
            <div className="w-full md:w-80">
              <label htmlFor={searchId} className="block text-xs font-medium text-[var(--text-secondary)] mb-1.5">
                Search table
              </label>
              <div className="flex items-center gap-2">
                <input
                  id={searchId}
                  type="search"
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                  placeholder={searchPlaceholder}
                  className="w-full min-h-[44px] rounded-lg border border-[var(--border-strong)] bg-[var(--surface-base)] px-3.5 py-2 text-sm text-[var(--text-primary)] placeholder:text-[var(--text-secondary)] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--color-focus-ring)] forced-colors:focus-visible:outline-[Highlight]"
                />
                {query && (
                  <button
                    type="button"
                    onClick={() => setQuery("")}
                    aria-label="Clear table filter"
                    className="min-h-[44px] min-w-[44px] shrink-0 rounded-lg border border-[var(--border-strong)] bg-[var(--surface-subtle)] px-3 text-xs font-semibold text-[var(--text-primary)] hover:bg-[var(--border-subtle)] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--color-focus-ring)] forced-colors:focus-visible:outline-[Highlight] cursor-pointer"
                  >
                    Clear
                  </button>
                )}
              </div>
            </div>
          )}
        </div>

        <div
          tabIndex={0}
          role="region"
          aria-labelledby={tableRegionLabelId}
          className="overflow-x-auto rounded-2xl border border-[var(--border-subtle)] bg-[var(--surface-base)] shadow-xs focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--color-focus-ring)] forced-colors:focus-visible:outline-[Highlight]"
        >
          <table className="w-full border-collapse text-left text-sm">
            {caption && <caption className="sr-only">{caption}</caption>}
            <thead className="sticky top-0 z-10 bg-[var(--surface-raised)] border-b border-[var(--border-subtle)]">
              <tr>
                {columns.map((col) => {
                  const isSorted = sortKey === col.key;
                  const ariaSort = col.sortable
                    ? isSorted
                      ? sortDir
                      : "none"
                    : undefined;
                  return (
                    <th
                      key={col.key}
                      scope="col"
                      aria-sort={ariaSort}
                      className={`px-4 py-3 font-semibold text-[var(--text-primary)] whitespace-nowrap ${
                        col.numeric ? "text-right" : "text-left"
                      }`}
                    >
                      {col.sortable ? (
                        <button
                          type="button"
                          onClick={() => toggleSort(col.key)}
                          className="min-h-[44px] inline-flex items-center gap-1.5 rounded-md px-2 -mx-2 font-semibold text-[var(--text-primary)] hover:bg-[var(--surface-subtle)] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--color-focus-ring)] forced-colors:focus-visible:outline-[Highlight] cursor-pointer"
                        >
                          <span>{col.label}</span>
                          <span aria-hidden="true" className="text-xs font-mono text-[var(--color-action-accent-text)]">
                            {isSorted ? (sortDir === "ascending" ? "↑" : "↓") : "↕"}
                          </span>
                        </button>
                      ) : (
                        <span className="inline-flex items-center min-h-[44px]">{col.label}</span>
                      )}
                    </th>
                  );
                })}
                {onRowAction && (
                  <th scope="col" className="px-4 py-3 text-right font-semibold text-[var(--text-primary)]">
                    <span className="inline-flex items-center min-h-[44px]">Action</span>
                  </th>
                )}
              </tr>
            </thead>
            <tbody className="divide-y divide-[var(--border-subtle)]">
              {filteredRows.length === 0 ? (
                <tr>
                  <td colSpan={columns.length + (onRowAction ? 1 : 0)} className="px-6 py-12 text-center">
                    <p className="text-sm font-medium text-[var(--text-secondary)]">{emptyMessage}</p>
                    {query && (
                      <button
                        type="button"
                        onClick={() => setQuery("")}
                        className="mt-4 min-h-[44px] inline-flex items-center justify-center rounded-lg border border-[var(--border-strong)] bg-[var(--surface-subtle)] px-4 py-2 text-xs font-semibold text-[var(--text-primary)] hover:bg-[var(--border-subtle)] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--color-focus-ring)] forced-colors:focus-visible:outline-[Highlight] cursor-pointer"
                      >
                        Reset filter
                      </button>
                    )}
                  </td>
                </tr>
              ) : (
                filteredRows.map((row) => (
                  <tr
                    key={row.id}
                    className="hover:bg-[var(--surface-raised)] transition-colors"
                  >
                    {columns.map((col, cIdx) => (
                      <td
                        key={col.key}
                        className={`px-4 py-3.5 text-[var(--text-primary)] ${
                          col.numeric ? "text-right font-mono tabular-nums" : ""
                        }`}
                      >
                        <div className={`flex items-center gap-2 ${col.numeric ? "justify-end" : ""}`}>
                          <span>{row.cells[col.key]}</span>
                          {cIdx === 0 && row.status && statusPill(row.status)}
                        </div>
                      </td>
                    ))}
                    {onRowAction && (
                      <td className="px-4 py-2.5 text-right">
                        <button
                          type="button"
                          onClick={() => onRowAction(row)}
                          aria-label={`${rowActionLabel} ${row.cells[columns[0]?.key] ?? row.id}`}
                          className="min-h-[44px] inline-flex items-center justify-center rounded-lg border border-[var(--border-strong)] bg-[var(--surface-base)] px-3.5 py-2 text-xs font-semibold text-[var(--text-primary)] hover:bg-[var(--surface-subtle)] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--color-focus-ring)] forced-colors:focus-visible:outline-[Highlight] cursor-pointer"
                        >
                          {rowActionLabel}
                        </button>
                      </td>
                    )}
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
    </section>
  );
};
