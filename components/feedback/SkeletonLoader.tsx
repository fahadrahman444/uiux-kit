import React from "react";

interface SkeletonProps {
  className?: string;
}

export const SkeletonLoader: React.FC<SkeletonProps> = ({ className = "h-4 w-full" }) => {
  return (
    <div
      aria-hidden="true"
      className={`animate-pulse rounded-md bg-slate-200 dark:bg-slate-800 ${className}`}
    />
  );
};
