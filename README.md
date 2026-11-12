# War Camp Kit

A personal AI command camp for Claude Code: ~290 specialist agents organised into divisions, playbooks of multi-agent campaigns, a daily rhythm, and a live dashboard that shows every agent working. One interview turns it into **your** camp: the agents, their orders, the org chart, the playbooks and the dashboard's whole look are rebuilt around your business, your workflows and your brand.

## Install: paste one message into Claude Code
Send this to Claude Code (desktop app or CLI). No GitHub account is needed:

> Install my camp from https://github.com/zenixuniverse/war-camp-kit. Clone it, follow its INSTALL_FOR_CLAUDE.md, then start /setup-camp with me.

Claude checks Python and Git, clones the repo to a permanent folder (`~/WarCamp`), runs `install.py`, and starts the interview. Claude never asks for passwords or keys.

<details><summary>Manual install</summary>

```bash
git clone https://github.com/zenixuniverse/war-camp-kit ~/WarCamp
cd ~/WarCamp
python install.py
```
Then type `/setup-camp` in Claude Code. `install.py` is safe to re-run. Anything it replaces in `~/.claude/` is backed up to `~/.claude/war-camp-backup/<timestamp>/`, and `--dry-run` previews it.
</details>

## The interview (`/setup-camp`, ~15–20 min)
It asks about you, your business(es), offers, customers, tools and your normal week. Then it designs two things with you:
- **How it looks:** your metaphor (war camp, royal court, starship, sports franchise, or anything you describe), a starting template or a brand-new design, the three questions your camp must answer each morning, your KPIs, your brand and your words. A designer, a builder and an inspector agent then build *your* dashboard and show you a screenshot to approve.
- **How it operates:** rename, merge or split divisions; keep, drop or add playbooks; your house rules.

It then writes your briefing, org chart, playbooks, daily rhythm and standing orders for every agent, and primes them. Change anything later with `/setup-camp look`, `/setup-camp operations`, `/setup-camp business` or `/setup-camp orders`.

## Daily use
- `/army` (from any Claude Code session) shows the board: what's deployed, what's due today, and the next best campaign.
- `/army <campaign-id>` runs a playbook, e.g. `/army inbox-triage`, `/army outbound-to-close`, `/army pitch-deck`.
- Or just say what you want ("we signed a new client", "get me 20 leads for dentists in Austin").
- Dashboard: `Dashboard/launch.bat` (Windows) or `bash Dashboard/launch.sh`, then http://localhost:5770 (or the port setup chose).
- Open Claude Code in the camp folder for `/today`, `/closeday`, `/meeting-notes`.

**Nothing leaves without you.** Agents produce drafts and branches only. Every email, post, deploy, price, contract or payment stops for your approval.

## What's inside
See `ARCHITECTURE.md` for how the pieces fit together.

| Path | What |
|---|---|
| `INSTALL_FOR_CLAUDE.md`, `install.py` | Auto-install steps for Claude; the installer |
| `commands/` | `/setup-camp` and `/army`, installed for use from any folder |
| `.claude/commands/` | `/today`, `/closeday`, `/new`, `/meeting-notes`, `/interview`, `/start` (inside the camp folder) |
| `Machine/Army/` | The army's source files: `camp.json`, `BRIEFING.md`, `divisions.py`, `orders/`, `campaigns.json`, `rhythm/`, `ROUTING.md`, `DOCTRINE.md`, `build_army.py`, `army_hook.py` |
| `Dashboard/` | `server.py` (data API, see `API.md`), `log_event.py`, `pages/` (templates plus your tuned page) |
| `agents/court/` | 10 generals: architect, herald, treasurer, bard, oracle, artisan, steward, chancellor, smith, quartermaster |
| `agents/specialists/` | 283 open-source specialists (sales, marketing, paid, design, engineering, QA, security, finance, games, and more) |
| `skills/` | The 10 generals' operating manuals |
| `00 Human/`, `Machine/Workflows`, `Machine/Templates` | The notes vault the daily commands use |

## Updating
Tell Claude "update my camp", or run `git pull` then `python install.py` in the camp folder.

## Uninstall
Delete the agents listed in `agents/` from `~/.claude/agents/`, the skills in `skills/` from `~/.claude/skills/`, `setup-camp.md` and `army.md` from `~/.claude/commands/`, and the three `army_hook.py` entries in `~/.claude/settings.json` (or restore the backup in `~/.claude/war-camp-backup/`).
