# /meeting-notes

Pull Zoom meetings transcribed by Notion AI into the vault as clean, enriched meeting records (action items, priorities, immediate next steps, full transcription), then create + route tasks. Also accepts a pasted transcript.

Read and execute the workflow file at `Machine/Workflows/meeting-notes.md` — follow every step exactly as documented.

Arguments (`$ARGUMENTS`):
- empty / `sync` → file every Notion meeting not yet in the vault (newest first)
- a name / search term / date → target one meeting (e.g. `Acme`, `2026-05-25`)
- a pasted transcript → process it directly

The user's arguments (if any) are: $ARGUMENTS
