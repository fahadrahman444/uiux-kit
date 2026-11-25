import React from "react";

interface SkeletonProps {
  className?: string;
}

export const SkeletonLoader: React.FC<SkeletonProps> = ({ className = "h-4 w-full" }) => {
  return (
    <div
      aria-hidden="true"
      className={`animate-pulse motion-reduce:animate-none rounded-md bg-[var(--surface-subtle)] ${className}`}
    />
  );
};
