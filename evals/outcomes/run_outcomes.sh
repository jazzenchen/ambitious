#!/bin/bash
# Outcome benchmark: does using /ambitious produce a better RESULT than not using it?
#   without_skill: claude -p "<task>"                (what you'd normally type)
#   with_skill:    claude -p "/ambitious --go <task>" (card, then its recommended rung, no human in the loop)
# Same model, same fresh git copy of each fixture, edits allowed in that throwaway copy only.
# No MCP servers and no claude.ai artifact tools, so every deliverable lands in the repo for both arms.
# Usage: evals/outcomes/run_outcomes.sh <out-dir> skills/ambitious/SKILL.md [eval-name ...]
# Costs real API usage (~$1.65/task for both arms on Opus).
set -u
W="$(cd "$(dirname "$0")" && pwd)"
E="$(cd "$W/.." && pwd)"   # evals/: evals.json, parse_run.py, fixtures/
OUT="$1"; SKILL="$2"; shift 2
MODEL="${MODEL:-claude-opus-5-5}"
EVALS=("$@"); [ ${#EVALS[@]} -eq 0 ] && EVALS=(flaky-checkout acme-qbr tidepool-launch-post csv-export)

task_for() {
  python3 -c "import json,sys; e=[x for x in json.load(open('$E/evals.json'))['evals'] if x['name']==sys.argv[1]][0]; print(e['task'] + '\t' + e['fixture'])" "$1"
}

run_one() {
  local name="$1" config="$2"
  IFS=$'\t' read -r task fixture <<<"$(task_for "$name")"
  local run="$OUT/$name/$config"
  rm -rf "$run"; mkdir -p "$run/outputs"
  cp -R "$E/$fixture" "$run/project"
  ( cd "$run/project" && git init -q && git add -A && git -c user.name=fixture -c user.email=fixture@example.com commit -qm fixture && echo ".claude/" > .git/info/exclude )
  local prompt="$task"
  if [ "$config" = with_skill ]; then
    mkdir -p "$run/project/.claude/skills/ambitious" && cp "$SKILL" "$run/project/.claude/skills/ambitious/SKILL.md"
    prompt="/ambitious --go $task"
  fi
  echo "$prompt" > "$run/prompt.txt"
  local start=$(python3 -c 'import time;print(time.time())')
  ( cd "$run/project" && claude -p "$prompt" --model "$MODEL" --output-format stream-json --verbose \
      --no-session-persistence --permission-mode acceptEdits --allowedTools "Read,Grep,Glob,Edit,Write,Bash" \
      --strict-mcp-config --disallowedTools "Artifact,ArtifactData,ArtifactComments" \
      --max-budget-usd 8 </dev/null >"$run/transcript.jsonl" 2>"$run/stderr.txt" )
  local end=$(python3 -c 'import time;print(time.time())')
  ( cd "$run/project" && git add -A && git diff --cached > "$run/outputs/diff.patch" && git diff --cached --stat > "$run/outputs/diffstat.txt" )
  python3 "$E/parse_run.py" "$run" "$start" "$end"
  echo "done: $name/$config"
}

for name in "${EVALS[@]}"; do
  for config in ${CONFIGS:-with_skill without_skill}; do
    run_one "$name" "$config" &
  done
done
wait
echo "all outcome runs finished"
