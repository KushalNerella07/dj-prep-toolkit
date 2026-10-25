# DJ Prep Toolkit

An open-source Windows toolkit for using Codex with a local Rekordbox library: inspect saved tracks and cues, plan short DJ transitions, and test cue generation on a copied database.

**Status: Windows x64 preview, Python 3.12.** Core tools have been verified locally. Fresh-machine acceptance testing is still pending. macOS and Linux are not supported in this release.

## Three parts, one workflow

| Part | Purpose |
|---|---|
| [Rekordbox MCP](https://github.com/davehenke/rekordbox-mcp) | Library and playlist access, extended here with a read-only saved-cue and beat-grid inspector. |
| [Rekordbox Short Blends skill](skills/rekordbox-short-blends/SKILL.md) | Reusable instructions for short selections, phrase timing, concise cues and preserving existing routines. |
| [CueGen](https://github.com/mganss/CueGen) | Cue generation from existing Rekordbox phrase analysis or Mixed in Key data, tested here on isolated copies. |

This is an independent toolkit. It is not affiliated with AlphaTheta/Pioneer, OpenAI, or the upstream project maintainers. It does not listen to an entire music library, choose every musical transition, remove vocals with a cue point, or perform a DJ set automatically.

## Quick start

Install **Codex**, **Rekordbox**, and **64-bit Python 3.12** on Windows. Initialize a test library in Rekordbox, import a track, and analyze it. Then clone or download this repository and open PowerShell in its root:

```powershell
py -3.12 setup_windows.py --register-mcp --install-skill
```

The default runtime destination is `%USERPROFILE%\Documents\Codex\DJStack`. Setup verifies the bundled payloads, creates a separate Python environment, installs pinned dependencies, preserves unrelated Codex configuration, and registers only read tools initially. It does not open a Rekordbox database. Existing installation/server/skill locations are not silently overwritten.

For a relocated library, add `--database 'D:\your-library\master.db'`. For a different runtime location, add `--target 'D:\DJStack'`.

Restart Codex or start a fresh chat if tools or the skill are not visible. Verify the real connection:

```powershell
& "$env:USERPROFILE\Documents\Codex\DJStack\rekordbox-mcp\.venv\Scripts\python.exe" "$env:USERPROFILE\Documents\Codex\DJStack\verify_connection.py" --library
```

Then ask Codex:

> Use $rekordbox-short-blends. Verify my connection, inspect my test playlist and saved cues/beat grids, and propose a short transition. Distinguish stored facts from musical interpretations. Leave my library and playback unchanged.

Or open this repo in Codex and paste [START-HERE.txt](START-HERE.txt) for guided setup. See [detailed Windows setup](docs/windows-setup.md) for prerequisites, paths, MCP refresh and troubleshooting.

## Try cue generation on a copy

Use MCP to discover the current ID of an analyzed test track. Prefer a track without custom cues for the first test. Close Rekordbox normally for the demo, then run:

```powershell
& "$env:USERPROFILE\Documents\Codex\DJStack\rekordbox-mcp\.venv\Scripts\python.exe" "$env:USERPROFILE\Documents\Codex\DJStack\stage_cuegen.py" --track-id YOUR_TEST_TRACK_ID
```

This helper backs up consistently, copies the target's analysis files, runs CueGen on the copy, repairs its cached cue count and checks every database table. **It has no live-apply option.** It rejects trials that alter existing cues or unrelated rows. Phrase mode does not require Mixed in Key.

The MCP has no general hot-cue write endpoint. Precise custom cue editing is separate, scoped work: the skill describes planning, copy testing, app closure, backups and transactional verification. Old machine-specific cue scripts are not part of this repository. A cue marker does not automatically control stems, faders or playback.

## What is included

- Windows installer and a read-only default MCP configuration.
- Custom MCP overlay for saved cue/grid inspection, logging and library paths.
- Portable DJ preparation skill.
- Copy-only CueGen trial tool.
- Pinned upstream source archives and the Windows x64 CueGen binary, with [provenance](manifest.json), [payload hashes](payload-sha256.json) and [upstream notices](licenses/).
- Installer/configuration/archive tests, Windows CI and source-kit packaging.

The pinned CueGen source snapshot omits upstream test audio/database fixtures. Bundled third-party code retains its own license. User music, Rekordbox databases/analysis, account files, virtual environments and previous track-specific plans are excluded.

## Validation and first-release scope

Local checks found 32 MCP server tools and successfully read saved beat-grid data. An isolated CueGen test added eight cues to its selected track while the live library remained unchanged. See [validation details and limits](docs/validation.md).

Automated tests use temporary directories and synthetic configuration; they never require a live library. CI verifies the Windows source kit, not a complete fresh Rekordbox installation or a live cue save. The next acceptance test is a clean Windows laptop installation.

The first release focuses on setup, library inspection, short-transition planning and copied-library cue generation. Audio/stem editing, automatic playback, macOS and Linux are outside this release.

## Development

```powershell
py -3.12 -m unittest discover -s tests -v
py -3.12 scripts/build_release.py
```

The build writes a checked ZIP and checksum to `dist/`. See [contributing](CONTRIBUTING.md), [security reporting](SECURITY.md), and the [video outline](docs/video-outline.md).

## Credits and license

Original toolkit code and skill: [MIT](LICENSE).

- Dave Henke — [rekordbox-mcp](https://github.com/davehenke/rekordbox-mcp), MIT. Its underlying library is [pyrekordbox](https://github.com/dylanljones/pyrekordbox).
- Michael Ganss — [CueGen](https://github.com/mganss/CueGen), MIT.

The custom overlay, launcher, verification tools and skill are this project's additions. The upstream pins are recorded in `manifest.json`; existing third-party copyright and license notices are preserved in their source archives and `licenses/`.
