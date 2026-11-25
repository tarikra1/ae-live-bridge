# ae-live-bridge

[![CI](https://github.com/tarikra1/ae-live-bridge/actions/workflows/ci.yml/badge.svg)](https://github.com/tarikra1/ae-live-bridge/actions/workflows/ci.yml)
[![Version](https://img.shields.io/badge/release-v1.0.0-0EA5E9.svg)](CHANGELOG.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

**Atomic file-queue IPC bridge for executing ExtendScript (`.jsx`) live inside an already-open Adobe After Effects session without spawning conflicting headless `AfterFX.exe -m -noui` processes.**

When automating Adobe After Effects from AI coding agents or Python pipelines, launching a separate headless process overwrites `.aep` files on disk while the artist's interactive session holds stale in-memory state. `ae-live-bridge` solves this with an atomic `.tmp` -> `os.replace` command queue (`cmd_<id>.jsx`) and heartbeat monitor (`bridge-heartbeat.json`).

## Quickstart

```bash
pip install -e .

# Check whether an interactive After Effects bridge is running
ae-bridge status

# Atomically enqueue a UTF-8 .jsx script into the live session
ae-bridge enqueue ./scripts/update_comp.jsx
```

## License

MIT License — see [LICENSE](LICENSE).
