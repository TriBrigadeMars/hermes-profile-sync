# Custom Skills Inventory — Hermes Agent

Generated: 2026-08-26

Inventory of all skills that are **custom to this agent** (i.e., *not* bundled with Hermes). Determined by diffing every `SKILL.md` on disk against the bundled manifest (`~/.hermes/skills/.bundled_manifest`).

- **Total custom skills:** 56
- **Bundled (shipped with Hermes):** 82
- **Total on disk:** 138

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

## 📝 Ballotpedia Editorial
| Skill | Purpose |
|---|---|
| `ballotpedia-style-reviewer` | Review prose, diction, neutrality, structure, and editorial mechanics against the supplied Ballotpedia Style Guide and bias framework (~162 KB extracted guide + 3 source PDFs) |

## 💼 Career Application Suite
| Skill | Purpose |
|---|---|
| `application-materials` | Orchestrator — bund evidence profile, job analysis, resume, cover letter, and gap analysis into a complete application package |
| `career-gap-analyzer` | Compare candidate evidence with a job description and optional labor-market data to distinguish strengths, partial matches, and development gaps |
| `career-profile` | Build and maintain a canonical evidence profile for truthful resume and cover-letter writing |
| `cover-letter-writer` | Write a role-specific cover letter from verified candidate evidence and the target job description |
| `job-description-analyzer` | Analyze a job description into requirements, responsibilities, terminology, seniority, and performance signals |
| `resume-ats-auditor` | Audit a resume for ATS readability, truthful keyword alignment, parsing risks, and evidence gaps |
| `resume-builder` | Build a truthful, ATS-readable resume from verified candidate evidence |
| `resume-bullet-writer` | Convert verified work evidence into concise accomplishment-oriented resume bullets |
| `resume-tailor` | Tailor an existing resume to a target job by selecting, ordering, and phrasing only supported candidate evidence |
| `professional-reframer` | Reframe real work experience into clear, credible, business-legible language for LinkedIn and other professional contexts without inflating scope or outcomes |

## 📊 Career Market Intelligence
| Skill | Purpose |
|---|---|
| `career-market-intelligence` | Local-first labor-market analysis for skill demand, experience benchmarks, gaps, and outcome associations |

## 📥 Outlook / Accessibility
| Skill | Purpose |
|---|---|
| `outlook-agents` | Manage Outlook calendar: daily briefs, conflict detection |
| `ocr-redaction-local` | Locally detect and redact sensitive text in images and PDFs (Tesseract OCR + Presidio) |

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
- **Installed from zip (2026-08-26):** `ballotpedia-style-reviewer` (v0.1.0), `hermes-career-application-suite` (v0.1.0 — 9 career writing skills + 1 market intelligence skill), `professional-reframer` (v0.1.0).
- This list is a snapshot; skills are added/removed over time. Re-derive by running the diff against `.bundled_manifest` when it needs refreshing.

## Inventory-only entries (not shipped in this repo)

The following 39 skills are listed above but have no `skills/` folder in this repository. Verified on 2026-08-27 from the second workstation (`cruzmars` desktop): they are not installed there either, so they exist only on the machine that authored this inventory. If their code still exists, it needs to be pushed from the source machine; otherwise these entries are stale and can be pruned.

- `album-media-downloader`
- `apa-7-style-agent`
- `ap-stylebook-agent`
- `azure-ad-app-registration`
- `batch-web-gallery-download`
- `compliant-markdown-converter`
- `davinci-resolve-free-local`
- `docx-accessibility-agent`
- `email-accessibility-agent`
- `evaluation-method-selector`
- `excalidraw-chart-reconstructor`
- `gimp-local`
- `job-board-rss-monitor`
- `krita-local`
- `ml-venv-package-conflicts`
- `outlook-mcp-server`
- `outlook-mcp-server-project`
- `paralegal-assistant`
- `pdf-accessibility-agent`
- `powerpoint-style-agent`
- `pptx-accessibility-agent`
- `prisma-review-harassment-minority-students`
- `prisma-review-output`
- `prisma-systematic-review`
- `public-health-evaluation-planning`
- `qualitative-literature-review`
- `research-design-orchestrator`
- `research-literature-monitor`
- `research-question-framer`
- `research-report-packaging`
- `rss_feed_monitoring`
- `social-media-accessibility-agent`
- `study-measures-and-sampling`
- `study-protocol-builder`
- `web-content-monitor`
- `web-media-download`
- `website-accessibility-agent`
- `workflow-orchestrator`
- `writing-style-agent`

(`security-safety-codebase-auditor` and `ai-guardrails-codebase-auditor` were shipped to this repo from the source machine on 2026-08-27, closing part of the gap.)

## Bundled skills (not custom)

All other skills on the desktop machine (82 of 97 installed) are Hermes bundled defaults (e.g., `creative/*`, `research/*`, `software-development/*` minus the custom ones above). They are intentionally not synced — any Hermes installation ships them. Custom skills are identified by diffing installed skills against `$HERMES_HOME/skills/.bundled_manifest`.