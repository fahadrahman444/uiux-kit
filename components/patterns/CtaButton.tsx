import React from "react";
import type { CtaAction } from "./types";

interface CtaButtonProps {
  cta: CtaAction;
  className: string;
}

/**
 * Renders a semantic <a> when href is provided and a native <button type="button">
 * when only an onClick handler is passed, avoiding broken "#" anchor navigation.
 */
export const CtaButton: React.FC<CtaButtonProps> = ({ cta, className }) => {
  const focusClasses =
    "focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-blue-600 forced-colors:focus-visible:outline-[Highlight]";

  if (cta.href) {
    return (
      <a href={cta.href} onClick={cta.onClick} className={`${className} ${focusClasses}`}>
        {cta.label}
      </a>
    );
  }

  return (
    <button type="button" onClick={cta.onClick} className={`${className} ${focusClasses}`}>
      {cta.label}
    </button>
  );
};
