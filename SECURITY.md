# Reporting security problems

Do not post secrets, account configuration or a real Rekordbox database in an issue. For a reproducible security concern, use a minimal synthetic example. Once hosted on GitHub, use the repository's private vulnerability reporting option if it is enabled; otherwise contact the maintainer privately before publishing sensitive details.

This project accesses local software and library data. Setup must not open or mutate a Rekordbox database. The initial MCP registration exposes only read tools, and the CueGen helper operates on a copied database with no live-apply option. Treat any unexpected write outside those boundaries as a bug.
