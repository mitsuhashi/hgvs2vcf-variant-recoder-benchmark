#!/usr/bin/env bash
set -euo pipefail

repo_root=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)

clinvar_release=${CLINVAR_RELEASE:-2026-07-02}
ensembl_release=${ENSEMBL_RELEASE:-116}
mane_release=${MANE_RELEASE:-1.5}

clinvar_dir=${CLINVAR_DIR:-"${repo_root}/sources/clinvar/${clinvar_release}"}
mane_summary=${MANE_SUMMARY:-"${repo_root}/sources/mane/${mane_release}/MANE.GRCh38.v${mane_release}.summary.txt.gz"}
variant_summary=${VARIANT_SUMMARY:-"${clinvar_dir}/variant_summary.txt.gz"}
hgvs4variation=${HGVS4VARIATION:-"${clinvar_dir}/hgvs4variation.txt.gz"}

truth_dir=${TRUTH_DIR:-"${repo_root}/truth"}
build_dir=${BUILD_DIR:-"${repo_root}/build"}
python_bin=${PYTHON_BIN:-python3}
target_count=${TARGET_COUNT:-100}
candidate_multiplier=${CANDIDATE_MULTIPLIER:-3}
ensembl_server=${ENSEMBL_SERVER:-https://rest.ensembl.org}

for required_file in "${variant_summary}" "${hgvs4variation}" "${mane_summary}"; do
    if [[ ! -f "${required_file}" ]]; then
        printf 'Required input file not found: %s\n' "${required_file}" >&2
        printf 'Download the ClinVar and MANE files described in README.md first.\n' >&2
        exit 2
    fi
done

exec "${python_bin}" "${repo_root}/tools/build_truth_set.py" \
    --variant-summary "${variant_summary}" \
    --hgvs4variation "${hgvs4variation}" \
    --mane-summary "${mane_summary}" \
    --clinvar-release "${clinvar_release}" \
    --ensembl-release "${ensembl_release}" \
    --mane-release "${mane_release}" \
    --server "${ensembl_server}" \
    --target-count "${target_count}" \
    --candidate-multiplier "${candidate_multiplier}" \
    --cache "${build_dir}/variant-recoder-cache.jsonl" \
    --output "${truth_dir}/gold.jsonl" \
    --quarantine "${truth_dir}/quarantine.jsonl" \
    --report "${truth_dir}/build-report.json" \
    "$@"
