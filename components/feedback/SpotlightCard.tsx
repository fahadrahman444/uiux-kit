import React, { useRef, useState } from "react";

export interface SpotlightCardProps extends React.HTMLAttributes<HTMLDivElement> {
  children: React.ReactNode;
  className?: string;
  contentClassName?: string;
  spotlightColor?: string;
  spotlightRadius?: number;
  interactive?: boolean;
}

/**
 * SpotlightCard
 * Hardware-accelerated cursor spotlight card driven directly by CSS Custom Properties
 * (--spotlight-x, --spotlight-y) to avoid React re-renders on mousemove.
 */
export const SpotlightCard: React.FC<SpotlightCardProps> = ({
  children,
  className = "",
  contentClassName = "",
  spotlightColor = "rgba(59, 130, 246, 0.12)", // default subtle blue glow
  spotlightRadius = 350,
  interactive = false,
  ...props
}) => {
  const divRef = useRef<HTMLDivElement>(null);
  const [opacity, setOpacity] = useState(0);

  const handleMouseMove = (e: React.MouseEvent<HTMLDivElement>) => {
    if (!divRef.current) return;
    const rect = divRef.current.getBoundingClientRect();
    divRef.current.style.setProperty("--spotlight-x", `${e.clientX - rect.left}px`);
    divRef.current.style.setProperty("--spotlight-y", `${e.clientY - rect.top}px`);
  };

  const handleMouseEnter = () => setOpacity(1);
  const handleMouseLeave = () => setOpacity(0);

  return (
    <div
      ref={divRef}
      onMouseMove={handleMouseMove}
      onMouseEnter={handleMouseEnter}
      onMouseLeave={handleMouseLeave}
      className={`relative overflow-hidden rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 transition-all duration-200 ${
        interactive
          ? "hover:border-blue-500/50 hover:shadow-lg hover:-translate-y-0.5 active:translate-y-0 cursor-pointer"
          : ""
      } ${className}`}
      {...props}
    >
      {/* 60fps compositor spotlight layer */}
      <div
        className="pointer-events-none absolute -inset-px z-0 transition-opacity duration-300 ease-out"
        style={{
          opacity,
          background: `radial-gradient(${spotlightRadius}px circle at var(--spotlight-x, -999px) var(--spotlight-y, -999px), ${spotlightColor}, transparent 70%)`,
        }}
        aria-hidden="true"
      />

      <div className={`relative z-10 h-full ${contentClassName}`}>
        {children}
      </div>
    </div>
  );
};
