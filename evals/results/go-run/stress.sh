#!/bin/sh
# usage: stress.sh N  — runs the suite N times, prints failure count
N=${1:-200}; fail=0
for i in $(seq 1 $N); do node --test "test/**/*.test.js" >/dev/null 2>&1 || fail=$((fail+1)); done
echo "fails: $fail/$N"
