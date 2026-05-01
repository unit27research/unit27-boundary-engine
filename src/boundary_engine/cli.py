from __future__ import annotations

import argparse
from pathlib import Path
import sys

from boundary_engine.core import BoundaryError, load_proof_ledger, scan_markdown, write_report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="boundary-engine",
        description="Check public repo language against recorded proof artifacts.",
    )
    subparsers = parser.add_subparsers(dest="action", required=True)

    scan_parser = subparsers.add_parser("scan", help="Scan a markdown file against a proof ledger.")
    scan_parser.add_argument("markdown", help="Markdown file to scan.")
    scan_parser.add_argument("--proof", default="u27/proof_ledger.json", help="Proof Ledger JSON path.")
    scan_parser.add_argument("--root", default=".", help="Project root. Defaults to current directory.")

    demo_parser = subparsers.add_parser("demo", help="Create a demo project and boundary register.")
    demo_parser.add_argument("--root", default="boundary-engine-demo", help="Demo project root.")

    args = parser.parse_args(argv)

    try:
        if args.action == "scan":
            root = Path(args.root).absolute()
            markdown = _resolve(root, args.markdown)
            proof_path = _resolve(root, args.proof)
            proof = load_proof_ledger(proof_path)
            report = scan_markdown(markdown, proof)
            report["source"] = _display_path(root, markdown)
            write_report(root, report)
            unsupported = report["summary"]["unsupported_claims"]
            print(f"Boundary scan complete: unsupported={unsupported}")
            return 1 if unsupported else 0

        if args.action == "demo":
            root = Path(args.root).absolute()
            _create_demo(root)
            proof = load_proof_ledger(root / "u27" / "proof_ledger.json")
            report = scan_markdown(root / "README.md", proof)
            report["source"] = "README.md"
            write_report(root, report)
            unsupported = report["summary"]["unsupported_claims"]
            print(f"Demo project: {root}")
            print(f"Boundary register: {root / 'u27' / 'BOUNDARY_REGISTER.md'}")
            print(f"Boundary scan complete: unsupported={unsupported}")
            return 0
    except BoundaryError as error:
        print(f"error: {error}", file=sys.stderr)
        return 2

    return 1


def _resolve(root: Path, value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else root / path


def _display_path(root: Path, path: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def _create_demo(root: Path) -> None:
    (root / "u27").mkdir(parents=True, exist_ok=True)
    (root / "README.md").write_text(
        "# Boundary Engine Demo\n\nThis repo is production-ready and proves reliable agent behavior.\n",
        encoding="utf-8",
    )
    (root / "u27" / "proof_ledger.json").write_text(
        (
            '{"schema_version":"0.1","runs":['
            '{"case_id":"tests-pass","claim":"The project test suite passes in the current local checkout.",'
            '"status":"pass","evidence":["u27/evidence/run-0001.txt"]}'
            "]}"
        ),
        encoding="utf-8",
    )


if __name__ == "__main__":
    raise SystemExit(main())
