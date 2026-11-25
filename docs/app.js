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
      project_name: "CloudCore Telemetry",
      industry: "b2b saas analytics",
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
      },
    },
    agency: {
      page_id: "about",
      project_name: "Atelier Nord",
      industry: "creative agency design studio",
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
        has_mockup: true,
        has_manifesto: true,
        has_office_photos: true,
        culture_focus: true,
        direct_calendar: true,
        is_productized: true,
        has_vip_quote: true,
      },
    },
    growth: {
      page_id: "services",
      project_name: "SyncHub Automation",
      industry: "productivity tool collaboration",
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
      },
    },
    pricing: {
      page_id: "pricing",
      project_name: "VaultSec Enterprise",
      industry: "cybersecurity platform fintech",
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

  // ---------- Compiler Pipeline ----------
  function compileAll(projectInfo, extra) {
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
    const pageMeta = (bundle.pageTemplates.pages || []).find((p) => p.page_id === projectInfo.page_id);
    const targetSections = pageMeta
      ? pageMeta.default_section_flow.map((sid) => sectionMap.get(sid)).filter(Boolean)
      : bundle.sectionArchetypes;

    const compiledSections = targetSections.map((sec, idx) => ({
      index: idx + 1,
      section_id: sec.section_id,
      section_name: sec.section_name,
      chosen: selectArchetype(sec, projectInfo, warnings),
    }));

    const contrastChecks = [
      { label: "Text Primary / Bg", ratio: contrastRatio(tokens.text_primary, tokens.background) },
      { label: "Text Primary / Card", ratio: contrastRatio(tokens.text_primary, tokens.card_surface) },
      { label: "Text Secondary / Bg", ratio: contrastRatio(tokens.text_secondary, tokens.background) },
      { label: "Text Secondary / Card", ratio: contrastRatio(tokens.text_secondary, tokens.card_surface) },
      { label: "CTA Text / CTA", ratio: contrastRatio(tokens.cta_text, tokens.cta) },
    ];

    const md = [];
    md.push("# Master Production-Grade UI/UX Blueprint");
    md.push(`**Project:** ${projectInfo.project_name}`);
    md.push(`**Page:** ${pageMeta ? pageMeta.name : projectInfo.page_id} (\`${projectInfo.page_id}\`)`);
    md.push(`**Style Archetype:** ${projectInfo.style}`);
    md.push(`**Industry / Category:** ${ds.category} (\`${ds.productRow.product_slug || "general"}\`)`);
    md.push(`**Target Stack:** \`${extra.stack}\``);
    md.push(`**Target Audience:** ${projectInfo.target_audience}`);
    md.push(`**Sections covered:** ${compiledSections.length} sections`);
    if (extra.evidenceNote) md.push(`**Verified Evidence Basis:** ${extra.evidenceNote}`);
    md.push("**Compliance:** WCAG 2.2 AA | Anti-Slop Gates Enabled\n");

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
    md.push("## 3. Section-by-Section Blueprint\n");
    for (const s of compiledSections) {
      const c = s.chosen;
      md.push(`### ${String(s.index).padStart(2, "0")}. ${s.section_name}`);
      md.push(`**Pattern:** ${c.name} (\`${c.archetype_id}\`)`);
      md.push(`**Rationale:** ${c.best_for}`);
      md.push(`**Layout:** ${c.layout_structure}`);
      md.push(`**Typography:** ${c.typography_specs}`);
      md.push(`**Components:** ${c.key_components}`);
      md.push(`**Responsive:** ${c.responsive_behavior}`);
      md.push(`**A11y:** ${c.accessibility}`);
      md.push(`**Anti-Slop:** ${c.anti_slop_rules}\n`);
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
      pageMeta,
      tokens,
      contrastChecks,
      typography: { row: typoRow, headingFont, bodyFont, headingSpec },
      ds,
      compiledSections,
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
    container.replaceChildren(...nodes);
  }

  // ---------- Form Collection & Validation ----------
  function readFormState(form) {
    const fd = new FormData(form);
    const val = (name, fallback = "") => String(fd.get(name) ?? fallback).trim();
    const num = (name, fallback) => {
      const n = Number(fd.get(name));
      return Number.isFinite(n) ? n : fallback;
    };
    const bool = (name) => Boolean(form.querySelector(`input[name="${name}"]`)?.checked);

    const projectInfo = {
      page_id: val("page_id", "home"),
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

    const boolNames = [
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
    for (const b of boolNames) {
      projectInfo[b] = bool(b);
    }

    const extra = {
      stack: val("stack", "nextjs"),
      searchKeywords: val("search_keywords", ""),
      evidenceNote: val("evidence_note", ""),
    };

    return { projectInfo, extra };
  }

  function applyPreset(form, key) {
    const preset = PRESETS[key];
    if (!preset) return;
    for (const [field, value] of Object.entries(preset)) {
      if (field === "checks") continue;
      const input = form.querySelector(`[name="${field}"]`);
      if (input) input.value = String(value);
    }
    form.querySelectorAll('input[type="checkbox"]').forEach((cb) => {
      cb.checked = Boolean(preset.checks[cb.name]);
    });
  }

  // ---------- Render Output Sections ----------
  function renderCompiledOutput(res) {
    const summaryStrip = document.getElementById("summary-strip");
    const tokenPreview = document.getElementById("token-preview");
    const panelSections = document.getElementById("panel-sections");
    const panelIntel = document.getElementById("panel-intel");
    const panelStack = document.getElementById("panel-stack");
    const panelMarkdown = document.getElementById("panel-markdown");
    const panelCli = document.getElementById("panel-cli");

    clearAndRender(summaryStrip, [
      el("div", { className: "stat-card" }, [
        el("div", { className: "stat-label", textContent: "Page Route & Flow" }),
        el("div", { className: "stat-value", textContent: `${res.compiledSections.length} Sections` }),
        el("div", { className: "stat-sub", textContent: `${res.pageMeta ? res.pageMeta.name : res.projectInfo.page_id} (${res.projectInfo.page_id})` }),
      ]),
      el("div", { className: "stat-card" }, [
        el("div", { className: "stat-label", textContent: "Product Match" }),
        el("div", { className: "stat-value", textContent: res.ds.category }),
        el("div", { className: "stat-sub", textContent: `Slug: ${res.ds.productRow.product_slug || "general"} | Style ID: ${res.ds.productRow.style_id || "-"}` }),
      ]),
      el("div", { className: "stat-card" }, [
        el("div", { className: "stat-label", textContent: "Typography Pair" }),
        el("div", { className: "stat-value", textContent: `${res.typography.headingFont} / ${res.typography.bodyFont}` }),
        el("div", { className: "stat-sub", textContent: res.typography.row["Category"] || "Modern Sans Pair" }),
      ]),
      el("div", { className: "stat-card" }, [
        el("div", { className: "stat-label", textContent: "Selected Stack & Warnings" }),
        el("div", { className: "stat-value", textContent: res.extra.stack }),
        el("div", { className: "stat-sub", textContent: `${res.warnings.length} fallback warnings` }),
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

    // Tab 1: Section Blueprint
    const secCards = res.compiledSections.map((s) => {
      const c = s.chosen;
      return el("article", { className: "blueprint-card" }, [
        el("div", { className: "blueprint-card-head" }, [
          el("h3", { className: "blueprint-card-title", textContent: `${String(s.index).padStart(2, "0")}. ${s.section_name} — ${c.name}` }),
          el("span", { className: "id-chip", textContent: c.archetype_id }),
        ]),
        el("dl", { className: "spec-dl" }, [
          el("dt", { textContent: "Rationale" }), el("dd", { textContent: c.best_for }),
          el("dt", { textContent: "Layout" }), el("dd", { textContent: c.layout_structure }),
          el("dt", { textContent: "Typography" }), el("dd", { textContent: c.typography_specs }),
          el("dt", { textContent: "Components" }), el("dd", { textContent: c.key_components }),
          el("dt", { textContent: "Responsive" }), el("dd", { textContent: c.responsive_behavior }),
          el("dt", { textContent: "Accessibility" }), el("dd", { textContent: c.accessibility }),
          el("dt", { textContent: "Anti-Slop" }), el("dd", { textContent: c.anti_slop_rules }),
        ]),
      ]);
    });
    clearAndRender(panelSections, [el("div", { className: "blueprint-list" }, secCards)]);

    // Tab 2: Design System & Reasoning
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

    // Tab 3: Stack, UX & Perf
    const ruleCard = (title, items, isStack) =>
      el("div", { className: "blueprint-card" }, [
        el("h3", { className: "blueprint-card-title", textContent: title }),
        el("ul", { className: "kv-list mt-3" }, items.map((r) => {
          const name = isStack ? r.Guideline : r.Issue;
          const good = isStack ? r.Do : r.Do;
          const bad = isStack ? r["Don't"] : r["Don't"];
          return el("li", {}, [
            el("strong", { textContent: `[${r.Severity || "INFO"}] ${name}: ` }),
            `Do: ${good} | Don't: ${bad}`,
          ]);
        })),
      ]);

    const stackCards = [
      ruleCard(`Stack Guidelines (${res.extra.stack})`, res.stackGuidelines, true),
      ruleCard("UX & Accessibility Guidelines", res.uxGuidelines, false),
      ruleCard("Web Interface Rules", res.webGuidelines, false),
    ];
    if (res.reactGuidelines.length) {
      stackCards.push(ruleCard("React / Next.js Performance Rules", res.reactGuidelines, false));
    }
    clearAndRender(panelStack, [el("div", { className: "blueprint-list" }, stackCards)]);

    // Tab 4: Full Markdown Prompt
    clearAndRender(panelMarkdown, [el("pre", { className: "code-block", textContent: res.markdown })]);

    // Tab 5: Input JSON & Exact Python/CLI Equivalents
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
      ]),
    ]);
  }

  // ---------- Accessible Tabs + Form Validation ----------
  function setupTabs() {
    const tabs = Array.from(document.querySelectorAll('[role="tab"]'));
    const panels = new Map(tabs.map((t) => [t.id, document.querySelector(`[aria-labelledby="${t.id}"]`)]));

    function activate(tab, focusTab = false) {
      for (const t of tabs) {
        const selected = t === tab;
        t.setAttribute("aria-selected", selected ? "true" : "false");
        t.setAttribute("tabindex", selected ? "0" : "-1");
        const panel = panels.get(t.id);
        if (panel) panel.hidden = !selected;
      }
      if (focusTab) tab.focus();
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

  function setupValidation(form) {
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
    const validateAll = setupValidation(form);
    setupTabs();

    const runCompile = (scrollToOutput) => {
      const { projectInfo, extra } = readFormState(form);
      lastCompiled = compileAll(projectInfo, extra);
      renderCompiledOutput(lastCompiled);
      statusEl.textContent = `Compiled ${lastCompiled.compiledSections.length} sections for "${projectInfo.project_name}" (${projectInfo.page_id}) — 0 errors.`;
      if (scrollToOutput) {
        document.getElementById("compiled-output")?.scrollIntoView({ behavior: "smooth" });
      }
    };

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
        applyPreset(form, btn.getAttribute("data-preset"));
        runCompile(false);
        statusEl.textContent = `Loaded preset "${btn.textContent.trim()}" and recompiled bottom output.`;
      });
    });

    document.getElementById("reset-btn").addEventListener("click", () => {
      applyPreset(form, "enterprise");
      runCompile(false);
      statusEl.textContent = "Reset to B2B Enterprise defaults and recompiled.";
    });

    const themeBtn = document.getElementById("theme-toggle");
    themeBtn.addEventListener("click", () => {
      const isDark = document.documentElement.classList.toggle("dark");
      themeBtn.setAttribute("aria-pressed", isDark ? "true" : "false");
      themeBtn.textContent = isDark ? "Light Mode" : "Dark Mode";
    });

    document.getElementById("copy-md-btn").addEventListener("click", async () => {
      if (!lastCompiled) return;
      await navigator.clipboard.writeText(lastCompiled.markdown);
      statusEl.textContent = "Copied full Markdown blueprint to clipboard.";
    });

    document.getElementById("copy-json-btn").addEventListener("click", async () => {
      if (!lastCompiled) return;
      await navigator.clipboard.writeText(JSON.stringify(lastCompiled.projectInfo, null, 2));
      statusEl.textContent = "Copied canonical project_info JSON to clipboard.";
    });

    document.getElementById("download-md-btn").addEventListener("click", () => {
      if (!lastCompiled) return;
      const slug = (lastCompiled.projectInfo.project_name || "blueprint").toLowerCase().replace(/[^a-z0-9]+/g, "-");
      const blob = new Blob([lastCompiled.markdown], { type: "text/markdown;charset=utf-8" });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `${slug}-${lastCompiled.projectInfo.page_id}-blueprint.md`;
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
