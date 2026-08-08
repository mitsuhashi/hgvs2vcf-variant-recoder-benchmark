#!/usr/bin/env bash
set -euo pipefail

repo_root=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)

python_bin=${PYTHON_BIN:-python3}
truth_set=${TRUTH_SET:-"${repo_root}/truth/gold.jsonl"}
base_url=${BASE_URL:-https://hgvs2vcf.togovar.org}
evaluation_dir=${EVALUATION_DIR:-"${repo_root}/evaluation"}
json_report=${JSON_REPORT:-"${evaluation_dir}/variant-recoder-result.json"}
markdown_report=${MARKDOWN_REPORT:-"${evaluation_dir}/variant-recoder-result.md"}
batch_size=${EVALUATION_BATCH_SIZE:-100}
timeout=${EVALUATION_TIMEOUT:-60}

if [[ ! -f "${truth_set}" ]]; then
    printf 'Truth set not found: %s\n' "${truth_set}" >&2
    printf 'Build it with scripts/build_truth_set.sh or set TRUTH_SET.\n' >&2
    exit 2
fi

exec "${python_bin}" "${repo_root}/tools/evaluate_hgvs2vcf.py" \
    --truth-set "${truth_set}" \
    --base-url "${base_url}" \
    --json-report "${json_report}" \
    --markdown-report "${markdown_report}" \
    --batch-size "${batch_size}" \
    --timeout "${timeout}" \
    "$@"
