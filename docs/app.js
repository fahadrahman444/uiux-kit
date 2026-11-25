(() => {
  "use strict";

  const INTENT_VOCABULARY = {
    fresh: ["minimal", "clean", "modern"],
    trustworthy: ["enterprise", "b2b", "corporate", "professional"],
    exciting: ["bold", "creative", "dynamic", "editorial"],
    premium: ["luxury", "editorial", "high-end", "boutique"],
    simple: ["minimal", "single-column", "clean"],
    technical: ["developer", "engineering", "terminal", "api"],
    friendly: ["modern", "saas", "approachable"],
    impressive: ["immersive", "interactive", "editorial", "bento"],
    innovative: ["tech", "ai", "modern", "cutting-edge"],
  };

  const HIGH_CONTRAST_SERIFS = new Set([
    "bodoni moda",
    "libre bodoni",
    "playfair display",
    "cormorant garamond",
    "instrument serif",
  ]);

  const DOMAIN_SEARCH_COLS = {
    style: ["Style Category", "Keywords", "Best For", "Type"],
    prompt: ["Style Category", "AI Prompt Keywords (Copy-Paste Ready)", "CSS/Technical Keywords"],
    color: ["Product Type", "Keywords", "Notes"],
    chart: ["Data Type", "Keywords", "Best Chart Type", "Accessibility Notes"],
    landing: ["Pattern Name", "Keywords", "Conversion Optimization", "Section Order"],
    product: ["Product Type", "Keywords", "Primary Style Recommendation", "Key Considerations"],
    ux: ["Category", "Issue", "Description", "Platform"],
    typography: ["Font Pairing Name", "Category", "Mood/Style Keywords", "Best For", "Heading Font", "Body Font"],
    icons: ["Category", "Icon Name", "Keywords", "Best For"],
    react: ["Category", "Issue", "Keywords", "Description"],
    web: ["Category", "Issue", "Keywords", "Description"],
  };

  const STACK_SEARCH_COLS = ["Category", "Guideline", "Description", "Do", "Don't"];

  const SECTION_FALLBACKS = {
    navbar: "nav-02",
    hero: "hero-01",
    trusted_by: "tb-01",
    about: "abt-02",
    services: "srv-01",
    why_choose_us: "wcu-01",
    how_we_work: "hww-04",
    portfolio: "port-01",
    testimonials: "tst-01",
    results_metrics: "res-01",
    pricing: "prc-01",
    team: "team-01",
    faq: "faq-01",
    final_cta: "cta-01",
    footer: "ftr-01",
    pricing_hero: "phero-01",
    pricing_comparison_matrix: "pmat-01",
    pricing_addons: "padd-01",
    pricing_enterprise_sla: "psla-01",
    pricing_guarantee_bar: "pbar-01",
    about_timeline: "time-01",
    about_values: "val-01",
    about_culture_gallery: "cult-01",
    about_leadership_board: "lead-01",
    service_architecture: "arch-01",
    service_deliverables_matrix: "deliv-01",
    service_tech_stack: "stack-01",
    service_use_cases: "use-01",
    contact_intake_form: "cform-01",
    contact_location_map: "cmap-01",
    contact_sla_banner: "csla-01",
    case_study_hero_highlight: "csh-01",
    case_study_filter_hub: "csf-01",
    case_study_client_quote_strip: "csq-01",
    blog_featured_editorial: "bfeat-01",
    blog_topic_filter_feed: "bfeed-01",
    blog_newsletter_capture: "bnews-01",
    careers_perks: "perk-01",
    careers_jobs: "jobs-01",
    legal_doc: "leg-01",
  };

  const PRESETS = {
    enterprise: {
      page_id: "home",
      sitemapPages: ["home"],
      customSitemapPages: [],
      project_name: "CloudCore Telemetry",
      legal_name: "CloudCore Systems Inc.",
      tagline: "Sub-second observability without telemetry bloat.",
      existing_url: "",
      industry: "b2b saas analytics",
      business_model: "B2B SaaS",
      primary_goal: "Qualified Sales Leads & Demos",
      primary_device: "Desktop-Heavy (Work / Procurement)",
      buying_cycle: "Research-Driven / Multiple Stakeholders",
      discovery_confidence: "Partial Discovery",
      buyer_pain_points: "Slow legacy observability dashboards and opaque per-host pricing surprise teams during procurement.",
      competitor_links: "",
      reference_urls: "",
      brand_colors_note: "",
      hero_direction: "bento",
      dark_mode_support: "Both Light & Dark Modes",
      wcag_target: "WCAG 2.2 AA",
      reduced_motion: "Subtle Micro-Interactions (150ms, Reduced Motion Safe)",
      copy_owner: "Hybrid (Client Drafts + Studio Messaging)",
      content_readiness: "Partial Drafts / Existing Site",
      core_usp: "Unified OpenTelemetry trace analytics with predictable ingest pricing.",
      avoid_claims: "Unverified % speed claims or vague AI buzzwords",
      site_type: "Marketing Website + Headless CMS",
      cms_preference: "Headless (Sanity / Contentful)",
      target_launch: "Q2 2027 (8–10 weeks)",
      budget_tier: "Growth Retainer / $15k–$35k",
      decision_maker: "",
      hosting_status: "Existing Domain + DNS Access Ready",
      custom_page_names: "",
      priority_p0_notes: "Core marketing site, interactive pricing calculator/matrix, SOC 2 proof, and CRM lead intake.",
      priority_p2_notes: "Interactive sandbox tour and localized EMEA microsites.",
      style: "Swiss Modern Technical",
      stack: "nextjs",
      search_keywords: "dashboard chart table accessibility",
      evidence_note: "Q4 2026 audited customer telemetry across 142 production deployments.",
      target_audience: "Enterprise & Growth Leaders",
      brand_tier: "enterprise",
      years_operating: 6,
      link_count: 5,
      logo_count: 10,
      step_count: 4,
      case_count: 8,
      review_count: 14,
      team_size: 18,
      faq_count: 12,
      pricing_model: "subscription",
      checks: {
        enterprise: true,
        has_svg_logo: true,
        stock_allowed: true,
        has_certifications: true,
        compliance_required: true,
        bento_hero: true,
        has_mockup: true,
        has_proof_stats: true,
        has_analytics_data: true,
        has_named_quotes: true,
        direct_calendar: true,
        has_billing_toggle: true,
        has_matrix: true,
        has_sla: true,
        has_enterprise_tier: true,
        has_newsletter: true,
        has_departments: true,
        has_categories: true,
        feat_booking: true,
        feat_analytics_crm: true,
      },
    },
    multisite: {
      page_id: "home",
      sitemapPages: ["home", "about", "services", "pricing", "case_studies"],
      customSitemapPages: ["Individual Service Detail Pages"],
      project_name: "Northstar Cloud Ops",
      legal_name: "Northstar Infrastructure Corp.",
      tagline: "Mission-critical cloud migration and zero-downtime SRE retainers.",
      existing_url: "https://northstarops.example.com",
      industry: "b2b saas analytics",
      business_model: "B2B Services / Agency",
      primary_goal: "Qualified Sales Leads & Demos",
      primary_device: "Desktop-Heavy (Work / Procurement)",
      buying_cycle: "Research-Driven / Multiple Stakeholders",
      discovery_confidence: "Verified Research",
      buyer_pain_points: "CTOs hesitate to outsource production Kubernetes workloads without audited uptime proof and SLA clarity.",
      competitor_links: "1) Rackspace (clear SLA proof, outdated visuals)\n2) Contino (strong enterprise case studies, slow navigation)",
      reference_urls: "Linear & Vercel docs — sharp contrast, tabular metrics, crisp typography.",
      brand_colors_note: "Deep Slate + High-Contrast Cobalt accent",
      hero_direction: "bento",
      dark_mode_support: "Both Light & Dark Modes",
      wcag_target: "WCAG 2.2 AA",
      reduced_motion: "Subtle Micro-Interactions (150ms, Reduced Motion Safe)",
      copy_owner: "Hybrid (Client Drafts + Studio Messaging)",
      content_readiness: "Partial Drafts / Existing Site",
      core_usp: "Dedicated SRE pods with 99.99% contracted uptime and fixed quarterly deliverables.",
      avoid_claims: "No buzzwords, no anonymous testimonials",
      site_type: "Marketing Website + Headless CMS",
      cms_preference: "Headless (Sanity / Contentful)",
      target_launch: "10 weeks from kickoff",
      budget_tier: "$35k–$60k Full Multi-Page Build",
      decision_maker: "VP Engineering & Head of Marketing",
      hosting_status: "Managed Edge Cloud (Vercel / Cloudflare / Pages)",
      custom_page_names: "Security & SOC 2 Trust Overview",
      priority_p0_notes: "Home, About, Services, Pricing, Case Studies + Cal.com executive booking + CRM routing.",
      priority_p2_notes: "Careers portal integration & self-serve architecture grader.",
      style: "Swiss Modern Technical",
      stack: "nextjs",
      search_keywords: "enterprise dashboard accessibility compliance",
      evidence_note: "Audited 2025-2026 SRE retainer ledger across 48 enterprise cloud migrations.",
      target_audience: "developers/ctos",
      brand_tier: "enterprise",
      years_operating: 9,
      link_count: 6,
      logo_count: 12,
      step_count: 4,
      case_count: 12,
      review_count: 18,
      team_size: 28,
      faq_count: 12,
      pricing_model: "subscription",
      checks: {
        enterprise: true,
        high_competition: true,
        has_svg_logo: true,
        stock_allowed: true,
        has_certifications: true,
        compliance_required: true,
        has_proof_stats: true,
        has_analytics_data: true,
        has_named_quotes: true,
        bento_hero: true,
        has_mockup: true,
        mega_menu: true,
        has_departments: true,
        has_categories: true,
        direct_calendar: true,
        has_billing_toggle: true,
        has_matrix: true,
        has_sla: true,
        direct_rfq_form: true,
        has_guarantee: true,
        has_enterprise_tier: true,
        has_newsletter: true,
        timeline_horizontal: true,
        has_manifesto: true,
        arch_layered: true,
        workflow_phases: true,
        multi_persona: true,
        data_dense: true,
        feat_booking: true,
        feat_analytics_crm: true,
      },
    },
    agency: {
      page_id: "about",
      sitemapPages: ["about"],
      customSitemapPages: ["Portfolio Showcase"],
      project_name: "Atelier Nord",
      legal_name: "Atelier Nord Partners ApS",
      tagline: "Digital architecture for cultural institutions and category leaders.",
      industry: "creative agency design studio",
      business_model: "B2B Services / Agency",
      primary_goal: "Brand Credibility & Positioning",
      primary_device: "Desktop & Mobile Balanced",
      buying_cycle: "Consultative Call (1–4 Weeks)",
      discovery_confidence: "Partial Discovery",
      hero_direction: "mockup",
      style: "Editorial Minimalist Luxury",
      stack: "nextjs",
      search_keywords: "editorial typography portfolio performance",
      evidence_note: "2019-2026 verified studio client engagements across 28 launches.",
      target_audience: "B2B Marketing and Sales Leaders",
      brand_tier: "boutique",
      years_operating: 7,
      link_count: 4,
      logo_count: 8,
      step_count: 4,
      case_count: 10,
      review_count: 12,
      team_size: 9,
      faq_count: 6,
      pricing_model: "subscription",
      checks: {
        founder_led: true,
        has_svg_logo: true,
        has_mockup: true,
        has_manifesto: true,
        has_office_photos: true,
        culture_focus: true,
        direct_calendar: true,
        is_productized: true,
        has_vip_quote: true,
        feat_booking: true,
      },
    },
    growth: {
      page_id: "services",
      sitemapPages: ["services"],
      customSitemapPages: ["Individual Service Detail Pages"],
      project_name: "SyncHub Automation",
      legal_name: "SyncHub Labs Inc.",
      tagline: "Connect product telemetry and revenue workflows in under 5 minutes.",
      industry: "productivity tool collaboration",
      business_model: "B2B SaaS",
      primary_goal: "Direct Self-Serve Signups / Sales",
      primary_device: "Desktop & Mobile Balanced",
      buying_cycle: "Fast Self-Serve / Impulse",
      discovery_confidence: "Verified Research",
      hero_direction: "devices",
      style: "Fresh Modern Clean",
      stack: "react",
      search_keywords: "workflow integration form speed",
      evidence_note: "Measured across 3,400 active workspaces in Q4 2026.",
      target_audience: "Founders & Product Teams",
      brand_tier: "standard",
      years_operating: 4,
      link_count: 5,
      logo_count: 12,
      step_count: 4,
      case_count: 6,
      review_count: 24,
      team_size: 32,
      faq_count: 10,
      pricing_model: "usage_based",
      checks: {
        has_svg_logo: true,
        stock_allowed: true,
        has_app_mockups: true,
        cro_split: true,
        has_mockup: true,
        has_portal: true,
        has_proof_stats: true,
        arch_layered: true,
        workflow_phases: true,
        searchable_integrations: true,
        multi_persona: true,
        has_partners: true,
        has_categories: true,
        feat_auth: true,
        feat_analytics_crm: true,
      },
    },
    pricing: {
      page_id: "pricing",
      sitemapPages: ["pricing"],
      customSitemapPages: [],
      project_name: "VaultSec Enterprise",
      legal_name: "VaultSec Security Technologies",
      tagline: "Zero-trust compliance automation with audited procurement SLAs.",
      industry: "cybersecurity platform fintech",
      business_model: "B2B SaaS",
      primary_goal: "Qualified Sales Leads & Demos",
      primary_device: "Desktop-Heavy (Work / Procurement)",
      buying_cycle: "Research-Driven / Multiple Stakeholders",
      discovery_confidence: "Verified Research",
      hero_direction: "editorial",
      style: "Trustworthy Corporate Clean",
      stack: "shadcn",
      search_keywords: "pricing comparison table form security",
      evidence_note: "SOC 2 Type II audited SLA uptime benchmark (99.98%, Jan-Nov 2026).",
      target_audience: "developers/ctos",
      brand_tier: "enterprise",
      years_operating: 8,
      link_count: 5,
      logo_count: 10,
      step_count: 4,
      case_count: 6,
      review_count: 12,
      team_size: 40,
      faq_count: 15,
      pricing_model: "subscription",
      checks: {
        enterprise: true,
        has_svg_logo: true,
        compliance_required: true,
        has_certifications: true,
        has_billing_toggle: true,
        has_matrix: true,
        matrix_tabs: true,
        has_addons: true,
        has_sla: true,
        direct_rfq_form: true,
        has_guarantee: true,
        has_roi: true,
        mobile_drawer: true,
        has_enterprise_tier: true,
        has_categories: true,
        feat_booking: true,
        feat_analytics_crm: true,
      },
    },
  };

  let bundle = null;
  let lastCompiled = null;

  // ---------- BM25 Search Engine (mirrors core.py) ----------
  class BM25 {
    constructor(k1 = 1.5, b = 0.75) {
      this.k1 = k1;
      this.b = b;
      this.corpus = [];
      this.docLengths = [];
      this.avgdl = 0;
      this.idf = new Map();
      this.N = 0;
    }

    tokenize(text) {
      return String(text || "")
        .toLowerCase()
        .replace(/[^\w\s]/g, " ")
        .split(/\s+/)
        .filter((w) => w.length >= 2);
    }

    fit(documents) {
      const docFreqs = new Map();
      this.corpus = documents.map((d) => this.tokenize(d));
      this.N = this.corpus.length;
      if (!this.N) return;
      this.docLengths = this.corpus.map((d) => d.length);
      this.avgdl = this.docLengths.reduce((a, b) => a + b, 0) / this.N;

      for (const doc of this.corpus) {
        const seen = new Set(doc);
        for (const word of seen) {
          docFreqs.set(word, (docFreqs.get(word) || 0) + 1);
        }
      }
      for (const [word, freq] of docFreqs.entries()) {
        this.idf.set(word, Math.log((this.N - freq + 0.5) / (freq + 0.5) + 1));
      }
    }

    score(query) {
      if (!this.avgdl) return this.corpus.map((_, idx) => [idx, 0]);
      const qTokens = this.tokenize(query);
      const out = [];
      for (let idx = 0; idx < this.corpus.length; idx++) {
        const doc = this.corpus[idx];
        const docLen = this.docLengths[idx];
        const tfMap = new Map();
        for (const w of doc) tfMap.set(w, (tfMap.get(w) || 0) + 1);

        let total = 0;
        for (const tok of qTokens) {
          const idf = this.idf.get(tok);
          if (idf !== undefined) {
            const tf = tfMap.get(tok) || 0;
            const num = tf * (this.k1 + 1);
            const den = tf + this.k1 * (1 - this.b + (this.b * docLen) / this.avgdl);
            total += (idf * num) / den;
          }
        }
        out.push([idx, total]);
      }
      return out.sort((a, b) => b[1] - a[1]);
    }
  }

  function searchRows(rows, searchCols, query, maxResults = 3) {
    if (!rows || !rows.length || !String(query || "").trim()) return [];
    const docs = rows.map((r) => searchCols.map((c) => r[c] || "").join(" "));
    const bm25 = new BM25();
    bm25.fit(docs);
    const ranked = bm25.score(query);
    const results = [];
    for (const [idx, sc] of ranked.slice(0, maxResults)) {
      if (sc > 0) results.push(rows[idx]);
    }
    return results;
  }

  function searchDomain(query, domain, maxResults = 3) {
    const rows = bundle.domains[domain] || [];
    const cols = DOMAIN_SEARCH_COLS[domain] || Object.keys(rows[0] || {});
    return searchRows(rows, cols, query, maxResults);
  }

  function searchStack(query, stackName, maxResults = 6) {
    const rows = bundle.stacks[stackName] || [];
    return searchRows(rows, STACK_SEARCH_COLS, query, maxResults);
  }

  // ---------- Intent, Contrast & Token Derivation (mirrors generate_section_prompt.py) ----------
  function normalizeIntent(rawStyle) {
    const lowered = String(rawStyle || "").toLowerCase();
    const tokens = lowered.match(/[a-z0-9-]+/g) || [];
    const expanded = [];
    for (const [vague, syns] of Object.entries(INTENT_VOCABULARY)) {
      const re = new RegExp(`\\b${vague}\\b`);
      if (re.test(lowered)) {
        for (const syn of syns) {
          if (!tokens.includes(syn) && !expanded.includes(syn)) expanded.push(syn);
        }
      }
    }
    return expanded.length ? [...tokens, ...expanded].join(" ") : rawStyle;
  }

  function relativeLuminance(hexColor) {
    const h = hexColor.replace("#", "");
    const chans = [0, 2, 4].map((i) => parseInt(h.slice(i, i + 2), 16) / 255);
    const lin = chans.map((c) => (c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4)));
    return 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2];
  }

  function contrastRatio(c1, c2) {
    const l1 = relativeLuminance(c1);
    const l2 = relativeLuminance(c2);
    return (Math.max(l1, l2) + 0.05) / (Math.min(l1, l2) + 0.05);
  }

  function deriveSurfaceTokens(colorRow = {}) {
    const hexRe = /^#[0-9A-Fa-f]{6}$/;
    let bgHex = (colorRow["Background (Hex)"] || "#0B0F17").trim();
    let ctaHex = (colorRow["CTA (Hex)"] || "#2563EB").trim();
    let textHex = (colorRow["Text (Hex)"] || "#F8FAFC").trim();
    let borderHex = (colorRow["Border (Hex)"] || "#1E293B").trim();

    if (!hexRe.test(bgHex)) bgHex = "#0B0F17";
    if (!hexRe.test(textHex)) textHex = "#F8FAFC";
    if (!hexRe.test(ctaHex)) ctaHex = "#2563EB";
    if (!hexRe.test(borderHex)) borderHex = "#1E293B";

    const isLight = relativeLuminance(bgHex) > 0.5;
    let cardSurface;
    let textSecondary;

    if (isLight) {
      cardSurface = bgHex.toUpperCase() !== "#FFFFFF" ? "#FFFFFF" : "#F8FAFC";
      textSecondary = "#475569";
      if (contrastRatio(textSecondary, bgHex) < 4.5 || contrastRatio(textSecondary, cardSurface) < 4.5) {
        textSecondary = "#334155";
      }
      if (contrastRatio(textSecondary, bgHex) < 4.5 || contrastRatio(textSecondary, cardSurface) < 4.5) {
        textSecondary = textHex;
      }
    } else {
      cardSurface = bgHex.toUpperCase() !== "#151C28" ? "#151C28" : "#1E293B";
      textSecondary = "#94A3B8";
      if (contrastRatio(textSecondary, bgHex) < 4.5 || contrastRatio(textSecondary, cardSurface) < 4.5) {
        textSecondary = "#CBD5E1";
      }
      if (contrastRatio(textSecondary, bgHex) < 4.5 || contrastRatio(textSecondary, cardSurface) < 4.5) {
        textSecondary = textHex;
      }
    }

    const ctaText = contrastRatio("#FFFFFF", ctaHex) >= contrastRatio("#020617", ctaHex) ? "#FFFFFF" : "#020617";

    return {
      background: bgHex,
      card_surface: cardSurface,
      cta: ctaHex,
      cta_text: ctaText,
      text_primary: textHex,
      text_secondary: textSecondary,
      border_subtle: borderHex,
      primary_brand: (colorRow["Primary (Hex)"] || ctaHex).trim(),
      secondary_brand: (colorRow["Secondary (Hex)"] || borderHex).trim(),
      palette_source: colorRow["Product Type"] || "Default Fallback",
    };
  }

  // ---------- Design System Reasoning (mirrors design_system.py) ----------
  function findReasoningRule(category) {
    const catLower = String(category || "").toLowerCase().trim();
    if (!catLower || catLower === "general") return {};

    for (const r of bundle.reasoning) {
      if ((r.UI_Category || "").toLowerCase().trim() === catLower) return r;
    }
    for (const r of bundle.reasoning) {
      const uiCat = (r.UI_Category || "").toLowerCase().trim();
      if (uiCat && new RegExp(`(?<![a-z0-9])${uiCat.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")}(?![a-z0-9])`).test(catLower)) {
        return r;
      }
    }
    const generic = new Set(["app", "tool", "platform", "service", "services", "system", "hub", "portal", "web", "page", "store", "shop", "client"]);
    const catToks = new Set((catLower.match(/[a-z0-9]{3,}/g) || []).filter((t) => !generic.has(t)));
    let best = {};
    let bestHits = 0;
    for (const r of bundle.reasoning) {
      const ruleToks = ((r.UI_Category || "").toLowerCase().match(/[a-z0-9]{3,}/g) || []).filter((t) => !generic.has(t));
      const hits = ruleToks.filter((t) => catToks.has(t)).length;
      if (hits > bestHits) {
        bestHits = hits;
        best = r;
      }
    }
    return best;
  }

  function selectBestStyle(results, priorityList) {
    if (!results.length) return {};
    if (!priorityList || !priorityList.length) return results[0];
    for (const pr of priorityList) {
      const pl = pr.toLowerCase().trim();
      const exact = results.find((r) => (r["Style Category"] || "").toLowerCase().trim() === pl);
      if (exact) return exact;
    }
    for (const pr of priorityList) {
      const pl = pr.toLowerCase().trim();
      const sub = results.find((r) => {
        const sn = (r["Style Category"] || "").toLowerCase().trim();
        return pl && sn && (sn.includes(pl) || pl.includes(sn));
      });
      if (sub) return sub;
    }
    return results[0];
  }

  function buildDesignSystem(query) {
    const productResults = searchDomain(query, "product", 1);
    const productRow = productResults[0] || {};
    const category = productRow["Product Type"] || "General";
    const rule = findReasoningRule(category);

    const stylePriority = rule.Style_Priority
      ? rule.Style_Priority.split("+").map((s) => s.trim()).filter(Boolean)
      : ["Minimalism", "Flat Design"];

    const styleMatches = searchDomain(`${query} ${stylePriority.slice(0, 2).join(" ")}`, "style", 3);
    const colorMatches = searchDomain(query, "color", 2);
    const typoMatches = searchDomain(query, "typography", 2);
    const landingMatches = searchDomain(query, "landing", 2);
    const chartMatches = searchDomain(query, "chart", 2);
    const iconMatches = searchDomain(query, "icons", 3);
    const bestStyle = selectBestStyle(styleMatches, stylePriority);
    const promptMatches = searchDomain(bestStyle["Style Category"] || query, "prompt", 1);

    let decisionRules = {};
    try {
      decisionRules = rule.Decision_Rules ? JSON.parse(rule.Decision_Rules) : {};
    } catch {
      decisionRules = {};
    }

    const mappingEntry = productRow.product_slug ? bundle.productMapping[productRow.product_slug] : null;

    return {
      category,
      productRow,
      mappingEntry,
      reasoning: {
        pattern: rule.Recommended_Pattern || "Hero + Features + CTA",
        stylePriority,
        colorMood: rule.Color_Mood || "Professional",
        typographyMood: rule.Typography_Mood || "Clean",
        keyEffects: rule.Key_Effects || "Subtle hover transitions",
        antiPatterns: rule.Anti_Patterns || "",
        decisionRules,
        severity: rule.Severity || "MEDIUM",
      },
      bestStyle,
      bestColor: colorMatches[0] || {},
      bestTypography: typoMatches[0] || {},
      bestLanding: landingMatches[0] || {},
      promptMatch: promptMatches[0] || {},
      chartMatches,
      iconMatches,
    };
  }

  // ---------- Section Archetype Selector (100% parity with generate_section_prompt.py) ----------
  function getArchetype(archetypes, archetypeId, sectionId, warnings) {
    const found = archetypes.find((a) => a.archetype_id === archetypeId);
    if (found) return found;
    warnings.push(`[FALLBACK] section=${sectionId}: archetype '${archetypeId}' not found. Using '${archetypes[0].archetype_id}'.`);
    return archetypes[0];
  }

  function selectArchetype(sectionData, p, warnings) {
    const archetypes = sectionData.archetypes || [];
    const secId = sectionData.section_id || "";
    if (!archetypes.length) {
      warnings.push(`[ERROR] section=${secId} has 0 archetypes`);
      return { archetype_id: "MISSING", name: "MISSING", best_for: "", layout_structure: "", typography_specs: "", key_components: "", responsive_behavior: "", accessibility: "", anti_slop_rules: "" };
    }
    const pick = (aid) => getArchetype(archetypes, aid, secId, warnings);
    const s = String(p.style || "").toLowerCase();

    if (secId === "navbar") {
      const linkCount = p.link_count ?? 5;
      if (p.mega_menu) return pick("nav-03");
      if (p.lead_header || p.primary_goal === "phone/lead" || p.conversion_focus === "ultra-high") return pick("nav-04");
      if (s.includes("editorial")) return pick("nav-05");
      if (p.has_portal) return pick("nav-06");
      return linkCount <= 5 ? pick("nav-01") : pick("nav-02");
    }
    if (secId === "hero") {
      if (p.has_video) return pick("hero-03");
      if (p.lead_magnet) return pick("hero-04");
      if (p.has_3d) return pick("hero-09");
      if (p.bento_hero || s.includes("bento") || p.has_multiple_features) return pick("hero-05");
      if (p.has_app_mockups) return pick("hero-06");
      if (p.cro_split || p.focus === "transformation") return pick("hero-10");
      if ((s.includes("editorial") || s.includes("swiss")) && p.brand_tier === "luxury") return pick("hero-08");
      if (s.includes("minimalist") || s.includes("editorial")) return pick("hero-02");
      if (p.has_mockup !== false) return pick("hero-01");
      return pick("hero-07");
    }
    if (secId === "trusted_by") {
      const logoCount = p.logo_count ?? 8;
      if (p.compliance_required) return pick("tb-06");
      if (p.has_press) return pick("tb-04");
      if (p.has_case_studies) return pick("tb-05");
      if ((p.has_metrics || p.has_proof_stats) && logoCount < 8) return pick("tb-03");
      return logoCount >= 8 ? pick("tb-01") : pick("tb-02");
    }
    if (secId === "about") {
      if (p.has_video) return pick("abt-06");
      if (p.founder_led) return pick("abt-01");
      if ((p.years_operating ?? 0) >= 5) return pick("abt-03");
      if (p.has_office_photos) return pick("abt-04");
      if (s.includes("editorial") || s.includes("minimalist")) return pick("abt-05");
      return pick("abt-02");
    }
    if (secId === "services") {
      if (p.target_audience === "developers/ctos") return pick("srv-08");
      if (p.enterprise) return pick("srv-07");
      if (p.is_productized) return pick("srv-06");
      if (p.mobile_heavy) return pick("srv-05");
      if (p.wants_tabs) return pick("srv-04");
      if (s.includes("creative") || s.includes("editorial")) return pick("srv-02");
      if (p.has_flagship_service) return pick("srv-03");
      return pick("srv-01");
    }
    if (secId === "why_choose_us") {
      if (p.has_founder_video) return pick("wcu-05");
      if (p.has_certifications) return pick("wcu-06");
      if (p.enterprise) return pick("wcu-04");
      if (p.high_competition) return pick("wcu-02");
      if (p.has_proof_stats) return pick("wcu-03");
      return pick("wcu-01");
    }
    if (secId === "how_we_work") {
      const stepCount = p.step_count ?? 4;
      if (p.is_cyclical) return pick("hww-09");
      if (p.has_rich_media) return pick("hww-10");
      if (p.has_cinematic_photos) return pick("hww-11");
      if (s.includes("creative") && p.immersive) return pick("hww-07");
      if (p.is_non_linear) return pick("hww-05");
      if (p.has_step_images) return pick("hww-06");
      if (stepCount > 6) return pick("hww-08");
      if (stepCount >= 5) return pick("hww-02");
      if (s.includes("bento") || s.includes("contemporary")) return pick("hww-12");
      if (stepCount <= 4 && p.complexity === "low") return pick("hww-01");
      if (stepCount === 4 && (s.includes("corporate") || s.includes("clean"))) return pick("hww-03");
      return pick("hww-04");
    }
    if (secId === "portfolio") {
      const caseCount = p.case_count ?? 6;
      if (s.includes("avant-garde") || s.includes("editorial")) return pick("port-08");
      if (caseCount >= 10) return pick("port-04");
      if (p.has_metrics) return pick("port-02");
      if (p.enterprise) return pick("port-03");
      if (p.focus === "responsive_web") return pick("port-06");
      if (p.analytical) return pick("port-07");
      if (caseCount <= 5) return pick("port-05");
      return pick("port-01");
    }
    if (secId === "testimonials") {
      const reviews = p.review_count ?? 5;
      if (p.has_video_reviews) return pick("tst-03");
      if (p.has_audio) return pick("tst-06");
      if (p.has_analytics_data) return pick("tst-05");
      if (p.social_proof_type === "social_posts") return pick("tst-04");
      if (p.has_vip_quote) return pick("tst-02");
      if (p.wants_compact) return pick("tst-08");
      if (reviews > 20) return pick("tst-07");
      return pick("tst-01");
    }
    if (secId === "results_metrics") {
      if (p.has_live_data) return pick("res-05");
      if (p.has_before_after) return pick("res-02");
      if (p.has_analytics_data) return pick("res-03");
      if ((p.years_operating ?? 0) >= 5) return pick("res-04");
      if (p.enterprise && p.has_named_quotes) return pick("res-06");
      return pick("res-01");
    }
    if (secId === "pricing") {
      if (p.is_productized) return pick("prc-04");
      if (p.custom_quotes) return pick("prc-06");
      if (p.has_annual_discount || p.has_billing_toggle) return pick("prc-02");
      if (p.pricing_model === "usage_based" || p.pricing_model === "usage/scope_based") return pick("prc-03");
      if (p.enterprise && p.feature_density === "high") return pick("prc-05");
      return pick("prc-01");
    }
    if (secId === "team") {
      const teamSize = p.team_size ?? 6;
      if (teamSize >= 30) return pick("team-06");
      if (teamSize >= 15 && p.has_departments) return pick("team-04");
      if (p.has_editorial_photos) return pick("team-05");
      if (p.culture_focus) return pick("team-03");
      if (p.founder_led) return pick("team-02");
      return pick("team-01");
    }
    if (secId === "faq") {
      const faqCount = p.faq_count ?? 6;
      if (faqCount >= 15) return pick("faq-04");
      if (faqCount >= 10 && p.has_categories) return pick("faq-02");
      if (p.goal === "consultation") return pick("faq-05");
      if (p.wants_compact) return pick("faq-06");
      if (faqCount <= 6 && p.answers_short) return pick("faq-03");
      return pick("faq-01");
    }
    if (secId === "final_cta") {
      if (p.direct_calendar) return pick("cta-02");
      if (p.lead_magnet) return pick("cta-03");
      if (p.needs_qualification) return pick("cta-04");
      if (p.founder_led && p.brand_tier === "boutique") return pick("cta-05");
      if (p.has_enterprise_tier) return pick("cta-06");
      return pick("cta-01");
    }
    if (secId === "footer") {
      if (p.has_mobile_app) return pick("ftr-06");
      if (p.has_multiple_offices) return pick("ftr-05");
      if (p.has_newsletter) return pick("ftr-03");
      if (s.includes("editorial") || s.includes("luxury")) return pick("ftr-02");
      if (p.single_page) return pick("ftr-04");
      return pick("ftr-01");
    }
    if (secId === "pricing_hero") {
      if (p.pricing_model === "usage_based" || p.pricing_model === "usage/scope_based") return pick("phero-03");
      if (p.has_roi || p.enterprise) return pick("phero-02");
      return pick("phero-01");
    }
    if (secId === "pricing_comparison_matrix") {
      if (p.matrix_tabs) return pick("pmat-02");
      if (p.minimal_diff) return pick("pmat-03");
      return pick("pmat-01");
    }
    if (secId === "pricing_addons") {
      return p.addon_compact ? pick("padd-02") : pick("padd-01");
    }
    if (secId === "pricing_enterprise_sla") {
      return p.direct_rfq_form ? pick("psla-02") : pick("psla-01");
    }
    if (secId === "pricing_guarantee_bar") {
      return p.mobile_drawer ? pick("pbar-02") : pick("pbar-01");
    }
    if (secId === "about_timeline") {
      if (p.timeline_horizontal) return pick("time-02");
      if (s.includes("minimalist") || s.includes("editorial")) return pick("time-03");
      return pick("time-01");
    }
    if (secId === "about_values") {
      if (p.has_manifesto || p.founder_led) return pick("val-02");
      if (s.includes("bento") || s.includes("contemporary")) return pick("val-03");
      return pick("val-01");
    }
    if (secId === "about_culture_gallery") {
      if (p.distributed_team) return pick("cult-02");
      if (p.culture_focus) return pick("cult-03");
      return pick("cult-01");
    }
    if (secId === "about_leadership_board") {
      return p.has_investors ? pick("lead-02") : pick("lead-01");
    }
    if (secId === "service_architecture") {
      if (p.arch_layered) return pick("arch-02");
      if (p.workflow_phases || p.service_model === "consulting") return pick("arch-03");
      return pick("arch-01");
    }
    if (secId === "service_deliverables_matrix") {
      if (p.has_sla) return pick("deliv-02");
      if (p.interactive_scope) return pick("deliv-03");
      return pick("deliv-01");
    }
    if (secId === "service_tech_stack") {
      if (p.has_partners) return pick("stack-02");
      if (p.searchable_integrations) return pick("stack-03");
      return pick("stack-01");
    }
    if (secId === "service_use_cases") {
      return p.multi_persona ? pick("use-02") : pick("use-01");
    }
    if (secId === "contact_intake_form") {
      if (p.direct_calendar) return pick("cform-03");
      if (p.multi_step) return pick("cform-02");
      return pick("cform-01");
    }
    if (secId === "contact_location_map") {
      return p.map_view ? pick("cmap-02") : pick("cmap-01");
    }
    if (secId === "contact_sla_banner") {
      return p.has_support_route ? pick("csla-02") : pick("csla-01");
    }
    if (secId === "case_study_hero_highlight") {
      if (p.has_video || p.immersive) return pick("csh-02");
      if (s.includes("minimalist") || s.includes("editorial")) return pick("csh-03");
      return pick("csh-01");
    }
    if (secId === "case_study_filter_hub") {
      if (p.data_dense || p.ledger_view) return pick("csf-03");
      if (s.includes("creative") || s.includes("editorial")) return pick("csf-02");
      return pick("csf-01");
    }
    if (secId === "case_study_client_quote_strip") {
      return p.has_vip_quote ? pick("csq-02") : pick("csq-01");
    }
    if (secId === "blog_featured_editorial") {
      if (p.has_trending || p.post_density === "high") return pick("bfeat-02");
      if (s.includes("minimalist") || s.includes("longform")) return pick("bfeat-03");
      return pick("bfeat-01");
    }
    if (secId === "blog_topic_filter_feed") {
      if (p.feed_horizontal) return pick("bfeed-02");
      if (p.feed_archive) return pick("bfeed-03");
      return pick("bfeed-01");
    }
    if (secId === "blog_newsletter_capture") {
      return p.split_digest ? pick("bnews-02") : pick("bnews-01");
    }
    if (secId === "careers_perks") {
      if (p.remote_stipend) return pick("perk-03");
      if (p.salary_transparent) return pick("perk-02");
      if (p.parental_wellness) return pick("perk-04");
      return pick("perk-01");
    }
    if (secId === "careers_jobs") {
      if (p.accordion_jobs) return pick("jobs-02");
      if (p.interview_pipeline) return pick("jobs-03");
      return pick("jobs-01");
    }
    if (secId === "legal_doc") {
      if (p.multi_policy) return pick("leg-02");
      if (p.has_version_selector) return pick("leg-03");
      return pick("leg-01");
    }

    const fb = SECTION_FALLBACKS[secId] || archetypes[0].archetype_id;
    warnings.push(`[FALLBACK] Unknown section_id='${secId}', using '${fb}'.`);
    return pick(fb);
  }

  // ---------- Compiler Pipeline (Single & Multi-Page) ----------
  function compileAll(projectInfo, extra, discovery) {
    const warnings = [];
    const normalized = normalizeIntent(projectInfo.style);
    const fullQuery = `${projectInfo.industry} ${normalized} ${extra.searchKeywords || ""}`.trim();

    const colorRow = searchDomain(`${projectInfo.industry} ${normalized}`, "color", 1)[0] || {};
    const tokens = deriveSurfaceTokens(colorRow);
    const typoRow = searchDomain(`${normalized} tech`, "typography", 1)[0] || {};
    const headingFont = typoRow["Heading Font"] || "Space Grotesk";
    const bodyFont = typoRow["Body Font"] || "Inter";
    const headingSpec = HIGH_CONTRAST_SERIFS.has(headingFont.toLowerCase())
      ? `\`${headingFont}\` — 600–700 weight max, tracking >= -0.015em (avoid 800/900 or 300 hairlines; use body/mono \`tabular-nums\` for KPI numerals)`
      : `\`${headingFont}\` — Bold (600–700), tracking-tight`;

    const ds = buildDesignSystem(fullQuery);
    const stackGuidelines = searchStack(`${normalized} ${extra.searchKeywords || "accessibility layout"}`, extra.stack, 8);
    const uxGuidelines = searchDomain(`${normalized} ${extra.searchKeywords || "accessibility contrast"}`, "ux", 6);
    const webGuidelines = searchDomain(`aria focus semantic form ${extra.searchKeywords || ""}`, "web", 5);
    const reactGuidelines =
      extra.stack === "react" || extra.stack === "nextjs" || extra.stack === "shadcn"
        ? searchDomain(`rerender memo bundle ${extra.searchKeywords || ""}`, "react", 5)
        : [];

    const sectionMap = new Map(bundle.sectionArchetypes.map((s) => [s.section_id, s]));
    const pageList = bundle.pageTemplates.pages || [];
    const selectedPageIds = discovery && Array.isArray(discovery.sitemap_pages) && discovery.sitemap_pages.length
      ? discovery.sitemap_pages
      : [projectInfo.page_id || "home"];

    const compiledPages = selectedPageIds.map((pid) => {
      const pMeta = pageList.find((p) => p.page_id === pid);
      const targetSections = pMeta
        ? pMeta.default_section_flow.map((sid) => sectionMap.get(sid)).filter(Boolean)
        : bundle.sectionArchetypes;
      const scopedInfo = { ...projectInfo, page_id: pid };
      const sections = targetSections.map((sec, idx) => ({
        index: idx + 1,
        section_id: sec.section_id,
        section_name: sec.section_name,
        chosen: selectArchetype(sec, scopedInfo, warnings),
      }));
      return {
        page_id: pid,
        page_name: pMeta ? pMeta.name : pid,
        sections,
      };
    });

    const primaryPageMeta = pageList.find((p) => p.page_id === projectInfo.page_id) || pageList.find((p) => p.page_id === selectedPageIds[0]);
    const compiledSections = compiledPages.flatMap((pg) => pg.sections);

    const customScopePages = [
      ...((discovery && discovery.custom_sitemap_pages) || []),
      ...String((discovery && discovery.custom_page_names) || "")
        .split(",")
        .map((s) => s.trim())
        .filter(Boolean),
    ];

    const researchGaps = [];
    if (discovery) {
      if (!discovery.competitor_links) researchGaps.push("Competitor benchmark links & likes/dislikes not yet captured.");
      if (!discovery.reference_urls) researchGaps.push("Visual inspiration links & first-5-second impression notes are open.");
      if (!discovery.core_usp) researchGaps.push("Primary headline direction / core USP should be sharpened with client.");
      if (!discovery.decision_maker) researchGaps.push("Final decision maker & sign-off authority needs confirmation.");
      if (discovery.discovery_confidence === "Assumptions Only") researchGaps.push("Discovery inputs flagged as Assumptions Only — validate with client analytics/interviews before wireframe lock.");
      if (projectInfo.has_brand_guidelines && !discovery.brand_colors_note) researchGaps.push("Client indicated existing brand guidelines — collect exact HEX/font files before build.");
      if (!extra.evidenceNote) researchGaps.push("SLOP-003 Warning: Verified metrics evidence citation is blank — keep proof numbers omitted until source URL/date is provided.");
    }

    const contrastChecks = [
      { label: "Text Primary / Bg", ratio: contrastRatio(tokens.text_primary, tokens.background) },
      { label: "Text Primary / Card", ratio: contrastRatio(tokens.text_primary, tokens.card_surface) },
      { label: "Text Secondary / Bg", ratio: contrastRatio(tokens.text_secondary, tokens.background) },
      { label: "Text Secondary / Card", ratio: contrastRatio(tokens.text_secondary, tokens.card_surface) },
      { label: "CTA Text / CTA", ratio: contrastRatio(tokens.cta_text, tokens.cta) },
    ];

    const md = [];
    md.push("# Master Production-Grade Client Discovery & UI/UX Blueprint");
    md.push(`**Project:** ${projectInfo.project_name}${discovery && discovery.legal_name ? ` (${discovery.legal_name})` : ""}`);
    if (discovery && discovery.tagline) md.push(`**Positioning:** ${discovery.tagline}`);
    md.push(`**Sitemap Blueprint Pages (${compiledPages.length}):** ${compiledPages.map((p) => `${p.page_name} (\`${p.page_id}\`: ${p.sections.length}s)`).join(", ")}`);
    if (customScopePages.length) md.push(`**Additional Custom Scope Pages:** ${customScopePages.join(", ")}`);
    md.push(`**Primary Route Fallback (--page):** ${primaryPageMeta ? primaryPageMeta.name : projectInfo.page_id} (\`${projectInfo.page_id}\`)`);
    md.push(`**Style Archetype:** ${projectInfo.style}`);
    md.push(`**Industry / Category:** ${ds.category} (\`${ds.productRow.product_slug || "general"}\`)`);
    md.push(`**Target Stack:** \`${extra.stack}\` | **CMS:** ${discovery ? discovery.cms_preference : "None"}`);
    md.push(`**Target Audience:** ${projectInfo.target_audience}`);
    md.push(`**Total Compiled Sections:** ${compiledSections.length} sections across ${compiledPages.length} route(s)`);
    if (extra.evidenceNote) md.push(`**Verified Evidence Basis:** ${extra.evidenceNote}`);
    if (discovery) md.push(`**Launch Target / Budget:** ${discovery.target_launch || "TBD"} | ${discovery.budget_tier || "TBD"} | Confidence: ${discovery.discovery_confidence}`);
    md.push("**Compliance:** WCAG 2.2 AA | Anti-Slop Gates Enabled\n");

    if (discovery) {
      md.push("---");
      md.push("## 0. Client Strategy, Audience & Scope Summary");
      md.push(`- **Business Model & Goal:** ${discovery.business_model} — Objective: ${discovery.primary_goal}`);
      md.push(`- **Buyer Profile & Device:** ${projectInfo.target_audience} | ${discovery.primary_device} | ${discovery.buying_cycle}`);
      if (discovery.buyer_pain_points) md.push(`- **Buyer Objections:** ${discovery.buyer_pain_points}`);
      if (discovery.core_usp) md.push(`- **Core Value Proposition:** ${discovery.core_usp}`);
      if (discovery.avoid_claims) md.push(`- **Messaging Guardrails (Avoid):** ${discovery.avoid_claims}`);
      md.push(`- **Copy & Assets:** ${discovery.copy_owner} (${discovery.content_readiness}) | SVG Logo: ${discovery.has_svg_logo ? "Yes" : "No"} | Dark Mode: ${discovery.dark_mode_support} | Contrast: ${discovery.wcag_target}`);
      if (discovery.priority_p0_notes) md.push(`- **P0 Launch Scope:** ${discovery.priority_p0_notes}`);
      if (discovery.priority_p2_notes) md.push(`- **P2 Post-Launch:** ${discovery.priority_p2_notes}`);
      if (researchGaps.length) {
        md.push("- **Open Research Gaps:**");
        for (const g of researchGaps) md.push(`  - [OPEN] ${g}`);
      }
      md.push("");
    }

    md.push("---");
    md.push("## 1. Global Design Token Foundation");
    md.push(`- **Surface Background:** \`${tokens.background}\``);
    md.push(`- **Card Surface / Raised:** \`${tokens.card_surface}\``);
    md.push(`- **Primary Action:** \`${tokens.cta}\` (text \`${tokens.cta_text}\`) — dual-ring focus`);
    md.push(`- **Text Primary:** \`${tokens.text_primary}\``);
    md.push(`- **Text Secondary:** \`${tokens.text_secondary}\``);
    md.push(`- **Border Subtle:** \`${tokens.border_subtle}\` (1px solid — borders/dividers only, never body/numeral text)`);
    md.push(`- **Heading Font:** ${headingSpec}`);
    md.push(`- **Body Font:** \`${bodyFont}\` — 400/500, leading-relaxed`);
    if (typoRow["Google Fonts URL"]) md.push(`- **Google Fonts URL:** ${typoRow["Google Fonts URL"]}`);
    md.push("- **Mono / Chips:** `JetBrains Mono` or `ui-monospace`");
    md.push("- **Motion:** 150–200ms `cubic-bezier(0.16,1,0.3,1)`, compositor-only (`transform`, `opacity`)");
    md.push("- **Anti-Slop:** Zero gradient blobs · Zero emoji icons · Zero rainbow borders\n");

    md.push("---");
    md.push("## 2. Design System Reasoning & Intelligence");
    md.push(`- **Matched Style:** ${ds.bestStyle["Style Category"] || projectInfo.style} (${ds.bestStyle["Performance"] || "Verified"})`);
    md.push(`- **Landing Pattern:** ${ds.bestLanding["Pattern Name"] || ds.reasoning.pattern}`);
    md.push(`- **Effects Guidance:** ${ds.bestStyle["Effects & Animation"] || ds.reasoning.keyEffects}`);
    if (ds.reasoning.antiPatterns) md.push(`- **Avoid Anti-Patterns:** ${ds.reasoning.antiPatterns}`);
    md.push("");

    md.push("---");
    md.push("## 3. Page-by-Page Section Blueprints\n");
    for (const pg of compiledPages) {
      if (compiledPages.length > 1) {
        md.push(`### Page Route: ${pg.page_name} (\`${pg.page_id}\` — ${pg.sections.length} sections)\n`);
      }
      for (const s of pg.sections) {
        const c = s.chosen;
        md.push(`#### ${String(s.index).padStart(2, "0")}. ${s.section_name}`);
        md.push(`**Pattern:** ${c.name} (\`${c.archetype_id}\`)`);
        md.push(`**Rationale:** ${c.best_for}`);
        md.push(`**Layout:** ${c.layout_structure}`);
        md.push(`**Typography:** ${c.typography_specs}`);
        md.push(`**Components:** ${c.key_components}`);
        md.push(`**Responsive:** ${c.responsive_behavior}`);
        md.push(`**A11y:** ${c.accessibility}`);
        md.push(`**Anti-Slop:** ${c.anti_slop_rules}\n`);
      }
    }

    md.push("---");
    md.push("## 4. Universal Interactive State Matrix");
    md.push("1. `default` — Resting semantic token colors");
    md.push("2. `hover` — Subtle transform/brightness shift (duration-150)");
    md.push("3. `focus-visible` — `outline-2 outline-offset-2 outline-[var(--color-focus-ring)] forced-colors:outline-[Highlight]`");
    md.push("4. `active` — Tactical downscale `scale-[0.98]`");
    md.push("5. `disabled` — `aria-disabled='true' opacity-50 cursor-not-allowed`");
    md.push("6. `loading` — Animated SVG spinner + `aria-busy='true'` + label preserved");
    md.push("7. `error` — `aria-invalid='true'` + `aria-describedby` pointing to inline error\n");

    md.push("---");
    md.push(`## 5. Stack & Verification Guidelines (\`${extra.stack}\`)`);
    for (const g of stackGuidelines.slice(0, 6)) {
      md.push(`- **[${g.Severity || "INFO"}] ${g.Guideline}:** Do: ${g.Do} | Don't: ${g["Don't"]}`);
    }
    md.push("\n---");
    md.push("## 6. Production Engineering & Audit Guardrails");
    md.push("1. **CSS Tokens & SVGs (`TOKEN-001`):** Define `:root` properties in `tokens.css` and reference `var(--...)` / `currentColor` everywhere else.");
    md.push("2. **Target Size & Sticky-Header Focus (`A11Y-001`, `2.4.11`):** Interactive controls >= 24x24px (>= 44x44px touch); set `scroll-margin-top` on anchored sections.");
    md.push("3. **Accordion & Backdrop Discipline (`PERF-001`):** Use `inert` + `aria-hidden` on collapsed `0fr` panels; avoid `backdrop-filter: blur(...)` on animated `opacity` backdrops.");
    md.push("4. **Verified Telemetry (`SLOP-003`):** Attach audited sources/date ranges to all KPI figures.");

    return {
      projectInfo,
      extra,
      discovery,
      pageMeta: primaryPageMeta,
      compiledPages,
      compiledSections,
      customScopePages,
      researchGaps,
      tokens,
      contrastChecks,
      typography: { row: typoRow, headingFont, bodyFont, headingSpec },
      ds,
      stackGuidelines,
      uxGuidelines,
      webGuidelines,
      reactGuidelines,
      warnings,
      markdown: md.join("\n"),
    };
  }

  // ---------- Safe DOM Helpers ----------
  function el(tag, attrs = {}, children = []) {
    const node = document.createElement(tag);
    for (const [k, v] of Object.entries(attrs)) {
      if (v === undefined || v === null) continue;
      if (k === "className") node.className = v;
      else if (k === "textContent") node.textContent = v;
      else if (k.startsWith("data-")) node.setAttribute(k, v);
      else node.setAttribute(k, String(v));
    }
    for (const ch of children) {
      if (ch === null || ch === undefined) continue;
      node.append(typeof ch === "string" ? document.createTextNode(ch) : ch);
    }
    return node;
  }

  function clearAndRender(container, nodes) {
    if (container) container.replaceChildren(...nodes);
  }

  // ---------- Hero Direction & Route Sync Helpers ----------
  const STORAGE_KEY = "slopguard_studio_draft_v2";
  const STEP_TITLES = [
    "Business & Buyers",
    "Brand, Visuals & A11y",
    "Content & Proof",
    "Sitemap & UX Flows",
    "Tech, Scope & Launch",
  ];

  function applyHeroDirectionToChecks(form, dir) {
    const map = {
      bento: { bento_hero: true, has_mockup: true, has_app_mockups: false, cro_split: false, has_3d: false },
      mockup: { bento_hero: false, has_mockup: true, has_app_mockups: false, cro_split: false, has_3d: false },
      devices: { bento_hero: false, has_mockup: false, has_app_mockups: true, cro_split: false, has_3d: false },
      cro: { bento_hero: false, has_mockup: false, has_app_mockups: false, cro_split: true, has_3d: false },
      editorial: { bento_hero: false, has_mockup: false, has_app_mockups: false, cro_split: false, has_3d: false },
      interactive_3d: { bento_hero: false, has_mockup: false, has_app_mockups: false, cro_split: false, has_3d: true },
    };
    const cfg = map[dir];
    if (!cfg) return;
    for (const [name, checked] of Object.entries(cfg)) {
      const cb = form.querySelector(`input[name="${name}"]`);
      if (cb) cb.checked = checked;
    }
  }

  function inferHeroDirectionFromChecks(form) {
    const heroSel = form.querySelector("#hero_direction");
    if (!heroSel) return;
    const chk = (n) => Boolean(form.querySelector(`input[name="${n}"]`)?.checked);
    if (chk("has_3d")) heroSel.value = "interactive_3d";
    else if (chk("bento_hero")) heroSel.value = "bento";
    else if (chk("has_app_mockups")) heroSel.value = "devices";
    else if (chk("cro_split")) heroSel.value = "cro";
    else if (chk("has_mockup")) heroSel.value = "mockup";
    else heroSel.value = "editorial";
  }

  function getCheckedSitemapPages(form) {
    const checked = Array.from(form.querySelectorAll('input[name="sitemap_pages"]:checked')).map((c) => c.value);
    if (checked.length) return checked;
    const focus = form.querySelector("#page_id")?.value || "home";
    return [focus];
  }

  function syncRouteContext(form) {
    const activeSet = new Set(getCheckedSitemapPages(form));
    const selectEl = form.querySelector("#page_id");
    if (selectEl && !activeSet.has(selectEl.value)) {
      const first = Array.from(activeSet)[0];
      if (first && activeSet.size === 1) selectEl.value = first;
    }

    form.querySelectorAll("details[data-route-group]").forEach((panel) => {
      const group = panel.getAttribute("data-route-group");
      const isMatch = activeSet.has(group);
      panel.open = isMatch;
      panel.classList.toggle("route-active", isMatch);
      const tag = panel.querySelector(".route-tag");
      if (tag) tag.hidden = !isMatch;
    });

    const noteEl = document.getElementById("route-context-note");
    if (noteEl) {
      const routeLabels = Array.from(activeSet).map((id) => {
        const opt = selectEl?.querySelector(`option[value="${id}"]`);
        return opt ? opt.textContent.trim() : id;
      });
      const subPagesActive = Array.from(activeSet).some((id) => !["home", "pricing"].includes(id));
      const suffix = subPagesActive
        ? " — Matching page-specific UX triggers are highlighted and expanded below."
        : " — Primary flows for Home/Pricing are configured above; check any sub-pages in the Sitemap to auto-expand their UX accordions.";
      noteEl.replaceChildren(
        document.createTextNode(`Active Sitemap (${routeLabels.length}): `),
        el("strong", { textContent: routeLabels.join(", ") }),
        document.createTextNode(suffix)
      );
    }
  }

  // ---------- Form Collection & Session Serialization ----------
  const BOOL_NAMES = [
    "enterprise", "founder_led", "has_certifications", "compliance_required",
    "high_competition", "has_press", "has_case_studies", "has_investors",
    "bento_hero", "has_app_mockups", "cro_split", "has_mockup", "has_video",
    "has_audio", "has_3d", "lead_header", "mega_menu", "has_portal",
    "has_proof_stats", "has_analytics_data", "has_before_after", "has_live_data",
    "has_named_quotes", "direct_calendar", "is_productized", "has_billing_toggle",
    "has_matrix", "matrix_tabs", "minimal_diff", "has_addons", "has_sla",
    "direct_rfq_form", "has_guarantee", "has_roi", "mobile_drawer",
    "has_enterprise_tier", "has_newsletter", "has_departments", "has_categories",
    "timeline_horizontal", "has_manifesto", "distributed_team", "culture_focus",
    "has_office_photos", "arch_layered", "workflow_phases", "interactive_scope",
    "has_partners", "searchable_integrations", "multi_persona", "multi_step",
    "map_view", "has_support_route", "data_dense", "has_vip_quote",
    "has_trending", "feed_horizontal", "feed_archive", "split_digest",
    "remote_stipend", "salary_transparent", "parental_wellness", "accordion_jobs",
    "interview_pipeline", "has_toc", "has_version_selector", "multi_policy",
  ];

  const EXTRA_BOOL_NAMES = [
    "has_svg_logo", "has_brand_guidelines", "stock_allowed",
    "multilingual_support", "rtl_required", "site_search",
    "feat_auth", "feat_payments", "feat_booking", "feat_dashboard", "feat_analytics_crm",
  ];

  function readFormState(form) {
    const fd = new FormData(form);
    const val = (name, fallback = "") => String(fd.get(name) ?? fallback).trim();
    const num = (name, fallback) => {
      const n = Number(fd.get(name));
      return Number.isFinite(n) ? n : fallback;
    };
    const bool = (name) => Boolean(form.querySelector(`input[name="${name}"]`)?.checked);

    const sitemapPages = getCheckedSitemapPages(form);
    const focusRoute = val("page_id", sitemapPages[0] || "home");

    const projectInfo = {
      page_id: focusRoute,
      project_name: val("project_name", "Modern Web Platform"),
      industry: val("industry", "b2b"),
      style: val("style", "Industrial Minimalist"),
      target_audience: val("target_audience", "B2B Marketing and Sales Leaders"),
      brand_tier: val("brand_tier", "standard"),
      years_operating: num("years_operating", 5),
      link_count: num("link_count", 5),
      logo_count: num("logo_count", 8),
      step_count: num("step_count", 4),
      case_count: num("case_count", 6),
      review_count: num("review_count", 12),
      team_size: num("team_size", 6),
      faq_count: num("faq_count", 6),
      pricing_model: val("pricing_model", "subscription"),
      feature_density: bool("has_matrix") && bool("enterprise") ? "high" : "standard",
      service_model: bool("workflow_phases") ? "consulting" : "agency",
    };

    for (const b of BOOL_NAMES) {
      projectInfo[b] = bool(b);
    }

    const extra = {
      stack: val("stack", "nextjs"),
      searchKeywords: val("search_keywords", ""),
      evidenceNote: val("evidence_note", ""),
    };

    const discovery = {
      legal_name: val("legal_name", ""),
      tagline: val("tagline", ""),
      existing_url: val("existing_url", ""),
      business_model: val("business_model", "B2B SaaS"),
      primary_goal: val("primary_goal", "Qualified Sales Leads & Demos"),
      primary_device: val("primary_device", "Desktop & Mobile Balanced"),
      buying_cycle: val("buying_cycle", "Research-Driven / Multiple Stakeholders"),
      discovery_confidence: val("discovery_confidence", "Partial Discovery"),
      buyer_pain_points: val("buyer_pain_points", ""),
      competitor_links: val("competitor_links", ""),
      brand_colors_note: val("brand_colors_note", ""),
      hero_direction: val("hero_direction", "bento"),
      reference_urls: val("reference_urls", ""),
      dark_mode_support: val("dark_mode_support", "Both Light & Dark Modes"),
      wcag_target: val("wcag_target", "WCAG 2.2 AA"),
      reduced_motion: val("reduced_motion", "Subtle Micro-Interactions (150ms, Reduced Motion Safe)"),
      copy_owner: val("copy_owner", "Hybrid (Client Drafts + Studio Messaging)"),
      content_readiness: val("content_readiness", "Partial Drafts / Existing Site"),
      core_usp: val("core_usp", ""),
      avoid_claims: val("avoid_claims", ""),
      sitemap_pages: sitemapPages,
      custom_sitemap_pages: Array.from(form.querySelectorAll('input[name="custom_sitemap_pages"]:checked')).map((c) => c.value),
      custom_page_names: val("custom_page_names", ""),
      site_type: val("site_type", "Marketing Website + Headless CMS"),
      cms_preference: val("cms_preference", "Headless (Sanity / Contentful)"),
      target_launch: val("target_launch", ""),
      budget_tier: val("budget_tier", ""),
      decision_maker: val("decision_maker", ""),
      hosting_status: val("hosting_status", ""),
      priority_p0_notes: val("priority_p0_notes", ""),
      priority_p2_notes: val("priority_p2_notes", ""),
    };
    for (const eb of EXTRA_BOOL_NAMES) {
      discovery[eb] = bool(eb);
    }

    return { projectInfo, extra, discovery };
  }

  function serializeSession(form, activeStep) {
    const scalar = {};
    form.querySelectorAll('input:not([type="checkbox"]):not([type="file"]), select, textarea').forEach((node) => {
      if (node.name) scalar[node.name] = node.value;
    });
    const checks = {};
    [...BOOL_NAMES, ...EXTRA_BOOL_NAMES].forEach((b) => {
      const cb = form.querySelector(`input[name="${b}"]`);
      if (cb) checks[b] = Boolean(cb.checked);
    });
    const sitemap_pages = getCheckedSitemapPages(form);
    const custom_sitemap_pages = Array.from(form.querySelectorAll('input[name="custom_sitemap_pages"]:checked')).map((c) => c.value);
    return { version: 2, savedAt: new Date().toISOString(), activeStep, scalar, checks, sitemap_pages, custom_sitemap_pages };
  }

  function applySessionData(form, session) {
    if (!session || typeof session !== "object") return false;
    if (session.scalar && typeof session.scalar === "object") {
      for (const [name, val] of Object.entries(session.scalar)) {
        const elNode = form.querySelector(`[name="${name}"]`);
        if (elNode) elNode.value = String(val ?? "");
      }
    }
    if (session.checks && typeof session.checks === "object") {
      [...BOOL_NAMES, ...EXTRA_BOOL_NAMES].forEach((b) => {
        const cb = form.querySelector(`input[name="${b}"]`);
        if (cb && Object.prototype.hasOwnProperty.call(session.checks, b)) {
          cb.checked = Boolean(session.checks[b]);
        }
      });
    }
    if (Array.isArray(session.sitemap_pages)) {
      const set = new Set(session.sitemap_pages);
      form.querySelectorAll('input[name="sitemap_pages"]').forEach((cb) => {
        cb.checked = set.has(cb.value);
      });
    }
    if (Array.isArray(session.custom_sitemap_pages)) {
      const cSet = new Set(session.custom_sitemap_pages);
      form.querySelectorAll('input[name="custom_sitemap_pages"]').forEach((cb) => {
        cb.checked = cSet.has(cb.value);
      });
    }
    syncRouteContext(form);
    return true;
  }

  function applyPreset(form, key) {
    const preset = PRESETS[key];
    if (!preset) return;
    ["legal_name", "tagline", "existing_url", "buyer_pain_points", "competitor_links", "reference_urls", "brand_colors_note", "core_usp", "avoid_claims", "custom_page_names", "priority_p0_notes", "priority_p2_notes", "target_launch", "budget_tier", "decision_maker"].forEach((k) => {
      const n = form.querySelector(`[name="${k}"]`);
      if (n) n.value = "";
    });
    for (const [field, value] of Object.entries(preset)) {
      if (field === "checks" || field === "sitemapPages" || field === "customSitemapPages") continue;
      const input = form.querySelector(`[name="${field}"]`);
      if (input) input.value = String(value);
    }
    [...BOOL_NAMES, ...EXTRA_BOOL_NAMES].forEach((name) => {
      const cb = form.querySelector(`input[name="${name}"]`);
      if (cb) cb.checked = Boolean(preset.checks && preset.checks[name]);
    });
    const siteSet = new Set(preset.sitemapPages || [preset.page_id || "home"]);
    form.querySelectorAll('input[name="sitemap_pages"]').forEach((cb) => {
      cb.checked = siteSet.has(cb.value);
    });
    const customSet = new Set(preset.customSitemapPages || []);
    form.querySelectorAll('input[name="custom_sitemap_pages"]').forEach((cb) => {
      cb.checked = customSet.has(cb.value);
    });
    if (!preset.hero_direction) inferHeroDirectionFromChecks(form);
    syncRouteContext(form);
  }

  // ---------- Render Output Sections & Live Inspector ----------
  function renderLiveInspector(res) {
    const body = document.getElementById("live-inspector-body");
    const readyText = document.getElementById("inspector-ready-text");
    const statusDot = document.getElementById("inspector-status-dot");
    if (!body) return;

    if (readyText) {
      readyText.textContent = res.researchGaps.length ? `${res.researchGaps.length} open gaps` : "0 open gaps";
    }
    if (statusDot) {
      statusDot.classList.toggle("status-dot-warn", res.researchGaps.length > 0);
    }

    const spectrumHexes = [
      res.tokens.background,
      res.tokens.card_surface,
      res.tokens.cta,
      res.tokens.text_primary,
      res.tokens.text_secondary,
    ];
    const stops = spectrumHexes.map((hex) => {
      const s = el("div", { className: "spectrum-stop", "aria-hidden": "true" });
      s.style.backgroundColor = hex;
      return s;
    });

    const minTextContrast = Math.min(
      res.contrastChecks[0].ratio,
      res.contrastChecks[1].ratio,
      res.contrastChecks[4].ratio
    );
    const wcagBadge = minTextContrast >= 7 ? "AAA Verified" : minTextContrast >= 4.5 ? "AA Verified" : "Review Contrast";

    clearAndRender(body, [
      el("div", { className: "inspector-block" }, [
        el("div", { className: "inspector-label", textContent: `Palette · ${res.tokens.palette_source}` }),
        el("div", {
          className: "spectrum-bar",
          role: "img",
          "aria-label": `Derived palette tokens: ${spectrumHexes.join(", ")}`,
        }, stops),
      ]),
      el("div", { className: "inspector-block" }, [
        el("div", { className: "inspector-label", textContent: "Type & Vertical Direction" }),
        el("p", { className: "specimen-title", textContent: res.projectInfo.project_name || "Untitled Project" }),
        el("div", { className: "specimen-meta", textContent: `${res.typography.headingFont} / ${res.typography.bodyFont} · ${res.ds.category}` }),
      ]),
      el("div", { className: "inspector-block" }, [
        el("dl", {}, [
          el("div", { className: "inspector-kv" }, [
            el("dt", { textContent: "Sitemap Scope" }),
            el("dd", { textContent: `${res.compiledPages.length}p · ${res.compiledSections.length} sections` }),
          ]),
          el("div", { className: "inspector-kv" }, [
            el("dt", { textContent: "Contrast Check" }),
            el("dd", { textContent: `${minTextContrast.toFixed(1)}:1 (${wcagBadge})` }),
          ]),
          el("div", { className: "inspector-kv" }, [
            el("dt", { textContent: "Primary CTA Hex" }),
            el("dd", { textContent: res.tokens.cta }),
          ]),
          el("div", { className: "inspector-kv" }, [
            el("dt", { textContent: "Stack / CMS" }),
            el("dd", { textContent: `${res.extra.stack}` }),
          ]),
          el("div", { className: "inspector-kv" }, [
            el("dt", { textContent: "Launch Window" }),
            el("dd", { textContent: res.discovery.target_launch || "TBD" }),
          ]),
        ]),
      ]),
    ]);
  }

  function renderCompiledOutput(res) {
    renderLiveInspector(res);
    const summaryStrip = document.getElementById("summary-strip");
    const tokenPreview = document.getElementById("token-preview");
    const panelSections = document.getElementById("panel-sections");
    const panelStrategy = document.getElementById("panel-strategy");
    const panelIntel = document.getElementById("panel-intel");
    const panelStack = document.getElementById("panel-stack");
    const panelMarkdown = document.getElementById("panel-markdown");
    const panelCli = document.getElementById("panel-cli");

    clearAndRender(summaryStrip, [
      el("div", { className: "stat-card" }, [
        el("div", { className: "stat-label", textContent: "Compiled Sitemap" }),
        el("div", { className: "stat-value", textContent: `${res.compiledPages.length} Page${res.compiledPages.length > 1 ? "s" : ""} · ${res.compiledSections.length} Sections` }),
        el("div", { className: "stat-sub", textContent: `${res.compiledPages.map((p) => p.page_id).join(", ")}${res.customScopePages.length ? ` (+${res.customScopePages.length} custom)` : ""}` }),
      ]),
      el("div", { className: "stat-card" }, [
        el("div", { className: "stat-label", textContent: "Product Match" }),
        el("div", { className: "stat-value", textContent: res.ds.category }),
        el("div", { className: "stat-sub", textContent: `${res.discovery.business_model} · ${res.ds.productRow.product_slug || "general"}` }),
      ]),
      el("div", { className: "stat-card" }, [
        el("div", { className: "stat-label", textContent: "Typography & Modes" }),
        el("div", { className: "stat-value", textContent: `${res.typography.headingFont} / ${res.typography.bodyFont}` }),
        el("div", { className: "stat-sub", textContent: `${res.discovery.dark_mode_support} · ${res.discovery.wcag_target}` }),
      ]),
      el("div", { className: "stat-card" }, [
        el("div", { className: "stat-label", textContent: "Stack & Open Gaps" }),
        el("div", { className: "stat-value", textContent: res.extra.stack }),
        el("div", { className: "stat-sub", textContent: `${res.warnings.length} fallbacks · ${res.researchGaps.length} open gaps` }),
      ]),
    ]);

    const swatches = [
      ["Background", res.tokens.background],
      ["Card Raised", res.tokens.card_surface],
      ["Primary CTA", res.tokens.cta],
      ["CTA Text", res.tokens.cta_text],
      ["Text Primary", res.tokens.text_primary],
      ["Text Secondary", res.tokens.text_secondary],
      ["Border Subtle", res.tokens.border_subtle],
    ].map(([role, hex]) => {
      const chip = el("div", { className: "swatch-chip" });
      chip.style.backgroundColor = hex;
      return el("div", { className: "swatch-card" }, [
        chip,
        el("div", { className: "swatch-info" }, [
          el("div", { className: "swatch-role", textContent: role }),
          el("div", { className: "swatch-hex", textContent: hex }),
        ]),
      ]);
    });

    const badges = res.contrastChecks.map((c) => {
      const level = c.ratio >= 7 ? "AAA" : c.ratio >= 4.5 ? "AA" : "LOW";
      return el("span", {
        className: "contrast-badge",
        textContent: `${c.label}: ${c.ratio.toFixed(2)}:1 (${level})`,
      });
    });

    clearAndRender(tokenPreview, [
      el("strong", { textContent: `Derived WCAG Token Palette — Source: ${res.tokens.palette_source}` }),
      el("div", { className: "swatch-grid" }, swatches),
      el("div", { className: "contrast-row" }, badges),
    ]);

    // Tab 1: Scannable 2-Column Section Blueprints
    const sectionNodes = [];
    const showPageHeaders = res.compiledPages.length > 1;
    const specCell = (label, value) =>
      el("div", { className: "spec-cell" }, [
        el("dt", { textContent: label }),
        el("dd", { textContent: value }),
      ]);

    for (const pg of res.compiledPages) {
      if (showPageHeaders) {
        sectionNodes.push(
          el("div", { className: "page-group-header" }, [
            el("h3", { className: "page-group-title", textContent: `${pg.page_name} (${pg.page_id})` }),
            el("span", { className: "id-chip", textContent: `${pg.sections.length} sections` }),
          ])
        );
      }
      sectionNodes.push(
        el("div", { className: "blueprint-list" }, pg.sections.map((s) => {
          const c = s.chosen;
          return el("article", { className: "blueprint-card" }, [
            el("div", { className: "blueprint-card-head" }, [
              el("h3", { className: "blueprint-card-title", textContent: `${String(s.index).padStart(2, "0")} · ${s.section_name} — ${c.name}` }),
              el("span", { className: "id-chip", textContent: c.archetype_id }),
            ]),
            el("dl", { className: "spec-grid" }, [
              specCell("Rationale", c.best_for),
              specCell("Layout Structure", c.layout_structure),
              specCell("Typography", c.typography_specs),
              specCell("Key Components", c.key_components),
              specCell("Responsive & Accessibility", `${c.responsive_behavior} | A11y: ${c.accessibility}`),
              specCell("Anti-Slop Guardrail", c.anti_slop_rules),
            ]),
          ]);
        }))
      );
    }
    clearAndRender(panelSections, sectionNodes);

    // Tab 2: Consolidated Client & UX Strategy Brief
    const d = res.discovery;
    const strategyCards = [
      el("div", { className: "intel-card" }, [
        el("h3", { textContent: "01. Business Identity & Positioning" }),
        el("ul", { className: "kv-list" }, [
          el("li", {}, [el("strong", { textContent: "Brand / Legal: " }), `${res.projectInfo.project_name}${d.legal_name ? ` (${d.legal_name})` : ""}`]),
          el("li", {}, [el("strong", { textContent: "Tagline: " }), d.tagline || "[Open — Draft during messaging phase]"]),
          el("li", {}, [el("strong", { textContent: "Model & Objective: " }), `${d.business_model} · ${d.primary_goal}`]),
          el("li", {}, [el("strong", { textContent: "Competitor Benchmarks: " }), d.competitor_links || "[Open — Request 3 competitor links]"]),
        ]),
      ]),
      el("div", { className: "intel-card" }, [
        el("h3", { textContent: "02. Target Audience, Behavior & Objections" }),
        el("ul", { className: "kv-list" }, [
          el("li", {}, [el("strong", { textContent: "Primary Buyer: " }), res.projectInfo.target_audience]),
          el("li", {}, [el("strong", { textContent: "Device & Decision Cycle: " }), `${d.primary_device} | ${d.buying_cycle}`]),
          el("li", {}, [el("strong", { textContent: "Pain Points & Friction: " }), d.buyer_pain_points || "[Open — Interview top objections]"]),
          el("li", {}, [el("strong", { textContent: "Research Confidence: " }), d.discovery_confidence]),
        ]),
      ]),
      el("div", { className: "intel-card" }, [
        el("h3", { textContent: "03. Creative Assets, Visuals & Accessibility" }),
        el("ul", { className: "kv-list" }, [
          el("li", {}, [el("strong", { textContent: "Brand Kit / SVG / Stock: " }), `SVG Logo: ${d.has_svg_logo ? "Yes" : "Needed"} · Brand Guide: ${d.has_brand_guidelines ? "Existing" : "Fresh Palette"} · Stock: ${d.stock_allowed ? "Allowed" : "Avoid"}`]),
          el("li", {}, [el("strong", { textContent: "Existing Hex / Font Notes: " }), d.brand_colors_note || "Derived cleanly from WCAG palette engine"]),
          el("li", {}, [el("strong", { textContent: "Hero Framing Intent: " }), `${d.hero_direction} · Modes: ${d.dark_mode_support}`]),
          el("li", {}, [el("strong", { textContent: "Accessibility & Motion: " }), `${d.wcag_target} · ${d.reduced_motion}`]),
        ]),
      ]),
      el("div", { className: "intel-card" }, [
        el("h3", { textContent: "04. Content Ownership & Verified Evidence (SLOP-003)" }),
        el("ul", { className: "kv-list" }, [
          el("li", {}, [el("strong", { textContent: "Copy & Readiness: " }), `${d.copy_owner} (${d.content_readiness})`]),
          el("li", {}, [el("strong", { textContent: "Core USP / Headline: " }), d.core_usp || "[Open — Define hero H1 claim]"]),
          el("li", {}, [el("strong", { textContent: "Avoid Claims: " }), d.avoid_claims || "Standard anti-slop ban on unverified statistics"]),
          el("li", {}, [el("strong", { textContent: "Verified Evidence Citation: " }), res.extra.evidenceNote || "[OPEN GAP — Add source URL/date before showing KPIs]"]),
        ]),
      ]),
      el("div", { className: "intel-card" }, [
        el("h3", { textContent: "05. Consolidated Project Sitemap" }),
        el("ul", { className: "kv-list" }, [
          el("li", {}, [el("strong", { textContent: `Compiled Blueprint Routes (${res.compiledPages.length}): ` }), res.compiledPages.map((p) => `${p.page_name} [${p.sections.length}s]`).join(" · ")]),
          el("li", {}, [el("strong", { textContent: "Custom / Scope-Only Pages: " }), res.customScopePages.length ? res.customScopePages.join(" · ") : "None requested"]),
          el("li", {}, [el("strong", { textContent: "Localization & IA: " }), `${res.projectInfo.link_count} nav links · Mega Menu: ${res.projectInfo.mega_menu ? "Yes" : "No"} · Multilingual: ${d.multilingual_support ? "Yes" : "No"} · RTL: ${d.rtl_required ? "Yes" : "No"}`]),
        ]),
      ]),
      el("div", { className: "intel-card" }, [
        el("h3", { textContent: "06. Scope Priorities, Delivery & Open Research Gaps" }),
        el("ul", { className: "kv-list" }, [
          el("li", {}, [el("strong", { textContent: "Site Type & CMS: " }), `${d.site_type} (${d.cms_preference}) · Hosting: ${d.hosting_status}`]),
          el("li", {}, [el("strong", { textContent: "Launch / Budget / Approver: " }), `${d.target_launch || "TBD"} · ${d.budget_tier || "TBD"} · Approver: ${d.decision_maker || "Unconfirmed"}`]),
          el("li", {}, [el("strong", { textContent: "P0 Launch Scope: " }), d.priority_p0_notes || "Core selected sitemap pages"]),
          el("li", {}, [el("strong", { textContent: "Open Research Gaps: " }), res.researchGaps.length ? res.researchGaps.join(" | ") : "All discovery fields documented"]),
        ]),
      ]),
    ];
    clearAndRender(panelStrategy, [el("div", { className: "intel-grid" }, strategyCards)]);

    // Tab 3: Design System & Reasoning
    const intelCards = [
      el("div", { className: "intel-card" }, [
        el("h3", { textContent: "UI Reasoning & Product FKs" }),
        el("ul", { className: "kv-list" }, [
          el("li", {}, [el("strong", { textContent: "Product Category: " }), res.ds.category]),
          el("li", {}, [el("strong", { textContent: "Style Priority: " }), res.ds.reasoning.stylePriority.join(" + ")]),
          el("li", {}, [el("strong", { textContent: "Landing Pattern: " }), res.ds.bestLanding["Pattern Name"] || res.ds.reasoning.pattern]),
          el("li", {}, [el("strong", { textContent: "Section Order: " }), res.ds.bestLanding["Section Order"] || "Default page template flow"]),
          el("li", {}, [el("strong", { textContent: "CTA Placement: " }), res.ds.bestLanding["Primary CTA Placement"] || "Above fold + bottom CTA"]),
          el("li", {}, [el("strong", { textContent: "Color Mood: " }), res.ds.reasoning.colorMood]),
          el("li", {}, [el("strong", { textContent: "Avoid Anti-Patterns: " }), res.ds.reasoning.antiPatterns || "None specified"]),
        ]),
      ]),
      el("div", { className: "intel-card" }, [
        el("h3", { textContent: "Typography & Style Prompt Specs" }),
        el("ul", { className: "kv-list" }, [
          el("li", {}, [el("strong", { textContent: "Heading Spec: " }), res.typography.headingSpec]),
          el("li", {}, [el("strong", { textContent: "Body Font: " }), `${res.typography.bodyFont} (400/500, leading-relaxed)`]),
          el("li", {}, [el("strong", { textContent: "Google Fonts: " }), res.typography.row["Google Fonts URL"] || "System stack"]),
          el("li", {}, [el("strong", { textContent: "Tailwind Config: " }), res.typography.row["Tailwind Config"] || "font-sans"]),
          el("li", {}, [el("strong", { textContent: "Matched Visual Style: " }), res.ds.bestStyle["Style Category"] || res.projectInfo.style]),
          el("li", {}, [el("strong", { textContent: "CSS/Prompt Keywords: " }), res.ds.promptMatch["CSS/Technical Keywords"] || res.ds.bestStyle["Effects & Animation"] || "Token surfaces + 150ms transitions"]),
        ]),
      ]),
      el("div", { className: "intel-card" }, [
        el("h3", { textContent: "Chart & Data Visualization Match" }),
        el("ul", { className: "kv-list" }, (res.ds.chartMatches.length ? res.ds.chartMatches : [{ "Data Type": "KPI / Trend", "Best Chart Type": "SVG Sparkline / Area + Bar", "Library Recommendation": "Inline SVG or Recharts", "Accessibility Notes": "Provide role=img, <title>, and tabular data fallback" }]).map((ch) =>
          el("li", {}, [
            el("strong", { textContent: `${ch["Data Type"]}: ` }),
            `${ch["Best Chart Type"]} (${ch["Library Recommendation"] || "SVG"}) — ${ch["Accessibility Notes"] || ""}`,
          ])
        )),
      ]),
      el("div", { className: "intel-card" }, [
        el("h3", { textContent: "Iconography Guidance" }),
        el("ul", { className: "kv-list" }, (res.ds.iconMatches.length ? res.ds.iconMatches : [{ Category: "Navigation", "Icon Name": "Chevron / Arrow", Library: "Lucide", Usage: "1.5px stroke SVG with aria-hidden='true'" }]).map((ic) =>
          el("li", {}, [
            el("strong", { textContent: `${ic["Icon Name"]} (${ic.Library}): ` }),
            `${ic.Usage} — ${ic["Best For"] || ic.Category}`,
          ])
        )),
      ]),
    ];
    clearAndRender(panelIntel, [el("div", { className: "intel-grid" }, intelCards)]);

    // Tab 4: Stack, UX & Perf
    const ruleCard = (title, items, isStack) =>
      el("div", { className: "blueprint-card" }, [
        el("h3", { className: "blueprint-card-title", textContent: title }),
        el("ul", { className: "kv-list mt-3" }, items.map((r) => {
          const name = isStack ? r.Guideline : r.Issue;
          return el("li", {}, [
            el("strong", { textContent: `[${r.Severity || "INFO"}] ${name}: ` }),
            `Do: ${r.Do} | Don't: ${r["Don't"]}`,
          ]);
        })),
      ]);

    const featureFlags = [
      d.feat_auth ? "User Auth & Roles" : null,
      d.feat_payments ? "Payment / Checkout" : null,
      d.feat_booking ? "Calendar / Booking" : null,
      d.feat_dashboard ? "Authenticated Dashboard" : null,
      d.feat_analytics_crm ? "CRM + Analytics" : null,
      d.site_search ? "Site Search" : null,
      d.multilingual_support ? "Multilingual" : null,
    ].filter(Boolean);

    const stackCards = [
      el("div", { className: "blueprint-card" }, [
        el("h3", { className: "blueprint-card-title", textContent: "Requested Functional Integrations & Architecture" }),
        el("p", {
          className: "fieldset-help mt-3",
          textContent: `Architecture: ${d.site_type} | CMS: ${d.cms_preference} | Hosting: ${d.hosting_status || "TBD"} | Capabilities: ${featureFlags.length ? featureFlags.join(", ") : "Static Marketing Scope Only"}`,
        }),
      ]),
      ruleCard(`Stack Guidelines (${res.extra.stack})`, res.stackGuidelines, true),
      ruleCard("UX & Accessibility Guidelines", res.uxGuidelines, false),
      ruleCard("Web Interface Rules", res.webGuidelines, false),
    ];
    if (res.reactGuidelines.length) {
      stackCards.push(ruleCard("React / Next.js Performance Rules", res.reactGuidelines, false));
    }
    clearAndRender(panelStack, [el("div", { className: "blueprint-list" }, stackCards)]);

    // Tab 5: Full Markdown Prompt
    clearAndRender(panelMarkdown, [el("pre", { className: "code-block", textContent: res.markdown })]);

    // Tab 6: Input JSON & Exact Python/CLI Equivalents
    const cliSnippet = [
      "# 1. Generate Design System & Stack Guidance",
      `python skills/ui-ux-pro-max/scripts/search.py "${res.projectInfo.industry} ${res.projectInfo.style}" --design-system -p "${res.projectInfo.project_name}" -f markdown`,
      `python skills/ui-ux-pro-max/scripts/search.py "${res.extra.searchKeywords || "accessibility"}" --stack ${res.extra.stack}`,
      "",
      "# 2. Generate Page Blueprint via Python API (100% of dict triggers)",
      `python -c "import json, sys; sys.path.insert(0, 'skills/ui-ux-pro-max/scripts'); from generate_section_prompt import generate_master_prompt; print(generate_master_prompt(json.loads(open('project_info.json').read())))"`,
      "",
      "# 3. Verify Generated Code with Static AST + Playwright/Axe",
      "npm test",
    ].join("\n");

    clearAndRender(panelCli, [
      el("div", { className: "blueprint-list" }, [
        el("div", { className: "blueprint-card" }, [
          el("h3", { className: "blueprint-card-title", textContent: "CLI / Verification Commands" }),
          el("pre", { className: "code-block mt-3", textContent: cliSnippet }),
        ]),
        el("div", { className: "blueprint-card" }, [
          el("h3", { className: "blueprint-card-title", textContent: "Canonical project_info JSON Input" }),
          el("pre", { className: "code-block mt-3", textContent: JSON.stringify(res.projectInfo, null, 2) }),
        ]),
        el("div", { className: "blueprint-card" }, [
          el("h3", { className: "blueprint-card-title", textContent: "Full Client Discovery & Sitemap JSON" }),
          el("pre", { className: "code-block mt-3", textContent: JSON.stringify(res.discovery, null, 2) }),
        ]),
      ]),
    ]);
  }

  // ---------- Progressive View Transitions + Accessible Tabs + Validation + Wizard ----------
  let activeViewTransition = null;

  function runViewTransition(type, updateFn, onDone) {
    const reduced = typeof window.matchMedia === "function" && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    if (reduced || typeof document.startViewTransition !== "function") {
      updateFn();
      if (onDone) onDone();
      return;
    }

    if (activeViewTransition && typeof activeViewTransition.skipTransition === "function") {
      try { activeViewTransition.skipTransition(); } catch { /* ignore */ }
    }

    const root = document.documentElement;
    if (type) root.setAttribute("data-vt", type);

    let vt;
    try {
      vt = document.startViewTransition({ update: updateFn, types: type ? [type] : [] });
    } catch {
      try {
        vt = document.startViewTransition(updateFn);
      } catch {
        root.removeAttribute("data-vt");
        updateFn();
        if (onDone) onDone();
        return;
      }
    }

    activeViewTransition = vt;
    if (onDone && vt.updateCallbackDone) {
      vt.updateCallbackDone.then(() => onDone()).catch(() => {});
    }
    if (vt.finished) {
      vt.finished.finally(() => {
        if (activeViewTransition === vt) {
          activeViewTransition = null;
          root.removeAttribute("data-vt");
        }
      });
    } else {
      root.removeAttribute("data-vt");
    }
  }

  function setupTabs() {
    const tabs = Array.from(document.querySelectorAll('[role="tab"]'));
    const panels = new Map(tabs.map((t) => [t.id, document.querySelector(`[aria-labelledby="${t.id}"]`)]));

    function activate(tab, focusTab = false) {
      runViewTransition("panel", () => {
        for (const t of tabs) {
          const selected = t === tab;
          t.setAttribute("aria-selected", selected ? "true" : "false");
          t.setAttribute("tabindex", selected ? "0" : "-1");
          const panel = panels.get(t.id);
          if (panel) panel.hidden = !selected;
        }
      }, () => {
        if (focusTab) tab.focus();
      });
    }

    tabs.forEach((tab, idx) => {
      tab.setAttribute("tabindex", idx === 0 ? "0" : "-1");
      tab.addEventListener("click", () => activate(tab, false));
      tab.addEventListener("keydown", (e) => {
        let nextIdx = null;
        if (e.key === "ArrowRight") nextIdx = (idx + 1) % tabs.length;
        else if (e.key === "ArrowLeft") nextIdx = (idx - 1 + tabs.length) % tabs.length;
        else if (e.key === "Home") nextIdx = 0;
        else if (e.key === "End") nextIdx = tabs.length - 1;
        if (nextIdx !== null) {
          e.preventDefault();
          activate(tabs[nextIdx], true);
        }
      });
    });
  }

  function setupValidation(form, goToStep) {
    const controls = Array.from(form.querySelectorAll("input, select, textarea"));
    const syncField = (input) => {
      const errorId = input.getAttribute("data-error");
      const invalid = !input.checkValidity();
      input.setAttribute("aria-invalid", invalid ? "true" : "false");
      if (errorId) {
        if (invalid) input.setAttribute("aria-describedby", errorId);
        else input.removeAttribute("aria-describedby");
      }
      return !invalid;
    };

    controls.forEach((c) => {
      c.setAttribute("aria-invalid", "false");
      c.addEventListener("blur", () => {
        if (c.matches(":user-invalid") || !c.checkValidity()) syncField(c);
      });
      c.addEventListener("input", () => {
        if (c.getAttribute("aria-invalid") === "true") syncField(c);
      });
    });

    return () => {
      let firstBad = null;
      for (const c of controls) {
        if (!syncField(c) && !firstBad) firstBad = c;
      }
      if (firstBad) {
        const ownerStep = firstBad.closest(".wizard-step");
        if (ownerStep && goToStep) {
          goToStep(Number(ownerStep.getAttribute("data-step") || 1));
        }
        firstBad.focus();
        return false;
      }
      return true;
    };
  }

  async function loadBundle() {
    if (window.__SLOPGUARD_KIT_BUNDLE__) return window.__SLOPGUARD_KIT_BUNDLE__;
    if (window.location.protocol === "file:") {
      await new Promise((resolve, reject) => {
        const s = document.createElement("script");
        s.src = "./data/kit-bundle.js";
        s.onload = resolve;
        s.onerror = () => reject(new Error("Failed to load local kit-bundle.js"));
        document.head.appendChild(s);
      });
      if (window.__SLOPGUARD_KIT_BUNDLE__) return window.__SLOPGUARD_KIT_BUNDLE__;
    }
    const res = await fetch("./data/kit-bundle.json");
    if (!res.ok) throw new Error("Failed to load kit-bundle.json");
    return res.json();
  }

  async function init() {
    bundle = await loadBundle();

    // Populate industry datalist with all 96 normalized product types
    const indList = document.getElementById("industry-list");
    for (const row of bundle.domains.product || []) {
      indList.append(el("option", { value: row["Product Type"] }));
    }

    const form = document.getElementById("blueprint-form");
    const statusEl = document.getElementById("compile-status");
    const draftEl = document.getElementById("draft-status");
    const stepPills = Array.from(document.querySelectorAll(".step-pill[data-wizard-step]"));
    const stepPanels = Array.from(form.querySelectorAll(".wizard-step[data-step]"));
    const prevBtn = document.getElementById("wizard-prev-btn");
    const nextBtn = document.getElementById("wizard-next-btn");
    const stepLabel = document.getElementById("wizard-step-label");

    let activeStep = 1;

    const saveDraft = () => {
      try {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(serializeSession(form, activeStep)));
        if (draftEl) draftEl.textContent = "Draft saved locally in browser.";
      } catch {
        // Ignore restricted storage on sandboxed file:// origins
      }
    };

    const setActiveStep = (nextStep, opts = {}) => {
      const targetStep = Math.max(1, Math.min(5, Number(nextStep) || 1));
      const { animate = true, focusControl = false } = opts;
      const shouldAnimate = animate && targetStep !== activeStep;
      const direction = targetStep >= activeStep ? "forward" : "backward";

      const applyStepDom = () => {
        activeStep = targetStep;
        stepPanels.forEach((sec) => {
          sec.hidden = Number(sec.getAttribute("data-step")) !== activeStep;
        });
        stepPills.forEach((btn) => {
          const isCurrent = Number(btn.getAttribute("data-wizard-step")) === activeStep;
          if (isCurrent) btn.setAttribute("aria-current", "step");
          else btn.removeAttribute("aria-current");
        });
        if (stepLabel) stepLabel.textContent = `Step 0${activeStep} of 05 · ${STEP_TITLES[activeStep - 1]}`;
        if (prevBtn) prevBtn.disabled = activeStep === 1;
        if (nextBtn) nextBtn.textContent = activeStep === 5 ? "Jump to Compile" : "Next Step";
        saveDraft();
      };

      const finishFocus = () => {
        if (focusControl && prevBtn && prevBtn.disabled) {
          const stepOneBtn = document.querySelector('.step-pill[data-wizard-step="1"]');
          stepOneBtn?.focus({ preventScroll: true });
        }
      };

      if (shouldAnimate) {
        runViewTransition(direction, applyStepDom, finishFocus);
      } else {
        applyStepDom();
        finishFocus();
      }
    };

    const validateAll = setupValidation(form, (s) => setActiveStep(s, { animate: false }));
    setupTabs();

    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      if (raw) {
        const parsed = JSON.parse(raw);
        if (parsed && parsed.version === 2) {
          applySessionData(form, parsed);
          if (parsed.activeStep) activeStep = Number(parsed.activeStep) || 1;
          if (draftEl) draftEl.textContent = "Restored saved local draft.";
        }
      }
    } catch {
      // Fall back to HTML defaults silently
    }

    setActiveStep(activeStep, { animate: false });
    syncRouteContext(form);

    stepPills.forEach((btn) => {
      btn.addEventListener("click", () => setActiveStep(btn.getAttribute("data-wizard-step"), { animate: true }));
    });
    prevBtn?.addEventListener("click", () => {
      if (activeStep > 1) setActiveStep(activeStep - 1, { animate: true, focusControl: true });
    });
    nextBtn?.addEventListener("click", () => {
      if (activeStep < 5) {
        setActiveStep(activeStep + 1, { animate: true });
      } else {
        document.getElementById("compile-btn")?.focus();
      }
    });

    const heroDirEl = form.querySelector("#hero_direction");
    heroDirEl?.addEventListener("change", () => {
      applyHeroDirectionToChecks(form, heroDirEl.value);
      saveDraft();
    });
    ["bento_hero", "has_app_mockups", "cro_split", "has_mockup", "has_3d"].forEach((name) => {
      form.querySelector(`input[name="${name}"]`)?.addEventListener("change", () => {
        inferHeroDirectionFromChecks(form);
        saveDraft();
      });
    });

    const pageIdEl = form.querySelector("#page_id");
    pageIdEl?.addEventListener("change", () => {
      const checked = Array.from(form.querySelectorAll('input[name="sitemap_pages"]:checked'));
      if (checked.length <= 1) {
        form.querySelectorAll('input[name="sitemap_pages"]').forEach((cb) => {
          cb.checked = cb.value === pageIdEl.value;
        });
      } else {
        const target = form.querySelector(`input[name="sitemap_pages"][value="${pageIdEl.value}"]`);
        if (target) target.checked = true;
      }
      syncRouteContext(form);
      saveDraft();
    });

    form.querySelectorAll('input[name="sitemap_pages"]').forEach((cb) => {
      cb.addEventListener("change", () => {
        const remaining = form.querySelectorAll('input[name="sitemap_pages"]:checked');
        if (!remaining.length) cb.checked = true;
        syncRouteContext(form);
        saveDraft();
      });
    });

    let liveTimer = null;
    const runCompile = (scrollToOutput) => {
      const { projectInfo, extra, discovery } = readFormState(form);
      lastCompiled = compileAll(projectInfo, extra, discovery);
      renderCompiledOutput(lastCompiled);
      statusEl.textContent = `Compiled ${lastCompiled.compiledSections.length} sections across ${lastCompiled.compiledPages.length} page(s) for "${projectInfo.project_name}" (${projectInfo.page_id}) — 0 errors.`;
      if (scrollToOutput) {
        document.getElementById("compiled-output")?.scrollIntoView({ behavior: "smooth" });
      }
    };

    const scheduleLiveCompile = () => {
      if (liveTimer) clearTimeout(liveTimer);
      liveTimer = setTimeout(() => {
        runCompile(false);
      }, 120);
    };

    const setPressedPreset = (activeKey) => {
      document.querySelectorAll("[data-preset]").forEach((b) => {
        b.setAttribute("aria-pressed", b.getAttribute("data-preset") === activeKey ? "true" : "false");
      });
    };

    document.getElementById("sitemap-core-btn")?.addEventListener("click", () => {
      const core = new Set(["home", "about", "services", "pricing", "contact"]);
      form.querySelectorAll('input[name="sitemap_pages"]').forEach((cb) => { cb.checked = core.has(cb.value); });
      if (pageIdEl) pageIdEl.value = "home";
      syncRouteContext(form);
      saveDraft();
      runCompile(false);
    });
    document.getElementById("sitemap-all-btn")?.addEventListener("click", () => {
      form.querySelectorAll('input[name="sitemap_pages"]').forEach((cb) => { cb.checked = true; });
      syncRouteContext(form);
      saveDraft();
      runCompile(false);
    });
    document.getElementById("sitemap-single-btn")?.addEventListener("click", () => {
      const focus = pageIdEl?.value || "home";
      form.querySelectorAll('input[name="sitemap_pages"]').forEach((cb) => { cb.checked = cb.value === focus; });
      syncRouteContext(form);
      saveDraft();
      runCompile(false);
    });

    form.addEventListener("input", () => {
      saveDraft();
      scheduleLiveCompile();
    });
    form.addEventListener("change", () => {
      saveDraft();
      runCompile(false);
    });

    form.addEventListener("submit", (e) => {
      e.preventDefault();
      if (!validateAll()) {
        statusEl.textContent = "Please fix the highlighted required field before compiling.";
        return;
      }
      runCompile(true);
    });

    document.querySelectorAll("[data-preset]").forEach((btn) => {
      btn.addEventListener("click", () => {
        const key = btn.getAttribute("data-preset");
        applyPreset(form, key);
        setPressedPreset(key);
        saveDraft();
        runCompile(false);
        statusEl.textContent = `Loaded preset "${btn.textContent.trim()}" and recompiled bottom output.`;
      });
    });

    document.getElementById("reset-btn")?.addEventListener("click", () => {
      try { localStorage.removeItem(STORAGE_KEY); } catch { /* noop */ }
      applyPreset(form, "enterprise");
      setPressedPreset("enterprise");
      setActiveStep(1);
      runCompile(false);
      statusEl.textContent = "Reset to B2B Enterprise defaults and recompiled.";
    });

    document.getElementById("export-session-btn")?.addEventListener("click", () => {
      const payload = serializeSession(form, activeStep);
      const slug = (form.querySelector("#project_name")?.value || "discovery").toLowerCase().replace(/[^a-z0-9]+/g, "-");
      const blob = new Blob([JSON.stringify(payload, null, 2)], { type: "application/json;charset=utf-8" });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `${slug}-discovery-session.json`;
      a.click();
      URL.revokeObjectURL(url);
      if (draftEl) draftEl.textContent = `Exported ${a.download}.`;
    });

    const importInput = document.getElementById("import-session-input");
    document.getElementById("import-session-btn")?.addEventListener("click", () => importInput?.click());
    importInput?.addEventListener("change", async () => {
      const file = importInput.files && importInput.files[0];
      if (!file) return;
      try {
        const data = JSON.parse(await file.text());
        if (!applySessionData(form, data)) throw new Error("Unrecognized session JSON format");
        setActiveStep(data.activeStep || 1);
        runCompile(false);
        if (draftEl) draftEl.textContent = `Loaded session from "${file.name}".`;
      } catch (err) {
        statusEl.textContent = `Session load error: ${err.message}`;
      } finally {
        importInput.value = "";
      }
    });

    const themeBtn = document.getElementById("theme-toggle");
    themeBtn.addEventListener("click", () => {
      runViewTransition("theme", () => {
        const isDark = document.documentElement.classList.toggle("dark");
        themeBtn.setAttribute("aria-pressed", isDark ? "true" : "false");
        themeBtn.textContent = isDark ? "Light Mode" : "Dark Mode";
      });
    });

    document.getElementById("copy-md-btn").addEventListener("click", async () => {
      if (!lastCompiled) return;
      await navigator.clipboard.writeText(lastCompiled.markdown);
      statusEl.textContent = "Copied full Markdown master brief to clipboard.";
    });

    document.getElementById("copy-json-btn").addEventListener("click", async () => {
      if (!lastCompiled) return;
      await navigator.clipboard.writeText(JSON.stringify(lastCompiled.projectInfo, null, 2));
      statusEl.textContent = "Copied canonical project_info JSON to clipboard.";
    });

    document.getElementById("download-md-btn").addEventListener("click", () => {
      if (!lastCompiled) return;
      const slug = (lastCompiled.projectInfo.project_name || "blueprint").toLowerCase().replace(/[^a-z0-9]+/g, "-");
      const scopeTag = lastCompiled.compiledPages.length > 1 ? `${lastCompiled.compiledPages.length}pages` : lastCompiled.projectInfo.page_id;
      const blob = new Blob([lastCompiled.markdown], { type: "text/markdown;charset=utf-8" });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `${slug}-${scopeTag}-blueprint.md`;
      a.click();
      URL.revokeObjectURL(url);
      statusEl.textContent = `Downloaded ${a.download}.`;
    });

    // Initial compile on load
    runCompile(false);
  }

  window.addEventListener("DOMContentLoaded", () => {
    init().catch((err) => {
      const statusEl = document.getElementById("compile-status");
      if (statusEl) statusEl.textContent = `Initialization error: ${err.message}`;
    });
  });
})();
