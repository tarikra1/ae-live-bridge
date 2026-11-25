"""Atomic file-queue IPC bridge for live Adobe After Effects sessions."""

from __future__ import annotations

import json
import os
import tempfile
import time
import uuid
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class HeartbeatStatus:
    alive: bool
    state: str
    age_seconds: float | None
    bridge_dir: str


def default_bridge_dir() -> Path:
    return Path(tempfile.gettempdir()) / "after-effects-mcp-bridge"


def build_eval_command(jsx_file_path: str | Path) -> str:
    """Build a single-line ExtendScript expression safe for atomic CEP polling."""
    posix_path = Path(jsx_file_path).resolve().as_posix()
    escaped = posix_path.replace('"', '\\"')
    return (
        f'(function(){{ try {{ $.evalFile("{escaped}"); return "OK"; }} '
        f'catch(e) {{ return "Error: " + e.toString(); }} }})()'
    )


def check_heartbeat(bridge_dir: Path | None = None, max_age_sec: float = 15.0) -> HeartbeatStatus:
    bdir = bridge_dir or default_bridge_dir()
    hb_file = bdir / "bridge-heartbeat.json"
    if not hb_file.is_file():
        return HeartbeatStatus(alive=False, state="missing", age_seconds=None, bridge_dir=str(bdir))
    try:
        data = json.loads(hb_file.read_text(encoding="utf-8"))
        age = max(0.0, time.time() - hb_file.stat().st_mtime)
        state = str(data.get("state", "unknown"))
        alive = state == "running" and age <= max_age_sec
        return HeartbeatStatus(alive=alive, state=state, age_seconds=round(age, 3), bridge_dir=str(bdir))
    except Exception:
        return HeartbeatStatus(alive=False, state="corrupt", age_seconds=None, bridge_dir=str(bdir))


def enqueue_command(jsx_script_path: str | Path, bridge_dir: Path | None = None, cmd_id: str | None = None) -> tuple[str, Path]:
    """Atomically stage and publish `cmd_<id>.jsx` so After Effects never reads a half-written file."""
    bdir = bridge_dir or default_bridge_dir()
    bdir.mkdir(parents=True, exist_ok=True)
    cid = cmd_id or uuid.uuid4().hex[:12]
    tmp_path = bdir / f"cmd_{cid}.jsx.tmp"
    final_path = bdir / f"cmd_{cid}.jsx"
    payload = build_eval_command(jsx_script_path)
    tmp_path.write_text(payload, encoding="utf-8", newline="\n")
    os.replace(tmp_path, final_path)
    return cid, final_path
