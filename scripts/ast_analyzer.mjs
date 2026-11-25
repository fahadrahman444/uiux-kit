#!/usr/bin/env node
/**
 * SlopGuard TypeScript AST Analyzer
 * Uses the official TypeScript compiler API to parse TSX/JSX/TS/JS files,
 * track cross-file component wrappers, and emit accurate AST nodes/attributes
 * (ignoring comments and non-JSX string literals).
 */

import fs from "node:fs";
import path from "node:path";
import ts from "typescript";

const inputPayload = JSON.parse(fs.readFileSync(0, "utf8"));
const files = Array.isArray(inputPayload.files) ? inputPayload.files : [];

const EMOJI_RE = /[\u{1F300}-\u{1FAFF}]/u;

function getLineCol(sf, pos) {
  const { line, character } = sf.getLineAndCharacterOfPosition(pos);
  return { line: line + 1, column: character + 1 };
}

function getTagName(node) {
  return node.tagName ? node.tagName.getText() : "";
}

function extractAttrString(attr) {
  if (!attr.initializer) return { present: true, value: "", isDynamic: false };
  if (ts.isStringLiteral(attr.initializer) || ts.isNoSubstitutionTemplateLiteral(attr.initializer)) {
    return { present: true, value: attr.initializer.text, isDynamic: false };
  }
  if (ts.isJsxExpression(attr.initializer) && attr.initializer.expression) {
    const expr = attr.initializer.expression;
    if (ts.isStringLiteral(expr) || ts.isNoSubstitutionTemplateLiteral(expr)) {
      return { present: true, value: expr.text, isDynamic: false };
    }
    return { present: true, value: expr.getText(), isDynamic: true };
  }
  return { present: true, value: attr.initializer.getText(), isDynamic: true };
}

function collectJsxTextAndChildren(node) {
  let textParts = [];
  let hasSvg = false;
  let hasDynamicChild = false;
  let hasSrOnly = false;
  let hasNonSvgChildElement = false;
  let hasEmojiInChildren = null;

  function walkChild(child) {
    if (ts.isJsxText(child)) {
      const cleaned = child.getText().replace(/\s+/g, " ").trim();
      if (cleaned) {
        textParts.push(cleaned);
        const em = EMOJI_RE.exec(cleaned);
        if (em && !hasEmojiInChildren) hasEmojiInChildren = em[0];
      }
      return;
    }
    if (ts.isJsxExpression(child)) {
      if (child.expression) {
        const txt = child.expression.getText();
        const em = EMOJI_RE.exec(txt);
        if (em && !hasEmojiInChildren) hasEmojiInChildren = em[0];
        if (child.expression.kind !== ts.SyntaxKind.JsxEmptyExpression) {
          hasDynamicChild = true;
        }
      }
      return;
    }
    if (ts.isJsxElement(child) || ts.isJsxSelfClosingElement(child)) {
      const opening = ts.isJsxElement(child) ? child.openingElement : child;
      const t = getTagName(opening);
      if (t.toLowerCase() === "svg" || /icon$/i.test(t)) {
        hasSvg = true;
      } else {
        hasNonSvgChildElement = true;
      }
      for (const prop of opening.attributes.properties) {
        if (ts.isJsxAttribute(prop) && prop.name.getText() === "className") {
          const v = extractAttrString(prop).value;
          if (v.includes("sr-only")) hasSrOnly = true;
        }
      }
      if (ts.isJsxElement(child)) {
        child.children.forEach(walkChild);
      }
    }
  }

  if (ts.isJsxElement(node)) {
    node.children.forEach(walkChild);
  }

  return {
    text: textParts.join(" ").trim(),
    hasSvg,
    hasDynamicChild,
    hasSrOnly,
    hasNonSvgChildElement,
    hasEmojiInChildren,
  };
}

// Pass 1: Discover wrapper components across all JS/TS/JSX/TSX files
// A component is an interactive wrapper if it renders <button> or <a> (or delegates to one)
const parsedFiles = [];
const wrapperRegistry = {};

for (const entry of files) {
  const absPath = entry.absPath;
  const relPath = entry.relPath;
  const sourceText = fs.readFileSync(absPath, "utf8");
  const scriptKind =
    absPath.endsWith(".tsx")
      ? ts.ScriptKind.TSX
      : absPath.endsWith(".jsx")
      ? ts.ScriptKind.JSX
      : absPath.endsWith(".ts")
      ? ts.ScriptKind.TS
      : ts.ScriptKind.JS;

  const sf = ts.createSourceFile(absPath, sourceText, ts.ScriptTarget.Latest, true, scriptKind);
  parsedFiles.push({ absPath, relPath, sourceText, sf });

  function inspectComponentDef(name, bodyNode) {
    if (!name || !/^[A-Z]/.test(name) || !bodyNode) return;
    let rendersButton = false;
    let rendersAnchor = false;
    let spreadsProps = false;
    let forwardsAriaLabel = false;
    let rendersChildren = false;
    let hasFixedLabel = false;

    function walkDef(n) {
      if (ts.isJsxOpeningElement(n) || ts.isJsxSelfClosingElement(n)) {
        const tag = getTagName(n);
        if (tag === "button") rendersButton = true;
        if (tag === "a") rendersAnchor = true;
        for (const prop of n.attributes.properties) {
          if (ts.isJsxSpreadAttribute(prop)) spreadsProps = true;
          if (ts.isJsxAttribute(prop)) {
            const pname = prop.name.getText();
            if (pname === "aria-label" || pname === "aria-labelledby" || pname === "title") {
              const info = extractAttrString(prop);
              if (info.isDynamic && /aria|label|title/i.test(info.value)) {
                forwardsAriaLabel = true;
              } else if (!info.isDynamic && info.value.trim()) {
                hasFixedLabel = true;
              }
            }
          }
        }
      } else if (ts.isJsxExpression(n) && n.expression) {
        const txt = n.expression.getText();
        if (/\bchildren\b|\blabel\b/.test(txt)) rendersChildren = true;
      }
      ts.forEachChild(n, walkDef);
    }

    walkDef(bodyNode);
    if (rendersButton || rendersAnchor) {
      wrapperRegistry[name] = {
        file: relPath,
        kind: rendersButton ? "button" : "a",
        spreadsProps,
        forwardsAriaLabel,
        rendersChildren,
        hasFixedLabel,
      };
    }
  }

  function walkTop(n) {
    if (ts.isFunctionDeclaration(n) && n.name && n.body) {
      inspectComponentDef(n.name.text, n.body);
    } else if (ts.isVariableStatement(n)) {
      for (const decl of n.declarationList.declarations) {
        if (ts.isIdentifier(decl.name) && decl.initializer) {
          if (ts.isArrowFunction(decl.initializer) || ts.isFunctionExpression(decl.initializer)) {
            inspectComponentDef(decl.name.text, decl.initializer.body);
          }
        }
      }
    }
    ts.forEachChild(n, walkTop);
  }
  walkTop(sf);
}

// Pass 2: Extract structured AST facts per file
const perFileAnalysis = {};

for (const { relPath, sourceText, sf } of parsedFiles) {
  const jsxElements = [];
  const mouseMoveStateUpdates = [];
  const imports = [];
  let usesReducedMotionHook = /\buseReducedMotion\b/.test(sourceText);
  let hasMultiStepHint = /\b(activeStep|currentStep|stepIndex|wizardStep)\b/.test(sourceText);
  let hasFormElement = false;
  let hasAutocompleteInput = false;
  let hasStickyBar = false;
  let hasAnchorSection = false;
  let hasScrollMarginClass = false;
  const helpLinks = [];
  const metricTokens = [];

  function walk(node) {
    if (ts.isImportDeclaration(node) && node.moduleSpecifier && ts.isStringLiteral(node.moduleSpecifier)) {
      imports.push(node.moduleSpecifier.text);
    }

    if (ts.isJsxElement(node) || ts.isJsxSelfClosingElement(node)) {
      const opening = ts.isJsxElement(node) ? node.openingElement : node;
      const tag = getTagName(opening);
      const pos = getLineCol(sf, opening.getStart(sf));
      const attrs = {};
      let hasSpread = false;

      for (const prop of opening.attributes.properties) {
        if (ts.isJsxSpreadAttribute(prop)) {
          hasSpread = true;
        } else if (ts.isJsxAttribute(prop)) {
          attrs[prop.name.getText()] = extractAttrString(prop);
        }
      }

      const classVal = attrs.className?.value || attrs.class?.value || "";
      if (/\b(?:sticky\s+top-0|fixed\s+bottom-0)\b/.test(classVal)) {
        hasStickyBar = true;
      }
      if ((tag === "section" || tag === "div") && attrs.id?.present) {
        hasAnchorSection = true;
        if (/\bscroll-mt-|\bscroll-pt-/.test(classVal)) {
          hasScrollMarginClass = true;
        }
      }
      if (tag === "form") hasFormElement = true;
      if (tag === "input" || tag === "select" || tag === "textarea") {
        if (attrs.autoComplete?.present || attrs.autocomplete?.present) {
          hasAutocompleteInput = true;
        }
      }

      // Check onMouseMove React state setter inside JSX
      if (attrs.onMouseMove?.present && /\bset[A-Z]\w*\(/.test(attrs.onMouseMove.value)) {
        mouseMoveStateUpdates.push({
          ...pos,
          expr: attrs.onMouseMove.value.slice(0, 80),
        });
      }

      const childSummary = collectJsxTextAndChildren(node);

      if ((tag === "a" || tag === "button") && /^(help|contact|faq|support)$/i.test(childSummary.text)) {
        helpLinks.push(childSummary.text.toLowerCase());
      }

      const isWrapper = Boolean(wrapperRegistry[tag]) || /^(IconButton|ActionButton|CtaButton|NavButton|LinkButton)$/.test(tag);
      const isInteractive = tag === "button" || tag === "a" || isWrapper;

      jsxElements.push({
        tag,
        isInteractive,
        isWrapper,
        wrapperMeta: wrapperRegistry[tag] || null,
        hasSpread,
        line: pos.line,
        column: pos.column,
        className: classVal,
        attrs,
        children: childSummary,
      });
    }

    // Collect numeric/KPI metric literals inside JSX text or object properties
    if (ts.isJsxText(node)) {
      const t = node.getText().trim();
      if (/^(?:\+?\d+(?:\.\d+)?%|\d+x|\$\d+[KMB]?\+?)$/i.test(t)) {
        const pos = getLineCol(sf, node.getStart(sf));
        metricTokens.push({ ...pos, value: t });
      }
    }

    ts.forEachChild(node, walk);
  }

  walk(sf);

  perFileAnalysis[relPath] = {
    jsxElements,
    mouseMoveStateUpdates,
    imports,
    usesReducedMotionHook,
    hasMultiStepHint,
    hasFormElement,
    hasAutocompleteInput,
    hasStickyBar,
    hasAnchorSection,
    hasScrollMarginClass,
    helpLinks,
    metricTokens,
    hasVerificationCitation: /\b(footnote|sourceNote|source|verified|citation|audit|dateRange|cite|figcaption)\b/i.test(sourceText),
    hasPricingContext: /\b(pricing|tier|plan|popular|billing|subscription|comparison|colSpan|bento|chart)\b/i.test(sourceText),
  };
}

process.stdout.write(
  JSON.stringify({
    wrappers: wrapperRegistry,
    files: perFileAnalysis,
  })
);
