#!/bin/bash
# Re-checks the go-run receipt from repo contents alone, no model involved:
#   1. original fixture suite, N runs → how often it fails
#   2. fixture + results/go-run/diff.patch, N runs → should be 0 failures
#   3. patched tests against the ORIGINAL src/checkout.js → should fail
# Usage: ./verify_go_run.sh [runs]   (default 200; needs node ≥ 22)
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"; N="${1:-200}"
T="$(mktemp -d)"; trap 'rm -rf "$T"' EXIT
cp -R "$HERE/fixtures/flaky-checkout" "$T/original"; cp -R "$HERE/fixtures/flaky-checkout" "$T/fixed"
(cd "$T/fixed" && git init -q && git apply "$HERE/results/go-run/diff.patch")
count() { local f=0; for _ in $(seq 1 "$N"); do (cd "$1" && npm test --silent >/dev/null 2>&1) || f=$((f+1)); done; echo "$f"; }
echo "node $(node --version) · $(date -u +%FT%TZ) · $N runs each"
echo "original suite:  $(count "$T/original")/$N runs failed"
echo "fixed suite:     $(count "$T/fixed")/$N runs failed"
cp "$T/original/src/checkout.js" "$T/fixed/src/checkout.js"
echo "fixed tests vs original checkout.js: $(cd "$T/fixed" && npm test 2>&1 | grep -E '^ℹ (tests|pass|fail)' | tr '\n' ' ')"
