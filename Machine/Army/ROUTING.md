# Army Routing: who to call for what

- Work goes to the **specialist** whose job it is, not to whichever general is nearest.
- A general (SMITH, ARTISAN, BARD, ORACLE…) is a **lead**: it plans, splits the job, dispatches specialists by `subagent_type`, validates their work, and merges it.
- The same generalist doing every job is a routing failure.

**How to dispatch:**
- `subagent_type` is the exact **Name** in the tables below (the `name:` in the agent's file).
- Research, design, review and QA → `model: "opus"`; building, rendering and file work → `model: "sonnet"`.
- Split independent pieces; no two writers on one file; respect shared limits (one dev server, one paid-generation spender at a time); the lead validates every result.

---

## By project

<!-- /setup-camp writes one section per real project, product or recurring client line of work, e.g.:

### Client websites
**Lead:** `artisan` (design) then `smith` (build).
| Job | Call |
|---|---|
| Brief, goals, pages | `Product Manager`, `UX Researcher` |
| Look and feel | `UI Designer`, `Brand Guardian` |
| Build | `Frontend Developer`, `CMS Developer` |
| Launch QA | `Reality Checker`, `Accessibility Auditor`, `Performance Benchmarker` |
-->

## By kind of job, any project
| Job | First call |
|---|---|
| "Research X" or "why does Y happen" | `oracle` → `Research Synthesist`, `Trend Researcher`, `UX Researcher` |
| "Is this good / done / true?" | `Reality Checker`, `Evidence Collector`, `Code Reviewer` |
| "Plan this big thing" | `architect`, `Master Plan Architect`, `Project Shepherd` |
| "Find and win customers" | `herald` → `Outbound Strategist`, `Sales Outreach`, `Proposal Strategist` |
| "Get attention" | `bard` → `Content Creator`, `Social Media Strategist`, `SEO Specialist` |
| "Make it look right" | `artisan` → `UI Designer`, `Brand Guardian`, `Visual Storyteller` |
| "Build it" | `smith` → `Frontend Developer`, `Backend Architect`, `Rapid Prototyper` |
| "Write it" | `Content Creator`, `Technical Writer`, `Proposal Strategist` |
| "Price it" | `Pricing Analyst`, `treasurer` |
| "Money in/out" | `treasurer` → `Bookkeeper & Controller`, `FP&A Analyst` |
| "Keep the client happy" | `steward` → `Customer Success Manager`, `Support Responder` |
| "Hire / contract a human" | `chancellor` → `Recruitment Specialist`, `HR Onboarding` |
| "Make it a process" | `quartermaster` → `Workflow Optimizer`, `Automation Governance Architect` |
| "Secure it / is it legal" | `Security Architect`, `Legal Compliance Checker` (not legal advice) |

When nothing fits, the division general picks. When a reserve agent keeps getting picked, promote it to active in `orders/`.
