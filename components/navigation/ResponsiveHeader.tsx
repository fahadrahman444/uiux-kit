import React from "react";

interface ResponsiveHeaderProps {
  logo: React.ReactNode;
  navLinks: { label: string; href: string }[];
  actions?: React.ReactNode;
  onMenuToggle?: () => void;
}

export const ResponsiveHeader: React.FC<ResponsiveHeaderProps> = ({
  logo,
  navLinks,
  actions,
  onMenuToggle,
}) => {
  return (
    <header className="sticky top-0 z-30 w-full border-b border-[var(--border-subtle)] bg-[var(--surface-base)] pt-[env(safe-area-inset-top,0px)]">
      <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-8">
        {/* Brand Logo */}
        <div className="flex items-center gap-6">
          <div className="flex items-center text-[var(--text-primary)]">{logo}</div>
          <nav aria-label="Desktop Navigation" className="hidden md:flex items-center gap-4">
            {navLinks.map((link) => (
              <a
                key={link.href}
                href={link.href}
                className="min-h-[44px] inline-flex items-center px-2 text-sm font-medium text-[var(--text-secondary)] hover:text-[var(--text-primary)] transition-colors rounded-md focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--color-focus-ring)] forced-colors:focus-visible:outline-[Highlight]"
              >
                {link.label}
              </a>
            ))}
          </nav>
        </div>

        {/* Right Actions */}
        <div className="flex items-center gap-3">
          {actions}

          {/* Mobile Menu Trigger */}
          {onMenuToggle && (
            <button
              type="button"
              onClick={onMenuToggle}
              aria-label="Open mobile menu"
              className="md:hidden min-h-[44px] min-w-[44px] flex items-center justify-center rounded-lg text-[var(--text-secondary)] hover:bg-[var(--surface-subtle)] hover:text-[var(--text-primary)] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--color-focus-ring)] forced-colors:focus-visible:outline-[Highlight] cursor-pointer"
            >
              <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16m-7 6h7" />
              </svg>
            </button>
          )}
        </div>
      </div>
    </header>
  );
};
