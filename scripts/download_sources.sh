#!/usr/bin/env bash
set -euo pipefail

repo_root=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)

clinvar_release=${CLINVAR_RELEASE:-2026-07-02}
mane_release=${MANE_RELEASE:-1.5}
sources_dir=${SOURCES_DIR:-"${repo_root}/sources"}
clinvar_dir=${CLINVAR_DIR:-"${sources_dir}/clinvar/${clinvar_release}"}
mane_dir=${MANE_DIR:-"${sources_dir}/mane/${mane_release}"}
curl_bin=${CURL_BIN:-curl}
force_download=${FORCE_DOWNLOAD:-0}
download_reference=${DOWNLOAD_REFERENCE:-0}

clinvar_base_url=${CLINVAR_BASE_URL:-https://ftp.ncbi.nlm.nih.gov/pub/clinvar/tab_delimited}
mane_base_url=${MANE_BASE_URL:-https://ftp.ncbi.nlm.nih.gov/refseq/MANE/MANE_human/release_${mane_release}}
reference_assembly=${REFERENCE_ASSEMBLY:-GCF_000001405.40_GRCh38.p14}
reference_dir=${REFERENCE_DIR:-"${sources_dir}/reference/grch38-p14"}
reference_base_url=${REFERENCE_BASE_URL:-https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/001/405/${reference_assembly}}
reference_gzip="${reference_dir}/${reference_assembly}_genomic.fna.gz"
reference_fasta="${reference_dir}/${reference_assembly}_genomic.fna"

mkdir -p "${clinvar_dir}" "${mane_dir}"

download() {
    local url=$1
    local destination=$2
    local temporary="${destination}.part"

    if [[ -f "${destination}" && "${force_download}" != "1" ]]; then
        printf 'Using existing file: %s\n' "${destination}"
        return
    fi

    printf 'Downloading: %s\n' "${url}"
    if ! "${curl_bin}" \
        --fail \
        --location \
        --retry 3 \
        --output "${temporary}" \
        "${url}"; then
        rm -f "${temporary}"
        return 1
    fi
    mv "${temporary}" "${destination}"
}

download \
    "${clinvar_base_url}/variant_summary.txt.gz" \
    "${clinvar_dir}/variant_summary.txt.gz"

download \
    "${clinvar_base_url}/hgvs4variation.txt.gz" \
    "${clinvar_dir}/hgvs4variation.txt.gz"

download \
    "${mane_base_url}/MANE.GRCh38.v${mane_release}.summary.txt.gz" \
    "${mane_dir}/MANE.GRCh38.v${mane_release}.summary.txt.gz"

printf '\nSource files ready:\n'
for source_file in \
    "${clinvar_dir}/variant_summary.txt.gz" \
    "${clinvar_dir}/hgvs4variation.txt.gz" \
    "${mane_dir}/MANE.GRCh38.v${mane_release}.summary.txt.gz"
do
    printf '  %s\n' "${source_file}"
done

if [[ "${download_reference}" == "1" ]]; then
    mkdir -p "${reference_dir}"
    download \
        "${reference_base_url}/${reference_assembly}_genomic.fna.gz" \
        "${reference_gzip}"
    if [[ -f "${reference_fasta}" && "${force_download}" != "1" ]]; then
        printf 'Using existing file: %s\n' "${reference_fasta}"
    else
        printf 'Decompressing: %s\n' "${reference_gzip}"
        if ! gzip -dc "${reference_gzip}" > "${reference_fasta}.part"; then
            rm -f "${reference_fasta}.part"
            exit 1
        fi
        mv "${reference_fasta}.part" "${reference_fasta}"
    fi
    printf '  %s\n' "${reference_fasta}"
fi

printf '\nVariant Recoder truth set:\n'
printf '  CLINVAR_RELEASE=%q MANE_RELEASE=%q %q\n' \
    "${clinvar_release}" \
    "${mane_release}" \
    "${repo_root}/scripts/build_truth_set.sh"

if [[ "${download_reference}" == "1" ]]; then
    printf '\nClinVar truth set:\n'
    printf '  CLINVAR_RELEASE=%q MANE_RELEASE=%q REFERENCE_FASTA=%q %q\n' \
        "${clinvar_release}" \
        "${mane_release}" \
        "${reference_fasta}" \
        "${repo_root}/scripts/build_clinvar_truth_set.sh"
fi
