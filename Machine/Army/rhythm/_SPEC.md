# Battle rhythm spec (`rhythm/<business id>.json`)

Each business in `camp.json` runs on its own rhythm: the recurring duties that make the army run that business day to day. A service agency (clients, retainers, deliveries, outbound) and a product/SaaS business (signups, trials, content, affiliates) need different duties, so each gets its own file. `/setup-camp` writes these from the interview.

```json
{
  "business": "main",
  "name": "Acme Studio",
  "mission": "One sentence: what the rhythm is for right now.",
  "duties": [
    {
      "id": "main-inbox-sweep",
      "when": "daily",
      "time": "08:00",
      "division": "sales",
      "duty": "Sweep the inboxes and booking tool listed in BRIEFING.md; classify and route every reply; draft answers.",
      "agents": ["engineering-email-intelligence-engineer", "sales-data-extraction-agent", "herald"],
      "campaign": "inbox-triage",
      "runner": "muster-1",
      "output": "Machine/Agents/Sales/<date>_inbox_sweep.md",
      "gate": "Operator approves each reply before sending",
      "kpi": "Replies answered same day"
    }
  ],
  "idle_divisions": {"games": "No game work today; activates if a client asks for a gamified experience."}
}
```

- **when**: one of `daily`, `weekdays`, `mon`, `tue`, `wed`, `thu`, `fri`, `sat`, `sun`, `monthly-1`, `monthly-15`, `monthly-last`, `quarterly`.
- **time**: 24h, in the `timezone` from `camp.json`.
- **division**: a division id from `divisions.py`. Give every division at least one duty where it plausibly has real work; a division with none goes under `idle_divisions` with why and what would activate it.
- **agents**: agent ids (lead first). They must exist in the roster.
- **campaign**: a campaign id from `campaigns.json` if the duty runs one, else `""`.
- **runner**: who runs it. `muster-1` / `muster-2` / `muster-3` (scheduled musters, see DOCTRINE.md), `manual` (only when the operator asks), or `lane:<scheduled task id>`. A duty with no runner never runs.
- **output**: a vault-relative path pattern. **gate**: what needs operator approval, or `""`. **kpi**: what proves the duty worked.
- Results: each muster writes `rhythm/status/<business id>_<date>.json` → `{"duties": {"<id>": {"division", "runner", "status": "done|blocked|skipped", "output", "note", "needs_operator", "at"}}}`. The camp dashboard reads it for the division lights.
- Facts only from `Machine/Army/BRIEFING.md`. No duty may send outward without a gate.
