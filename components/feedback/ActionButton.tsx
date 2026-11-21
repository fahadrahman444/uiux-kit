import React from "react";
import { motion } from "framer-motion";

interface ActionButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  loading?: boolean;
  variant?: "primary" | "secondary" | "danger";
  children: React.ReactNode;
}

export const ActionButton: React.FC<ActionButtonProps> = ({
  loading = false,
  variant = "primary",
  children,
  disabled,
  onClick,
  className = "",
  ...props
}) => {
  const handleClick = (e: React.MouseEvent<HTMLButtonElement>) => {
    if (loading || disabled) {
      e.preventDefault();
      return;
    }
    if (onClick) onClick(e);
  };

  const variantStyles = {
    primary: "bg-blue-600 hover:bg-blue-700 text-white focus-visible:outline-blue-600",
    secondary: "bg-slate-100 dark:bg-slate-800 text-slate-900 dark:text-slate-100 hover:bg-slate-200 dark:hover:bg-slate-700 border border-slate-300 dark:border-slate-700 focus-visible:outline-slate-500",
    danger: "bg-rose-600 hover:bg-rose-700 text-white focus-visible:outline-rose-600",
  };

  return (
    <motion.button
      whileTap={!loading && !disabled ? { scale: 0.98 } : undefined}
      onClick={handleClick}
      disabled={disabled || loading}
      className={`relative inline-flex items-center justify-center min-h-[44px] min-w-[44px] px-5 py-2.5 rounded-lg font-medium text-sm transition-colors focus-visible:outline-2 focus-visible:outline-offset-2 forced-colors:focus-visible:outline-[Highlight] focus-visible:ring-2 focus-visible:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed ${variantStyles[variant]} ${className}`}
      {...props}
    >
      {loading ? (
        <span className="flex items-center gap-2">
          <svg className="h-4 w-4 animate-spin" viewBox="0 0 24 24" fill="none">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z" />
          </svg>
          <span>Processing...</span>
        </span>
      ) : (
        children
      )}
    </motion.button>
  );
};
