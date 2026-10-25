---
name: rekordbox-short-blends
description: Prepare and edit Rekordbox hot cues for short vocal selections, drop swaps and phrase-aligned DJ blends while preserving existing routines. Use for cue timing and transition preparation, not automatic cue maps for every track.
---

# Rekordbox Short Blends

Use the Rekordbox MCP and the installed CueGen/programmatic integration. Do not control Rekordbox through its UI, close/reopen it, dismiss dialogs, or capture screenshots unless the user explicitly authorizes that particular UI action. Ask the user to close/reopen it when necessary.

Read [the portable workflow](references/workflow.md) before setup or database edits. The installer adds `references/installation.json` with this computer's installation root. Do not assume the old laptop's paths, tracks, IDs, cues or playlist order exist here.

## Prepare a musical routine

- Read current tracks, playlist order, saved cues and loops from MCP. Read numerical beat grids from `get_track_analysis`. Freshly discover track IDs. A title alone is not evidence of BPM, key or cue timestamps.
- Preserve successful routines and unrelated cues/loops. Use a small number of purposeful markers; use A as START when the user wants that layout. Give concise labels naming the destination pad where useful.
- Distinguish incoming launch pads from outgoing visual action markers. A marker does not automatically switch decks, change stems, move a fader or stop a track.
- Count grid indices and beat-in-bar alignment. Four beats equal one bar in a confirmed 4/4 section. Verify the planned overlap/loop in beats; do not confuse two beats with two bars. For two matched windows, check both start alignment and equal beat counts.
- Phrase labels such as Chorus or Up do not prove a vocal entry. State when evidence is grid/metadata based rather than freshly auditioned. Keep musical judgement separate from numerical facts.
- Keep one lead vocal prominent during an overlap. A hot cue cannot remove a vocal from a full mix. If a preview used separated drums, disclose the required stem controls or prepare a separate practice edit when requested. A new audio edit does not alter the original source unless explicitly requested.
- Estimate runtime from played selections minus overlaps, at the selected playback tempo; do not sum full file lengths for a short-selection routine.

## Plan, stage, then save

- Discover actual tools. This MCP reads library/cue/grid data but has no general hot-cue writer. CueGen generates structural or Mixed-in-Key-based cues; it does not design the user's exact musical routine by itself. The skill is instructions, not an executable or a model that hears every track.
- Initial installation enables only read tools. Start with `verify_connection.py --library`, then propose a cue plan. `stage_cuegen.py` runs only on an isolated copy and has no live-apply option.
- Precise custom cue edits require a separately prepared, scoped programmatic writer. Do not run old laptop scripts or guessed IDs. Prepare the actual plan and validate it on a copy before asking for any final user closure step.
- Direct database writes require Rekordbox closed. Back up through SQLCipher's backup API to include committed WAL data. Compare every table, update both cue rows and their cache/count, and reject unrelated changes. Require an explicit user's normal closure plus a process check. Never force-kill Rekordbox.
- Apply transactionally after checking the current baseline, re-read persistence through a fresh connection, and report actual changes and backup location. Have the user reopen manually.

Keep original tracks, audio files, memory cues, saved loops and playlists intact outside the requested scope. Installation or skill invocation alone does not authorize library mutations.
