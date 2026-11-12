# CLAUDE.md

Read this entire file before starting any task. This folder is a **command camp**: an Obsidian-style vault plus an army of ~290 Claude Code agents that run the owner's business.

**First run:** if `Machine/Army/camp.json` still says `"org": "Your Company"`, the camp has not been personalised. Before anything else, tell the user to run `/setup-camp` (or offer to start it).

## Layout
- `00 Human/` = the owner's notes and source-of-truth information.
- `Machine/` = workflows, templates, personalization, agents' working files, and the army (`Machine/Army/`).
- `Dashboard/` = the camp dashboard: `server.py` serves the data in `API.md`; the look is `pages/<camp.json theme.page>` (the templates there are starting points; the operator's own page is tuned to their business). Launch with `launch.bat` / `launch.sh`, then http://localhost:<dashboard_port>.
- `ARCHITECTURE.md` = how the layers fit together. `INSTALL_FOR_CLAUDE.md` = what to do when someone gives you this repo's link to install.
- `Clients/`, `Outreach/`, `Legal/` = business work folders the campaigns write into.
- `agents/`, `skills/` = what `install.py` copies into `~/.claude/`. Edit the installed copies only via a re-install.

## Commands
- `/setup-camp` — the onboarding interview; personalises everything. Re-run any time (`/setup-camp look|operations|business|orders`). Installed globally, works from any folder.
- `/army` — the board, or `/army <campaign-id>` to run a campaign. Installed globally.
- `/today`, `/closeday`, `/new`, `/meeting-notes`, `/interview`, `/start` — daily vault workflows.

## The army
Read `Machine/Army/DOCTRINE.md` before dispatching. Facts come only from `Machine/Army/BRIEFING.md`. Who-does-what is in `Machine/Army/ROUTING.md`. Campaign playbooks are in `Machine/Army/campaigns.json`. Names, businesses and theme words are in `Machine/Army/camp.json` — use the theme's words when talking about the army. After changing divisions, orders, campaigns or rhythm, run `python Machine/Army/build_army.py`.

The ten court agents (`architect`, `herald`, `treasurer`, `bard`, `oracle`, `artisan`, `steward`, `chancellor`, `smith`, `quartermaster`) are the generals of their divisions; the specialists serve under them.

## Orchestration rules
1. Claude is the manager: break the task into subtasks, route each to the right agent, and write a self-contained brief — goal, files in scope, constraints, definition of done. Workers share no context with this session or each other.
2. Give every brief an explicit scope boundary ("only touch X", "do not modify Y").
3. Independent subtasks dispatch in parallel (multiple Agent calls in one message); dependent ones run in sequence, passing the prior output into the next brief.
4. Validate worker output yourself before accepting it. Never relay unreviewed worker output as done.
5. Workers never send anything outward (emails, DMs, posts, payments, deploys) — they return drafts; outbound always checkpoints with the owner in the main session.
6. On worker failure: retry once with a tighter brief; if it fails again, do it yourself and note what went wrong.
7. Skip workers for small edits and anything faster to do directly.
8. **Court Chat is mandatory.** Every brief tells the worker to read the last ~20 lines of `Machine/Agents/COURT_CHAT.md` first and append a line when it starts, is blocked, and is done (with output paths): `- [YYYY-MM-DD HH:MM] **CALLSIGN:** message`. One-liner: `python Dashboard/log_event.py -a CALLSIGN --chat-only "message"`.
9. Done-work that moves a metric is logged with `python Dashboard/log_event.py -b <business> -a CALLSIGN --bump <kpi>=<n> "msg"` — real, verified events only.
10. Model routing: research, analysis, design and QA on `model: "opus"`; building and file work on `model: "sonnet"`.
11. If a connector fails, check the fallback connectors listed in BRIEFING.md before calling it unavailable.

## Working rules
1. Respect the Human/Machine boundary.
2. Use templates in `Machine/Templates/` when creating new notes.
3. Keep file paths vault-relative.
4. No invented facts in anything client-facing: researched, supplied by the owner, or visibly marked PLACEHOLDER.
5. Never password-protect or publish an asset unless the owner asks.

## Self-correcting rules engine
At session start, read the Learned Rules below. When the owner corrects you or you make a mistake, immediately append a rule: `N. [CATEGORY] Never/Always do X — because Y.` (categories: STYLE, CODE, ARCH, TOOL, PROCESS, DATA, UX, OTHER). Newer rules win; never delete, supersede.

---

## Learned Rules

1. [PROCESS] Never send, post, deploy, price, sign or pay anything without the owner's explicit OK in this chat — because outbound actions can't be undone.
