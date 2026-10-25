# DJ Prep Toolkit: detailed Windows setup

Prepared 2026-10-25. This reproduces the three-part setup for a Windows x64 laptop. The toolkit is an independent project, not an official Rekordbox integration. Use the root README as the primary entry point.

| Part | Source | What it does |
|---|---|---|
| Rekordbox MCP | https://github.com/davehenke/rekordbox-mcp | Connects Codex to library/search/playlist tools. This kit adds our read-only cue/beat-grid inspection tool and launch fixes. |
| Rekordbox Short Blends skill | `skills/rekordbox-short-blends/SKILL.md` | Our custom instructions for the short-selection workflow, timing checks, cue labels, preservation and staged-save procedure; included in this repository. |
| CueGen | https://github.com/mganss/CueGen | Generates hot/memory cues from existing Rekordbox phrase data or Mixed in Key cues. Phrase-only use does not require Mixed in Key. |

Our precise Rani/Jennie pad edits used additional scoped Python/SQLCipher scripts. Those old scripts contain machine/library-specific assumptions and are deliberately not shipped. The portable skill describes how to prepare and verify a new scoped edit. Neither a skill nor CueGen automatically discovers the best musical transition or removes vocals from a full mix.

## Before recording the fresh-laptop test

You need Codex, **64-bit Python 3.12**, and Rekordbox installed on the second laptop. Open Rekordbox normally, create a local library, import one or two test tracks, and analyze them. Music/library migration is a separate operation; this kit contains no audio or database. Use a backed-up test library for the first cue-writing demonstration.

If Python is missing, ask Codex on that laptop to install official Python 3.12 x64 before running this installer. This kit does not install an operating-system runtime automatically. Git is needed for the on-camera clone demonstration, but not for the included pinned-source installer.

## Install

1. Clone or download this repository on the second laptop, or extract a Windows source kit built from it.
2. Open that extracted folder as a local Codex project. Paste the prompt in `START-HERE.txt`.
3. Or run this from PowerShell in the extracted kit:

```powershell
py -3.12 .\setup_windows.py --register-mcp --install-skill
```

The default destination is `%USERPROFILE%\Documents\Codex\DJStack`. A different destination can be supplied with `--target`. If the library is relocated, also pass `--database 'D:\path\to\master.db'` (replace this example with the actual local path).

The installer unpacks source archives created from our exact cloned commits, applies our included overlay, installs pinned Python dependencies, registers a new **read-only** `rekordbox` MCP entry, and installs the portable skill in `~/.agents/skills/rekordbox-short-blends`. CueGen's upstream test fixtures are excluded because they include sample audio and a test database; clone the full upstream repo if you want to build or run its tests. The installer backs up an existing Codex config and preserves other entries. Existing destinations/server names/skill folders are not overwritten automatically. If the setup exits partway through, inspect the printed error before retrying into a new destination.

The MCP config lives in `~/.codex/config.toml` (or `CODEX_HOME`). Native MCP tools may need a fresh chat or app restart to appear. Skill discovery locations vary with old clients: current official docs use `~/.agents/skills`; this original laptop used the older `~/.codex/skills`. If the second app cannot find the skill, have Codex inspect its installed skill locations rather than installing duplicate copies with the same name.

## Verify the connection before changing anything

```powershell
& "$env:USERPROFILE\Documents\Codex\DJStack\rekordbox-mcp\.venv\Scripts\python.exe" "$env:USERPROFILE\Documents\Codex\DJStack\verify_connection.py" --library
```

Adjust the paths if you used `--target`. This launches a real stdio MCP client, discovers tools, lists playlists, finds a test track dynamically and reads its cue/grid data. It does not use old track IDs or modify library data. A successful direct client test does not prove the already-running Codex chat has refreshed its own tool list; check both.

Then ask Codex:

> Use $rekordbox-short-blends. Verify the Rekordbox connection, list the available tools, read my test playlist and its existing cues/beat grids, then propose a short transition. Distinguish stored facts from musical interpretations. Leave the library unchanged.

## Test CueGen on a copy only

Choose one already-analyzed test track and obtain its current ID with MCP. Close Rekordbox normally for this demo, then run:

```powershell
& "$env:USERPROFILE\Documents\Codex\DJStack\rekordbox-mcp\.venv\Scripts\python.exe" "$env:USERPROFILE\Documents\Codex\DJStack\stage_cuegen.py" --track-id YOUR_TEST_TRACK_ID
```

Replace `YOUR_TEST_TRACK_ID` with the newly discovered numeric ID. For an initial demonstration, choose a normally imported, analyzed test track with no custom cues and an existing cue-cache row. This makes a consistent encrypted copy, copies that track's ANLZ files, runs CueGen against the copy, repairs its cached count, and audits every database table. It has **no live apply option**. If a trial fails or changes unrelated rows, inspect the trial report/log; the live library is unchanged. A track with all cue pads already occupied may produce no new cues. CueGen can rewrite existing cue rows even in merge mode; the wrapper rejects that trial rather than treating it as a preservation success.

CueGen 1.0.37 can return exit code 1 even after success and can leave a stale cached cue count; our wrapper validates results rather than trusting the code alone. Read the log and report before calling the demo successful. Applying custom cues to the real library is a subsequent, explicitly scoped task: prepare/test the plan first, close Rekordbox, make a fresh backup, apply transactionally and re-read the saved rows. Initial MCP registration exposes read tools only.

## Clone commands to show in the video

```powershell
git clone https://github.com/davehenke/rekordbox-mcp.git
git -C rekordbox-mcp checkout d8dce67700911b6bef84b25c5f93ae07f200a1c5
git clone https://github.com/mganss/CueGen.git
git -C CueGen checkout eac34c8c1f007599261f45127095717e0f4abd01
```

For a matching demo, apply the kit's MCP overlay and pinned requirements after cloning; upstream alone does not include our `get_track_analysis` extension. CueGen source and its executable are distinct: this kit includes the official Windows x64 v1.0.37 executable archive. The GitHub release is https://github.com/mganss/CueGen/releases/tag/v1.0.37.

## Scope and evidence

Source commits and exclusions are in the root `manifest.json`; pinned payload hashes are in `payload-sha256.json`. Generated release ZIPs also include `SHA256SUMS.json`. The source overlays, installer and portable skill are custom additions, not claims about upstream functionality. No account config, auth tokens, music, databases, virtual environments or old track-ID-specific plans are included. The launcher uses the generic application SQLCipher key published in CueGen source; it does not copy a user's account credentials.

The video should say what was actually tested. Local verification on the original Windows laptop is not a completed clean installation on the second laptop. Record the second laptop's install, MCP discovery, read-only checks and copied-library CueGen report before describing that fresh install as successful.

Audio/stem work is optional and separate: the Jennie preview used local PyTorch/torchaudio HDEMUCS and FFmpeg. Those libraries, model weights and the practice-edit audio are not part of these three core components or included in this kit.

Official references: [Codex MCP configuration](https://developers.openai.com/codex/mcp), [Codex skills and discovery locations](https://developers.openai.com/codex/skills), [Rekordbox MCP](https://github.com/davehenke/rekordbox-mcp), [CueGen](https://github.com/mganss/CueGen).
