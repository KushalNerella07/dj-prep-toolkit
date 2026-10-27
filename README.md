# DJ Prep Toolkit

Use Codex with your Rekordbox library to inspect tracks and saved cues, plan short transitions, and try cue generation on a copied library.

**Windows x64 preview · Python 3.12.** Verified locally; testing on a fresh laptop is still pending.

## The three pieces

| Project | What it does |
|---|---|
| [Rekordbox MCP](https://github.com/davehenke/rekordbox-mcp) by Dave Henke | Connects Codex to your library and playlists. Our extension adds read-only saved-cue and beat-grid inspection. |
| [Rekordbox Short Blends skill](skills/rekordbox-short-blends/SKILL.md) | Our instructions for planning short transitions, clear cue labels, and preserving existing routines. |
| [CueGen](https://github.com/mganss/CueGen) by Michael Ganss | Generates cues from existing Rekordbox phrase analysis or Mixed in Key data. This toolkit tests it on a copy only. |

Rekordbox MCP uses [pyrekordbox](https://github.com/dylanljones/pyrekordbox). The installer includes pinned versions of the dependencies; you don't need to clone each project separately.

## Get started

Install **Codex**, **Rekordbox**, and **Python 3.12 x64**. Import and analyze a test track in Rekordbox, then run in PowerShell:

```powershell
git clone https://github.com/KushalNerella07/dj-prep-toolkit.git
cd dj-prep-toolkit
py -3.12 setup_windows.py --register-mcp --install-skill
```

You can also use **Code → Download ZIP**. For guided setup, open the project in Codex and paste [START-HERE.txt](START-HERE.txt).

Restart Codex if the tools aren't visible, then ask:

> Use $rekordbox-short-blends. Verify my connection, inspect my test playlist and saved cues, and propose a short transition. Leave my library and playback unchanged.

The default connection is read-only. CueGen trials stay on a copied library; the toolkit has no general hot-cue write endpoint or automatic DJ playback.

[Setup, connection checks & CueGen trials](docs/windows-setup.md) · [What has been tested](docs/validation.md) · [Contributing](CONTRIBUTING.md)

## License

Our toolkit code and skill are [MIT licensed](LICENSE). Third-party projects retain their own [license notices](licenses/); exact versions are in [manifest.json](manifest.json). This is an independent project.
