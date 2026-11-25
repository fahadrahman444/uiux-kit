import React, { useId, useRef, useState } from "react";
import type { FormFieldConfig, PatternFormEngineProps } from "./types";

const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

export const PatternFormEngine: React.FC<PatternFormEngineProps> = ({
  id = "intake-form",
  badge = "Verification Gate",
  title,
  description,
  fields,
  submitLabel = "Submit request",
  action = "/api/submit",
  method = "POST",
  minSubmitMs = 2500,
  honeypotFieldName = "company_fax_field",
  successMessage = "Submission validated and queued safely.",
  onSubmitData,
  onTelemetry,
  // Optional client-side submission handler + zero-PII telemetry
}) => {
  const baseId = useId();
  const mountedAtRef = useRef<number>(Date.now());
  const errorSummaryRef = useRef<HTMLDivElement>(null);

  const initialValues = () => {
    const map: Record<string, string> = {};
    for (const f of fields) {
      map[f.name] = f.defaultValue ?? "";
    }
    return map;
  };

  const [values, setValues] = useState<Record<string, string>>(initialValues);
  const [honeypot, setHoneypot] = useState("");
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [formBannerError, setFormBannerError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);
  const [submitted, setSubmitted] = useState(false);

  const validateField = (field: FormFieldConfig, rawVal: string): string | null => {
    const val = rawVal.trim();
    if (field.required && !val) {
      return `${field.label} is required.`;
    }
    if (val && field.type === "email" && !EMAIL_RE.test(val)) {
      return `Enter a valid email address for ${field.label}.`;
    }
    if (val && field.minLength && val.length < field.minLength) {
      return `${field.label} must be at least ${field.minLength} characters.`;
    }
    return null;
  };

  const handleChange = (name: string, val: string) => {
    setValues((prev) => ({ ...prev, [name]: val }));
    if (errors[name]) {
      setErrors((prev) => {
        const next = { ...prev };
        delete next[name];
        return next;
      });
    }
    if (submitted) setSubmitted(false);
  };

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (submitting) return;

    const elapsedMs = Date.now() - mountedAtRef.current;

    // 1. Honeypot trap: silently discard automated submissions without CRM sync
    if (honeypot.trim().length > 0) {
      onTelemetry?.({
        event: "form_honeypot_discarded",
        durationMs: elapsedMs,
        valid: false,
        errorCount: 1,
      });
      setSubmitted(true);
      setFormBannerError(null);
      return;
    }

    // 2. Cryptographic / time-trap guard (< minSubmitMs)
    if (minSubmitMs > 0 && elapsedMs < minSubmitMs) {
      setFormBannerError("Submission arrived too quickly. Please review your details and try again.");
      onTelemetry?.({
        event: "form_timetrap_rejected",
        durationMs: elapsedMs,
        valid: false,
        errorCount: 1,
      });
      window.requestAnimationFrame(() => errorSummaryRef.current?.focus());
      return;
    }

    // 3. Field validation
    const nextErrors: Record<string, string> = {};
    for (const field of fields) {
      const err = validateField(field, values[field.name] ?? "");
      if (err) nextErrors[field.name] = err;
    }

    if (Object.keys(nextErrors).length > 0) {
      setErrors(nextErrors);
      setFormBannerError(`Please fix ${Object.keys(nextErrors).length} highlighted field(s) below.`);
      onTelemetry?.({
        event: "form_validation_error",
        durationMs: elapsedMs,
        valid: false,
        errorCount: Object.keys(nextErrors).length,
      });
      window.requestAnimationFrame(() => errorSummaryRef.current?.focus());
      return;
    }

    setErrors({});
    setFormBannerError(null);
    setSubmitting(true);
    try {
      await onSubmitData?.(values);
      setSubmitted(true);
      onTelemetry?.({
        event: "form_submitted",
        durationMs: elapsedMs,
        valid: true,
        errorCount: 0,
      });
    } finally {
      setSubmitting(false);
    }
  };

  const errorEntries = Object.entries(errors);

  return (
    <section id={id} className="scroll-mt-20 py-14 sm:py-20 border-b border-[var(--border-subtle)] bg-[var(--surface-raised)]">
      <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="mb-8">
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

        <form
          action={action}
          method={method}
          noValidate
          onSubmit={handleSubmit}
          className="rounded-2xl border border-[var(--border-subtle)] bg-[var(--surface-base)] p-6 sm:p-8 shadow-xs space-y-6"
        >
          {/* Honeypot field for bot defense */}
          <div className="sr-only" aria-hidden="true">
            <label htmlFor={`${baseId}-hp`}>Leave this field blank</label>
            <input
              id={`${baseId}-hp`}
              type="text"
              name={honeypotFieldName}
              tabIndex={-1}
              autoComplete="off"
              value={honeypot}
              onChange={(e) => setHoneypot(e.target.value)}
            />
          </div>

          {(formBannerError || errorEntries.length > 0) && (
            <div
              ref={errorSummaryRef}
              role="alert"
              tabIndex={-1}
              className="rounded-xl border border-[var(--color-danger-border)] bg-[var(--color-danger-surface)] p-4 text-sm text-[var(--color-danger-text)] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--color-focus-ring)] forced-colors:focus-visible:outline-[Highlight]"
            >
              <p className="font-semibold">{formBannerError || "Please resolve the following errors:"}</p>
              {errorEntries.length > 0 && (
                <ul className="mt-2 list-disc list-inside space-y-1">
                  {errorEntries.map(([fieldName, msg]) => (
                    <li key={fieldName}>
                      <a
                        href={`#${baseId}-${fieldName}`}
                        onClick={(ev) => {
                          ev.preventDefault();
                          document.getElementById(`${baseId}-${fieldName}`)?.focus();
                        }}
                        className="underline font-medium inline-flex items-center min-h-[24px] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--color-focus-ring)]"
                      >
                        {msg}
                      </a>
                    </li>
                  ))}
                </ul>
              )}
            </div>
          )}

          {submitted && !formBannerError && errorEntries.length === 0 && (
            <div
              role="status"
              className="rounded-xl border border-[var(--color-success-border)] bg-[var(--color-success-surface)] p-4 text-sm font-medium text-[var(--color-success-text)]"
            >
              {successMessage}
            </div>
          )}

          <div className="space-y-5">
            {fields.map((field) => {
              const inputId = `${baseId}-${field.name}`;
              const helperId = field.helperText ? `${inputId}-help` : undefined;
              const errorId = errors[field.name] ? `${inputId}-error` : undefined;
              const describedBy = [helperId, errorId].filter(Boolean).join(" ") || undefined;
              const hasError = Boolean(errors[field.name]);
              const commonClass = `w-full min-h-[44px] rounded-lg border px-3.5 py-2.5 text-sm bg-[var(--surface-base)] text-[var(--text-primary)] placeholder:text-[var(--text-secondary)] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--color-focus-ring)] forced-colors:focus-visible:outline-[Highlight] ${
                hasError
                  ? "border-[var(--color-danger)]"
                  : "border-[var(--border-strong)]"
              }`;

              return (
                <div key={field.name}>
                  <label htmlFor={inputId} className="block text-sm font-semibold text-[var(--text-primary)] mb-1.5">
                    {field.label}
                    {field.required && (
                      <span className="text-[var(--color-danger-text)] ml-1" aria-hidden="true">
                        *
                      </span>
                    )}
                  </label>

                  {field.type === "textarea" ? (
                    <textarea
                      id={inputId}
                      name={field.name}
                      rows={4}
                      required={field.required}
                      autoComplete={field.autoComplete}
                      placeholder={field.placeholder}
                      value={values[field.name] ?? ""}
                      onChange={(e) => handleChange(field.name, e.target.value)}
                      aria-invalid={hasError || undefined}
                      aria-describedby={describedBy}
                      className={commonClass}
                    />
                  ) : field.type === "select" ? (
                    <select
                      id={inputId}
                      name={field.name}
                      required={field.required}
                      autoComplete={field.autoComplete}
                      value={values[field.name] ?? ""}
                      onChange={(e) => handleChange(field.name, e.target.value)}
                      aria-invalid={hasError || undefined}
                      aria-describedby={describedBy}
                      className={commonClass}
                    >
                      <option value="">Select an option</option>
                      {(field.options ?? []).map((opt) => (
                        <option key={opt.value} value={opt.value}>
                          {opt.label}
                        </option>
                      ))}
                    </select>
                  ) : (
                    <input
                      id={inputId}
                      name={field.name}
                      type={field.type ?? "text"}
                      required={field.required}
                      autoComplete={field.autoComplete}
                      placeholder={field.placeholder}
                      value={values[field.name] ?? ""}
                      onChange={(e) => handleChange(field.name, e.target.value)}
                      aria-invalid={hasError || undefined}
                      aria-describedby={describedBy}
                      className={commonClass}
                    />
                  )}

                  {field.helperText && (
                    <p id={helperId} className="mt-1.5 text-xs text-[var(--text-secondary)]">
                      {field.helperText}
                    </p>
                  )}
                  {hasError && (
                    <p id={errorId} className="mt-1.5 text-xs font-medium text-[var(--color-danger-text)]">
                      {errors[field.name]}
                    </p>
                  )}
                </div>
              );
            })}
          </div>

          <div className="pt-2 flex flex-wrap items-center justify-between gap-4">
            <button
              type="submit"
              aria-disabled={submitting || undefined}
              aria-busy={submitting || undefined}
              className="min-h-[44px] min-w-[44px] inline-flex items-center justify-center gap-2 rounded-lg bg-[var(--color-action-primary)] hover:bg-[var(--color-action-primary-hover)] text-[var(--color-action-primary-text)] px-6 py-2.5 text-sm font-semibold transition-colors cursor-pointer focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--color-focus-ring)] forced-colors:focus-visible:outline-[Highlight] aria-[disabled=true]:opacity-50 aria-[disabled=true]:cursor-not-allowed"
            >
              {submitting && (
                <svg className="h-4 w-4 animate-spin motion-reduce:animate-none" viewBox="0 0 24 24" fill="none" aria-hidden="true">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z" />
                </svg>
              )}
              <span>{submitLabel}</span>
            </button>
            <span className="text-xs font-mono text-[var(--text-secondary)]">
              Protected by honeypot + time-trap ({minSubmitMs}ms)
            </span>
          </div>
        </form>
      </div>
    </section>
  );
};
