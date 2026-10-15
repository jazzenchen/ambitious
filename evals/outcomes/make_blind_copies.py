"""Copy each outcome run's finished repo to blind/<task>/run-A|run-B (skill files removed), counterbalanced.

The mapping goes to blind/mapping.json, which graders never see.
"""
import json
import shutil
import sys
from pathlib import Path

out = Path(sys.argv[1])
blind = out.parent / "blind"
ALL = ["flaky-checkout", "acme-qbr", "tidepool-launch-post", "csv-export"]
only = sys.argv[2:] or ALL
map_file = blind / "mapping.json"
mapping = json.load(open(map_file)) if map_file.exists() else {}
for i, task in enumerate(ALL):
    if task not in only:
        continue
    shutil.rmtree(blind / task, ignore_errors=True)
    skill_label = "A" if i % 2 == 0 else "B"  # counterbalance which label the skill gets
    for config in ("with_skill", "without_skill"):
        label = skill_label if config == "with_skill" else ("B" if skill_label == "A" else "A")
        src = out / task / config / "project"
        dst = blind / task / f"run-{label}"
        shutil.copytree(src, dst, ignore=shutil.ignore_patterns(".git", ".claude", "node_modules"))
        diff = out / task / config / "outputs" / "diff.patch"
        shutil.copy(diff, dst.parent / f"run-{label}.diff.patch")
        if diff.stat().st_size == 0:  # nothing written to the repo: the chat reply is the deliverable
            shutil.copy(out / task / config / "outputs" / "response.md", dst.parent / f"run-{label}.response.md")
        mapping.setdefault(task, {})[config] = label
json.dump(mapping, open(map_file, "w"), indent=2)
print(json.dumps(mapping))
