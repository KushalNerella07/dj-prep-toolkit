# Portable integration workflow

Read the adjacent `installation.json` added by the installer to locate this laptop's DJStack. If absent, locate the kit/installation with the user; do not substitute a previous computer's path.

The stack contains:

- `rekordbox-mcp/`: pinned davehenke/rekordbox-mcp with the local cue/grid reader and stderr logging fixes.
- `cuegen/source/`: pinned mganss/CueGen source; `cuegen/bin/`: Windows x64 release 1.0.37.
- `run_rekordbox_mcp.py`: portable local launcher. The default library is `%APPDATA%\Pioneer\rekordbox\master.db`. Relocated libraries can be selected with `dj-stack.json` or the `REKORDBOX_DATABASE` environment variable. Explicitly pass both `path` and `db_dir` when constructing a pyrekordbox database: `db_dir` alone does not select a different database file.
- `verify_connection.py`: actual stdio MCP discovery and optional read-only library checks using a dynamically selected track.
- `stage_cuegen.py`: scoped copy-only CueGen trial. It backs up consistently, copies the target's ANLZ data, repairs the trial's cue count, verifies every database table and preserves existing cues.

Use the venv at `rekordbox-mcp/.venv/Scripts/python.exe`. Do not copy another machine's venv, Codex auth/config, library database or path-specific cue plans. Rekordbox must be installed and initialized locally, with test music imported and analyzed for a meaningful cue/grid trial. Library transfer is separate and should use Rekordbox's supported migration workflow.

## Direct cue-write details

The cue table is `djmdCue`. A-H Kind values are `[1,2,3,5,6,7,8,9]`; Kind 0 denotes memory cues. Kind 4 is not ordinary pad D. Preserve existing ID/UUID/content linkage when editing a cue. Preserve complete loop rows unless loop edits were requested.

Positions are `InMsec`; `InFrame = floor(InMsec * 150 / 1000)`. Moved cues must not retain stale MPEG seek hints. Verified time-only layouts use cleared seek fields. Preserve explicit loop boundaries, loop size and active-loop state appropriately.

`contentCue.Cues` is the cue JSON cache; `rb_cue_count` must match it and the individual rows. SQL cue timestamps must use the syntax written by Rekordbox (for the tested Windows library, `YYYY-MM-DD HH:mm:ss.sss +00:00`); JSON dates use ISO format. Do not copy ISO JSON date strings blindly into SQL date columns: the previous laptop exposed malformed regenerated cache dates after such writes.

Use `sqlcipher3` with read-only connections for planning. The generic application key is already published in the pinned CueGen source; the launcher reads it without printing or transferring account credentials. Never print encryption keys or personal configuration.

Before live changes, create a new SQLCipher backup, validate the exact scoped edit on a copy, check no Rekordbox process remains after the user closes it, compare the live baseline, apply in a transaction, and validate through a fresh connection. Do not overwrite a live master.db wholesale with a stale test copy.

CueGen 1.0.37 has two locally observed quirks: its CLI exit status can be inverted, and the cached cue count can be stale. Validate the log and database results; an exit code alone is insufficient. CueGen uses existing phrase analysis; phrase-only mode does not require Mixed in Key. Native waveform/beat-grid analysis is performed by Rekordbox, not this integration.
