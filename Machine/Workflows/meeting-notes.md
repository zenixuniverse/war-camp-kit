---
type: workflow
status: active
trigger: /meeting-notes
last_verified: "2026-05-28"
tags: [workflow, meeting]
---

# Workflow - /meeting-notes

Pull Zoom meetings transcribed by Notion AI into the vault as clean, enriched meeting records — with action items, priorities, immediate next steps, and the full transcription — then create + route tasks.

`$ARGUMENTS` can be:
- *empty* or `sync` → process every Notion meeting not yet filed in the vault (newest first).
- a search term / name / date → target that specific meeting (e.g. `Acme`, `Q3 planning`, `2026-05-25`).
- a pasted transcript → skip Step 2 and process the pasted text directly.

## Step 1 - Read context
Read `Machine/Personalization/meeting-notes-prompt.md`. Note the routing rules and the "include full transcript" rule.

## Step 2 - Find the meeting(s) in Notion
Source of truth is Notion (Zoom is a supplement; its cloud-recording list is often empty).
1. `notion-search` (query_type `internal`) for recent meeting pages — e.g. query `meeting notes`, with a `created_date_range` covering the last ~14 days (or the date in `$ARGUMENTS`). Meeting pages look like `@<Day Time (TZ)> - Meeting with X` or `Zoom Call with X`.
2. Optional supplement for a recording URL / participants: Zoom `search_meetings` then `get_meeting_assets` (timezone = America/New_York). Skip if it returns nothing.

## Step 3 - Dedupe against the vault
List `00 Human/40 Resources/Meetings/`. Skip any meeting whose `notion_url` already appears in an existing note's frontmatter (or whose date + name already matches a file). Only process **new** meetings.

## Step 4 - Fetch full content
For each new meeting, `notion-fetch` the page with `include_transcript: true`. Extract: title, date, time, attendees, the `<summary>` sections, all action items, the recording URL (if any), and the full `<transcript>`.

## Step 5 - Build the enriched note
Create from `00 Human/80 Templates/Meeting.md`:
- **🔥 Do Immediately** — the 1–3 things the *user* must act on now.
- **✅ Action Items** — owner · due · project; mark which are routed to tasks.
- **⭐ Priority / Important**, **🧭 Decisions**, **💰 Revenue/Pipeline**, **⚠️ Risks & Blockers** — derived from summary + transcript.
- **📝 Summary** — mirror Notion's summary headings; strip `[^...#blockid]` footnotes.
- **🗣️ Full Transcription** — paste the whole transcript inside the foldable `> [!quote]-` callout.
- **Source** — link the Notion page; add the Zoom recording URL only if real, else leave the "live transcription — no audio asset" note.
- Set frontmatter `notion_url`, `attendees`, `project`, `date`.
- Save to `00 Human/40 Resources/Meetings/YYYY-MM-DD - [meeting name].md`.

## Step 6 - Create + route tasks
For each action item **owned by the user or their team** (per personalization routing):
- Create a task file in `00 Human/20 Tasks/` from `00 Human/80 Templates/Task.md`, linking back to the meeting note.
- Items for a specific business or client → also reference them in that business's project note in `00 Human/30 Projects/`.
- Outside-party items with no user follow-up: list in the note only, don't create a task.

## Step 7 - Update people notes
Create or update attendee notes in `00 Human/50 People/` (template `Person.md`).

## Step 8 - Log it
Append to today's daily-note Activity Log: meeting filed (with link), number of tasks created, people updated. If multiple meetings were synced, list each.
