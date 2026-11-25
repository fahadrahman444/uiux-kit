import React from "react";
import { motion, useReducedMotion, type HTMLMotionProps } from "framer-motion";

interface ActionButtonProps extends Omit<HTMLMotionProps<"button">, "children"> {
  loading?: boolean;
  variant?: "primary" | "secondary" | "danger";
  disabled?: boolean;
  children: React.ReactNode;
}

export const ActionButton: React.FC<ActionButtonProps> = ({
  loading = false,
  variant = "primary",
  children,
  disabled,
  onClick,
  onKeyDown,
  className = "",
  ...props
}) => {
  const shouldReduceMotion = useReducedMotion();
  const isInactive = Boolean(disabled || loading);

  const handleClick = (e: React.MouseEvent<HTMLButtonElement>) => {
    if (isInactive) {
      e.preventDefault();
      return;
    }
    if (onClick) onClick(e);
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLButtonElement>) => {
    if (isInactive && (e.key === "Enter" || e.key === " ")) {
      e.preventDefault();
      return;
    }
    if (onKeyDown) onKeyDown(e);
  };

  const variantStyles = {
    primary:
      "bg-[var(--color-action-primary)] hover:bg-[var(--color-action-primary-hover)] text-[var(--color-action-primary-text)] focus-visible:outline-[var(--color-focus-ring)]",
    secondary:
      "bg-[var(--surface-subtle)] text-[var(--text-primary)] hover:bg-[var(--border-subtle)] border border-[var(--border-strong)] focus-visible:outline-[var(--color-focus-ring)]",
    danger:
      "bg-[var(--color-danger)] hover:bg-[var(--color-danger-hover)] text-[var(--color-action-primary-text)] focus-visible:outline-[var(--color-danger)]",
  };

  return (
    <motion.button
      whileTap={!isInactive && !shouldReduceMotion ? { scale: 0.98 } : undefined}
      onClick={handleClick}
      onKeyDown={handleKeyDown}
      aria-disabled={isInactive || undefined}
      aria-busy={loading || undefined}
      className={`relative inline-flex items-center justify-center min-h-[44px] min-w-[44px] px-5 py-2.5 rounded-lg font-medium text-sm transition-colors cursor-pointer focus-visible:outline-2 focus-visible:outline-offset-2 forced-colors:focus-visible:outline-[Highlight] aria-[disabled=true]:opacity-50 aria-[disabled=true]:cursor-not-allowed ${variantStyles[variant]} ${className}`}
      {...props}
    >
      <span className="inline-flex items-center gap-2">
        {loading && (
          <>
            <svg className="h-4 w-4 animate-spin motion-reduce:animate-none" viewBox="0 0 24 24" fill="none" aria-hidden="true">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z" />
            </svg>
            <span className="sr-only">Loading</span>
          </>
        )}
        <span>{children}</span>
      </span>
    </motion.button>
  );
};
