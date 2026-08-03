#!/usr/bin/env bash
set -euo pipefail

repo_root=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)

clinvar_release=${CLINVAR_RELEASE:-2026-07-02}
mane_release=${MANE_RELEASE:-1.5}
clinvar_dir=${CLINVAR_DIR:-"${repo_root}/sources/clinvar/${clinvar_release}"}
mane_summary=${MANE_SUMMARY:-"${repo_root}/sources/mane/${mane_release}/MANE.GRCh38.v${mane_release}.summary.txt.gz"}
variant_summary=${VARIANT_SUMMARY:-"${clinvar_dir}/variant_summary.txt.gz"}
hgvs4variation=${HGVS4VARIATION:-"${clinvar_dir}/hgvs4variation.txt.gz"}
reference_fasta=${REFERENCE_FASTA:-}

truth_dir=${CLINVAR_TRUTH_DIR:-"${repo_root}/truth/clinvar"}
python_bin=${PYTHON_BIN:-python3}
bcftools_bin=${BCFTOOLS_BIN:-bcftools}
target_count=${TARGET_COUNT:-100}
candidate_multiplier=${CANDIDATE_MULTIPLIER:-3}

for required_file in "${variant_summary}" "${hgvs4variation}" "${mane_summary}"; do
    if [[ ! -f "${required_file}" ]]; then
        printf 'Required input file not found: %s\n' "${required_file}" >&2
        printf 'Run scripts/download_sources.sh first.\n' >&2
        exit 2
    fi
done

if [[ -z "${reference_fasta}" ]]; then
    printf 'REFERENCE_FASTA is required for ClinVar VCF normalization.\n' >&2
    printf 'Specify an uncompressed GRCh38.p14 genomic FASTA with NC_ accession headers.\n' >&2
    exit 2
fi
if [[ ! -f "${reference_fasta}" ]]; then
    printf 'Reference FASTA not found: %s\n' "${reference_fasta}" >&2
    exit 2
fi

exec "${python_bin}" "${repo_root}/tools/build_clinvar_truth_set.py" \
    --variant-summary "${variant_summary}" \
    --hgvs4variation "${hgvs4variation}" \
    --mane-summary "${mane_summary}" \
    --reference-fasta "${reference_fasta}" \
    --clinvar-release "${clinvar_release}" \
    --mane-release "${mane_release}" \
    --target-count "${target_count}" \
    --candidate-multiplier "${candidate_multiplier}" \
    --bcftools "${bcftools_bin}" \
    --output "${truth_dir}/gold.jsonl" \
    --quarantine "${truth_dir}/quarantine.jsonl" \
    --report "${truth_dir}/build-report.json" \
    "$@"
