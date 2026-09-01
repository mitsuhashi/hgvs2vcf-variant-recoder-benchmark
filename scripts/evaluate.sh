#!/usr/bin/env bash
set -euo pipefail

repo_root=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)

python_bin=${PYTHON_BIN:-python3}
truth_set=${TRUTH_SET:-"${repo_root}/truth/gold500.jsonl"}
api_type=${API_TYPE:-marshal}
if [[ -n "${BASE_URL:-}" ]]; then
    base_url=${BASE_URL}
else
    base_url=https://hgvs2vcf.togovar.org
fi
evaluation_dir=${EVALUATION_DIR:-"${repo_root}/evaluation"}
json_report=${JSON_REPORT:-"${evaluation_dir}/${api_type}-result.json"}
markdown_report=${MARKDOWN_REPORT:-"${evaluation_dir}/${api_type}-result.md"}
batch_size=${EVALUATION_BATCH_SIZE:-100}
timeout=${EVALUATION_TIMEOUT:-60}

if [[ ! -f "${truth_set}" ]]; then
    printf 'Truth set not found: %s\n' "${truth_set}" >&2
    printf 'Build it with scripts/build_truth_set.sh or set TRUTH_SET.\n' >&2
    exit 2
fi

exec "${python_bin}" "${repo_root}/tools/evaluate_hgvs2vcf.py" \
    --truth-set "${truth_set}" \
    --api-type "${api_type}" \
    --base-url "${base_url}" \
    --json-report "${json_report}" \
    --markdown-report "${markdown_report}" \
    --batch-size "${batch_size}" \
    --timeout "${timeout}" \
    "$@"
