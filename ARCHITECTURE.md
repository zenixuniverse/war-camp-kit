# How the camp is built

The camp is five layers. Each one only talks to the layer next to it, so you can change any one (the look, the facts, the org chart, the playbooks) without breaking the rest.

```
 1. PEOPLE        You (the operator) ──intent / approvals──▶ Claude (main session = commander)
                                                                   │ dispatches with the Agent tool
 2. ARMY          ~293 agents in ~/.claude/agents ◀── primed with standing orders by build_army.py
                  10 generals (court) + 283 specialists, grouped into divisions
                                                                   │ every dispatch / tool call
 3. NERVES        army_hook.py (Claude Code hook) ──▶ Machine/Army/army_live.json
                  Court Chat (Machine/Agents/COURT_CHAT.md) · KPI files (log_event.py)
                                                                   │ read by
 4. DATA API      Dashboard/server.py (localhost) ── /api/camp /api/army /api/live /api/chat /api/brief
                                                                   │ any page that speaks the API
 5. LOOK          Dashboard/pages/<your-page>.html  (templates: war-camp-3d, royal-roundtable, command-grid)
```

## 1. People: who decides
- **The operator** gives intent ("get me 20 dental leads", "we signed Acme") and approves anything that leaves the building.
- **Claude, the main session,** is the commander. It never does big jobs alone: it picks a campaign or the right lead, writes self-contained briefs, dispatches agents in parallel, checks their work, and stops at every gate for approval. The rules for this are in `CLAUDE.md` and `Machine/Army/DOCTRINE.md`.

## 2. The army: who does the work
- **Agents** are Markdown files in `~/.claude/agents/` (installed from `agents/`). Each has a `name:` (the dispatch key) and a description of its craft.
- **Generals** (the 10 court agents: architect, herald, treasurer, bard, oracle, artisan, steward, chancellor, smith, quartermaster) each have a full operating manual in `~/.claude/skills/<domain>/SKILL.md`. They lead a division and delegate to specialists.
- **Specialists** (283) are deep single-craft experts: Outbound Strategist, UI Designer, Bookkeeper, Penetration Tester, and so on.
- **The source files that shape the army** (all in `Machine/Army/`):

| File | Decides |
|---|---|
| `camp.json` | Whose camp it is: company, operator, businesses, the look's words and colours, the dashboard page |
| `BRIEFING.md` | The facts every agent works from: offers, prices, customers, clients, tools, hard rules |
| `divisions.py` | The org chart: which agent sits in which division, and who leads it |
| `orders/*.json` | Each agent's standing orders: callsign, rank, active or reserve, role in *this* business, what triggers it, what it delivers, cadence |
| `campaigns.json` | Playbooks: multi-phase operations (which agents per phase, the output, the approval gate) |
| `rhythm/<business>.json` | The daily and weekly duties per business, and who runs them |
| `ROUTING.md` | Who to call for what, per project and per kind of job |

- **`build_army.py` compiles them.** It merges all of that into `army.json` and writes a "standing orders" block into every agent file. That block tells each agent its division, callsign and role in this business, plus the rules of engagement: read the briefing, post to Court Chat, never send anything outward, never invent facts, route work to specialists. Re-run it after any change. `--check` validates without touching the agents.

## 3. Nerves: how you see what's happening
- **`army_hook.py`** is wired into Claude Code's hooks (PreToolUse, SubagentStart, SubagentStop). Every time Claude dispatches an agent, and every tool call that agent makes, it records who, which campaign, which business, and what it's doing right now into `army_live.json`. You never log this by hand.
- **Court Chat** (`Machine/Agents/COURT_CHAT.md`) is the radio. Agents post START, BLOCKED and DONE with output paths, and you can post too.
- **KPI files** (`Dashboard/data/<business>_live.json`) hold each business's numbers. Agents bump them with `log_event.py`, and only for real, verified events.

## 4. Data API: one stable contract
`Dashboard/server.py` is a tiny local web server (Python stdlib, nothing to install). It reads layers 2–3 and serves them as JSON. The contract is in `Dashboard/API.md`, and it is the only thing a look depends on.

## 5. The look: fully replaceable
A look is one HTML file in `Dashboard/pages/`, and `camp.json` → `theme.page` picks it. The kit ships three **templates** built for the original camp: a 3D war camp, a 3D round table and a flat command grid. `/setup-camp` never ships a template as-is. It copies one (or starts blank), then a designer, a builder and an inspector agent tune it to the business: their three morning questions on the first screen, their KPIs and pipeline, their brand and their words. You can redesign any time with `/setup-camp look`.

## How it was built (and how to extend it)
1. **Install agents** (open-source specialists plus custom generals) into `~/.claude/agents`.
2. **Write the facts** once (`BRIEFING.md`), so no agent guesses.
3. **Draw the org chart** (`divisions.py`) so every agent has a home and a leader.
4. **Write standing orders** per agent (`orders/`), done by parallel writer agents from the briefing, so each knows its job in *this* business.
5. **Write playbooks** (`campaigns.json`) and the **rhythm** (`rhythm/`) so work happens in repeatable, gated phases.
6. **Compile and prime** (`build_army.py`).
7. **Wire the hook** so every dispatch is visible.
8. **Serve the data** (`server.py`), then **design the look** on top of it.

To extend:
- **New agent:** drop its `.md` into `~/.claude/agents`, add its id to a division in `divisions.py`, write its orders, and run `build_army.py`.
- **New playbook:** add it to `campaigns.json` and run `build_army.py`.
- **New look:** add a page to `Dashboard/pages/` that follows `API.md`, then point `theme.page` at it.
