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

clinvar_base_url=${CLINVAR_BASE_URL:-https://ftp.ncbi.nlm.nih.gov/pub/clinvar/tab_delimited}
mane_base_url=${MANE_BASE_URL:-https://ftp.ncbi.nlm.nih.gov/refseq/MANE/MANE_human/release_${mane_release}}

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

printf '\nDownloaded source files:\n'
for source_file in \
    "${clinvar_dir}/variant_summary.txt.gz" \
    "${clinvar_dir}/hgvs4variation.txt.gz" \
    "${mane_dir}/MANE.GRCh38.v${mane_release}.summary.txt.gz"
do
    printf '  %s\n' "${source_file}"
done

printf '\nNext step:\n'
printf '  CLINVAR_RELEASE=%q MANE_RELEASE=%q %q\n' \
    "${clinvar_release}" \
    "${mane_release}" \
    "${repo_root}/scripts/build_truth_set.sh"
