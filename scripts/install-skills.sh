#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 || $# -gt 2 ]]; then
  echo "usage: $0 /absolute/path/to/project [--claude-links]" >&2
  exit 2
fi

target_root="$1"
mode="${2:-}"
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(cd "${script_dir}/.." && pwd)"
source_root="${repo_root}/.agents/skills"
target_skills="${target_root}/.agents/skills"

if [[ ! -d "${target_root}" ]]; then
  echo "target project does not exist: ${target_root}" >&2
  exit 2
fi

skills=(
  junho-plate
  junho-plate-feature
  junho-plate-refactor
  junho-plate-review
  junho-probe-skill
  junho-probe-coach
  junho-probe-build
  junho-probe-audit
  junho-probe-quiz
  junho-probe-demo
  junho-query-wiki
)

mkdir -p "${target_skills}"
for skill in "${skills[@]}"; do
  if [[ ! -d "${source_root}/${skill}" ]]; then
    echo "missing bundled skill: ${skill}" >&2
    exit 1
  fi
  if [[ -e "${target_skills}/${skill}" ]]; then
    echo "target skill already exists; move or remove it explicitly before install: ${target_skills}/${skill}" >&2
    exit 1
  fi
done

for skill in "${skills[@]}"; do
  cp -R "${source_root}/${skill}" "${target_skills}/${skill}"
done

if [[ "${mode}" == "--claude-links" ]]; then
  mkdir -p "${target_root}/.claude/skills"
  for skill in "${skills[@]}"; do
    ln -sfn "../../.agents/skills/${skill}" "${target_root}/.claude/skills/${skill}"
  done
elif [[ -n "${mode}" ]]; then
  echo "unknown option: ${mode}" >&2
  exit 2
fi

echo "installed ${#skills[@]} skills into ${target_skills}"
