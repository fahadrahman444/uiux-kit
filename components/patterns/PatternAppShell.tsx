import React, { useEffect, useId, useRef, useState } from "react";
import { useDialogA11y } from "../overlays/useDialogA11y";
import type { PatternAppShellProps } from "./types";

export const PatternAppShell: React.FC<PatternAppShellProps> = ({
  brandName,
  brandMark,
  navItems,
  breadcrumbs,
  user,
  notifications = [],
  headerActions,
  onNavigate,
  children,
}) => {
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
  const [mobileNavOpen, setMobileNavOpen] = useState(false);
  const [notifOpen, setNotifOpen] = useState(false);
  const [userMenuOpen, setUserMenuOpen] = useState(false);

  const sidebarId = useId();
  const mobileDrawerRef = useRef<HTMLDivElement>(null);
  const notifRef = useRef<HTMLDivElement>(null);
  const userMenuRef = useRef<HTMLDivElement>(null);

  useDialogA11y(mobileNavOpen, () => setMobileNavOpen(false), mobileDrawerRef);

  useEffect(() => {
    const onKeyDown = (e: KeyboardEvent) => {
      if (e.key === "Escape") {
        setNotifOpen(false);
        setUserMenuOpen(false);
      }
    };
    window.addEventListener("keydown", onKeyDown);
    return () => window.removeEventListener("keydown", onKeyDown);
  }, []);

  const unreadCount = notifications.filter((n) => n.unread).length;

  return (
    <div className="min-h-[100dvh] bg-[var(--surface-base)] text-[var(--text-primary)] flex flex-col">
      <a
        href="#main-content"
        className="sr-only focus:not-sr-only focus:fixed focus:top-3 focus:left-3 focus:z-50 min-h-[44px] inline-flex items-center rounded-lg bg-[var(--color-action-primary)] px-4 py-2 text-sm font-semibold text-[var(--color-action-primary-text)] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--color-focus-ring)] forced-colors:focus-visible:outline-[Highlight]"
      >
        Skip to main content
      </a>

      {/* Top Sticky Utility Header */}
      <header className="sticky top-0 z-30 h-16 border-b border-[var(--border-subtle)] bg-[var(--surface-base)] px-4 sm:px-6 flex items-center justify-between gap-4">
        <div className="flex items-center gap-3 min-w-0">
          <button
            type="button"
            onClick={() => setMobileNavOpen(true)}
            aria-label="Open navigation drawer"
            className="lg:hidden min-h-[44px] min-w-[44px] flex items-center justify-center rounded-lg border border-[var(--border-subtle)] text-[var(--text-primary)] hover:bg-[var(--surface-subtle)] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--color-focus-ring)] forced-colors:focus-visible:outline-[Highlight] cursor-pointer"
          >
            <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
            </svg>
          </button>

          <button
            type="button"
            onClick={() => setSidebarCollapsed((c) => !c)}
            aria-expanded={!sidebarCollapsed}
            aria-controls={sidebarId}
            aria-label={sidebarCollapsed ? "Expand sidebar" : "Collapse sidebar"}
            className="hidden lg:flex min-h-[44px] min-w-[44px] items-center justify-center rounded-lg border border-[var(--border-subtle)] text-[var(--text-secondary)] hover:text-[var(--text-primary)] hover:bg-[var(--surface-subtle)] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--color-focus-ring)] forced-colors:focus-visible:outline-[Highlight] cursor-pointer"
          >
            <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h10M4 18h16" />
            </svg>
          </button>

          <div className="flex items-center gap-2 font-bold text-base tracking-tight truncate">
            {brandMark}
            <span>{brandName}</span>
          </div>

          {breadcrumbs && breadcrumbs.length > 0 && (
            <nav aria-label="Breadcrumb" className="hidden sm:flex items-center gap-2 pl-4 border-l border-[var(--border-subtle)] text-xs text-[var(--text-secondary)]">
              <ol className="flex items-center gap-2">
                {breadcrumbs.map((crumb, idx) => (
                  <li key={idx} className="flex items-center gap-2">
                    {idx > 0 && <span aria-hidden="true">/</span>}
                    {crumb.href ? (
                      <a
                        href={crumb.href}
                        className="min-h-[24px] inline-flex items-center hover:text-[var(--text-primary)] rounded px-1 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--color-focus-ring)]"
                      >
                        {crumb.label}
                      </a>
                    ) : (
                      <span aria-current="page" className="font-semibold text-[var(--text-primary)]">
                        {crumb.label}
                      </span>
                    )}
                  </li>
                ))}
              </ol>
            </nav>
          )}
        </div>

        <div className="flex items-center gap-2">
          {headerActions}

          {/* Notification Drawer Toggle */}
          <div className="relative" ref={notifRef}>
            <button
              type="button"
              onClick={() => {
                setNotifOpen((o) => !o);
                setUserMenuOpen(false);
              }}
              aria-expanded={notifOpen}
              aria-label={`Notifications (${unreadCount} unread)`}
              className="relative min-h-[44px] min-w-[44px] flex items-center justify-center rounded-lg border border-[var(--border-subtle)] text-[var(--text-secondary)] hover:text-[var(--text-primary)] hover:bg-[var(--surface-subtle)] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--color-focus-ring)] forced-colors:focus-visible:outline-[Highlight] cursor-pointer"
            >
              <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6 6 0 10-12 0v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
              </svg>
              {unreadCount > 0 && (
                <span className="absolute top-1.5 right-1.5 h-2.5 w-2.5 rounded-full bg-[var(--color-action-primary)]" aria-hidden="true" />
              )}
            </button>

            {notifOpen && (
              <div
                role="region"
                aria-label="Recent notifications"
                className="absolute right-0 mt-2 w-80 max-w-[calc(100vw-2rem)] rounded-xl border border-[var(--border-subtle)] bg-[var(--surface-base)] p-3 shadow-xl z-40"
              >
                <div className="flex items-center justify-between pb-2 mb-2 border-b border-[var(--border-subtle)]">
                  <span className="text-xs font-semibold text-[var(--text-primary)]">Notifications</span>
                  <button
                    type="button"
                    onClick={() => setNotifOpen(false)}
                    aria-label="Close notifications"
                    className="min-h-[24px] min-w-[24px] px-2 text-xs font-medium text-[var(--text-secondary)] hover:text-[var(--text-primary)] rounded focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--color-focus-ring)] cursor-pointer"
                  >
                    Close
                  </button>
                </div>
                {notifications.length === 0 ? (
                  <p className="text-xs text-[var(--text-secondary)] py-3">All caught up.</p>
                ) : (
                  <ul className="space-y-2">
                    {notifications.map((n) => (
                      <li key={n.id} className="rounded-lg bg-[var(--surface-raised)] p-2.5 text-xs">
                        <div className="font-medium text-[var(--text-primary)]">{n.title}</div>
                        <div className="text-[var(--text-secondary)] mt-0.5 font-mono">{n.time}</div>
                      </li>
                    ))}
                  </ul>
                )}
              </div>
            )}
          </div>

          {/* User Profile Menu */}
          {user && (
            <div className="relative" ref={userMenuRef}>
              <button
                type="button"
                onClick={() => {
                  setUserMenuOpen((o) => !o);
                  setNotifOpen(false);
                }}
                aria-expanded={userMenuOpen}
                aria-haspopup="menu"
                aria-label={`Account menu for ${user.name}`}
                className="min-h-[44px] inline-flex items-center gap-2 rounded-lg border border-[var(--border-subtle)] bg-[var(--surface-raised)] px-2.5 py-1.5 text-xs font-semibold text-[var(--text-primary)] hover:bg-[var(--surface-subtle)] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--color-focus-ring)] forced-colors:focus-visible:outline-[Highlight] cursor-pointer"
              >
                <span className="h-7 w-7 rounded-full bg-[var(--color-action-primary)] text-[var(--color-action-primary-text)] inline-flex items-center justify-center font-mono text-xs">
                  {user.initials}
                </span>
                <span className="hidden sm:inline">{user.name}</span>
              </button>

              {userMenuOpen && (
                <div
                  role="menu"
                  aria-label="User profile actions"
                  className="absolute right-0 mt-2 w-56 rounded-xl border border-[var(--border-subtle)] bg-[var(--surface-base)] p-2 shadow-xl z-40"
                >
                  <div className="px-3 py-2 border-b border-[var(--border-subtle)] mb-1">
                    <div className="text-xs font-semibold text-[var(--text-primary)]">{user.name}</div>
                    <div className="text-xs text-[var(--text-secondary)]">{user.role}</div>
                  </div>
                  <button
                    type="button"
                    role="menuitem"
                    onClick={() => setUserMenuOpen(false)}
                    className="w-full min-h-[44px] flex items-center rounded-lg px-3 text-left text-xs font-medium text-[var(--text-primary)] hover:bg-[var(--surface-subtle)] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--color-focus-ring)] cursor-pointer"
                  >
                    Workspace preferences
                  </button>
                </div>
              )}
            </div>
          )}
        </div>
      </header>

      <div className="flex flex-1 min-h-0">
        {/* Desktop Collapsible Sidebar */}
        <aside
          id={sidebarId}
          aria-label="Primary Workspace Navigation"
          className={`hidden lg:flex flex-col border-r border-[var(--border-subtle)] bg-[var(--surface-raised)] transition-all duration-200 motion-reduce:transition-none ${
            sidebarCollapsed ? "w-20" : "w-64"
          }`}
        >
          <nav className="p-3 space-y-1.5" aria-label="Sidebar links">
            {navItems.map((item) => (
              <a
                key={item.id}
                href={item.href}
                onClick={() => onNavigate?.(item)}
                aria-current={item.active ? "page" : undefined}
                className={`min-h-[44px] flex items-center justify-between gap-2 rounded-lg px-3 py-2 text-sm font-medium transition-colors focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--color-focus-ring)] forced-colors:focus-visible:outline-[Highlight] ${
                  item.active
                    ? "bg-[var(--color-action-accent-surface)] text-[var(--color-action-accent-text)] border border-[var(--color-action-accent-border)]"
                    : "text-[var(--text-secondary)] hover:bg-[var(--surface-subtle)] hover:text-[var(--text-primary)]"
                }`}
              >
                <span className="truncate">{sidebarCollapsed ? item.label.slice(0, 2) : item.label}</span>
                {!sidebarCollapsed && item.badge && (
                  <span className="text-xs font-mono px-2 py-0.5 rounded bg-[var(--surface-subtle)] text-[var(--text-primary)]">
                    {item.badge}
                  </span>
                )}
              </a>
            ))}
          </nav>
        </aside>

        {/* Mobile Drawer */}
        {mobileNavOpen && (
          <div className="fixed inset-0 z-50 flex lg:hidden">
            <div
              onClick={() => setMobileNavOpen(false)}
              className="fixed inset-0 bg-[var(--overlay-scrim)]"
              aria-hidden="true"
            />
            <div
              ref={mobileDrawerRef}
              role="dialog"
              aria-modal="true"
              aria-label="Mobile navigation drawer"
              tabIndex={-1}
              className="relative z-10 w-72 max-w-[85vw] bg-[var(--surface-base)] border-r border-[var(--border-subtle)] p-4 flex flex-col gap-4 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--color-focus-ring)]"
            >
              <div className="flex items-center justify-between pb-3 border-b border-[var(--border-subtle)]">
                <span className="font-bold text-sm text-[var(--text-primary)]">{brandName}</span>
                <button
                  type="button"
                  onClick={() => setMobileNavOpen(false)}
                  aria-label="Close navigation drawer"
                  className="min-h-[44px] min-w-[44px] flex items-center justify-center rounded-lg text-[var(--text-secondary)] hover:bg-[var(--surface-subtle)] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--color-focus-ring)] cursor-pointer"
                >
                  <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>
              <nav aria-label="Mobile drawer links" className="space-y-1.5">
                {navItems.map((item) => (
                  <a
                    key={item.id}
                    href={item.href}
                    onClick={() => {
                      onNavigate?.(item);
                      setMobileNavOpen(false);
                    }}
                    aria-current={item.active ? "page" : undefined}
                    className={`min-h-[44px] flex items-center justify-between rounded-lg px-3 py-2 text-sm font-medium focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--color-focus-ring)] ${
                      item.active
                        ? "bg-[var(--color-action-accent-surface)] text-[var(--color-action-accent-text)]"
                        : "text-[var(--text-secondary)] hover:bg-[var(--surface-subtle)] hover:text-[var(--text-primary)]"
                    }`}
                  >
                    <span>{item.label}</span>
                    {item.badge && <span className="text-xs font-mono">{item.badge}</span>}
                  </a>
                ))}
              </nav>
            </div>
          </div>
        )}

        {/* Main Workspace Content */}
        <main id="main-content" tabIndex={-1} className="flex-1 min-w-0 focus:outline-none">
          {children}
        </main>
      </div>
    </div>
  );
};
