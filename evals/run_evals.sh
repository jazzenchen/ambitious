#!/bin/bash
# Real headless runs of /ambitious vs. the "just say be more ambitious" baseline.
# Usage: ./run_evals.sh <output-dir> [skill-file] [eval-name ...]
#   e.g. ./run_evals.sh /tmp/ambitious-bench   (defaults to ../skills/ambitious/SKILL.md)
# Costs real API usage: ~$0.30 per with-skill run and ~$0.17 per baseline run on Opus.
# Each run gets a throwaway git copy of its fixture; Edit/Write are disallowed so we
# measure the ladder phase only (the skill must stop and ask before doing work).
set -u
W="$(cd "$(dirname "$0")" && pwd)"
ITER="$1"; SKILL="${2:-$W/../skills/ambitious/SKILL.md}"; shift; [ $# -gt 0 ] && shift
MODEL="${MODEL:-claude-opus-5-5}"
EVALS=("$@"); [ ${#EVALS[@]} -eq 0 ] && EVALS=(flaky-checkout acme-qbr tidepool-launch-post csv-export)

task_for() {
  python3 -c "import json,sys; e=[x for x in json.load(open('$W/evals.json'))['evals'] if x['name']==sys.argv[1]][0]; print(e['task'] + '\t' + e['fixture'] + '\t' + str(e['id']))" "$1"
}

ALLOWED='Read,Grep,Glob,LS,Bash(ls:*),Bash(cat:*),Bash(head:*),Bash(tail:*),Bash(wc:*),Bash(npm test:*),Bash(node:*),Bash(python3:*),Bash(sqlite3:*),Bash(duckdb:*),Bash(git status:*),Bash(git log:*),Bash(git diff:*),Bash(which:*),Bash(command -v:*),Bash(claude mcp list:*),Bash(for:*),Bash(seq:*)'

run_one() {
  local name="$1" config="$2"
  IFS=$'\t' read -r task fixture id <<<"$(task_for "$name")"
  local run="$ITER/eval-$name/$config/run-1"
  rm -rf "$run"; mkdir -p "$run/outputs"
  cp -R "$W/$fixture" "$run/project"
  ( cd "$run/project" && git init -q && git add -A && git -c user.name=fixture -c user.email=fixture@example.com commit -qm "fixture" )
  local prompt
  if [ "$config" = with_skill ]; then
    mkdir -p "$run/project/.claude/skills/ambitious"
    cp "$SKILL" "$run/project/.claude/skills/ambitious/SKILL.md"
    prompt="/ambitious $task"
  else
    prompt="$task. Be more ambitious than I'm asking — propose the most ambitious version first, before doing any work."
  fi
  python3 - "$run" "$id" "$name" "$prompt" <<'EOF'
import json,sys
run,i,name,prompt=sys.argv[1:]
m={"eval_id":int(i),"eval_name":name,"prompt":prompt,"assertions":[]}
json.dump(m,open(f"{run}/eval_metadata.json","w"),indent=2)
EOF
  local start=$(python3 -c 'import time;print(time.time())')
  ( cd "$run/project" && claude -p "$prompt" --model "$MODEL" --output-format stream-json --verbose \
      --no-session-persistence --allowedTools "$ALLOWED" --disallowedTools "Edit,Write,NotebookEdit" \
      --max-budget-usd 4 </dev/null >"$run/transcript.jsonl" 2>"$run/stderr.txt" )
  local end=$(python3 -c 'import time;print(time.time())')
  python3 "$W/parse_run.py" "$run" "$start" "$end"
  echo "done: $name/$config"
}

for name in "${EVALS[@]}"; do
  for config in ${CONFIGS:-with_skill without_skill}; do
    run_one "$name" "$config" &
  done
done
wait
echo "all runs finished"
