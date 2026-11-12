# /army

Command the army: run a campaign, deploy an agent, or show the board.

The camp lives at `{{VAULT}}`. Every relative path below is under that folder; run shell commands from it, whatever folder this session was opened in.

0. If `Machine/Army/camp.json` still says "Your Company", the camp isn't set up yet: tell the user to run `/setup-camp` first and stop.
1. Read `Machine/Army/camp.json`, `Machine/Army/DOCTRINE.md` and `Machine/Army/BRIEFING.md`. Use the theme words from `camp.json` (`terms`) when you talk about the army, divisions, generals and campaigns.
2. Decide what the arguments ask for:
   - **No arguments** → read `Machine/Army/campaigns.json`, `Machine/Army/rhythm/*.json` and `Machine/Army/army_live.json`. Report what is deployed now, which standing operations are due today (DOCTRINE table + rhythm + today's date), and recommend the one campaign to run next. Point to `http://localhost:<dashboard_port>`.
   - **A campaign id** → run that campaign from `campaigns.json` phase by phase.
   - **Free text** ("get me 10 leads", "we signed a new client") → match it to the campaign whose trigger fits. If none fits, look up the best agents by role and triggers in `Machine/Army/army.json` and `ROUTING.md`.
3. Running a campaign:
   - Post the dispatch to Court Chat as CLAUDE.
   - For each phase, dispatch its agents with the Agent tool: `subagent_type` = the agent's `name` from `army.json`. Run agents within a phase in parallel, each with a self-contained brief: goal, inputs from prior phases, files in scope, definition of done.
   - Start every brief with two tag lines, `Campaign: <campaign-id>` and `Business: <business id from camp.json>` (or `all`). The dashboard hook reads them to group and colour the task force.
   - Validate every output yourself before starting the next phase.
   - At every **gate**, stop and get the operator's approval in chat. Never send, post, deploy, price, or sign anything without it.
   - Call up reserve agents whenever their triggers match.
4. Finish with: what was produced (paths), what is waiting on the operator, and the counters logged. Only log real, verified events via `python Dashboard/log_event.py -b <business> -a <CALLSIGN> ...`.

The user's arguments (if any) are: $ARGUMENTS
