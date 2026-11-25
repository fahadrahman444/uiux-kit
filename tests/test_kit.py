#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unit & adversarial verification suite for SlopGuard / Gemini UI/UX Kit:
- Verifies all 19 rules in audit_engine.py (A11Y-001..008, TOKEN-001..002, PERF-001..003, SLOP-001..006)
- Verifies TypeScript AST wrapper resolution & comment immunity
- Verifies multi-file CSS variable & class resolution across separate CSS + TSX files
- Verifies .designrc.json blocker protection & 90-day time-boxed waivers
- Verifies kit components + demo host app pass 100/100 (--strict)
- Verifies Phase 5 Golden-Set evaluation average >= 95/100
"""

import json
import sys
import tempfile
import unittest
from pathlib import Path

KIT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(KIT_ROOT / "scripts"))
sys.path.insert(0, str(KIT_ROOT / "skills" / "ui-ux-pro-max" / "scripts"))

import audit_engine  # noqa: E402
import eval_golden_set  # noqa: E402
import generate_section_prompt as gsp  # noqa: E402


class AuditEngineTestSuite(unittest.TestCase):
    def test_kit_components_and_demo_pass_strict(self):
        payload, exit_code = audit_engine.run_audit(
            [KIT_ROOT / "components", KIT_ROOT / "apps" / "demo" / "src"],
            strict=True,
        )
        self.assertEqual(payload["analyzerMode"], "typescript-ast+multifile-css")
        self.assertEqual(payload["rulesEnabled"], 19)
        self.assertEqual(payload["summary"]["score"], 100, msg=json.dumps(payload["results"], indent=2))
        self.assertEqual(exit_code, 0)

    def test_all_19_rules_and_multifile_wrapper_detection(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)

            # Multi-file tokens + low contrast + sub-24px class + ::backdrop blur
            (root / "theme.css").write_text(
                ":root {\n"
                "  --bad-muted: #CBD5E1;\n"
                "  --bad-bg: #FFFFFF;\n"
                "}\n"
                ".tiny-btn { height: 18px; width: 18px; }\n"
                ".low-contrast-card { color: var(--bad-muted); background-color: var(--bad-bg); }\n"
                ".raw-hex-box { color: #123456; }\n"
                "@keyframes spinFast { to { transform: rotate(360deg); } }\n"
                "dialog { transition: opacity 200ms; }\n"
                "dialog::backdrop { backdrop-filter: blur(8px); }\n",
                encoding="utf-8",
            )

            # Wrapper component file
            (root / "IconWrapper.tsx").write_text(
                "import React from 'react';\n"
                "export const IconWrapper = ({ children }: { children?: React.ReactNode }) => (\n"
                "  <button type='button' className='p-2'>{children}</button>\n"
                ");\n",
                encoding="utf-8",
            )

            # Violation fixture page 1
            (root / "PageOne.tsx").write_text(
                "import React, { useState } from 'react';\n"
                "import { motion } from 'framer-motion';\n"
                "import { IconWrapper } from './IconWrapper';\n"
                "export function PageOne() {\n"
                "  const [pos, setPos] = useState(0);\n"
                "  const activeStep = 1;\n"
                "  return (\n"
                "    <div className='min-h-screen bg-white text-slate-300 mt-[13px]' onMouseMove={(e) => setPos(e.clientX)}>\n"
                "      <header className='sticky top-0'><a href='/help'>Help</a><a href='/faq'>FAQ</a></header>\n"
                "      <section id='overview'>\n"
                "        <div className='bg-purple-600 blur-3xl' />\n"
                "        <span className='uppercase'>One</span><span className='uppercase'>Two</span>\n"
                "        <h1>Build <em>fast</em></h1>\n"
                "        <div className='grid grid-cols-3 gap-4'><div>99.9%</div></div>\n"
                "        <button type='button' className='tiny-btn outline-none animate-pulse bg-[#112233]'>\n"
                "          <svg viewBox='0 0 24 24'><path stroke='#ff0000' d='M0 0' /></svg>\n"
                "        </button>\n"
                "        <button type='button'>🚀</button>\n"
                "        <IconWrapper />\n"
                "        <p className='low-contrast-card'>Muted</p>\n"
                "        <motion.div className='backdrop-blur animate-fade' animate={{ opacity: 1 }} />\n"
                "        <img src='/hero.png' alt='Hero' />\n"
                "        <iframe title='Embed' src='https://example.com' />\n"
                "        <form><input name='email' /></form>\n"
                "      </section>\n"
                "    </div>\n"
                "  );\n"
                "}\n",
                encoding="utf-8",
            )

            # Violation fixture page 2 (divergent help order -> A11Y-007)
            (root / "PageTwo.tsx").write_text(
                "import React from 'react';\n"
                "export const PageTwo = () => (\n"
                "  <nav><a href='/faq'>FAQ</a><a href='/help'>Help</a></nav>\n"
                ");\n",
                encoding="utf-8",
            )

            payload, exit_code = audit_engine.run_audit([root], strict=True)
            found_rules = {r["ruleId"] for r in payload["results"]}
            expected_all_19 = set(audit_engine.RULES.keys())
            missing = sorted(expected_all_19 - found_rules)
            self.assertEqual(missing, [], msg=f"Rules did not trigger: {missing}\nFound: {sorted(found_rules)}")
            self.assertEqual(exit_code, 2)

            # Verify wrapper call site in PageOne.tsx was specifically flagged for A11Y-002
            wrapper_hits = [
                r for r in payload["results"]
                if r["ruleId"] == "A11Y-002" and r["file"] == "PageOne.tsx" and "IconWrapper" in r["message"]
            ]
            self.assertTrue(wrapper_hits, msg="Expected AST cross-file wrapper violation on <IconWrapper />")

            # Verify multi-file CSS class height violation on PageOne.tsx
            css_size_hits = [
                r for r in payload["results"]
                if r["ruleId"] == "A11Y-001" and r["file"] == "PageOne.tsx" and "tiny-btn" in r["message"]
            ]
            self.assertTrue(css_size_hits, msg="Expected multi-file CSS class A11Y-001 hit on .tiny-btn")

    def test_comments_ignored_and_waivers_and_blocker_guard(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / ".designrc.json").write_text(
                json.dumps({"rules": {"SLOP-001": "off", "TOKEN-002": "warn"}}),
                encoding="utf-8",
            )
            (root / ".design").mkdir()
            (root / ".design" / "audit-baseline.json").write_text(
                json.dumps({
                    "waivers": [
                        {
                            "ruleId": "TOKEN-001",
                            "file": "Waived.tsx",
                            "expiresAt": "2099-01-01T00:00:00Z",
                        },
                        {
                            "ruleId": "TOKEN-001",
                            "file": "Expired.tsx",
                            "expiresAt": "2020-01-01T00:00:00Z",
                        },
                    ]
                }),
                encoding="utf-8",
            )
            (root / "Waived.tsx").write_text(
                "import React from 'react';\n"
                "// radial-gradient(#6366f1) filter: blur(80px)\n"
                "{/* <button>🚀</button> */}\n"
                "export const Waived = () => <div className='bg-[#123456]'>Ok</div>;\n",
                encoding="utf-8",
            )
            (root / "Expired.tsx").write_text(
                "import React from 'react';\n"
                "export const Expired = () => <div className='bg-[#123456]'>Expired</div>;\n",
                encoding="utf-8",
            )

            payload, _ = audit_engine.run_audit([root], strict=False)
            overrides = {o["ruleId"]: o for o in payload["configOverrides"]}
            self.assertTrue(overrides["SLOP-001"]["rejected"])
            self.assertEqual(overrides["SLOP-001"]["effective"], "blocker")

            files_flagged = {(r["ruleId"], r["file"]) for r in payload["results"]}
            self.assertNotIn(("SLOP-001", "Waived.tsx"), files_flagged)
            self.assertNotIn(("TOKEN-001", "Waived.tsx"), files_flagged)
            self.assertIn(("TOKEN-001", "Expired.tsx"), files_flagged)


class PromptAndGoldenTestSuite(unittest.TestCase):
    def test_all_9_pages_generate_cleanly(self):
        pages = ["home", "pricing", "about", "services", "case_studies", "contact", "blog", "careers", "legal"]
        for pg in pages:
            out = gsp.generate_master_prompt({"page_id": pg, "project_name": f"Test {pg}", "style": "Editorial Minimalist"})
            self.assertIn("# Master Production-Grade UI/UX Blueprint", out)
            self.assertEqual(gsp.fallback_warnings, [])

    def test_golden_set_meets_95_threshold(self):
        avg, results = eval_golden_set.run_evaluation()
        self.assertEqual(len(results), 30)
        self.assertGreaterEqual(avg, 95.0, msg=f"Golden set avg {avg:.2f} < 95.0")


if __name__ == "__main__":
    unittest.main()
