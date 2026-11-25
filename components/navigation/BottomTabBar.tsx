import React from "react";

interface TabItem {
  id: string;
  label: string;
  icon: React.ReactNode;
  isActive?: boolean;
  onClick: () => void;
}

interface BottomTabBarProps {
  tabs: TabItem[];
}

export const BottomTabBar: React.FC<BottomTabBarProps> = ({ tabs }) => {
  return (
    <nav
      aria-label="Mobile Navigation"
      className="fixed bottom-0 left-0 right-0 z-40 block sm:hidden bg-[var(--surface-base)] border-t border-[var(--border-subtle)] pb-[env(safe-area-inset-bottom,0px)] shadow-lg"
    >
      <div className="flex items-center justify-around h-16 px-2">
        {tabs.map((tab) => (
          <button
            key={tab.id}
            type="button"
            onClick={tab.onClick}
            aria-label={tab.label}
            aria-current={tab.isActive ? "page" : undefined}
            className={`min-h-[44px] min-w-[44px] px-2 flex flex-col items-center justify-center gap-1 rounded-md text-xs font-medium transition-colors cursor-pointer focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--color-focus-ring)] forced-colors:focus-visible:outline-[Highlight] ${
              tab.isActive
                ? "text-[var(--color-action-accent-text)]"
                : "text-[var(--text-secondary)] hover:text-[var(--text-primary)]"
            }`}
          >
            <span aria-hidden="true" className="h-5 w-5 inline-flex items-center justify-center">
              {tab.icon}
            </span>
            <span>{tab.label}</span>
          </button>
        ))}
      </div>
    </nav>
  );
};
