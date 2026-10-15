#!/bin/bash
# Usage: flaky_check.sh <result-project-dir> [runs]  → JSON with suite flake rate + hidden tests H1-H3
P="$1"; N="${2:-200}"; T="$(mktemp -d)"; trap 'rm -rf "$T"' EXIT
cp -R "$P/." "$T/"; rm -rf "$T/.git" "$T/.claude"
fail=0; for _ in $(seq 1 "$N"); do (cd "$T" && node --test "test/**/*.test.js" >/dev/null 2>&1) || fail=$((fail+1)); done
cp "$(dirname "$0")/flaky_hidden.test.js" "$T/zz_hidden.test.js"
h=""; for t in H1 H2 H3; do
  if (cd "$T" && node --test --test-name-pattern="^$t " zz_hidden.test.js >/dev/null 2>&1); then h="$h\"$t\":true,"; else h="$h\"$t\":false,"; fi
done
echo "{\"suite_fail\":$fail,\"suite_runs\":$N,${h%,}}"
