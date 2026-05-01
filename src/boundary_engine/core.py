from __future__ import annotations

import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


class BoundaryError(Exception):
    """Raised when a boundary scan cannot be completed."""


@dataclass(frozen=True)
class ProofClaims:
    verified_claims: tuple[str, ...]
    verified_cases: set[str]


CLAIM_PATTERNS = [
    (re.compile(r"\bproduction-ready\b", re.IGNORECASE), "Replace with the exact verified readiness state."),
    (re.compile(r"\bproves? [^.!\n]+", re.IGNORECASE), "Tie the claim to a recorded proof case or soften it."),
    (
        re.compile(r"\bguarantees?\b(?!\s+language\b)\s+[^.!\n]+", re.IGNORECASE),
        "Avoid guarantee language unless the proof ledger directly supports it.",
    ),
    (re.compile(r"\bfully verified\b", re.IGNORECASE), "Name the verified cases instead of broad verification."),
    (re.compile(r"\bready for review\b", re.IGNORECASE), "State which proof packet or evidence supports review readiness."),
]


def load_proof_ledger(path: Path | str) -> ProofClaims:
    ledger_path = Path(path)
    if not ledger_path.exists():
        raise BoundaryError(f"Proof ledger not found: {ledger_path}")
    payload = json.loads(ledger_path.read_text(encoding="utf-8"))
    if payload.get("schema_version") != "0.1":
        raise BoundaryError("Unsupported proof ledger schema_version")

    verified_claims = []
    verified_cases = set()
    for run in payload.get("runs", []):
        if run.get("status") == "pass":
            verified_claims.append(run.get("claim", ""))
            verified_cases.add(run.get("case_id", ""))
    return ProofClaims(verified_claims=tuple(item for item in verified_claims if item), verified_cases=verified_cases)


def scan_markdown(path: Path | str, proof: ProofClaims) -> dict:
    markdown_path = Path(path)
    if not markdown_path.exists():
        raise BoundaryError(f"Markdown file not found: {markdown_path}")
    text = markdown_path.read_text(encoding="utf-8")
    scannable_text = _mask_markdown_code(text)
    findings = []

    for pattern, safer_wording in CLAIM_PATTERNS:
        for match in pattern.finditer(scannable_text):
            claim_text = match.group(0).strip()
            if _is_supported(claim_text, proof):
                continue
            line = scannable_text[: match.start()].count("\n") + 1
            findings.append(
                {
                    "line": line,
                    "text": claim_text,
                    "risk": "unsupported-claim",
                    "reason": "No matching passing proof-ledger claim was found.",
                    "safer_wording": safer_wording,
                }
            )

    return {
        "schema_version": "0.1",
        "source": markdown_path.as_posix(),
        "generated_at": _now(),
        "summary": {
            "unsupported_claims": len(findings),
            "verified_claims": len(proof.verified_claims),
        },
        "proof_cases": sorted(proof.verified_cases),
        "findings": findings,
    }


def render_register(report: dict) -> str:
    lines = [
        "# Boundary Register",
        "",
        f"Source: `{report['source']}`",
        f"Generated: {report['generated_at']}",
        "",
        "## Summary",
        f"- Unsupported claims: {report['summary']['unsupported_claims']}",
        f"- Verified proof claims: {report['summary']['verified_claims']}",
        "",
        "## Findings",
    ]
    if report["findings"]:
        for finding in report["findings"]:
            lines.extend(
                [
                    "",
                    f"- Line {finding['line']}: `{finding['text']}`",
                    f"  - Risk: {finding['risk']}",
                    f"  - Reason: {finding['reason']}",
                    f"  - Safer wording: {finding['safer_wording']}",
                ]
            )
    else:
        lines.append("")
        lines.append("- No unsupported boundary claims found.")

    lines.extend(["", "## Proof Cases"])
    if report["proof_cases"]:
        for case_id in report["proof_cases"]:
            lines.append(f"- `{case_id}`")
    else:
        lines.append("- No passing proof cases were found.")

    return "\n".join(lines) + "\n"


def write_report(root: Path | str, report: dict) -> dict[str, Path]:
    project_root = Path(root).absolute()
    u27_dir = project_root / "u27"
    u27_dir.mkdir(parents=True, exist_ok=True)
    register_path = u27_dir / "BOUNDARY_REGISTER.md"
    json_path = u27_dir / "boundary_report.json"
    register_path.write_text(render_register(report), encoding="utf-8")
    json_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return {"register": register_path, "json": json_path}


def _is_supported(claim_text: str, proof: ProofClaims) -> bool:
    normalized = _normalize(claim_text)
    return any(normalized and normalized in _normalize(claim) for claim in proof.verified_claims)


def _normalize(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip().lower())


def _mask_markdown_code(text: str) -> str:
    masked_lines = []
    in_fence = False
    for line in text.splitlines(keepends=True):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            masked_lines.append(_spaces_like(line))
            continue
        if in_fence:
            masked_lines.append(_spaces_like(line))
        else:
            masked_lines.append(re.sub(r"`[^`\n]+`", lambda match: " " * (match.end() - match.start()), line))
    return "".join(masked_lines)


def _spaces_like(value: str) -> str:
    return "".join("\n" if char == "\n" else " " for char in value)


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()
