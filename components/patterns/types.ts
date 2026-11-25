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
