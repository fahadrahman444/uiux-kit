BEGIN TRANSACTION;
CREATE TABLE audit_remediations (
  finding_id TEXT PRIMARY KEY,
  theme_id TEXT NOT NULL REFERENCES design_themes(theme_id),
  category TEXT NOT NULL,
  severity TEXT NOT NULL,
  source_selector_or_line TEXT NOT NULL,
  observed_issue TEXT NOT NULL,
  remediation_applied TEXT NOT NULL
);
INSERT INTO "audit_remediations" VALUES('rem-01','dark-kinetic-emerald','contrast','blocker','rgb(33, 37, 41) / #212529 (186-323 elements/page)','Bootstrap default dark body color leaked onto black #000000 containers across routes.','Enforce --text-primary (#FFFFFF, 21:1) and --text-secondary (#C2C2C2, 11.5:1) on all dark wrappers.');
INSERT INTO "audit_remediations" VALUES('rem-02','dark-kinetic-emerald','contrast','major','#6B6B6B / #494C4F / #999999 captions','Muted greys drop below WCAG AA on #000000 and #121212 card surfaces.','Standardize caption ink on --text-muted (#A8A8A8, 8.74:1 AAA on #000000).');
INSERT INTO "audit_remediations" VALUES('rem-03','dark-kinetic-emerald','contrast','blocker','.filter-button.active','White #FFFFFF text rendered over light green #65BC7B active filter background fails WCAG AA contrast.','Pair active #65BC7B and #3BC77B surfaces with --text-on-accent (#020617, 9.0:1-9.9:1 AAA).');
INSERT INTO "audit_remediations" VALUES('rem-04','dark-kinetic-emerald','performance','blocker','axtra_main.js lines 766 & 1897 (.service__item-3, .team__item-7)','mousemove attaches un-cleared setInterval(followImageCursor(...), 1000) and invokes callback eagerly per pointer frame.','Replace mousemove timers with CSS compositor hover transitions and optional requestAnimationFrame throttling.');
INSERT INTO "audit_remediations" VALUES('rem-05','dark-kinetic-emerald','a11y-motion','blocker','ScrollSmoother, SplitText .title-anim, bounce drops, custom cursors','3D rotationX(-80deg) line flips, velocity skewY, smooth scroll inertia, and infinite marquees run without reduced-motion checks.','Gate all GSAP timelines behind matchMedia reduced-motion checks and apply global @media (prefers-reduced-motion: reduce) CSS.');
INSERT INTO "audit_remediations" VALUES('rem-06','dark-kinetic-emerald','a11y-keyboard','major','.service__img / .portfolio__content-5 / .wc-btn-primary.btn-hover','Sticky image swaps and sliding project labels respond only to mouse hover events.','Mirror :hover visibility rules with :focus-visible / :focus-within and apply 2px #3BC77B focus-visible outlines.');
INSERT INTO "audit_remediations" VALUES('rem-07','dark-kinetic-emerald','responsive-type','minor','/projects H1 (82px) & /blog H1 (62px) at 375px','Some display headings stayed disproportionately huge on 375px viewports despite 0px overflow.','Use fluid clamp() typography scales (e.g. clamp(3rem, 1.5rem + 5.5vw, 7.5rem)) across all hero tokens.');
INSERT INTO "audit_remediations" VALUES('rem-08','dark-kinetic-emerald','anti-slop','minor','axtra_main.js .end (chroma [''#F9D371'',''#F47340'',''#EF2F88'',''#8843F2''])','Multi-stop repeating elastic rainbow text animation conflicts with clean emerald agency identity.','Exclude rainbow chroma loop; restrict accents cleanly to #3BC77B / #61CE70 / #65BC7B.');
CREATE TABLE breakpoints (
  bp_id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  min_width_px INTEGER NOT NULL,
  max_width_px INTEGER NOT NULL,
  columns_desktop INTEGER NOT NULL,
  columns_mobile INTEGER NOT NULL,
  container_padding TEXT NOT NULL,
  source_layer TEXT NOT NULL
);
INSERT INTO "breakpoints" VALUES('bp-01','mobile_xs',0,479,1,1,'16px','theme-custom');
INSERT INTO "breakpoints" VALUES('bp-02','mobile_bs',480,575,1,1,'16px','bootstrap-sm');
INSERT INTO "breakpoints" VALUES('bp-03','tablet_sm',576,767,2,1,'24px','axtra-responsive');
INSERT INTO "breakpoints" VALUES('bp-04','tablet_md',768,1024,2,2,'32px','elementor-tablet');
INSERT INTO "breakpoints" VALUES('bp-05','laptop_nav_collapse',1025,1199,3,2,'40px','header-mobile-drawer');
INSERT INTO "breakpoints" VALUES('bp-06','desktop_std',1200,1365,3,2,'48px','axtra-desktop');
INSERT INTO "breakpoints" VALUES('bp-07','desktop_wide',1366,1919,4,2,'64px','elementor-widescreen');
CREATE TABLE button_catalog (
  button_id TEXT PRIMARY KEY,
  theme_id TEXT NOT NULL REFERENCES design_themes(theme_id),
  selector TEXT NOT NULL,
  name TEXT NOT NULL,
  dimensions TEXT NOT NULL,
  border_radius TEXT NOT NULL,
  border_spec TEXT NOT NULL,
  resting_bg TEXT NOT NULL,
  hover_bg TEXT NOT NULL,
  resting_text TEXT NOT NULL,
  hover_text_wcag TEXT NOT NULL,
  transition_css TEXT NOT NULL,
  js_hover_behavior TEXT NOT NULL,
  a11y_notes TEXT NOT NULL
);
INSERT INTO "button_catalog" VALUES('btn-01','dark-kinetic-emerald','.wc-btn-primary.btn-hover.btn-item','Circular Radial-Fill & Magnetic Outline CTA','170x170px (inside 250/220/190/180/175px .btn_wrapper)','100% (circle)','1px solid #2C2C2C (hover #3BC77B)','transparent','#3BC77B (20px->350px cursor-origin span fill)','#C2C2C2 (i rotated -45deg)','#020617','outer: all 0.3s; inner radial span: all 0.7s','mouseenter/mouseout repositions inner 20px circle span to cursor coords and expands to 350px; .btn_wrapper mousemove pulls button +/-80px via gsap.to(0.5s, power2.out)','Preserve native <a>/<button> focus ring (#3BC77B); disable 80px magnetic offset on coarse pointers & reduced-motion.');
INSERT INTO "button_catalog" VALUES('btn-02','dark-kinetic-emerald','.wc-btn-secondary, .wc-btn-pink, .wc-btn-light','Secondary / Variant Circular Magnetic CTAs','170x170px','100% (circle)','1px solid #2C2C2C','transparent','Variant radial span (#FFFFFF / accent)','#999999 -> #C2C2C2','#020617 / #121212','all 0.3s; inner span: all 0.7s','Shares .btn-hover cursor-origin radial circle + .btn_wrapper GSAP magnetic pull.','Avoid un-highlighted #999999 resting text on dark backgrounds; enforce >= 4.5:1 text contrast.');
INSERT INTO "button_catalog" VALUES('btn-03','dark-kinetic-emerald','.hfe-menu-item.elementor-button','Header Emerald-Outlined Pill CTA','~182x50px','46px (30.66px variant)','1px solid #61CE70 / #96DEA0','transparent','#3BC77B','#FFFFFF','#020617','color/background/border 200ms cubic-bezier(0.16,1,0.3,1)','Pinned right side of 90px top navigation bar; collapses into mobile drawer trigger < 1200px.','Min height >= 50px satisfies WCAG touch size; ensure clear focus outline on dark translucent headers.');
INSERT INTO "button_catalog" VALUES('btn-04','dark-kinetic-emerald','.wc-btn-dark','Dark Rounded Action Pill','padding: 20px 54px','33px','1.3px solid #121212','transparent / light contrast','#FFFFFF','#121212 (15px uppercase)','#121212 on #FFFFFF','all 0.3s','High-contrast rectangular pill hover invert used on alternate light/card surfaces.','Confirm resting parent background contrast if placed inside dark sections.');
INSERT INTO "button_catalog" VALUES('btn-05','dark-kinetic-emerald','.filter-button','MixItUp Category Filter Pill','height: 44px; width: 39-172px','5px','none (recommended 1px solid #2C2C2C)','transparent','#65BC7B (active)','#FFFFFF','#020617 (fixed from #FFFFFF)','background-color 200ms ease','Triggers declarative MixItUp filtering on 3-col dark portfolio grid.','Add aria-pressed + aria-live filtered count; fix white-on-#65BC7B contrast to #020617.');
INSERT INTO "button_catalog" VALUES('btn-06','dark-kinetic-emerald','.cursor-btn, .yt-btn','Oversized Video Lightbox Trigger Circle','250x250px','100% (circle)','none (subtle ring optional)','rgba(255, 255, 255, 0.04)','rgba(59, 199, 123, 0.14)','#FFFFFF','#FFFFFF','transform/opacity 200ms cubic-bezier(0.16,1,0.3,1)','Opens full-screen modal lightbox (#modal_testimonial, toggling .modal-show).','Expose aria-label=''Play showcase video''; use native <dialog> focus trap + Escape close.');
CREATE TABLE color_tokens (
  token_id TEXT PRIMARY KEY,
  theme_id TEXT NOT NULL REFERENCES design_themes(theme_id),
  token_group TEXT NOT NULL,
  css_var TEXT NOT NULL,
  hex_value TEXT NOT NULL,
  raw_observed_value TEXT NOT NULL,
  wcag_role TEXT NOT NULL,
  contrast_on_dark REAL NOT NULL,
  usage_notes TEXT NOT NULL
);
INSERT INTO "color_tokens" VALUES('col-01','dark-kinetic-emerald','accent','--color-accent-primary','#3BC77B','rgb(59, 199, 123)','primary-action',10.3,'Primary CTA radial hover fill, marquee strip background, cursor ring');
INSERT INTO "color_tokens" VALUES('col-02','dark-kinetic-emerald','accent','--color-accent-pill','#61CE70','rgb(97, 206, 112)','cta-border',10.1,'Header 46px-radius pill CTA 1px outline stroke');
INSERT INTO "color_tokens" VALUES('col-03','dark-kinetic-emerald','accent','--color-accent-soft','#96DEA0','rgb(150, 222, 160)','secondary-border',12.6,'Light emerald highlight pill border variant');
INSERT INTO "color_tokens" VALUES('col-04','dark-kinetic-emerald','accent','--color-filter-active','#65BC7B','rgb(101, 188, 123)','active-filter',9.0,'Active portfolio/catalog MixItUp category filter pill fill');
INSERT INTO "color_tokens" VALUES('col-05','dark-kinetic-emerald','surface','--surface-canvas','#000000','#000','bg-primary',1.0,'Full-bleed OLED black section and hero backdrop');
INSERT INTO "color_tokens" VALUES('col-06','dark-kinetic-emerald','surface','--surface-base','#0A0A0A','rgb(10, 10, 10)','bg-secondary',1.04,'Alternate deep obsidian section background');
INSERT INTO "color_tokens" VALUES('col-07','dark-kinetic-emerald','surface','--surface-card','#121212','#121212','card-surface',1.12,'Card tile surface, dark button stroke, and dark wrapper (--black-2)');
INSERT INTO "color_tokens" VALUES('col-08','dark-kinetic-emerald','surface','--surface-elevated','#1E1E1E','rgb(30, 30, 30)','surface-elevated',1.25,'Map land tint, subtle raised strips, background grid rule');
INSERT INTO "color_tokens" VALUES('col-09','dark-kinetic-emerald','text','--text-primary','#FFFFFF','#fff','text-primary',21.0,'Primary display headlines and high-emphasis body copy');
INSERT INTO "color_tokens" VALUES('col-10','dark-kinetic-emerald','text','--text-secondary','#C2C2C2','#c2c2c2','text-secondary',11.5,'Body copy, descriptions, and circular CTA labels (--gray)');
INSERT INTO "color_tokens" VALUES('col-11','dark-kinetic-emerald','text','--text-muted','#A8A8A8','#a8a8a8','text-muted',8.7,'WCAG AAA metadata captions replacing unstyled #6B6B6B/#212529');
INSERT INTO "color_tokens" VALUES('col-12','dark-kinetic-emerald','text','--text-on-accent','#020617','#000000','text-on-accent',9.9,'High-contrast dark text rendered over emerald #3BC77B/#65BC7B');
INSERT INTO "color_tokens" VALUES('col-13','dark-kinetic-emerald','border','--border-subtle','#2C2C2C','#2c2c2c','border-subtle',1.4,'Hairline 1px section dividers, row rules, circular CTA outlines (--secondary)');
INSERT INTO "color_tokens" VALUES('col-14','dark-kinetic-emerald','surface','--surface-dropdown','#FFFFFF','#fff','dropdown-surface',21.0,'Light dropdown / mega-menu drawer surface paired with #121212 links');
CREATE TABLE component_patterns (
  component_id TEXT PRIMARY KEY,
  theme_id TEXT NOT NULL REFERENCES design_themes(theme_id),
  name TEXT NOT NULL,
  category TEXT NOT NULL,
  dimensions TEXT NOT NULL,
  border_radius TEXT NOT NULL,
  border_spec TEXT NOT NULL,
  background_spec TEXT NOT NULL,
  text_spec TEXT NOT NULL,
  interaction_spec TEXT NOT NULL,
  a11y_requirements TEXT NOT NULL,
  slot_schema_json TEXT NOT NULL
);
INSERT INTO "component_patterns" VALUES('cmp-01','dark-kinetic-emerald','Overlay Navbar with Char-Wave & Emerald Pill CTA','navigation','width: 100%; height: 90px','0px (wrapper), 46px (CTA pill)','1px solid #1E1E1E bottom hairline; 1px solid #61CE70 CTA border','rgba(0, 0, 0, 0.92); #FFFFFF dropdown menus','#FFFFFF links; #121212 dropdown items','Sticky class toggles past 20px scroll; char-wave hover (0.4s ease, 0.05s/char stagger); dropdown slides to top:75px; < 1200px mobile drawer','Skip link before nav; aria-expanded on dropdown triggers; Escape key closes submenus','{"slots": ["{{brand_logo_svg}}", "{{nav_links[]}}", "{{dropdown_items[]}}", "{{primary_cta_label}}"]}');
INSERT INTO "component_patterns" VALUES('cmp-02','dark-kinetic-emerald','Circular Radial-Fill & Magnetic Outline CTA','cta','170x170px in 250px wrapper','100% (circle)','1px solid #2C2C2C (hover #3BC77B)','transparent -> #3BC77B radial fill (20->350px in 0.7s)','#C2C2C2 -> #020617','Cursor-origin radial emerald circle expansion (0.7s) + +/-80px magnetic GSAP pull (0.5s power2.out)','Clear emerald focus-visible ring; disable magnetic pull on coarse pointers & reduced motion','{"slots": ["{{cta_label}}", "{{cta_href}}", "{{icon_arrow}}"]}');
INSERT INTO "component_patterns" VALUES('cmp-03','dark-kinetic-emerald','Circular Video Modal & Cursor Play Trigger','media-trigger','250x250px (.cursor-btn/.yt-btn)','100% (circle)','1px solid #2C2C2C / subtle translucent ring','rgba(255, 255, 255, 0.04)','#FFFFFF','Centered play glyph opening modal lightbox (.modal-show); paired desktop-only .cursor-testi 80->100px ''Play'' circle','aria-label=''Play showcase video''; native <dialog> modal restores trigger focus','{"slots": ["{{video_url}}", "{{poster_image}}", "{{trigger_aria_label}}"]}');
INSERT INTO "component_patterns" VALUES('cmp-04','dark-kinetic-emerald','Emerald Full-Bleed Swiper Marquee Strip','ticker','height: 108px, width: 100%','0px','none','#3BC77B','#000000 / #020617 (21px, weight 700)','Swiper freemode loop (.roll__slider speed:2000ms autoplay delay:1, breakpoints 1/3/4/5/8 slides)','Pause on hover/focus + explicit pause control; static chip grid under reduced-motion','{"slots": ["{{ticker_keywords[]}}"]}');
INSERT INTO "component_patterns" VALUES('cmp-05','dark-kinetic-emerald','Sticky 15deg Preview + Ribbon-Wipe Service Row','service-list','Row min-height: 120px; sticky 4-col left','0px','1px solid #2C2C2C row separators','#000000','#FFFFFF title (36px); #C2C2C2 summary (16px)','Row hover rotates preview image from -100px to rotate(15deg) translate(60px,30px) in 0.5s + 175x70px -26deg green ribbon span in 0.3s','Mirror mouse hover state on :focus-visible; avoid un-cleared setInterval mousemove handlers','{"slots": ["{{index_num}}", "{{service_title}}", "{{service_summary}}", "{{preview_img}}", "{{detail_href}}"]}');
INSERT INTO "component_patterns" VALUES('cmp-06','dark-kinetic-emerald','Oversized Bounce-Drop Count-Up Stat Block','metric','4-col desktop / 2x2 mobile','0px','1px solid #2C2C2C grid frame','#000000 / #0A0A0A','#FFFFFF numeral (100px w400 tabular-nums); #C2C2C2 label','Drops from y:-100 via GSAP bounce easing (1.5s, stagger 0.3s) + counter digit roll','Expose final value in aria-label; skip bounce & count-up under reduced motion','{"slots": ["{{metric_value}}", "{{metric_suffix}}", "{{metric_label}}", "{{metric_scope_note}}"]}');
INSERT INTO "component_patterns" VALUES('cmp-07','dark-kinetic-emerald','MixItUp Filter Pill & Velocity-Skew Portfolio Card','portfolio-card','Pills height 44px; Cards 29%/48.5%/100%','5px pills; 8px thumbnail','1px solid #2C2C2C inactive pills','#65BC7B active pill; #121212 card wrapper','#FFFFFF title (24px); #C2C2C2 vertical tag','Filter buttons filter grid; scroll velocity skews images -15..15deg; hover slides .portfolio__content-5 right:-70->-50px (0.5s)','Use dark #020617 ink on active #65BC7B pills; mirror overlay slide on :focus-within','{"slots": ["{{category_slug}}", "{{category_label}}", "{{project_title}}", "{{thumbnail_webp}}", "{{case_study_href}}"]}');
INSERT INTO "component_patterns" VALUES('cmp-08','dark-kinetic-emerald','8-Card Bordered Capability Tile','feature-card','4-col desktop / 2-col tablet / 1-col mobile','8px','1px solid #2C2C2C','#121212','#FFFFFF heading (22px); #C2C2C2 copy (14px)','ScrollTrigger vertical entry (.animation__feature2 y:40->0 power4.out stagger 0.3s); subtle border highlight','Semantic H3 under H2; SVG icons inherit currentColor','{"slots": ["{{icon_svg}}", "{{feature_title}}", "{{feature_description}}"]}');
INSERT INTO "component_patterns" VALUES('cmp-09','dark-kinetic-emerald','SVG Interactive Coverage Map + Country Marquee','geo-coverage','aspect-[2/1] SVG map + horizontal marquee','0px','none','#000000 canvas, #1E1E1E landmasses, #3BC77B active regions','#FFFFFF tooltip; #C2C2C2 labels','Hovering landmass reveals active region highlight and floating tooltip card','Pair with accessible semantic <ul> list of supported markets for keyboard & AT access','{"slots": ["{{active_region_codes[]}}", "{{region_names[]}}"]}');
INSERT INTO "component_patterns" VALUES('cmp-10','dark-kinetic-emerald','Pre-Footer Consultation Band & 4-Col Footer','footer','Pre-footer band + 4-col footer grid','100% CTA circle','1px solid #2C2C2C top divider','#121212 pre-footer; #000000 footer','#FFFFFF headings; #C2C2C2 links & contact info','Footer links transition smoothly to #3BC77B; bottom text-shadow hover mirrors .menu-text','Single semantic <footer> landmark; >= 44x44px social hit areas','{"slots": ["{{prefooter_headline}}", "{{kpi_pills[]}}", "{{footer_columns[4]}}", "{{copyright_notice}}"]}');
INSERT INTO "component_patterns" VALUES('cmp-11','dark-kinetic-emerald','Dual Difference-Blend Cursor & Contextual Followers','cursor','.cursor1 40px ring / .cursor2 8->60px dot','50%','1px solid #3BC77B (.cursor1)','#3BC77B (.cursor2) / #FFFFFF (#featured_cursor)','inherit / #FFFFFF (.cursor-testi.play)','Desktop (>1200px) mousemove tracks clientX/Y via GSAP power2.out/power4.out with contextual labels on galleries & video posters','Hidden <= 1200px, pointer-events: none; never replaces semantic buttons or focusable targets','{"slots": ["{{cursor_label}}"]}');
INSERT INTO "component_patterns" VALUES('cmp-12','dark-kinetic-emerald','Character-Wave Stacked Text-Shadow Menu Link','nav-effect','inline span stack, lh 16px, py 29px','0px','none','transparent','#FFFFFF (18px, text-shadow: 0 16px 0 #FFFFFF)','JS splits characters into spans shifting translateY over 0.4s ease with +0.05s incremental nth-child delay up to 1.5s','Disable cascade under prefers-reduced-motion; maintain clean focus-visible ring','{"slots": ["{{menu_label}}"]}');
INSERT INTO "component_patterns" VALUES('cmp-13','dark-kinetic-emerald','Dark Rounded Action Pill (.wc-btn-dark)','cta','padding: 20px 54px','33px','1.3px solid #121212','transparent / #FFFFFF hover','#121212 resting -> #121212 on #FFFFFF (15px uppercase)','Inverts fill and border to #FFFFFF on hover over 0.3s','Ensure high contrast resting surface when placed on dark bands','{"slots": ["{{pill_label}}", "{{pill_href}}"]}');
INSERT INTO "component_patterns" VALUES('cmp-14','dark-kinetic-emerald','ScrollTrigger Pinned Title & Sidebar Wrapper','layout-motion','column sticky track','0px','1px solid #2C2C2C','#000000 / #121212','#FFFFFF title; #C2C2C2 copy','ScrollTrigger pin (.portfolio__title-wrap-6, .job__detail-sidebar) holds header/sidebar while sibling grid scrolls cleanly','Ensure scroll-margin-top prevents obscured focusable links; release pin safely on mobile widths','{"slots": ["{{pinned_title}}", "{{scrolling_items[]}}"]}');
CREATE TABLE design_themes (
  theme_id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  mode TEXT NOT NULL,
  kit_style_ref TEXT NOT NULL,
  primary_accent TEXT NOT NULL,
  background_base TEXT NOT NULL,
  surface_raised TEXT NOT NULL,
  border_subtle TEXT NOT NULL,
  heading_font TEXT NOT NULL,
  body_font TEXT NOT NULL,
  notes TEXT NOT NULL
);
INSERT INTO "design_themes" VALUES('dark-kinetic-emerald','Dark Kinetic Emerald Agency','dark','Dark Kinetic Emerald','#3BC77B','#000000','#121212','#2C2C2C','Poppins','Kanit','Dark OLED canvas paired with ScrollSmoother (1.35), data-speed parallax, SplitText rotationX (-80deg) reveals, 170px radial/magnetic CTAs, char-wave nav links, 15deg diagonal service previews, and 100px bounce counters.');
CREATE TABLE motion_specs (
  motion_id TEXT PRIMARY KEY,
  theme_id TEXT NOT NULL REFERENCES design_themes(theme_id),
  name TEXT NOT NULL,
  library TEXT NOT NULL,
  trigger_type TEXT NOT NULL,
  target_selector TEXT NOT NULL,
  duration_ms INTEGER NOT NULL,
  stagger_s REAL NOT NULL,
  easing TEXT NOT NULL,
  properties_json TEXT NOT NULL,
  reduced_motion_fallback TEXT NOT NULL
);
INSERT INTO "motion_specs" VALUES('mot-01','dark-kinetic-emerald','ScrollSmoother Continuous Inertia','GSAP ScrollSmoother','document scroll','#smooth-wrapper / document',0,0.0,'linear','{"smooth": 1.35, "smoothTouch": false, "effectsMinWidthPx": 1025, "ignoreMobileResize": true, "snapSections": false}','Disable ScrollSmoother completely when prefers-reduced-motion: reduce or pointer: coarse');
INSERT INTO "motion_specs" VALUES('mot-02','dark-kinetic-emerald','Differential data-speed Image & Shape Parallax','GSAP ScrollSmoother Effects','continuous scroll','[data-speed], .axtra_parallax_image img',0,0.0,'linear','{"observedSpeeds": [0.2, 0.3, 0.5, 0.9], "dataLag": 0, "willChange": "transform"}','Strip data-speed transform offsets when prefers-reduced-motion: reduce or < 1025px');
INSERT INTO "motion_specs" VALUES('mot-03','dark-kinetic-emerald','Scroll-Velocity Portfolio Y-Skew','GSAP ScrollSmoother + quickTo','scroll velocity update/stop','.portfolio__item-5 img',0,0.0,'linear','{"velocityDivisor": -80, "clampDeg": [-15, 15], "onStop": "skewY(0)"}','Keep skewY statically at 0deg under prefers-reduced-motion');
INSERT INTO "motion_specs" VALUES('mot-04','dark-kinetic-emerald','Scroll-Scrubbed Image Scale Zooms','GSAP ScrollTrigger Scrub','scroll progress','.about__img-2 img / .portfolio__item-6 img',1000,0.0,'linear','{"aboutImg2": {"scale": [1, 1.15], "scrub": 1, "start": "top bottom", "end": "bottom center"}, "portfolioImg6": {"fromScale": 2.5, "toScale": 1, "scrub": 1.5, "start": "top center"}}','Render static final scale(1) with zero scrub scaling under reduced motion');
INSERT INTO "motion_specs" VALUES('mot-05','dark-kinetic-emerald','Line-by-Line SplitText 3D Headline Reveal','GSAP SplitText + ScrollTrigger','scroll-enter (top 90%)','.title-anim',1000,0.1,'power2.out','{"splitBy": "words, lines", "perspective": 400, "delayS": 0.3, "rotationXDeg": -80, "force3D": true, "transformOrigin": "top center -50", "toggleActions": "play none none none"}','Render headline immediately at opacity: 1 and rotationX: 0 under reduced motion');
INSERT INTO "motion_specs" VALUES('mot-06','dark-kinetic-emerald','Line-by-Line SplitText Paragraph Fold','GSAP SplitText + ScrollTrigger','scroll-enter (top 90%)','.text-anim p',1000,0.1,'power2.out','{"splitBy": "lines", "perspective": 400, "delayS": 0.5, "rotationXDeg": -80, "force3D": true, "transformOrigin": "top center -50"}','Render paragraph immediately with zero 3D transform under reduced motion');
INSERT INTO "motion_specs" VALUES('mot-07','dark-kinetic-emerald','Char & Word Slide-In Typography Reveals','GSAP SplitText','section entrance','.animation__char_come, .animation__char_come_long, .animation__word_come, .animation__word_up',1000,0.05,'power2.out','{"charCome": {"x": 70, "stagger": 0.05}, "charComeLong": {"x": 70, "stagger": 0.15}, "wordCome": {"x": 50, "stagger": 0.05}, "wordUp": {"y": 50, "stagger": 0.05}}','Render split text immediately at opacity: 1 without translate offsets under reduced motion');
INSERT INTO "motion_specs" VALUES('mot-08','dark-kinetic-emerald','Randomized Word Pop & Char Back-Out Tilt','GSAP SplitText + ScrollTrigger','scroll-enter (top 100%)','.text-anim-top, .sec-title-3',2000,0.1,'back.out','{"textAnimTop": {"scaleChoices": [0, 2], "randomDelay": true}, "secTitle3": {"rotateDeg": 20, "durationS": 2, "ease": "back.out"}}','Render static visible typography under reduced motion');
INSERT INTO "motion_specs" VALUES('mot-09','dark-kinetic-emerald','Section Block Vertical Fade-Up Stagger','GSAP ScrollTrigger','scroll-enter (top center+=300)','.fade_bottom, .fade_bottom_2..5',1000,0.2,'power2.out','{"fromY": 30, "desktopStaggerS": 0.2, "mobilePerItemTrigger": "< 1023px (1.5s at top center+=200)"}','Show section children immediately at opacity: 1 under reduced motion');
INSERT INTO "motion_specs" VALUES('mot-10','dark-kinetic-emerald','Workflow Left Slide-In Stagger','GSAP ScrollTrigger','scroll-enter (top center+=300)','.fade_left',1000,0.2,'power2.out','{"fromX": -20, "fromOpacity": 0}','Disable horizontal entrance slide under reduced motion');
INSERT INTO "motion_specs" VALUES('mot-11','dark-kinetic-emerald','Home Numbered Service Row Sequenced Reveal','GSAP Timeline + ScrollTrigger','scroll-enter (top center+=300)','.animation_home1_service (number, title, text, link)',1200,0.2,'power2.out','{"fromX": -50, "fromOpacity": 0, "timelineOverlap": "-=1"}','Render service rows immediately visible under reduced motion');
INSERT INTO "motion_specs" VALUES('mot-12','dark-kinetic-emerald','Service Pillars & Workflow Horizontal Reveal','GSAP ScrollTrigger','scroll-enter (top center+=200)','.animation__service-2, .animation_service_7, .workflow__item-4, .animation__service_page',2000,0.4,'power2.out','{"fromX": [-30, -50], "fromOpacity": 0, "responsiveBreakpoint": 1023}','Disable directional entrance transition under reduced motion');
INSERT INTO "motion_specs" VALUES('mot-13','dark-kinetic-emerald','Section Media Scale-Up & Feature Rise','GSAP ScrollTrigger','scroll-enter (top center+=200)','.zoom_in, .animation_image_zoom img, .animation__feature2 .feature__item',1000,0.2,'power4.out','{"zoomIn": {"y": 30, "scale": 0.5}, "testimonialZoom": {"scale": 0.5, "x": 20, "durationS": 2.5}, "feature2": {"yDesktop": 40, "yMobile": 60, "staggerS": 0.3}}','Render cards/images at scale(1) and opacity: 1 immediately');
INSERT INTO "motion_specs" VALUES('mot-14','dark-kinetic-emerald','Counter & CTA Bounce Drop Entrances','GSAP ScrollTrigger','scroll-enter (top center+=150..300)','.counter_animation .counter__anim, #btn_wrapper, .btn_wrapper',1500,0.3,'bounce','{"counterFromY": -100, "buttonFromY": -70, "skipHeroButtonClass": "hero__button"}','Avoid bounce overshoot under reduced motion; use instant reveal');
INSERT INTO "motion_specs" VALUES('mot-15','dark-kinetic-emerald','Editorial Blog Card Horizontal Slide-In','GSAP ScrollTrigger','scroll-enter (top center+=300)','.blog__animation .blog__item, .blog__item-2, .blog__item-3',2000,0.3,'power2.out','{"fromX": 50, "mobileDurationS": 1.5}','Display editorial cards immediately without x-offset slide');
INSERT INTO "motion_specs" VALUES('mot-16','dark-kinetic-emerald','Radial Cursor-Origin Fill + Magnetic CTA Parallax','jQuery/JS + GSAP','mouseenter / mousemove / mouseout','.btn-hover span + .btn_wrapper -> .btn-item',500,0.0,'power2.out','{"radialSpanPx": [20, 350], "radialDurationS": 0.7, "outerDurationS": 0.3, "magneticMovePx": 80, "magneticEase": "power2.out"}','Disable magnetic coordinate tracking; keep crisp border/fill transition on focus & hover');
INSERT INTO "motion_specs" VALUES('mot-17','dark-kinetic-emerald','Header Character-Wave Text-Shadow Hover & Dropdown','JS Char Split + CSS Transition','nav link hover','.menu-anim > li > a .menu-text span + .main-dropdown',400,0.05,'ease','{"textShadowYOffsetPx": 16, "perCharDelayStepS": 0.05, "maxChars": 30, "dropdownTopPx": 75}','Disable per-character vertical delay cascade under reduced motion');
INSERT INTO "motion_specs" VALUES('mot-18','dark-kinetic-emerald','Sticky Service Preview 15deg Tilt + -26deg Ribbon Wipe','jQuery + CSS Transform/Opacity','row hover / focus-visible','.service__item -> .service__img + span.current',500,0.0,'ease','{"resting": "rotate(0deg) translateX(-100px)", "active": "rotate(15deg) translateX(60px) translateY(30px)", "ribbonSpan": {"size": "175x70px", "active": "rotate(-26deg) translate(120px,-100%)", "durationS": 0.3, "delayS": 0.2}}','Instant opacity crossfade + mirror hover state on :focus-visible; replace un-cleared setInterval');
INSERT INTO "motion_specs" VALUES('mot-19','dark-kinetic-emerald','Portfolio Floating Caption Slide Reveal','CSS Transition','card hover / focus-within','.portfolio__item-5:hover .portfolio__content-5',500,0.0,'ease','{"restingRightPx": -70, "hoverRightPx": -50, "mobileAlwaysVisible": "<=767px right:0 opacity:1"}','Mirror :hover visibility on :focus-within for keyboard access');
INSERT INTO "motion_specs" VALUES('mot-20','dark-kinetic-emerald','Dual Mix-Blend Cursors, Contextual Rings, Pins & Sticky Bar','GSAP Timeline + ScrollTrigger','mousemove / scroll','.cursor1/.cursor2, #client_cursor, #featured_cursor, .portfolio__title-wrap-6, .job__detail-sidebar',150,0.0,'power4.out','{"cursor1": "40px 1px #3BC77B 0.15s difference", "cursor2": "8->60px 0.2s difference", "clientPlayCursor": "80->100px", "cursorHidden": "<=1200px", "stickyThresholdPx": 20}','Hide custom pointer overlays on coarse pointers/reduced motion; keep semantic pin layout non-overlapping');
INSERT INTO "motion_specs" VALUES('mot-21','dark-kinetic-emerald','Emerald Marquee Continuous FreeMode Ticker','Swiper.js','continuous autoplay','.roll__slider, .roll__slider2',2000,0.0,'linear','{"rollSlider": {"speedMs": 2000, "delayMs": 1, "freemode": true, "breakpoints": {"640": 3, "1024": 4, "1300": 5, "1900": 8}}, "rollSlider2": {"speedMs": 10000, "spaceBetween": 60}}','Pause marquee autoplay and wrap chips statically under prefers-reduced-motion');
CREATE TABLE page_section_slots (
  slot_id TEXT PRIMARY KEY,
  page_id TEXT NOT NULL REFERENCES page_templates(page_id),
  position INTEGER NOT NULL,
  section_id TEXT NOT NULL REFERENCES section_templates(section_id),
  layout_variant TEXT NOT NULL,
  sample_slots_json TEXT NOT NULL
);
INSERT INTO "page_section_slots" VALUES('ps-01','tpl-01',1,'sec-01','dark-overlay','{"slots": ["{{brand_logo}}", "{{nav_links[6]}}", "{{pill_cta}}"]}');
INSERT INTO "page_section_slots" VALUES('ps-02','tpl-01',2,'sec-02','asymmetric-98px-hero','{"slots": ["{{hero_eyebrow}}", "{{hero_h1}}", "{{hero_copy}}", "{{circle_cta}}", "{{video_modal_btn}}"]}');
INSERT INTO "page_section_slots" VALUES('ps-03','tpl-01',3,'sec-03','emerald-108px-marquee','{"slots": ["{{marquee_chips[]}}"]}');
INSERT INTO "page_section_slots" VALUES('ps-04','tpl-01',4,'sec-04','sticky-preview-numbered-rows','{"slots": ["{{services_intro}}", "{{service_rows[01..05]}}"]}');
INSERT INTO "page_section_slots" VALUES('ps-05','tpl-01',5,'sec-05','100px-countup-4col','{"slots": ["{{stat_1}}", "{{stat_2}}", "{{stat_3}}", "{{stat_4}}"]}');
INSERT INTO "page_section_slots" VALUES('ps-06','tpl-01',6,'sec-06','svg-world-map-ticker','{"slots": ["{{coverage_headline}}", "{{active_countries[]}}"]}');
INSERT INTO "page_section_slots" VALUES('ps-07','tpl-01',7,'sec-03','24-logo-monochrome-wall','{"slots": ["{{client_logos[24]}}"]}');
INSERT INTO "page_section_slots" VALUES('ps-08','tpl-01',8,'sec-08','video-modal-swiper','{"slots": ["{{testimonial_slides[]}}"]}');
INSERT INTO "page_section_slots" VALUES('ps-09','tpl-01',9,'sec-12','prefooter-form-4col-footer','{"slots": ["{{consultation_form}}", "{{footer_columns[4]}}"]}');
INSERT INTO "page_section_slots" VALUES('ps-10','tpl-02',1,'sec-01','dark-overlay','{"slots": ["{{brand_logo}}", "{{nav_links[6]}}", "{{pill_cta}}"]}');
INSERT INTO "page_section_slots" VALUES('ps-11','tpl-02',2,'sec-02','62px-manifesto-hero','{"slots": ["{{about_headline}}", "{{studio_video_trigger}}"]}');
INSERT INTO "page_section_slots" VALUES('ps-12','tpl-02',3,'sec-05','100px-countup-4col','{"slots": ["{{milestone_stats[4]}}"]}');
INSERT INTO "page_section_slots" VALUES('ps-13','tpl-02',4,'sec-03','24-logo-monochrome-wall','{"slots": ["{{client_logos[24]}}"]}');
INSERT INTO "page_section_slots" VALUES('ps-14','tpl-02',5,'sec-12','prefooter-form-4col-footer','{"slots": ["{{consultation_form}}", "{{footer_columns[4]}}"]}');
INSERT INTO "page_section_slots" VALUES('ps-15','tpl-03',1,'sec-01','dark-overlay','{"slots": ["{{brand_logo}}", "{{nav_links[6]}}", "{{pill_cta}}"]}');
INSERT INTO "page_section_slots" VALUES('ps-16','tpl-03',2,'sec-04','full-service-showcase-blocks','{"slots": ["{{practice_pillars[4..6]}}"]}');
INSERT INTO "page_section_slots" VALUES('ps-17','tpl-03',3,'sec-03','24-logo-monochrome-wall','{"slots": ["{{client_logos[24]}}"]}');
INSERT INTO "page_section_slots" VALUES('ps-18','tpl-03',4,'sec-12','prefooter-form-4col-footer','{"slots": ["{{consultation_form}}", "{{footer_columns[4]}}"]}');
INSERT INTO "page_section_slots" VALUES('ps-19','tpl-04',1,'sec-01','dark-overlay','{"slots": ["{{brand_logo}}", "{{nav_links[6]}}", "{{pill_cta}}"]}');
INSERT INTO "page_section_slots" VALUES('ps-20','tpl-04',2,'sec-02','110px-detail-hero','{"slots": ["{{service_title}}", "{{service_banner_img}}"]}');
INSERT INTO "page_section_slots" VALUES('ps-21','tpl-04',3,'sec-10','4col-subcapability-grid','{"slots": ["{{subcapabilities[]}}"]}');
INSERT INTO "page_section_slots" VALUES('ps-22','tpl-04',4,'sec-12','prefooter-form-4col-footer','{"slots": ["{{consultation_form}}", "{{footer_columns[4]}}"]}');
INSERT INTO "page_section_slots" VALUES('ps-23','tpl-05',1,'sec-01','dark-overlay','{"slots": ["{{brand_logo}}", "{{nav_links[6]}}", "{{pill_cta}}"]}');
INSERT INTO "page_section_slots" VALUES('ps-24','tpl-05',2,'sec-09','92px-hero-staggered-catalog','{"slots": ["{{catalog_headline}}", "{{product_cards[]}}"]}');
INSERT INTO "page_section_slots" VALUES('ps-25','tpl-05',3,'sec-12','prefooter-form-4col-footer','{"slots": ["{{consultation_form}}", "{{footer_columns[4]}}"]}');
INSERT INTO "page_section_slots" VALUES('ps-26','tpl-06',1,'sec-01','dark-overlay','{"slots": ["{{brand_logo}}", "{{nav_links[6]}}", "{{pill_cta}}"]}');
INSERT INTO "page_section_slots" VALUES('ps-27','tpl-06',2,'sec-02','100px-product-hero','{"slots": ["{{product_title}}", "{{product_mockup}}"]}');
INSERT INTO "page_section_slots" VALUES('ps-28','tpl-06',3,'sec-10','8-card-feature-matrix-portals','{"slots": ["{{core_features[8]}}", "{{extra_chips[6]}}", "{{portal_tabs[3]}}"]}');
INSERT INTO "page_section_slots" VALUES('ps-29','tpl-06',4,'sec-12','prefooter-form-4col-footer','{"slots": ["{{consultation_form}}", "{{footer_columns[4]}}"]}');
INSERT INTO "page_section_slots" VALUES('ps-30','tpl-07',1,'sec-01','dark-overlay','{"slots": ["{{brand_logo}}", "{{nav_links[6]}}", "{{pill_cta}}"]}');
INSERT INTO "page_section_slots" VALUES('ps-31','tpl-07',2,'sec-07','120px-mixitup-portfolio-grid','{"slots": ["{{filter_pills[]}}", "{{portfolio_cards[]}}"]}');
INSERT INTO "page_section_slots" VALUES('ps-32','tpl-07',3,'sec-03','24-logo-monochrome-wall','{"slots": ["{{client_logos[24]}}"]}');
INSERT INTO "page_section_slots" VALUES('ps-33','tpl-07',4,'sec-12','prefooter-form-4col-footer','{"slots": ["{{consultation_form}}", "{{footer_columns[4]}}"]}');
INSERT INTO "page_section_slots" VALUES('ps-34','tpl-08',1,'sec-01','dark-overlay','{"slots": ["{{brand_logo}}", "{{nav_links[6]}}", "{{pill_cta}}"]}');
INSERT INTO "page_section_slots" VALUES('ps-35','tpl-08',2,'sec-11','100px-dossier-challenge-solution','{"slots": ["{{meta_4col}}", "{{ui_gallery}}", "{{challenge_solution_split}}", "{{next_prev_dossier}}"]}');
INSERT INTO "page_section_slots" VALUES('ps-36','tpl-08',3,'sec-12','prefooter-cta-4col-footer','{"slots": ["{{prefooter_cta}}", "{{footer_columns[4]}}"]}');
INSERT INTO "page_section_slots" VALUES('ps-37','tpl-09',1,'sec-01','dark-overlay','{"slots": ["{{brand_logo}}", "{{nav_links[6]}}", "{{pill_cta}}"]}');
INSERT INTO "page_section_slots" VALUES('ps-38','tpl-09',2,'sec-03','72px-24-logo-wall','{"slots": ["{{clients_heading}}", "{{client_logos[24]}}"]}');
INSERT INTO "page_section_slots" VALUES('ps-39','tpl-09',3,'sec-05','100px-countup-4col','{"slots": ["{{impact_stats[4]}}"]}');
INSERT INTO "page_section_slots" VALUES('ps-40','tpl-09',4,'sec-12','prefooter-form-4col-footer','{"slots": ["{{consultation_form}}", "{{footer_columns[4]}}"]}');
INSERT INTO "page_section_slots" VALUES('ps-41','tpl-10',1,'sec-01','dark-overlay','{"slots": ["{{brand_logo}}", "{{nav_links[6]}}", "{{pill_cta}}"]}');
INSERT INTO "page_section_slots" VALUES('ps-42','tpl-10',2,'sec-04','72px-partner-benefit-tiers','{"slots": ["{{partner_headline}}", "{{benefit_cards[]}}"]}');
INSERT INTO "page_section_slots" VALUES('ps-43','tpl-10',3,'sec-12','prefooter-form-4col-footer','{"slots": ["{{partner_inquiry_form}}", "{{footer_columns[4]}}"]}');
INSERT INTO "page_section_slots" VALUES('ps-44','tpl-11',1,'sec-01','dark-overlay','{"slots": ["{{brand_logo}}", "{{nav_links[6]}}", "{{pill_cta}}"]}');
INSERT INTO "page_section_slots" VALUES('ps-45','tpl-11',2,'sec-02','110px-translucent-team-hero','{"slots": ["{{team_headline}}", "{{leadership_grid[]}}"]}');
INSERT INTO "page_section_slots" VALUES('ps-46','tpl-11',3,'sec-12','careers-cta-4col-footer','{"slots": ["{{careers_cta}}", "{{footer_columns[4]}}"]}');
INSERT INTO "page_section_slots" VALUES('ps-47','tpl-12',1,'sec-01','dark-overlay','{"slots": ["{{brand_logo}}", "{{nav_links[6]}}", "{{pill_cta}}"]}');
INSERT INTO "page_section_slots" VALUES('ps-48','tpl-12',2,'sec-04','72px-job-requisitions-list','{"slots": ["{{open_roles[]}}", "{{circle_apply_cta}}"]}');
INSERT INTO "page_section_slots" VALUES('ps-49','tpl-12',3,'sec-12','footer-4col','{"slots": ["{{footer_columns[4]}}"]}');
INSERT INTO "page_section_slots" VALUES('ps-50','tpl-13',1,'sec-01','dark-overlay','{"slots": ["{{brand_logo}}", "{{nav_links[6]}}", "{{pill_cta}}"]}');
INSERT INTO "page_section_slots" VALUES('ps-51','tpl-13',2,'sec-07','62px-3col-blog-grid-pagination','{"slots": ["{{article_cards[3col]}}", "{{circular_pagination}}"]}');
INSERT INTO "page_section_slots" VALUES('ps-52','tpl-13',3,'sec-12','footer-4col','{"slots": ["{{footer_columns[4]}}"]}');
INSERT INTO "page_section_slots" VALUES('ps-53','tpl-14',1,'sec-01','dark-overlay','{"slots": ["{{brand_logo}}", "{{nav_links[6]}}", "{{pill_cta}}"]}');
INSERT INTO "page_section_slots" VALUES('ps-54','tpl-14',2,'sec-12','84px-contact-2col-intake-footer','{"slots": ["{{office_placeholders}}", "{{intake_form}}", "{{footer_columns[4]}}"]}');
CREATE TABLE page_templates (
  page_id TEXT PRIMARY KEY,
  theme_id TEXT NOT NULL REFERENCES design_themes(theme_id),
  template_name TEXT NOT NULL,
  source_route_pattern TEXT NOT NULL,
  kit_page_id TEXT NOT NULL,
  desktop_section_count INTEGER NOT NULL,
  h1_size_px INTEGER NOT NULL,
  mobile_h1_size_px INTEGER NOT NULL,
  layout_notes TEXT NOT NULL
);
INSERT INTO "page_templates" VALUES('tpl-01','dark-kinetic-emerald','Home / Agency Flagship Landing','/','home',14,98,28,'Continuous ScrollSmoother (1.35) + data-speed (0.2-0.9) parallax across 14 bands: SplitText hero -> emerald marquee -> split intro -> 15deg sticky services -> quote -> bounce counters -> coverage map -> 24-logo wall -> video testimonials -> 3-col blog slide-in -> intake form -> footer');
INSERT INTO "page_templates" VALUES('tpl-02','dark-kinetic-emerald','About Company & Global Delivery','/about','about',8,62,42,'About manifesto header -> studio ethos + video modal -> marquee & scrub-zoom imagery -> bounce count-up milestones -> team highlights -> 24-logo wall -> consultation pre-footer -> footer');
INSERT INTO "page_templates" VALUES('tpl-03','dark-kinetic-emerald','Services Index Directory','/services','services',7,84,50,'Lead hero (84px) -> 4-5 vertical numbered service blocks (.animation_home1_service x:-50->0) with 170px radial CTAs & nested capability chips -> logo wall -> footer');
INSERT INTO "page_templates" VALUES('tpl-04','dark-kinetic-emerald','Service Practice Detail','/services/{{service_slug}}','service_detail',11,110,42,'110px display title -> hero banner -> layered technical breakdown -> 4-col sub-capabilities -> workflow__slider -> flip cards -> 24-logo wall -> intake footer');
INSERT INTO "page_templates" VALUES('tpl-05','dark-kinetic-emerald','Software Products Catalog','/products','product_showcase',4,92,52,'92px catalog H1 + staggered thumbnail showcase strip -> 2/3-col dark product card grid -> pre-footer intake -> footer');
INSERT INTO "page_templates" VALUES('tpl-06','dark-kinetic-emerald','Product / SaaS Platform Detail','/products/{{product_slug}}','product_detail',9,100,48,'100px product H1 -> banner -> 8-card feature matrix (.animation__feature2) -> 6 feature chips -> multi-portal capabilities -> 3-col differentiators -> intake footer');
INSERT INTO "page_templates" VALUES('tpl-07','dark-kinetic-emerald','Projects / Portfolio Filter Hub','/projects','case_studies',4,120,82,'120px index H1 -> MixItUp 44px filter pills (#65BC7B active) + 3-col dark project grid with scroll velocity skewY & hover overlay -> logo wall -> footer');
INSERT INTO "page_templates" VALUES('tpl-08','dark-kinetic-emerald','Case Study Dossier Detail','/projects/{{project_slug}}','case_study_detail',14,100,48,'100px project H1 -> scrub hero UI mockup -> 4-col meta grid -> Challenge/Solution split -> feature cards + screen gallery slider -> circular CTA + outcome metrics -> Next/Prev nav -> footer');
INSERT INTO "page_templates" VALUES('tpl-09','dark-kinetic-emerald','Clients & Impact Wall','/clients','case_studies',5,72,42,'72px client headline -> 24-tile monochrome client wall -> 100px bounce count-up impact stats -> video/executive testimonials -> pre-footer intake -> footer');
INSERT INTO "page_templates" VALUES('tpl-10','dark-kinetic-emerald','Technology & Solution Partners','/partners','about',6,72,38,'72px partnership headline -> partner model banner -> tier benefit cards -> workflow showcase -> partnership intake form -> footer');
INSERT INTO "page_templates" VALUES('tpl-11','dark-kinetic-emerald','Leadership & Engineering Team','/team','about',8,110,52,'110px translucent editorial H1 -> multi-tier portrait grid with cursor follow -> visual culture banner -> careers CTA band -> footer');
INSERT INTO "page_templates" VALUES('tpl-12','dark-kinetic-emerald','Careers & Open Positions','/careers','careers',2,72,42,'Centered careers intro + radial circular CTA -> 72px Open Positions header + bold 28px job listing cards + pinned job sidebar -> footer');
INSERT INTO "page_templates" VALUES('tpl-13','dark-kinetic-emerald','Editorial Insights & Engineering Blog','/blog','blog',2,62,62,'62px Blog heading -> 3-column article grid (.blog__item-3 horizontal x:50->0 slide, underline links) + 60px circular pagination -> footer');
INSERT INTO "page_templates" VALUES('tpl-14','dark-kinetic-emerald','Contact & Consultation Intake','/contact','contact',3,84,50,'84px contact hero -> 2-column office & channels details + consultation form with 170px radial magnetic submit CTA -> footer');
CREATE TABLE section_templates (
  section_id TEXT PRIMARY KEY,
  theme_id TEXT NOT NULL REFERENCES design_themes(theme_id),
  name TEXT NOT NULL,
  kit_section_id TEXT NOT NULL,
  kit_archetype_id TEXT NOT NULL,
  component_refs_json TEXT NOT NULL,
  layout_css TEXT NOT NULL,
  responsive_rules TEXT NOT NULL,
  slot_schema_json TEXT NOT NULL,
  anti_slop_notes TEXT NOT NULL
);
INSERT INTO "section_templates" VALUES('sec-01','dark-kinetic-emerald','Dark Overlay Navigation Header with Char-Wave','navbar','nav-07','["cmp-01", "cmp-12"]','90px overlay header toggling sticky state >20px scroll, char-wave text-shadow links (0.05s/char stagger), white dropdowns (top:75px), and 46px emerald-outlined CTA pill.','1200px collapse to mobile hamburger drawer; wave pauses on reduced motion','{"brand_logo": "{{brand_mark}}", "nav_links": ["{{link_1}}", "{{link_2}}", "{{link_3}}"], "cta_label": "{{primary_cta}}"}','Use keyboard-accessible button disclosures instead of hover-only menus.');
INSERT INTO "section_templates" VALUES('sec-02','dark-kinetic-emerald','Kinetic Display Hero with Radial/Magnetic CTAs','hero','hero-11','["cmp-02", "cmp-03", "cmp-11"]','Dark canvas inside ScrollSmoother (1.35 factor, data-speed 0.3-0.9 imagery) opening with SplitText rotationX(-80deg) headline, 170px radial-fill/magnetic CTA (0.7s/0.5s), and 250px video trigger.','H1 scales down to 28-44px at 375px; effects disabled <1025px; cursors hidden <=1200px','{"eyebrow": "{{eyebrow}}", "headline": "{{hero_headline}}", "summary": "{{hero_summary}}", "cta_text": "{{circle_cta}}"}','Enforce >= 7:1 text contrast and disable 3D rotation/magnetic tracking under reduced motion.');
INSERT INTO "section_templates" VALUES('sec-03','dark-kinetic-emerald','Swiper Emerald Marquee + 24-Logo Wall','trusted_by','tb-07','["cmp-04"]','108px #3BC77B Swiper freemode marquee (speed:2000ms/10000ms, delay:1) above 6x4 dark monochrome client grid entering with .fade_bottom (y:30 stagger 0.2s).','Swiper slides 1->3->4->5->8; grid 6->3->2 columns','{"marquee_items": ["{{capability_1}}", "{{capability_2}}"], "heading": "{{trust_heading}}", "logo_slots": ["{{client_svg_01}}..{{client_svg_24}}"]}','Normalize client marks to uniform height and monochrome finish.');
INSERT INTO "section_templates" VALUES('sec-04','dark-kinetic-emerald','Sticky 15deg Preview + Ribbon-Wipe Service List','services','srv-09','["cmp-05", "cmp-02"]','Left sticky preview rotates to 15deg translate(60px,30px) in 0.5s with -26deg 175x70px green ribbon sweep; right rows enter sequentially x:-50->0 (.animation_home1_service).','Below 1024px hides sticky preview frame and shows clean inline list','{"section_title": "{{services_heading}}", "services": [{"num": "01", "title": "{{srv_title}}", "desc": "{{srv_desc}}"}]}','Replace un-cleared mousemove setInterval leaks with CSS classes mirrored on :focus-visible.');
INSERT INTO "section_templates" VALUES('sec-05','dark-kinetic-emerald','Oversized 100px Bounce Count-Up Metrics Band','results_metrics','res-07','["cmp-06"]','4-column strip entering with bounce drop (y:-100->0, 1.5s, stagger 0.3s) showcasing 100px tabular-nums counters above short descriptors.','4 cols desktop -> 2x2 grid <768px','{"stats": [{"value": "{{stat_num}}", "suffix": "+", "label": "{{stat_label}}"}]}','Include audited measurement scope note and never fabricate live telemetry.');
INSERT INTO "section_templates" VALUES('sec-06','dark-kinetic-emerald','Interactive Geo Coverage Map & Country Ticker','contact_location_map','cmap-03','["cmp-09", "cmp-04"]','SVG world map highlighting delivery regions in #3BC77B on #1E1E1E landmasses above horizontal country marquee.','Proportional aspect-[2/1] scaling on mobile','{"section_title": "{{geo_heading}}", "regions": ["{{region_01}}", "{{region_02}}"]}','Pair SVG map with semantic region list for screen-reader accessibility.');
INSERT INTO "section_templates" VALUES('sec-07','dark-kinetic-emerald','MixItUp Portfolio Grid with Velocity SkewY & Slide Badge','portfolio','port-09','["cmp-07", "cmp-14"]','MixItUp 44px 5px-radius filter pills controlling 3-col cards that skewY (-15..15deg) on fast scroll and slide card labels right:-70->-50px on hover.','3 cols (29%) -> 2 cols (48.5%) -> 1 col (100% with label pinned visible)','{"filters": ["{{filter_all}}", "{{filter_industry}}"], "items": [{"title": "{{case_title}}", "tag": "{{industry_tag}}", "img": "{{thumb}}"}]}','Pair active #65BC7B pills with #020617 ink and announce count via aria-live=''polite''.');
INSERT INTO "section_templates" VALUES('sec-08','dark-kinetic-emerald','Video-Modal Testimonial Carousel with Cursor Play','testimonials','tst-09','["cmp-03", "cmp-11"]','Swiper stage pairing zoom-in video poster (.animation_image_zoom scale 0.5->1 + +/-15px pointer parallax) and .cursor-testi ''Play'' overlay beside executive quote.','Video poster stacks over quote card mobile; cursor hides <=1200px','{"slides": [{"quote": "{{quote_text}}", "role": "{{speaker_role}}", "video_poster": "{{poster_url}}"}]}','Provide closed captions or transcript inside accessible <dialog> modal.');
INSERT INTO "section_templates" VALUES('sec-09','dark-kinetic-emerald','Staggered Software Product Catalog Grid','product_catalog_grid','pcg-01','["cmp-07", "cmp-02"]','Multi-product showcase pairing staggered horizontal showcase strip with 2/3-col product cards linking to deep-dive pages.','3 cols -> 2 cols -> 1 col','{"products": [{"title": "{{product_name}}", "category": "{{category}}", "preview": "{{ui_mockup}}"}]}','Limit each product card to one primary interactive link covering title & preview.');
INSERT INTO "section_templates" VALUES('sec-10','dark-kinetic-emerald','8-Card Capability & Multi-Portal Matrix','product_feature_matrix','pfm-01','["cmp-08", "cmp-13"]','Modular 4x2 feature card grid entering vertically (.animation__feature2) + 6 secondary chips + 3-col differentiators + role switcher tabs.','4 cols -> 2 cols -> 1 col','{"features": ["{{feat_1}}..{{feat_8}}"], "chips": ["{{chip_1}}..{{chip_6}}"], "portals": ["User", "Branch", "Admin"]}','Never duplicate cards across separate mobile/desktop markup trees.');
INSERT INTO "section_templates" VALUES('sec-11','dark-kinetic-emerald','Case Study Dossier: Meta, Challenge/Solution & Nav','case_study_dossier','csd-01','["cmp-08", "cmp-02", "cmp-14"]','3-part project dossier: 4-col metadata grid -> full-bleed scrub-zoom UI banner -> 2-col Challenge vs Solution split, feature carousel & Next/Prev nav.','4-col meta -> 2x2 mobile; 2-col split stacks <768px','{"meta": {"industry": "{{ind}}", "services": "{{srv}}", "stack": "{{stack}}", "year": "{{year}}"}, "challenge": "{{challenge}}", "solution": "{{solution}}"}','Document concrete engineering choices rather than generic claims.');
INSERT INTO "section_templates" VALUES('sec-12','dark-kinetic-emerald','Pre-Footer Consultation Band & 4-Col Footer','footer','ftr-07','["cmp-10", "cmp-02", "cmp-12"]','Upper pre-footer callout with data-speed=''0.2'' backdrop imagery, 3 proof stats & embedded intake form above 4-col footer.','4 cols -> 2 cols tablet -> 1 col mobile','{"prefooter_title": "{{cta_headline}}", "columns": ["{{col_brand}}", "{{col_nav}}", "{{col_contact}}", "{{col_legal}}"]}','Ensure all footer copy exceeds 4.5:1 contrast on #000000.');
CREATE TABLE typography_tokens (
  type_id TEXT PRIMARY KEY,
  theme_id TEXT NOT NULL REFERENCES design_themes(theme_id),
  role TEXT NOT NULL,
  html_tag TEXT NOT NULL,
  font_family TEXT NOT NULL,
  font_weight TEXT NOT NULL,
  desktop_size_px INTEGER NOT NULL,
  desktop_line_height_px INTEGER NOT NULL,
  mobile_size_px INTEGER NOT NULL,
  fluid_clamp TEXT NOT NULL,
  selector_hint TEXT NOT NULL,
  usage_notes TEXT NOT NULL
);
INSERT INTO "typography_tokens" VALUES('typ-01','dark-kinetic-emerald','display_index_h1','h1','Poppins','500',120,120,52,'clamp(3rem, 1.5rem + 5.5vw, 7.5rem)','h1.portfolio__title','Oversized index showcase hero headline');
INSERT INTO "typography_tokens" VALUES('typ-02','dark-kinetic-emerald','display_detail_h1','h1','Poppins','500',110,121,42,'clamp(2.625rem, 1.5rem + 4.5vw, 6.875rem)','h1.service__detail-title','Detail dossier hero H1 across service, product, and team routes');
INSERT INTO "typography_tokens" VALUES('typ-03','dark-kinetic-emerald','display_counter','h2','Poppins','400',100,110,48,'clamp(3rem, 1.8rem + 4.2vw, 6.25rem)','.counter__number','Light-weight oversized count-up telemetry numerals with tabular-nums');
INSERT INTO "typography_tokens" VALUES('typ-04','dark-kinetic-emerald','display_home_h1','h1','Poppins','500',98,115,28,'clamp(2.25rem, 1.4rem + 4.2vw, 6.125rem)','.hero__title-3','Asymmetrical kinetic landing hero H1 with SplitText line reveal');
INSERT INTO "typography_tokens" VALUES('typ-05','dark-kinetic-emerald','display_catalog_h1','h1','Poppins','600',92,98,44,'clamp(2.75rem, 1.6rem + 4vw, 5.75rem)','h1.catalog-hero','Product showcase directory H1');
INSERT INTO "typography_tokens" VALUES('typ-06','dark-kinetic-emerald','display_lead_h1','h1','Poppins','500',84,84,42,'clamp(2.625rem, 1.6rem + 3.5vw, 5.25rem)','h1.page-lead','Services and Contact primary header headline');
INSERT INTO "typography_tokens" VALUES('typ-07','dark-kinetic-emerald','page_heading_secondary','h1','Poppins','600',72,72,38,'clamp(2.375rem, 1.5rem + 3vw, 4.5rem)','h1.page-secondary','Clients, Partners, and Careers lead section heading');
INSERT INTO "typography_tokens" VALUES('typ-08','dark-kinetic-emerald','section_heading','h3','Poppins','500',60,60,32,'clamp(2rem, 1.4rem + 2.5vw, 3.75rem)','.sec-title','Primary section display heading');
INSERT INTO "typography_tokens" VALUES('typ-09','dark-kinetic-emerald','service_row_heading','h3','Poppins','500',36,43,24,'clamp(1.5rem, 1.2rem + 1.2vw, 2.25rem)','.service__title-2, .service__title-7','Numbered hover service list & detail service block titles');
INSERT INTO "typography_tokens" VALUES('typ-10','dark-kinetic-emerald','card_heading','h3','Poppins','500',24,32,20,'1.5rem','.portfolio__title-5, .blog__title','Product, case-study, and editorial article card headings');
INSERT INTO "typography_tokens" VALUES('typ-11','dark-kinetic-emerald','marquee_item','h2','Poppins','700',21,25,18,'1.3125rem','.roll__slide h2','Full-bleed accent marquee capability label');
INSERT INTO "typography_tokens" VALUES('typ-12','dark-kinetic-emerald','body_copy','p','Kanit','400',16,24,16,'1rem','body, p','Readable geometric-humanist sans-serif body text');
INSERT INTO "typography_tokens" VALUES('typ-13','dark-kinetic-emerald','caption_meta','span','Poppins','400',14,20,14,'0.875rem','.testimonial__role, .portfolio__name-5','Role subtitle, category tag, and metadata caption');
CREATE VIEW v_page_blueprints AS
SELECT
  p.page_id,
  p.template_name,
  p.source_route_pattern,
  p.kit_page_id,
  s.position,
  s.section_id,
  st.name AS section_name,
  st.kit_archetype_id,
  s.layout_variant,
  s.sample_slots_json
FROM page_templates p
JOIN page_section_slots s ON s.page_id = p.page_id
JOIN section_templates st ON st.section_id = s.section_id
ORDER BY p.page_id, s.position;
COMMIT;
