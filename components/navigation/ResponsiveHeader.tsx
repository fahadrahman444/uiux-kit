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
    <header className="sticky top-0 z-30 w-full border-b border-slate-200 dark:border-slate-800 bg-white/95 dark:bg-slate-900/95 pt-[env(safe-area-inset-top,0px)]">
      <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-8">
        {/* Brand Logo */}
        <div className="flex items-center gap-6">
          <div className="flex items-center">{logo}</div>
          <nav aria-label="Desktop Navigation" className="hidden md:flex items-center gap-6">
            {navLinks.map((link) => (
              <a
                key={link.href}
                href={link.href}
                className="text-sm font-medium text-slate-600 hover:text-slate-900 dark:text-slate-300 dark:hover:text-white transition-colors focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-blue-600 forced-colors:focus-visible:outline-[Highlight]"
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
              onClick={onMenuToggle}
              aria-label="Open mobile menu"
              className="md:hidden min-h-[44px] min-w-[44px] flex items-center justify-center rounded-lg text-slate-600 hover:bg-slate-100 dark:text-slate-300 dark:hover:bg-slate-800 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-blue-600 forced-colors:focus-visible:outline-[Highlight]"
            >
              <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16m-7 6h7" />
              </svg>
            </button>
          )}
        </div>
      </div>
    </header>
  );
};
