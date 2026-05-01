import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SRC_PATH = Path(__file__).resolve().parents[1] / "src"


class BoundaryEngineCliTests(unittest.TestCase):
    def run_cli(self, root, *args):
        env = os.environ.copy()
        env["PYTHONPATH"] = str(SRC_PATH)
        return subprocess.run(
            [sys.executable, "-m", "boundary_engine.cli", *args],
            cwd=root,
            env=env,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_scan_command_writes_boundary_artifacts(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_text("This repo is production-ready.\n", encoding="utf-8")
            _write_ledger(root)

            result = self.run_cli(root, "scan", "README.md", "--proof", "u27/proof_ledger.json")

            self.assertEqual(result.returncode, 1, result.stderr)
            self.assertIn("unsupported=1", result.stdout)
            self.assertTrue((root / "u27" / "BOUNDARY_REGISTER.md").exists())
            self.assertTrue((root / "u27" / "boundary_report.json").exists())
            self.assertIn("Source: `README.md`", (root / "u27" / "BOUNDARY_REGISTER.md").read_text(encoding="utf-8"))

    def test_scan_command_returns_zero_when_claims_match_proof(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_text(
                "The project test suite passes in the current local checkout.\n",
                encoding="utf-8",
            )
            _write_ledger(root)

            result = self.run_cli(root, "scan", "README.md", "--proof", "u27/proof_ledger.json")

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("unsupported=0", result.stdout)

    def test_demo_command_creates_complete_demo(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)

            result = self.run_cli(root, "demo")

            self.assertEqual(result.returncode, 0)
            demo_root = root / "boundary-engine-demo"
            self.assertTrue((demo_root / "u27" / "BOUNDARY_REGISTER.md").exists())
            self.assertIn("production-ready", (demo_root / "u27" / "BOUNDARY_REGISTER.md").read_text(encoding="utf-8"))


def _write_ledger(root: Path):
    u27 = root / "u27"
    u27.mkdir()
    (u27 / "proof_ledger.json").write_text(
        '{"schema_version":"0.1","runs":[{"case_id":"tests-pass","claim":"The project test suite passes in the current local checkout.","status":"pass","evidence":["u27/evidence/run-0001.txt"]}]}',
        encoding="utf-8",
    )


if __name__ == "__main__":
    unittest.main()
