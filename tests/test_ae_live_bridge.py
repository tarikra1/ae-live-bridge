import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import json
import tempfile
import unittest

from ae_live_bridge.core import build_eval_command, check_heartbeat, enqueue_command


class TestAeLiveBridge(unittest.TestCase):
    def test_build_eval_command_uses_forward_slashes_and_single_line(self) -> None:
        expr = build_eval_command("scripts/build_comp.jsx")
        self.assertNotIn("\n", expr)
        self.assertNotIn("//", expr)
        self.assertIn("$.evalFile(", expr)
        self.assertIn("build_comp.jsx", expr)

    def test_heartbeat_and_atomic_enqueue(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            bdir = Path(tmp)
            self.assertFalse(check_heartbeat(bdir).alive)
            (bdir / "bridge-heartbeat.json").write_text(json.dumps({"state": "running"}), encoding="utf-8")
            self.assertTrue(check_heartbeat(bdir).alive)

            dummy_jsx = bdir / "task.jsx"
            dummy_jsx.write_text("app.beginUndoGroup('test'); app.endUndoGroup();", encoding="utf-8")
            cid, queued = enqueue_command(dummy_jsx, bridge_dir=bdir, cmd_id="abc123")
            self.assertEqual(cid, "abc123")
            self.assertTrue(queued.is_file())
            self.assertFalse((bdir / "cmd_abc123.jsx.tmp").exists())


if __name__ == "__main__":
    unittest.main()
