import React from "react";

export type IconType = React.ComponentType<{ className?: string }>;

export interface CtaAction {
  label: string;
  href?: string;
  onClick?: () => void;
  variant?: "primary" | "secondary" | "outline";
}

// 1. Split Hero
export interface HeroStat {
  value: string;
  label: string;
  sublabel?: string;
}

export interface PatternSplitHeroProps {
  id?: string;
  badge?: string;
  title: React.ReactNode;
  subhead: string;
  primaryCta: CtaAction;
  secondaryCta?: CtaAction;
  proofCard: {
    title?: string;
    liveStatus?: string;
    stats: HeroStat[];
    techChips?: string[];
    footnote?: string;
  };
  trustBadges?: Array<{
    icon?: IconType;
    text: string;
  }>;
  mediaSlot?: React.ReactNode;
}

// 2. Bento Grid
export interface BentoItem {
  icon?: IconType;
  title: string;
  description: string;
  caption?: string;
  href?: string;
  colSpan?: 1 | 2 | 3;
}

export interface PatternBentoGridProps {
  id?: string;
  badge?: string;
  title: string;
  description?: string;
  items: BentoItem[];
  columns?: 2 | 3 | 4;
}

// 3. Comparison (Old Way vs New Way)
export interface ComparisonItem {
  title: string;
  desc: string;
}

export interface PatternComparisonProps {
  id?: string;
  badge?: string;
  title: string;
  description?: string;
  leftCard: {
    title: string;
    subtitle: string;
    items: ComparisonItem[];
  };
  rightCard: {
    title: string;
    subtitle: string;
    items: ComparisonItem[];
  };
}

// 4. Spec Accordion (Progressive Disclosure)
export interface AccordionSpecItem {
  id: string;
  question: string;
  answer: string;
  tags?: string[];
}

export interface PatternSpecAccordionProps {
  id?: string;
  badge?: string;
  title: string;
  description?: string;
  items: AccordionSpecItem[];
}

// 5. Stepper (Roadmap / Delivery Pipeline)
export interface StepItem {
  step: string;
  title: string;
  description: string;
  duration?: string;
  deliverables?: string[];
}

export interface PatternStepperProps {
  id?: string;
  badge?: string;
  title: string;
  description?: string;
  steps: StepItem[];
}

// 6. Social Proof (Metrics & Trust Badges)
export interface SocialMetric {
  value: string;
  label: string;
  growth?: string;
}

export interface PatternSocialProofProps {
  id?: string;
  badge?: string;
  title?: string;
  metrics: SocialMetric[];
  footnote?: string;
  clientLogos?: Array<{ name: string; logoUrl?: string }>;
}

// 7. Tiered Pricing
export interface PricingPlan {
  name: string;
  price: string;
  period?: string;
  description: string;
  popular?: boolean;
  features: string[];
  cta: CtaAction;
}

export interface PatternTieredPricingProps {
  id?: string;
  badge?: string;
  title: string;
  description?: string;
  plans: PricingPlan[];
}

// 8. CTA Band
export interface PatternCtaBandProps {
  id?: string;
  title: string;
  description: string;
  primaryCta: CtaAction;
  secondaryCta?: CtaAction;
  guaranteeNote?: string;
}

// 9. Enterprise Data Table
export interface DataTableColumn {
  key: string;
  label: string;
  sortable?: boolean;
  numeric?: boolean;
}

export interface DataTableRow {
  id: string;
  cells: Record<string, string | number>;
  status?: "healthy" | "warning" | "critical";
}

export interface PatternDataTableProps {
  id?: string;
  badge?: string;
  title: string;
  description?: string;
  caption?: string;
  columns: DataTableColumn[];
  rows: DataTableRow[];
  searchable?: boolean;
  searchPlaceholder?: string;
  emptyMessage?: string;
  rowActionLabel?: string;
  onRowAction?: (row: DataTableRow) => void;
}

// 10. Enterprise Form Engine
export interface FormFieldConfig {
  name: string;
  label: string;
  type?: "text" | "email" | "tel" | "textarea" | "select";
  required?: boolean;
  autoComplete?: string;
  placeholder?: string;
  helperText?: string;
  defaultValue?: string;
  minLength?: number;
  options?: Array<{ label: string; value: string }>;
}

export interface FormTelemetryEvent {
  event: string;
  durationMs: number;
  valid: boolean;
  errorCount: number;
}

export interface PatternFormEngineProps {
  id?: string;
  badge?: string;
  title: string;
  description?: string;
  fields: FormFieldConfig[];
  submitLabel?: string;
  action?: string;
  method?: "POST" | "GET";
  minSubmitMs?: number;
  honeypotFieldName?: string;
  successMessage?: string;
  onSubmitData?: (values: Record<string, string>) => Promise<void> | void;
  onTelemetry?: (event: FormTelemetryEvent) => void;
}

// 11. Enterprise App Shell
export interface AppShellNavItem {
  id: string;
  label: string;
  href: string;
  active?: boolean;
  badge?: string;
}

export interface AppShellNotification {
  id: string;
  title: string;
  time: string;
  unread?: boolean;
}

export interface PatternAppShellProps {
  brandName: string;
  brandMark?: React.ReactNode;
  navItems: AppShellNavItem[];
  breadcrumbs?: Array<{ label: string; href?: string }>;
  user?: { name: string; role: string; initials: string };
  notifications?: AppShellNotification[];
  headerActions?: React.ReactNode;
  onNavigate?: (item: AppShellNavItem) => void;
  children: React.ReactNode;
}

// 12. Enterprise Chart Row
export interface ChartPoint {
  label: string;
  value: number;
}

export interface ChartSeriesCard {
  id: string;
  title: string;
  metricValue: string;
  deltaLabel: string;
  deltaTone?: "positive" | "negative" | "neutral";
  dateRange: string;
  points: ChartPoint[];
}

export interface PatternChartRowProps {
  id?: string;
  badge?: string;
  title: string;
  description?: string;
  sourceNote: string;
  charts: ChartSeriesCard[];
}
