# Changelog

All notable changes to `ae-live-bridge` are documented in this file.

## [1.0.0] - 2026-11-25

### Added
- Atomic `cmd_<id>.jsx` command writer using `.tmp` staging and `os.replace` to prevent partial ExtendScript reads.
- Heartbeat verifier (`bridge-heartbeat.json`) detecting stale vs active After Effects CEP sessions.
- Single-line safe `$.evalFile(...)` wrapper escaping Windows backslashes and stripping line-breaking `//` comments.
- CLI (`ae-bridge`) and multi-version GitHub Actions CI matrix.
