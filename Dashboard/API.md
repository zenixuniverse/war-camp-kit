# Camp dashboard — data contract

The **look** of the camp is replaceable. The **data** is not. `server.py` (stdlib Python, binds 127.0.0.1) serves the data below. A look is any HTML file in `Dashboard/pages/`; `camp.json` → `theme.page` picks which one `/` serves. A look may bring its own assets (css, js, images, models) in `Dashboard/pages/`; they are served at `/<path>`.

The templates in `pages/` are **starting points**, not the product. During `/setup-camp` the chosen template is copied to a new page named for the business and then tuned until it reads as theirs (see "Tuning checklist").

## Read
| Route | Returns |
|---|---|
| `GET /api/camp` | `camp.json` merged over defaults: `{org, army_name, operator, businesses:[{id,name,color}], theme:{page, camp_title, metaphor, accent, accent_2, background, font_display, terms:{army,division,general,campaign,deploy,chat}}, dashboard_port, timezone, ...}` plus any extra keys `/setup-camp` added (e.g. `kpi_labels`, `pipeline_stages`, `panels`). |
| `GET /api/army` | `{generated, divisions:[{id,name,codename,general,color,mission}], agents:[{id,name,emoji,color,vibe,description,division,rank,status,callsign,role,triggers[],deliverables[],cadence,pairs_with[]}], campaigns:[{id,name,goal,trigger,phases:[{name,agents[],output,gate}]}], rhythm:{<bizid>:{business,name,mission,duties[...]}}, deployments:[...], duty_status:{<duty id>:{division,runner,status,output,note,needs_operator,at}}, server_time}` |
| `GET /api/army?live=1` | Only `{deployments, duty_status, server_time}`. Poll this every 2–5 s; fetch the full roster once. |
| `GET /api/live?biz=<id>` | That business's KPI file: `{kpis:{name:number}, revenue:{name:number}, log:[{time,msg,type}], last_updated, ...}` |
| `GET /api/brief` | Newest morning brief: `{name, date, markdown, mtime, path}` or `{name:null}` |
| `GET /api/chat` | `{messages:[{ts, agent, msg}], path}` (the Court Chat log, oldest first) |
| `GET /api/ping` | `{status:"ok", time}` |

A **deployment** (one agent dispatch, written by the Claude Code hook): `{key, type (agent name), description, campaign, biz, by, session, agent_id, status: deployed|working|done|lost, doing (what it is doing right now, e.g. "Write: plan.md"), actions, started, updated, ended}`.

## Write
| Route | Body |
|---|---|
| `POST /api/chat` | `{agent, msg}` → appends `- [ts] **AGENT:** msg` to Court Chat |
| `POST /api/log` | `{biz, msg, type}` → adds to that business's log |
| `POST /api/bump` | `{biz, path:"kpis.leads", by:1}` → increments a counter |
| `POST /api/update` | `{biz, data:{...}}` → merges into that business's KPI file |

Unknown `biz` → HTTP 400. Agents write KPIs with `python Dashboard/log_event.py -b <biz> -a <CALLSIGN> --bump <kpi>=<n> "msg"`.

## Every look must have
1. Live operations: who is deployed now, what they are doing, grouped by campaign and coloured by business.
2. The roster: every division and agent, with a dossier (role, triggers, deliverables) and a **copy deploy order** button that copies `Use the <name> agent to: ` for pasting into Claude.
3. Campaigns with their phases and gates.
4. Today's rhythm: each duty's status (done / running / blocked / due).
5. The business's KPIs from `/api/live`, labelled in the business's own words.
6. Court Chat (read + post).
7. The morning brief / approval packet when one exists.
8. Works offline except pinned CDN libraries (exact versions); no build step; one HTML file plus optional assets.

## Tuning checklist (a look isn't done until all are true)
- The first screen answers the operator's top 3 daily questions from the interview (e.g. "Who owes me a reply?", "What's the pipeline worth?", "What's due for clients today?").
- KPIs are **their** metrics with their names and units (from BRIEFING.md and `camp.json`), not generic "leads/revenue" placeholders.
- Their businesses, offers, pipeline stages and active clients appear where they matter.
- Their brand: palette, fonts, logo (if given in `Dashboard/pages/assets/`), voice in every label and empty state.
- Their metaphor and words (`theme.terms`) everywhere: no leftover "army/war/court" words unless they chose that theme.
- Nothing from another business or template remains (grep the page for the template's old names).
- Screenshot shown to the operator and approved.
