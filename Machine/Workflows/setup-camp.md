---
type: workflow
status: active
trigger: /setup-camp
tags: [workflow, onboarding, army, personalization]
---

# Workflow — /setup-camp

Interview the new owner of this camp, then rebuild the whole army around **their** business: names, theme, facts, divisions, campaigns, daily rhythm and every agent's standing orders. At the end the dashboard shows their company and their army is primed to work for it.

Re-runnable: on a second run, load what exists, show it, and only ask about what they want to change (`/setup-camp look` → Steps 6 + 10b, `/setup-camp operations` → Step 6b + 8–10, `/setup-camp business` → Steps 3–5 + 8, `/setup-camp orders` → Step 9).

Tone: warm, quick, plain English. Ask in short rounds (3–5 related questions per message, or one AskUserQuestion with options when the answer is a choice). Never ask for passwords, API keys or card numbers — connectors are authorised by the user in Claude's own UI.

## Step 0 — Preflight (silent unless something is wrong)
1. Check `~/.claude/agents/herald.md` exists and `~/.claude/settings.json` has a hook that runs `Machine/Army/army_hook.py`. If either is missing, tell the user to run `python install.py` from this folder in a terminal, then re-run `/setup-camp`. Stop.
2. Read `Machine/Army/camp.json`, `Machine/Army/BRIEFING.md`, `Machine/Army/DOCTRINE.md`, `Machine/Army/divisions.py`, `Machine/Army/campaigns.json`, `Machine/Army/orders/_SPEC.md`, `Machine/Army/rhythm/_SPEC.md`.
3. Get today's date and local time from the shell (on Windows use PowerShell `Get-Date`).

## Step 1 — Welcome
In 4 lines: this folder is their command camp; ~290 specialist agents in 18 divisions will work for their business; the next ~15 minutes of questions make it theirs; nothing ever gets sent, posted or paid without their OK.

Offer a shortcut: "If you have a website, a pitch deck, a one-pager or old notes about the business, paste the link or drop the file — I'll read it and pre-fill answers so you only confirm." If they give one, research it (web fetch / read the file) and pre-fill; mark every pre-filled fact as "from your site — correct?" in the next rounds. Never guess a fact you couldn't read.

## Step 2 — You and the company
1. Your name, and what should the army call you? (operator)
2. Company name, and what you do in one sentence.
3. Who else works with you (people, contractors) and who owns what?
4. Where are you based / what timezone do you work in?

## Step 3 — The businesses (repeat per business, max 4)
Ask: "Is everything one business, or do you run separate lines (e.g. an agency and a product)?" Each separate line becomes a business in `camp.json` with its own colour and daily rhythm.
For each:
1. What is it, and how does it make money (service retainer, projects, product/SaaS, ecommerce, other)?
2. Offers and prices (exact; "I don't want to share" is fine — mark it).
3. Ideal customers: who buys, and what pain makes them buy?
4. Where do customers come from today, and what's working / not working?
5. Current numbers you're comfortable sharing (revenue or MRR, clients, leads per week) and the 30- and 90-day targets.

## Step 4 — Clients, proof, brand
1. Active clients (name, what you do for them). Which results may the army quote publicly?
2. Brand: colours (hex if known), fonts, logo location, voice in 3 words, words or claims you never use.
3. Anything legally sensitive in your industry (health, finance, alcohol, kids, etc.)?

## Step 5 — Tools and workflows
1. Inboxes, CRM / where leads live, calendar & booking link, payments/invoicing, social accounts, websites, file storage.
2. Check which MCP servers/connectors this Claude install has (the tools available to you, or `claude mcp list` in a terminal) and show them. Ask which accounts each one is for and which are missing. Record fallbacks (e.g. a connector broker) under Tools in the briefing.
3. Walk me through a normal week. What do you do every day / every Monday / every month?
4. What recurring deliverables do you owe clients?
5. What eats the most time, and what do you most want the army to take off your plate first?
6. Approval style: one daily approval packet, approve each item as it comes, or only weekly?
7. Should the army run on its own every day (scheduled musters) or only when you ask?

## Step 6 — Design your camp: how it looks
The camp is theirs, not a copy of anyone else's. Explain: the dashboards in `Dashboard/pages/` are **templates**. Whatever they pick gets copied and tuned to their business until it reads as theirs.
1. **Metaphor** (AskUserQuestion): **War camp** · **Royal court / kingdom** · **Starship crew** · **Sports franchise** · Other (they describe it: a studio, a newsroom, a restaurant kitchen, a heist crew, a plain professional "operations centre"...).
2. **Starting look** (AskUserQuestion, describe each in one line):
   - `war-camp-3d.html`: a 3D field where every agent stands in formation and glows when deployed.
   - `royal-roundtable.html`: a 3D table with the division leads seated around it.
   - `command-grid.html`: a flat, dense numbers-first grid. Fast and businesslike.
   - **Something new**: they describe it (or share a screenshot or site they like) and the camp is designed from scratch on the same data.
3. **What it must answer at a glance**: "When you open your camp each morning, what are the 3 questions it should answer?" (e.g. who needs a reply, what's the pipeline worth, what's due for clients today).
4. **Their numbers**: which KPIs to show for each business, with their names and units (e.g. "booked calls", "MRR", "jobs scheduled", "average ticket"), and where each number comes from (an agent logging it, or a tool). Pipeline stages if they have a sales process.
5. **Brand**: logo file (ask them to drop it into `Dashboard/pages/assets/`), colours (accent, second accent, background), display font. Suggest from Step 4 and confirm.
6. **Names and words**: camp title, army name, and what to call the army, a division, a general, a campaign, deploying, and the chat, translated to their metaphor (e.g. starship → Fleet, Deck, Commander, Mission, Launch, Comms; kitchen → Brigade, Station, Chef de partie, Service, Fire, The Pass).
7. Anything they want **left out** of the dashboard.

## Step 6b — Design your camp: how it operates
1. **Divisions**: show the 18 divisions and their generals. They can rename them (and codenames) to fit the metaphor, **merge** divisions they won't use separately, **split** one they lean on heavily, or change a general. Every agent must still belong to exactly one division (fold unused specialists into a "Reserve"-style division rather than deleting them).
2. **Campaigns**: show the starter playbooks with one line each. Which match how they actually work? Which to drop? What 1–3 workflows of their own should become campaigns (Step 5 answers)?
3. **Rules of the house**: anything the army must always or never do (approval rules, hours, tone with clients, tools never to touch). These go in BRIEFING.md hard rules and the root CLAUDE.md Learned Rules.

## Step 7 — Confirm
Play back a one-screen summary: operator, company, businesses (offers, prices, ICPs, targets), tools, top 3 things to take off their plate, approval style, the look (metaphor, starting template or new, glance questions, KPIs, brand, words) and the operations (division changes, campaigns kept/dropped/added, house rules). Ask "Anything wrong or missing?" Fix, then proceed. Do not write files before this confirmation.

## Step 8 — Write the camp (main session does this itself)
1. `Machine/Army/camp.json` — org, army_name, operator, businesses `[{id, name, color}]` (ids: short lowercase slugs), theme `{page, camp_title, metaphor, accent, accent_2, background, font_display, terms{army, division, general, campaign, deploy, chat}}` (`page` stays the chosen template until Step 10 builds theirs), `kpi_labels {key: "Label (unit)"}`, `pipeline_stages []`, `glance_questions []` (Step 6.3), dashboard_port (keep 5770 unless taken — check with a quick connect test and pick 5771+ if busy), timezone, connectors.
2. `Machine/Army/BRIEFING.md` — fill every section from the answers. Unknowns stay `UNKNOWN — ask the operator`. No invented facts.
3. Vault context (same files `/interview` maintains): `00 Human/70 Context/business-profile.md`, `audience-profile.md`, `writing-style.md`, `Machine/Personalization/operator-profile.md`, then regenerate `today-prompt.md`, `closeday-prompt.md`, `meeting-notes-prompt.md` per `Machine/Workflows/interview.md` steps 5–6. Create one project note per business/active client in `00 Human/30 Projects/`.
4. `Machine/Army/divisions.py` — apply Step 6b.1: names, codenames, missions written for this business, merges/splits (move ids between ASSIGN lists; a new division gets a new id), generals. Every agent id appears exactly once (`build_army.py --check` fails loudly otherwise). A division with no current use keeps its agents and says so in its mission ("reserve: activates if…").
5. `Machine/Army/ROUTING.md` — write the "By project" section: one subsection per business / product / recurring client line, with a lead and a job → agent table, using agent **names** from the agents' frontmatter.
6. `Machine/Army/campaigns.json` — apply Step 6b.2: rewrite goals, triggers, outputs and gates with their real tools and folders; drop the ones they don't want; add their own workflows as new campaigns (same schema; agent ids must exist; gates on anything outward). Rename display names to their metaphor.
6b. House rules from Step 6b.3 → BRIEFING.md "Hard rules" and numbered Learned Rules in the root `CLAUDE.md`.
7. `Machine/Army/rhythm/<business id>.json` per business, per `rhythm/_SPEC.md`, built from their real week (Step 5). Runners: `muster-1/2/3` if they chose daily automation, else `manual`.
8. `Machine/Army/DOCTRINE.md` — update the Standing operations table to match campaigns.json + rhythm.

## Step 9 — Write standing orders (parallel workers)
Split the roster in `divisions.py` into 7 writer groups (about 40 agents each, whole divisions per group). Dispatch 7 workers in parallel with the Agent tool (`subagent_type: "general-purpose"`, `model: "sonnet"`), each brief:
- `Campaign: setup-camp` and `Business: all` as the first two lines.
- Goal: write `Machine/Army/orders/g<N>_<divisions>.json` for exactly these agent ids: <list>. Follow `Machine/Army/orders/_SPEC.md` exactly. Facts only from `Machine/Army/BRIEFING.md`. Read each agent's file in `~/.claude/agents/<id>.md` for what it can do. Be honest about active vs reserve. Callsigns unique and themed to: <metaphor>. Avoid these taken callsigns: <the 10 court names + CLAUDE + any from other groups if known>.
- Only write that one file. Validate it parses as JSON.
- Court Chat START/DONE lines per CLAUDE.md.
Then validate yourself: every file parses, every id covered once, then run `python Machine/Army/build_army.py --check`. Fix duplicate callsigns or bad refs and re-check until it exits 0.

## Step 10 — Build the army
1. `python Machine/Army/build_army.py` (primes every agent in `~/.claude/agents` with its orders).
2. Seed each business's KPI file with their real starting numbers if they gave any: `python Dashboard/log_event.py -b <biz> -a CLAUDE --bump <kpi>=<n> "Starting number from setup"` (only numbers they stated).

## Step 10b — Build their dashboard (tuned, never a copy)
Read `Dashboard/API.md` first: it is the data contract and the tuning checklist.
1. **Design** — dispatch one `UI Designer` (`model: "opus"`) with: the Step 6 answers, BRIEFING.md, `camp.json`, the chosen template file (or "new design"), and API.md. Output: `Dashboard/pages/<org-slug>.design.md`, a one-page spec: layout of the first screen built around their 3 glance questions, which KPIs/stages/clients appear where, palette/type/logo use, the metaphor's visual language (what replaces soldiers/tents/banners: crew stations, players on a pitch, cooks at stations…), and the words on every panel and empty state.
2. **Build** — dispatch one `Frontend Developer` (`model: "sonnet"`): copy the template to `Dashboard/pages/<org-slug>.html` (or build new) and implement the spec against API.md. Only touch that file and `Dashboard/pages/assets/`. It tests on its own port (`python Dashboard/server.py --port 5799`) by loading `/<org-slug>.html`, with zero console errors, and grep-proves no template-only names remain.
3. **Inspect** — dispatch `Reality Checker` (`model: "opus"`): screenshot it, go through the API.md tuning checklist item by item, and return PASS or a numbered fix list. Loop build → inspect until PASS (max 3 rounds; then do the remaining fixes yourself).
4. Set `camp.json` `theme.page` to `<org-slug>.html`. Keep the templates in `pages/` (they can switch back).
5. **Show them**: start the dashboard (`Dashboard/launch.bat` on Windows, `bash Dashboard/launch.sh` elsewhere), open `http://localhost:<port>`, send a screenshot, and ask what to change. Apply changes the same way until they're happy. Later changes: `/setup-camp look`.
6. Post to Court Chat: `- [<date time>] **CLAUDE:** Camp personalised for <company>. <N> agents primed (<a> active, <r> reserve), <c> campaigns, dashboard <page>.`

## Step 11 — Hand over
Report in plain English:
- What was set up (files), the dashboard link, how many agents are active vs reserve.
- The 3 campaigns to run first (from their Step 5 answers), each as a copy-paste command: `/army <campaign-id>`.
- What's still UNKNOWN in the briefing.
- If they chose daily automation: offer to create the three muster scheduled tasks now (create them only on a clear yes, showing the schedule first).
- How to change anything later: re-run `/setup-camp <part>`, or edit `Machine/Army/*` and run `python Machine/Army/build_army.py`.
