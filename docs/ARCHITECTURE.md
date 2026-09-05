# Architecture

ChangeBench deliberately separates nondeterministic proposal generation from deterministic evaluation.

1. An external agent receives the scenario and produces a proposal contract.
2. The runner validates the declared mutation boundary before scoring any business objective.
3. Independent checks score correctness, safety, reliability, economics and efficiency.
4. The reporter produces a human-reviewable decision and SHA-256 integrity receipt.
5. Production adapters may later execute disposable sandboxes, but never receive implicit permission to mutate customer infrastructure.

## Extension boundaries

Provider integrations implement proposal collection; they do not change the scoring contract. Planned adapters include Terraform/OpenTofu plans, Bicep validation, Kubernetes dry runs, Ansible check mode, Batfish/Containerlab, OPA/Rego, OpenTelemetry and MCP. These are roadmap contracts, not present capabilities in v0.1.

## Evidence vocabulary

- **Implemented:** code and automated tests exist.
- **Deployed:** retained evidence came from an authorized environment.
- **Simulated:** deterministic fixtures exercise a declared scenario.
- **Contract:** an interface is specified but the external system was not called.

