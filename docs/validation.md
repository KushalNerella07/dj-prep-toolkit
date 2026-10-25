# Local validation — 2026-10-25

Passed on the original Windows laptop using a freshly unpacked source tree and the existing pinned Python 3.12 dependency environment:

- Installer prepare-only extraction and overlay application into a new directory.
- Portable skill frontmatter/structure validation.
- Synthetic Codex configuration test: unrelated entries preserved, read-tool allowlist correct, duplicate registration refused, original configuration backed up.
- Real stdio MCP initialization and discovery: 32 server tools.
- Read-only playlist/search/cue inspection and a dynamically selected track with 368 saved beat-grid entries.
- Copied-library CueGen test: zero existing cues -> eight trial cues; full table diff limited to target cue/cache rows; cached count repaired; integrity check passed; live database not modified by the trial.
- Negative tests: rejected a trial that rewrote existing cues and a track without a cue-cache row.

The sandbox blocked Python's local event-loop self-pipe socket. The actual MCP test passed when run with approved local execution outside that sandbox. This was an execution-environment restriction, not a change made to networking or the Windows firewall.

Not yet verified: fresh dependency installation on the second laptop, that laptop's Rekordbox version/library compatibility, its Codex native tool refresh, or a live cue save there. The second-laptop run is the remaining acceptance test. No runtime installation, Codex configuration or skill installation on this original laptop was changed by the kit test.

The portable skill contains instructions for scoped custom edits; it is not a bundled general-purpose cue-writing endpoint. The included CueGen wrapper intentionally has no live-apply option.
