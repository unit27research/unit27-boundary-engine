# U27-S05 // Boundary Engine

[![CI](https://github.com/unit27research/unit27-boundary-engine/actions/workflows/ci.yml/badge.svg)](https://github.com/unit27research/unit27-boundary-engine/actions/workflows/ci.yml)

Boundary Engine enforces claim discipline by checking public repo language against recorded proof artifacts.

```text
U27-S05
BOUNDARY ENGINE

CLASS: SYSTEM
FUNCTION: Claim Boundary + Proof Alignment
REF_ID: BOUNDARY-ENGINE-01
```

It answers one narrow question:

> Do this repo's public claims stay inside its recorded proof?

## Why Use It

Use Boundary Engine before publishing a repo, demo, or research artifact to catch public claims that outrun recorded evidence.

It is useful when a README says things like `production-ready`, `tested`, `validated`, or `ready for review`, but the repo needs an explicit proof trail for those claims.

Example:

```text
Claim: This repo is production-ready.
Result: unsupported unless a matching passing proof case exists.
```

## 60-Second Start

From this repo:

```bash
pip install -e .
boundary-engine demo
cat boundary-engine-demo/u27/BOUNDARY_REGISTER.md
```

On your own repo:

```bash
boundary-engine scan README.md --proof u27/proof_ledger.json
```

## What It Does

Boundary Engine scans markdown claims and writes:

1. `u27/BOUNDARY_REGISTER.md`
2. `u27/boundary_report.json`

It flags unsupported public language such as `production-ready`, broad proof claims, guarantee language, and review-readiness language when no matching passing Proof Ledger claim exists.

It is designed to feel like a deterministic claim-boundary check, not a legal review or copywriting assistant.

## Install

For local development:

```bash
pip install -e .
```

After this repo is public:

```bash
pipx install git+https://github.com/unit27research/unit27-boundary-engine
```

## CLI

```bash
boundary-engine scan README.md --proof u27/proof_ledger.json
boundary-engine demo
```

Exit codes:

```text
0 = no unsupported claims
1 = unsupported claims found
2 = scan error
```

## Architecture

```text
README -> extract claim risks -> compare proof ledger -> write boundary register
```

Boundary Engine does not decide whether a project is good. It checks whether public-facing language has outrun recorded evidence.

## Reliability

Boundary Engine is maintained as part of the Unit27 research toolchain. CI verifies the test suite, wheel build, and wheel contents before changes are considered ready.

## What It Does Not Do

Boundary Engine does not:

1. Certify truth
2. Replace legal or compliance review
3. Rewrite full documents
4. Judge product quality
5. Infer evidence that is not in the proof ledger

## Verify

```bash
PYTHONPATH=src python3 -m unittest discover -s tests
boundary-engine demo
boundary-engine scan README.md --proof u27/proof_ledger.json
```

## Acceptance

```bash
PYTHONPATH=src python3 -m unittest discover -s tests
PYTHONPATH=src python3 -m boundary_engine.cli demo --root examples/sample-project
PYTHONPATH=src python3 -m boundary_engine.cli scan README.md --proof u27/proof_ledger.json --root examples/sample-project || test $? -eq 1
python3 -m pip wheel . --no-deps --no-build-isolation -w /tmp/boundary-engine-wheel
python3 scripts/verify_wheel.py /tmp/boundary-engine-wheel/unit27_boundary_engine-0.1.0-py3-none-any.whl
```

## License

MIT
