# Standing-orders spec (for the writers of orders/*.json)

One JSON file per writer group: `orders/<group>.json`, an object keyed by agent id (the agent's filename in `~/.claude/agents` without `.md`):

```json
{
  "sales-outbound-strategist": {
    "callsign": "SIGNAL-FIRE",
    "rank": "Captain",
    "status": "active",
    "role": "Designs the company's signal-based outbound: picks the niche + area each week, defines the trigger signals (no website, bad reviews, new opening), and hands HERALD a sequenced list.",
    "triggers": [
      "Start of each outbound sprint (weekly, Monday)",
      "Reply rate on the last batch < 3%",
      "A new offer or niche is launched"
    ],
    "deliverables": [
      "Outreach/<date>_<niche>_<area>_plan.md — ICP, signals, 3-touch sequence",
      "Lead list CSV handed to sales-outreach"
    ],
    "cadence": "Weekly (Mon)",
    "pairs_with": ["herald", "sales-outreach", "oracle"]
  }
}
```

Field rules
- **callsign**: 1–2 words, UPPERCASE, hyphenated, army-flavoured and memorable, unique across the whole army (no clash with HERALD, BARD, ARTISAN, SMITH, ORACLE, TREASURER, STEWARD, QUARTERMASTER, CHANCELLOR, ARCHITECT, CLAUDE, SCOUT, SENIOR-DEV). Max 18 chars. The division general keeps its existing callsign if it has one (the 10 court agents: their name uppercased).
- **rank**: `Captain` (leads a recurring function in the division, max ~1 per 4 agents) or `Soldier`. The general's rank is set automatically; still write its orders.
- **status**: `active` = has a real recurring or near-term job for one of the businesses in `camp.json` or a current client, per the briefing. `reserve` = no job today, but primed: the triggers say exactly what situation calls it up. Be honest. A GIS engineer is reserve unless the briefing gives it real work.
- **role**: 1–2 sentences, specific to THIS business: name the real offers, clients, tools, channels and file paths from the briefing. No generic "helps with marketing".
- **triggers**: 2–4 concrete, observable situations ("A client signs a website build", "A deck is ready to send", "MRR report due on the 1st"). For reserve agents, the triggers are the call-up conditions.
- **deliverables**: 1–3 outputs, each with a vault-relative destination path where sensible (follow existing folder conventions: `Clients/<Client>/…`, `Outreach/…`, `Machine/Agents/<dept>/…`).
- **cadence**: `Daily`, `Weekly (Mon)`, `Monthly (1st)`, `Per client`, `Per project`, `On trigger`, …
- **pairs_with**: 1–4 agent ids it hands off to or receives from (any division).

Hard rules
- Cover EVERY agent id you were given. No extras.
- Facts (prices, clients, tools) only from `Machine/Army/BRIEFING.md`; never invent clients or numbers.
- Agents never send anything outward; deliverables are drafts or internal artifacts.
- Output must be valid JSON (UTF-8, no comments, no trailing commas). Validate with `python -c "import json;json.load(open(r'<path>',encoding='utf-8'))"`.
