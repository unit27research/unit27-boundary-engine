# Proof Packet

Project: unit27-boundary-engine
Generated: 2026-05-01T02:48:07+00:00

## Verified Claims

- Boundary Engine can scan markdown against Proof Ledger claims, flag unsupported public language, and write boundary artifacts.
  - Case: `core-cli-acceptance`
  - Command: `/usr/bin/env PYTHONPATH=src python3 -m unittest discover -s tests`
  - Evidence: `u27/evidence/run-0009.txt`

- Boundary Engine can create a demo project and boundary register from a single command.
  - Case: `first-use-demo`
  - Command: `/usr/bin/env PYTHONPATH=src python3 -m boundary_engine.cli demo --root /tmp/boundary-engine-proof-demo-live`
  - Evidence: `u27/evidence/run-0002.txt`

- Boundary Engine packages as an installable Python project.
  - Case: `wheel-build`
  - Command: `/Users/joshuabloodworth/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -m pip wheel . --no-deps --no-build-isolation -w /tmp/boundary-engine-karpathy-hook-wheel`
  - Evidence: `u27/evidence/run-0010.txt`

- Boundary Engine's built wheel contains the CLI modules and boundary-engine console entry point.
  - Case: `wheel-contents`
  - Command: `/Users/joshuabloodworth/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/verify_wheel.py /tmp/boundary-engine-karpathy-hook-wheel/unit27_boundary_engine-0.1.0-py3-none-any.whl`
  - Evidence: `u27/evidence/run-0011.txt`

- Boundary Engine's own README stays inside its recorded proof boundary.
  - Case: `self-boundary-check`
  - Command: `/usr/bin/env PYTHONPATH=src python3 -m boundary_engine.cli scan README.md --proof u27/proof_ledger.json --root .`
  - Evidence: `u27/evidence/run-0012.txt`

- Boundary Engine is published as a public Unit27 GitHub repository with aligned metadata.
  - Case: `github-publication`
  - Command: `gh repo view unit27research/unit27-boundary-engine --json nameWithOwner,description,visibility,url,repositoryTopics`
  - Evidence: `u27/evidence/run-0006.txt`

- Boundary Engine's live GitHub Actions workflow passes on the published main branch.
  - Case: `live-ci`
  - Command: `gh run view 25199856545 --json conclusion,status,headSha,workflowName,url`
  - Evidence: `u27/evidence/run-0013.txt`

## Open Failures

- No failing, blocked, or regression runs are recorded.

## Known Limits
- This evidence covers deterministic local markdown scanning, not legal review or universal truth verification.
- The current scanner uses a fixed high-risk phrase set rather than a configurable policy file.
- The demo intentionally includes unsupported claims so the register is visible on first use.
- Demo evidence proves the first-use flow only; it does not prove every repository shape.
- Wheel evidence proves local packaging only; it does not prove PyPI publication or GitHub release state.
- Wheel contents evidence proves local artifact structure only; it does not prove installation in every target environment.
- This check covers the current README only; future public docs should be scanned separately.
- This claim covers the GitHub repository state at the time of recording only.
- This does not prove package registry publication.
- This claim covers the latest recorded workflow run only.
- It does not prove future commits or external service availability.

## Case Inventory
- `core-cli-acceptance`: pass - Boundary Engine can scan markdown against Proof Ledger claims, flag unsupported public language, and write boundary artifacts.
- `first-use-demo`: pass - Boundary Engine can create a demo project and boundary register from a single command.
- `github-publication`: pass - Boundary Engine is published as a public Unit27 GitHub repository with aligned metadata.
- `live-ci`: pass - Boundary Engine's live GitHub Actions workflow passes on the published main branch.
- `self-boundary-check`: pass - Boundary Engine's own README stays inside its recorded proof boundary.
- `wheel-build`: pass - Boundary Engine packages as an installable Python project.
- `wheel-contents`: pass - Boundary Engine's built wheel contains the CLI modules and boundary-engine console entry point.
