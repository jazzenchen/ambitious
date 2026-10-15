"""Turn a claude -p stream-json transcript into outputs/response.md, transcript.md, timing.json, metrics.json."""
import json
import sys
from collections import Counter
from pathlib import Path

run = Path(sys.argv[1])
start, end = float(sys.argv[2]), float(sys.argv[3])

events = []
for line in (run / "transcript.jsonl").read_text().splitlines():
    line = line.strip()
    if line.startswith("{"):
        try:
            events.append(json.loads(line))
        except json.JSONDecodeError:
            pass

tools = Counter()
skill_invoked = False
md = []
final_text, usage, cost, model = "", {}, None, None
for e in events:
    t = e.get("type")
    if t == "system" and e.get("subtype") == "init":
        model = e.get("model")
    if t == "assistant":
        for block in e.get("message", {}).get("content", []):
            if block.get("type") == "text":
                md.append(block["text"])
            elif block.get("type") == "tool_use":
                tools[block["name"]] += 1
                if block["name"] == "Skill":
                    skill_invoked = True
                md.append(f"`[tool] {block['name']}: {json.dumps(block.get('input'))[:300]}`")
    if t == "user":
        content = e.get("message", {}).get("content", [])
        if isinstance(content, list):
            for block in content:
                if block.get("type") == "text" and "ambitious" in block.get("text", "").lower() and "Base directory" in block.get("text", ""):
                    skill_invoked = True
    if t == "result":
        final_text = e.get("result", "") or ""
        usage = e.get("usage", {}) or {}
        cost = e.get("total_cost_usd")

# Slash-command skills expand into the prompt rather than calling the Skill tool; detect the expansion too.
raw = (run / "transcript.jsonl").read_text()
if (run / "project/.claude/skills/ambitious/SKILL.md").exists() and ("\u25b2 /ambitious" in raw or "▲ /ambitious" in raw):
    skill_invoked = True

out = run / "outputs"
out.mkdir(exist_ok=True)
(out / "response.md").write_text(final_text or "(no final result — see transcript.md)")
(run / "transcript.md").write_text("\n\n".join(md))

tokens = sum(v for k, v in usage.items() if isinstance(v, int) and "tokens" in k)
json.dump({
    "total_tokens": tokens,
    "duration_ms": int((end - start) * 1000),
    "total_duration_seconds": round(end - start, 1),
    "executor_duration_seconds": round(end - start, 1),
    "cost_usd": cost,
    "model": model,
}, open(run / "timing.json", "w"), indent=2)
json.dump({
    "tool_calls": dict(tools),
    "total_tool_calls": sum(tools.values()),
    "skill_invoked": skill_invoked,
    "output_chars": len(final_text),
    "transcript_chars": len(raw),
    "errors_encountered": (run / "stderr.txt").read_text().count("rror") if (run / "stderr.txt").exists() else 0,
}, open(out / "metrics.json", "w"), indent=2)
