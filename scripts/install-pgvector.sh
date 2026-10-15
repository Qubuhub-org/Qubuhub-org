#!/usr/bin/env bash
set -Eeuo pipefail

# Build and install pgvector for the PostgreSQL installation selected by pg_config.
# This script intentionally does not install OS packages or modify Docker services.
PGVECTOR_VERSION="${PGVECTOR_VERSION:-v0.8.7}"
PG_CONFIG="${PG_CONFIG:-pg_config}"
SUDO="${SUDO:-sudo}"

die() { printf 'error: %s\n' "$*" >&2; exit 1; }
for cmd in git make "$PG_CONFIG"; do
  command -v "$cmd" >/dev/null 2>&1 || die "required command not found: $cmd"
done

pg_version="$("$PG_CONFIG" --version)"
pg_bindir="$("$PG_CONFIG" --bindir)"
printf 'Target PostgreSQL: %s\n' "$pg_version"
printf 'pg_config: %s\n' "$(command -v "$PG_CONFIG")"
printf 'pgvector version: %s\n' "$PGVECTOR_VERSION"

tmpdir="$(mktemp -d)"
cleanup() { rm -rf "$tmpdir"; }
trap cleanup EXIT

git clone --depth 1 --branch "$PGVECTOR_VERSION" \
  https://github.com/pgvector/pgvector.git "$tmpdir/pgvector"
make -C "$tmpdir/pgvector"
if [[ "$(id -u)" -eq 0 ]]; then
  make -C "$tmpdir/pgvector" install
else
  command -v "$SUDO" >/dev/null 2>&1 || die "need root or a sudo command to install pgvector"
  "$SUDO" make -C "$tmpdir/pgvector" install
fi

printf '\nInstalled pgvector for %s. Verify in the target database with:\n' "$pg_version"
printf '  CREATE EXTENSION vector;\n'
printf 'PostgreSQL binaries: %s\n' "$pg_bindir"
