# Contributing

Start with an issue describing the problem, Windows/Python/Rekordbox versions, expected behavior, and a redacted error message. Never attach an actual music library, account configuration, authentication tokens, or copyrighted track files.

Use Python 3.12 x64 on Windows. The initial test suite uses the standard library:

```powershell
py -3.12 -m unittest discover -s tests -v
py -3.12 scripts/build_release.py
```

These tests check payload integrity, real source extraction, read-only MCP configuration, preservation of existing settings, installer preflight, and release contents. They do not touch Rekordbox. Integration tests involving a library must remain opt-in and use a copied test database. Keep the initial MCP tool allowlist read-only.

Source versions live in manifest.json. Public payloads are bundled for a reproducible first installation and are covered by payload-sha256.json. If changing a payload, record its upstream source/version, keep the appropriate notices, verify provenance, and update its hash deliberately. Do not casually replace an upstream archive with a local working tree.

For platform expansion, propose the path/dependency/binary strategy and a real-machine test plan first. macOS and Linux are not currently supported. Audio separation and performance playback are separate future features.
