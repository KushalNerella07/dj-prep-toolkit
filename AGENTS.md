# Project scope

This repository supports Windows x64 and Python 3.12 only. Keep the first release focused on reproducible setup, read-only Rekordbox inspection, the short-blends skill, and copied-library CueGen trials. macOS/Linux support and audio/stem production are outside this release.

Never modify a developer's live Rekordbox library as a coding or CI test. Tests must use temporary directories, synthetic configuration, or explicitly isolated database copies. Never commit music, user databases, account settings/tokens, virtual environments, or machine-specific cue plans.

Preserve upstream MIT notices and pinned provenance in manifest.json and licenses/. The overlay is custom code; do not present it as an upstream feature. Source archives and release binaries are pinned payloads; verify their hashes before installation. Change pins deliberately, with corresponding validation and attribution.

Run `py -3.12 -m unittest discover -s tests -v` and `py -3.12 scripts/build_release.py` before publishing a code change. These tests and packaging do not require a real Rekordbox library. A successful CI run does not establish fresh-machine or live cue-edit compatibility. Keep documentation honest about actual validation.

Do not use UI automation to control Rekordbox. Custom live cue writes remain separately scoped work requiring a closed app, backup, staged verification and fresh persistence checks. The CueGen trial helper intentionally has no live-apply option.
