"""CLI entrypoint for ae-live-bridge."""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from pathlib import Path

from .core import build_eval_command, check_heartbeat, enqueue_command


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="ae-bridge", description="Live After Effects IPC bridge utility.")
    sub = parser.add_subparsers(dest="command", required=True)

    st = sub.add_parser("status", help="Inspect live CEP bridge heartbeat.")
    st.add_argument("--bridge-dir", default="", help="Custom bridge directory.")

    wr = sub.add_parser("wrap", help="Print single-line ExtendScript wrapper for a .jsx file.")
    wr.add_argument("jsx_path", help="Path to target .jsx script.")

    eq = sub.add_parser("enqueue", help="Atomically enqueue a .jsx script for live execution.")
    eq.add_argument("jsx_path", help="Path to target .jsx script.")
    eq.add_argument("--bridge-dir", default="", help="Custom bridge directory.")

    args = parser.parse_args(argv)
    bdir = Path(args.bridge_dir) if getattr(args, "bridge_dir", "") else None

    if args.command == "status":
        status = check_heartbeat(bdir)
        print(json.dumps(asdict(status), indent=2))
        return 0 if status.alive else 1
    if args.command == "wrap":
        print(build_eval_command(args.jsx_path))
        return 0
    if args.command == "enqueue":
        cid, path = enqueue_command(args.jsx_path, bridge_dir=bdir)
        print(json.dumps({"cmd_id": cid, "queued_file": str(path)}, indent=2))
        return 0
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
