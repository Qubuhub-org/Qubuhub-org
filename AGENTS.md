# Repository Engineering Rules

- Inspect the repository's actual files and existing instructions before changing code.
- Keep claims in documentation tied to verified implementations; label plans and external projects clearly.
- Never commit credentials, tokens, private keys, or sensitive logs.
- Treat scripts that change host services, install packages, or alter databases as opt-in operations. Explain prerequisites and side effects.
- Prefer minimal changes and existing dependencies. Do not execute destructive commands as part of tests.
- Validate shell scripts with `bash -n`; use ShellCheck when available; run relevant tests and report exactly what was executed.
- A successful dependency installation is not proof of a successful build or test run.
- Do not claim CI, runtime, deployment, or integration success without actual evidence.
- Keep pull requests focused, leave them unmerged unless explicitly instructed, and report remaining limitations.
