---
name: static-site-audit-remediation
version: 1.0.0
description: Use when auditing a live site and fixing its repo code.
tags: [web, seo, accessibility, tailwind, github-pages, code-review]
---

# Static Site Audit & Remediation

End-to-end review of a deployed site plus application of recommended fixes to its local repository (not just a report). Common triggers: "review my website", "improve my portfolio site's code", "audit and fix <url>".

## Workflow

1. **Audit the LIVE deployment first** — `curl -s <url> -o /tmp/site.html` plus its stylesheet; never review only rendered text (hydration/inline styles/build output differ from source).
2. **Compute contrast ratios programmatically** (relative luminance formula) for every Tailwind gray/blue pair used — don't eyeball them.
3. **Locate the local repo** BEFORE proposing to edit. Check likely Desktop/Documents folders first (`portfolio-site`, `portfolio-*` patterns) rather than asking the user where it lives.
4. **Verify external claims via API** — e.g. list the user's GitHub repos (`api.github.com/users/<u>/repos`) before changing project links; never link to repos that don't exist publicly. If no matching repo exists, link to the profile's repository list as placeholder and tell the user.
5. **Apply patches** one at a time with the `patch` tool; after multi-edit runs on structured markup, re-read the section to confirm no card/element got swallowed by an overlapping match.
6. **Rebuild generated assets** if the repo has a build step (e.g. Tailwind CLI: `node node_modules/tailwindcss/lib/cli.js -i ./src/input.css -o ./assets/styles.css --minify`) and grep the OUTPUT file to confirm new rules landed.
7. **Check git status before committing** — `git diff -w --stat` reveals line-ending-only churn (CRLF noise); revert unrelated files so the commit contains intended changes only. Consider `core.autocrlf false`.
8. **Commit** (set repo-local `user.name`/`user.email` if unset).
9. **Push or hand off**: attempt push once; if credential interop fails (common from sandboxed environments), commit locally and give the user the one-click instruction (GitHub Desktop → Push origin) — do not retry auth loops.

## Common high-value findings checklist

- Masked/redacted values left in production hrefs (`tel:+155****3725`) — compare visible text vs href
- Repeated identical link text pointing at different URLs (WCAG SC 2.4.4) → distinct text + `sr-only` context note
- Inline `<style>` fighting a CSS build pipeline → move into `src/input.css` `@layer base`
- Missing `<link rel="canonical">`, `sitemap.xml`; JSON-LD email should have no `mailto:` prefix
- Print stylesheet absent → `@media print { nav, footer { display:none } }` + print URLs after external links
- Duplicate phrasing ("over 150+") and duty-flavored summary copy

## Pitfalls

- Tailwind builds wipe hand-edited `assets/styles.css` — always edit `src/input.css`, then run the build.
- Multi-card grids: a too-wide old_string can delete a neighboring card's opening tags; verify element counts after each structural edit.
- Node/npm binaries may be Windows-flavored (.cmd shims fail in Linux shell) — invoke the package's JS entry directly with node.
