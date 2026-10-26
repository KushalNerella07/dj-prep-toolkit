# Video outline: Codex helps me prepare a DJ set

Aim for a clear 2-3 minute explanation, followed by a separate full installation walkthrough if desired.

## Hook (0:00-0:15)

Show the controller routine, then the cue plan in Codex.

“I use Codex to inspect my Rekordbox library and help prepare short DJ transitions. Three pieces make this work: a connection, a skill, and a cue-generation tool.”

## 1. Connection: Rekordbox MCP (0:15-0:45)

Show https://github.com/davehenke/rekordbox-mcp and the clone command. Credit Dave Henke and the underlying pyrekordbox project.

“This MCP server lets Codex search tracks and inspect my library. We added a small extension to read the saved cues and numerical beat grid directly, so Codex doesn't need to click through Rekordbox or read waveform screenshots.”

Show the actual available-tool list and one read-only track inspection. Distinguish the upstream project from our `get_track_analysis` addition. It does not listen to the whole library or expose a general hot-cue write command.

## 2. Instructions: our Rekordbox Short Blends skill (0:45-1:15)

Show `skills/rekordbox-short-blends/SKILL.md` and invoke `$rekordbox-short-blends`.

“The skill teaches Codex how I want to work: short memorable sections, clear cue labels, counted musical phrases, and preserving routines I've already built. It also separates timing facts from ideas that still need a listening check.”

The skill is our own instructions package, not a music-analysis model. It is included in this toolkit repository alongside the custom integration files; viewers need those files as well as the upstream repo links.

## 3. Cue generation: CueGen (1:15-1:45)

Show https://github.com/mganss/CueGen and credit Michael Ganss. Show a copied-library trial report, not an unverified live write.

“CueGen can place hot cues or memory cues using Rekordbox's existing phrase analysis or Mixed in Key data. For phrase mode, Mixed in Key isn't required. My specific Rani/Jennie cue layout used additional custom scripts—we backed up, tested a copy, and verified the saved changes.”

Say that Rekordbox must be closed for actual database writes. Do not say that CueGen alone automatically chose the exact vocal transitions or that the skill itself writes cues.

## Fresh laptop proof (1:45-2:30)

Show the second Windows laptop with Codex, Python 3.12 and an initialized Rekordbox test library. Show installer completion, MCP tool discovery, one saved-grid read, skill-based proposed timing, and the one-track CueGen trial report. Clearly label a copied-library demo. Record any further live save separately after its scoped verification.

Finish: “The tools handle connection and preparation; I still listen, choose the musical moment, and perform the transition on the controller.”

## Caption / description links

- Rekordbox MCP: https://github.com/davehenke/rekordbox-mcp
- CueGen: https://github.com/mganss/CueGen
- Our portable skill + local additions: https://github.com/KushalNerella07/dj-prep-toolkit
- Setup references: https://developers.openai.com/codex/mcp and https://developers.openai.com/codex/skills

Optional follow-up: explain the separate local drum-separation workflow. The clean Jennie loop came from an audio edit using an estimated drum stem, not from moving a cue point. Do not present AI-generated BPM, key or timestamps from titles as measured facts.
