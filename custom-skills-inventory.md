# Custom Skills Inventory — Hermes Agent

Generated: 2026-08-25

Inventory of all skills that are **custom to this agent** (i.e., *not* bundled with Hermes). Determined by diffing every `SKILL.md` on disk against the bundled manifest (`~/.hermes/skills/.bundled_manifest`).

- **Total custom skills:** 42
- **Bundled (shipped with Hermes):** 82
- **Total on disk:** 124

---

## 🔬 Research & Academic Writing
| Skill | Purpose |
|---|---|
| `prisma-systematic-review` | Run PRISMA systematic reviews with a 6-agent pipeline |
| `prisma-review-output` | Store PRISMA scoping-review pipeline output files |
| `prisma-review-harassment-minority-students` | Scoping review of harassment of minority US students |
| `research-design-orchestrator` | Design a study end-to-end via 4 interactive stages |
| `research-question-framer` | Turn a broad topic into an answerable research question |
| `evaluation-method-selector` | Pick a study methodology grounded in current journals |
| `study-measures-and-sampling` | Validated measures, sampling plan, sample size |
| `study-protocol-builder` | Compile full study protocol with .docx conversion |
| `qualitative-literature-review` | Batch qualitative lit reviews with theme tracking |
| `public-health-evaluation-planning` | Design public health evaluation plans (CDC framework) |
| `research-literature-monitor` | Monitor academic feeds (PubMed, Crossref, RSS) |
| `research-report-packaging` | Convert research md → .docx, audit a11y, package |

## ♿ Accessibility Agents (Section 508 / WCAG)
| Skill | Purpose |
|---|---|
| `docx-accessibility-agent` | .docx 508/WCAG review |
| `pdf-accessibility-agent` | .pdf 508/WCAG review |
| `pptx-accessibility-agent` | .pptx 508/WCAG review |
| `email-accessibility-agent` | Email 508 review |
| `social-media-accessibility-agent` | Social content 508 review |
| `website-accessibility-agent` | Website WCAG 2.2 audit |

## ✍️ Style & Formatting Agents
| Skill | Purpose |
|---|---|
| `apa-7-style-agent` | APA 7th Edition audit/revise |
| `ap-stylebook-agent` | AP Stylebook audit/revise |
| `writing-style-agent` | Apply personal writing style |
| `powerpoint-style-agent` | PowerPoints in personal style |

## 📡 Monitoring & Automation
| Skill | Purpose |
|---|---|
| `job-board-rss-monitor` | Job boards without RSS via sitemap discovery |
| `rss_feed_monitoring` | RSS monitoring (arXiv, news, job boards) |
| `web-content-monitor` | Monitor sites without RSS via sitemaps |
| `workflow-orchestrator` | Multi-skill pipelines: plan, delegate, verify, package |

## 📧 Outlook / Email Tooling
| Skill | Purpose |
|---|---|
| `outlook-mcp-server` | Outlook MCP server (email, calendar, tasks, contacts) |
| `outlook-mcp-server-project` | Build complete Outlook MCP server w/ full project files |
| `azure-ad-app-registration` | Azure AD app registration for Graph API |

## 📥 Media & Web Downloads
| Skill | Purpose |
|---|---|
| `album-media-downloader` | Download all media from album/gallery URLs |
| `batch-web-gallery-download` | Batch-download from multiple gallery/album URLs |
| `web-media-download` | Bulk-download images/videos from a webpage |

## ⚖️ Legal
| Skill | Purpose |
|---|---|
| `paralegal-assistant` | Court cases, dockets, rulings, amicus briefs (CourtListener) |

## 🎨 Creative / Media Software (local)
| Skill | Purpose |
|---|---|
| `excalidraw-chart-reconstructor` | Rebuild chart images as editable Excalidraw scenes |
| `davinci-resolve-free-local` | Prepare Resolve Free edits via local file interchange |
| `gimp-local` | Automate GIMP 3 via batch-safe Script-Fu jobs |
| `krita-local` | Automate Krita via local CLI + manual-trigger plugin |

## 🔐 Code Audit
| Skill | Purpose |
|---|---|
| `security-safety-codebase-auditor` | Conventional app-security / supply-chain audit |
| `ai-guardrails-codebase-auditor` | AI/LLM guardrails & agentic security audit |

## 🛠️ Technical / Misc
| Skill | Purpose |
|---|---|
| `compliant-markdown-converter` | Batch-convert PDF/DOCX/EPUB → 508-compliant markdown |
| `ml-venv-package-conflicts` | Diagnose ML venv import errors |
| `hermes-skill-installation` | Install custom skills from zip/folder + verify |

---

## Provenance notes

- **Agent-created during sessions** (curator ledger): `album-media-downloader`, `batch-web-gallery-download`, `compliant-markdown-converter`, `hermes-skill-installation`.
- **Deleted/merged:** `erome-album-downloader` → absorbed into `album-media-downloader` (no longer on disk).
- **Installed from zip (2026-08-25):** `security-safety-codebase-auditor`, `ai-guardrails-codebase-auditor`, `excalidraw-chart-reconstructor`, `davinci-resolve-free-local`, `gimp-local`, `krita-local`.
- This list is a snapshot; skills are added/removed over time. Re-derive by running the diff against `.bundled_manifest` when it needs refreshing.