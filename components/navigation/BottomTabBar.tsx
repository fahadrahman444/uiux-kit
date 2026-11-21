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
      className="fixed bottom-0 left-0 right-0 z-40 block sm:hidden bg-white/95 dark:bg-slate-900/95 border-t border-slate-200 dark:border-slate-800 pb-[env(safe-area-inset-bottom,0px)] shadow-lg"
    >
      <div className="flex items-center justify-around h-16 px-2">
        {tabs.map((tab) => (
          <button
            key={tab.id}
            onClick={tab.onClick}
            aria-label={tab.label}
            aria-current={tab.isActive ? "page" : undefined}
            className={`min-h-[44px] min-w-[44px] flex flex-col items-center justify-center gap-1 rounded-md text-xs font-medium transition-colors ${
              tab.isActive
                ? "text-blue-600 dark:text-blue-400"
                : "text-slate-500 hover:text-slate-900 dark:text-slate-400 dark:hover:text-slate-100"
            }`}
          >
            <div className="h-5 w-5">{tab.icon}</div>
            <span>{tab.label}</span>
          </button>
        ))}
      </div>
    </nav>
  );
};
