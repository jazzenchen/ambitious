#!/bin/bash
# Builds dist/ambitious.zip for claude.ai / Claude desktop upload (Customize → Skills).
# claude.ai rejects Claude Code-only frontmatter keys such as argument-hint, so strip them.
set -euo pipefail
cd "$(dirname "$0")/.."
rm -rf dist && mkdir -p dist/ambitious
awk 'BEGIN{fm=0} /^---$/{fm++; print; next} fm==1 && /^(argument-hint|disable-model-invocation|user-invocable|version):/{next} {print}' \
  skills/ambitious/SKILL.md > dist/ambitious/SKILL.md
(cd dist && zip -qr ambitious.zip ambitious && rm -rf ambitious)
echo "dist/ambitious.zip"
