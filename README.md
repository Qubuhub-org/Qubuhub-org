# Qubuhub

Qubuhub is an organization-level workspace for documenting projects and development resources across web technologies, decentralized systems, and related research.

> **Status note:** This repository is an organization overview and workspace. A feature or technology mentioned here should not be assumed to be implemented, deployed, audited, or maintained unless its own repository and evidence confirm that status.

## Repository map

- `AGENTS.md` — repository-wide engineering and validation expectations.
- `CODEX.md` — extended agent workflow and operational guidance.
- `scripts/install-pgvector.sh` — opt-in source build/install helper for pgvector; requires Git, Make, a PostgreSQL `pg_config`, and installation privileges.
- `dev/docker-service-management.md` — documentation for inspecting Docker contexts and service-management risks.
- `src/`, `paper/`, `workspace/`, `auraecosystem/`, and `www/` — additional project notes, artifacts, workspace material, and web content. Their presence alone does not establish a complete application build.

## Engineering principles

1. Inspect the actual project and its local instructions before making changes.
2. Prefer small, reviewable changes with explicit prerequisites and side effects.
3. Keep secrets out of source control, logs, and documentation.
4. Validate changes with reproducible checks and report only results that were actually observed.
5. Keep scripts that modify a host or install software opt-in; never run them automatically as part of CI.

## Validation

The repository workflow checks the Bash installer syntax and runs ShellCheck. These checks are intentionally limited: they do not install pgvector, modify host services, or prove that a target PostgreSQL server can load the extension.

Run the local checks with:

```sh
bash -n scripts/install-pgvector.sh
shellcheck --severity=warning scripts/install-pgvector.sh
git diff --check
```

The installer requires a supported build environment and a `pg_config` matching the PostgreSQL instance where pgvector will be used. See the script comments and upstream [pgvector documentation](https://github.com/pgvector/pgvector).

## Contributing

Submit focused pull requests with a clear explanation of the problem, the change, and the validation performed. Do not claim builds, tests, deployments, security reviews, or runtime behavior that have not been verified.
