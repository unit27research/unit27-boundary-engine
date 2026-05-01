import json
import tempfile
import unittest
from pathlib import Path

from boundary_engine.core import (
    BoundaryError,
    load_proof_ledger,
    render_register,
    scan_markdown,
    write_report,
)


class BoundaryEngineCoreTests(unittest.TestCase):
    def test_load_proof_ledger_extracts_verified_claims(self):
        with tempfile.TemporaryDirectory() as tmp:
            ledger_path = Path(tmp) / "proof_ledger.json"
            ledger_path.write_text(
                json.dumps(
                    {
                        "schema_version": "0.1",
                        "runs": [
                            {
                                "case_id": "tests-pass",
                                "claim": "The project test suite passes in the current local checkout.",
                                "status": "pass",
                                "evidence": ["u27/evidence/run-0001.txt"],
                            },
                            {
                                "case_id": "missing-demo",
                                "claim": "The hosted demo works.",
                                "status": "fail",
                                "evidence": ["u27/evidence/run-0002.txt"],
                            },
                        ],
                    }
                ),
                encoding="utf-8",
            )

            proof = load_proof_ledger(ledger_path)

            self.assertEqual(list(proof.verified_claims), ["The project test suite passes in the current local checkout."])
            self.assertEqual(proof.verified_cases, {"tests-pass"})

    def test_scan_markdown_flags_claims_without_proof(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            readme = root / "README.md"
            readme.write_text(
                "# Demo\n\nThis repo is production-ready and proves reliable agent behavior.\n",
                encoding="utf-8",
            )
            proof = load_proof_ledger(_write_ledger(root, verified_cases=["tests-pass"]))

            report = scan_markdown(readme, proof)

            self.assertEqual(report["summary"]["unsupported_claims"], 2)
            findings = [item["text"] for item in report["findings"]]
            self.assertIn("production-ready", findings[0])
            self.assertIn("proves reliable agent behavior", findings[1])

    def test_scan_markdown_allows_claim_with_matching_proof_phrase(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            readme = root / "README.md"
            readme.write_text(
                "# Demo\n\nThe project test suite passes in the current local checkout.\n",
                encoding="utf-8",
            )
            proof = load_proof_ledger(_write_ledger(root, verified_cases=["tests-pass"]))

            report = scan_markdown(readme, proof)

            self.assertEqual(report["summary"]["unsupported_claims"], 0)
            self.assertEqual(report["findings"], [])

    def test_scan_markdown_ignores_code_examples(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            readme = root / "README.md"
            readme.write_text(
                "This phrase is an example: `production-ready`.\n\n"
                "```text\n"
                "This project guarantees perfect behavior.\n"
                "```\n",
                encoding="utf-8",
            )
            proof = load_proof_ledger(_write_ledger(root, verified_cases=[]))

            report = scan_markdown(readme, proof)

            self.assertEqual(report["summary"]["unsupported_claims"], 0)
            self.assertEqual(report["findings"], [])

    def test_scan_markdown_does_not_flag_explanatory_guarantee_language_phrase(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            readme = root / "README.md"
            readme.write_text(
                "It flags unsupported guarantee language when no matching proof exists.\n",
                encoding="utf-8",
            )
            proof = load_proof_ledger(_write_ledger(root, verified_cases=[]))

            report = scan_markdown(readme, proof)

            self.assertEqual(report["summary"]["unsupported_claims"], 0)
            self.assertEqual(report["findings"], [])

    def test_render_register_includes_rewrites_and_limits(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            readme = root / "README.md"
            readme.write_text("This project is production-ready.\n", encoding="utf-8")
            proof = load_proof_ledger(_write_ledger(root, verified_cases=[]))
            report = scan_markdown(readme, proof)

            register = render_register(report)

            self.assertIn("# Boundary Register", register)
            self.assertIn("production-ready", register)
            self.assertIn("Safer wording", register)

    def test_write_report_writes_markdown_and_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            readme = root / "README.md"
            readme.write_text("This project is production-ready.\n", encoding="utf-8")
            proof = load_proof_ledger(_write_ledger(root, verified_cases=[]))
            report = scan_markdown(readme, proof)

            paths = write_report(root, report)

            self.assertTrue(paths["register"].exists())
            self.assertTrue(paths["json"].exists())
            self.assertIn("Boundary Register", paths["register"].read_text(encoding="utf-8"))


def _write_ledger(root: Path, verified_cases: list[str]) -> Path:
    claims = {
        "tests-pass": "The project test suite passes in the current local checkout.",
    }
    ledger = {
        "schema_version": "0.1",
        "runs": [
            {
                "case_id": case_id,
                "claim": claims[case_id],
                "status": "pass",
                "evidence": ["u27/evidence/run-0001.txt"],
            }
            for case_id in verified_cases
        ],
    }
    path = root / "u27" / "proof_ledger.json"
    path.parent.mkdir(parents=True)
    path.write_text(json.dumps(ledger), encoding="utf-8")
    return path


if __name__ == "__main__":
    unittest.main()
