# Design Notes

Boundary Engine is intentionally small. The point is not to create a truth oracle, compliance tool, or copywriting assistant. The point is to compare public repo language against recorded proof and make unsupported claims visible.

The core design claim is:

> A repo's public claims should stay inside its recorded proof boundary.

## Why This Is Not A Legal Review

Boundary Engine does not determine whether a claim is legally safe or universally true. It checks whether a claim has matching evidence in a local Proof Ledger artifact.

That boundary matters:

1. Proof artifacts are inspectable.
2. Public README language drifts easily.
3. Claim checks should be deterministic and rerunnable.
4. Unsupported claims should produce a register, not a vague warning.

## System Layers

- **Proof layer:** Loads passing Proof Ledger claims and case ids.
- **Claim layer:** Finds high-risk public language in markdown.
- **Boundary layer:** Compares detected claims against recorded proof.
- **Register layer:** Renders unsupported claims, reasons, and safer wording.

## Unit27 README Gate

Every public Unit27 repo should include a near-top `## Why Use It` section before setup details.

That section is allowed to be more plainspoken than the surrounding system language because it serves the pickup-and-use test: a technical reviewer should understand not only what the tool is, but why they would run it now.

The section should stay narrow:

1. Name the concrete moment when the tool is useful.
2. Name the failure it prevents.
3. Show a short example of input or outcome.
4. Avoid sales language, broad readiness claims, or unsupported proof language.

## Failure Modes

Boundary Engine should fail or downgrade when:

- The proof ledger is missing.
- The proof ledger schema is unsupported.
- The markdown file is missing.
- A claim pattern is detected without matching proof.
- The register implies broader certainty than the proof ledger supports.
- A Unit27 README is understandable but does not explain why a reviewer would pick up and use the tool.

## What I Would Improve Next

The strongest next improvements would be:

1. Add configurable claim patterns.
2. Add line-level ignore annotations with reasons.
3. Add phrase matching against specific proof case ids.
4. Add scan support for multiple markdown files.
5. Add a paired Proof Ledger + Boundary Engine workflow example.

Those deepen the tool without turning it into a platform.

## What This Demonstrates

This project is designed to show:

- Claim discipline over README hype
- Proof alignment over trust language
- Local deterministic checks over model judgment
- Reviewer artifacts over hidden lint output
- Public-safe boundaries over broad certification claims
