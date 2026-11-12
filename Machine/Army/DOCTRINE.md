# Army Doctrine

The army is every installed Claude Code agent (~293), organised into 18 divisions, with standing orders to run the business(es) in `camp.json`. The main Claude session (**CLAUDE**) commands. The operator (name in `camp.json`) gives intent and approves anything that leaves the building.

## Files
| File | What |
|---|---|
| `camp.json` | Who this camp belongs to: company, operator, businesses, theme colours and words, dashboard port. Written by `/setup-camp`. |
| `BRIEFING.md` | The facts every agent works from: offers, prices, proof, clients, tools, hard rules, gaps. Update it when facts change. |
| `ROUTING.md` | **Who to call for what**, per project and per kind of job. |
| `divisions.py` | Order of battle: which agent serves in which division, and each division's general. |
| `orders/*.json` | Standing orders per agent: callsign, rank, active/reserve, role, triggers, deliverables, cadence, pairs. Spec: `orders/_SPEC.md`. |
| `campaigns.json` | Campaign playbooks: multi-division operations with phases and operator gates. |
| `rhythm/<business>.json` | The day-to-day battle rhythm per business. Spec: `rhythm/_SPEC.md`. |
| `build_army.py` | Compiles all of the above into `army.json` and primes every agent file in `~/.claude/agents` with its orders. Re-run after any change. |
| `army_hook.py` | Global Claude Code hook (installed by `install.py`). Records every agent dispatch and what it is doing. Writes `army_live.json`. |
| Dashboard | `Dashboard/launch.bat` (Windows) or `Dashboard/launch.sh` → http://localhost:<dashboard_port>. Data contract: `Dashboard/API.md`. The look is `Dashboard/pages/<camp.json theme.page>`. |

## Chain of command
1. **Operator intent** → CLAUDE picks the campaign, or the lead named in `ROUTING.md` for that project. The lead dispatches the specialists. Reusing the same general for every job is a routing failure.
2. **CLAUDE dispatches** with the Agent tool. `subagent_type` is the agent's **name** (e.g. `"Growth Hacker"`, `"herald"`), as shown in its dossier on the dashboard ("Copy deploy order").
3. **Every brief** states the goal, files in scope, "only touch X / don't modify Y", and definition of done. It starts with two tag lines, `Campaign: <id>` and `Business: <business id>` so the dashboard groups and colours the task force.
4. **Independent phases run in parallel.** Dependent phases run in order, each feeding the prior output into the next brief.
5. **CLAUDE validates** every output before it moves on.
6. **Gates:** anything outward (email, DM, post, client message, deploy, contract, price, payment) stops for operator approval. No exceptions.
7. **Model routing:** research, design, review and QA on the strongest model (`model: "opus"`); building and file work on `model: "sonnet"`. No two writers on one file.

## Standing operations
`/setup-camp` fills this table from the interview. Until then, the default heartbeat is:

| When | Campaign | Purpose |
|---|---|---|
| Daily, morning | `inbox-triage` | Every reply, lead and client message read, routed and drafted. |
| Monday | `weekly-command` | Pipeline, delivery, money → this week's orders. |
| Monday | `outbound-to-close` | A fresh outbound sprint. |
| Weekly | `product-growth` | Growth experiments on the live offers. |
| 1st of month | `social-retainer` per client, `monthly-close` | Deliver and report; close the books. |
| 15th of month | `retention-expansion` | Client health, renewals, case studies. |
| On trigger | `client-onboarding`, `website-build`, `pitch-deck`, `paid-launch`, `product-sprint`, `hiring`, `incident`, `new-market`, `reputation` | Run when the trigger in the playbook happens. |
| One-time build-out | `revenue-ops`, `measurement` | Close the CRM/billing/contract and analytics gaps. |

Run one with `/army <campaign-id>`, or `/army` to see the board.

### Musters (optional automation)
If the operator wants the army to work every day without being asked, create three scheduled tasks (Claude desktop → Scheduled, or `/schedule`) that each run the duties in `rhythm/<business>.json` whose `runner` matches:
- `muster-1` (morning): money and clients (sales, intel, finance, success).
- `muster-2` (midday): make and build (design, engineering, product, studio, paid).
- `muster-3` (afternoon): guard and grow (marketing, ops, people, shield) → QA → tomorrow's **approval packet** at `Board/Daily/<date>_packet.md` (max 10 items, ranked by value per minute of the operator's time).

Each muster dispatches one lead per division in parallel, validates, and writes `rhythm/status/<business>_<date>.json`. Everything is drafts or branches only: nothing is sent, posted, merged, deployed or paid without the operator.

## Reserve
Reserve agents are primed: their orders name the situation that calls them up. A reserve agent that gets deployed often should be promoted to `active` in its orders file.

## Court Chat
`Machine/Agents/COURT_CHAT.md` is the army radio. Agents post START / BLOCKED / DONE as `- [YYYY-MM-DD HH:MM] **CALLSIGN:** message`. CLAUDE posts dispatch and merge notes. The dashboard tails it. Results that move a KPI also go through `python Dashboard/log_event.py -b <business> -a <CALLSIGN> --bump <kpi>=<n> "msg"`, only for real, verified events.

## Maintenance
- New agents installed → add their ids to `divisions.py`, write their orders, then `python Machine/Army/build_army.py`.
- `python Machine/Army/build_army.py --check` must exit 0.
- The hook never blocks a session. If the dashboard shows nothing live, check `army_live.json` is updating and the hooks block is in `~/.claude/settings.json` (re-run `python install.py`).
