# Ensembl Variant RecoderによるHGVS→VCF正解セット

このプロジェクトでは、Ensembl Variant Recoderの返却値をHGVS→GRCh38 VCF変換の
正解とする。ClinVarは入力候補を多数集めるためだけに使い、ClinVarの座標は正解値へ
コピーしない。

## 生成内容

`tools/build_truth_set.py` は次を行う。

1. 同一リリースのClinVar `variant_summary.txt.gz` と
   `hgvs4variation.txt.gz` を結合し、バージョン付きの `NM_`、`NR_`、`ENST`
   transcript HGVSを候補にする。
2. coding/non-coding/UTR/intronic と substitution/del/ins/dup/delins の
   組み合わせで候補を分類し、固定seedでラウンドロビンに並べる。
3. Ensembl REST APIの `POST /variant_recoder/homo_sapiens` を最大200件ずつ呼び、
   `vcf_string=1` の結果を取得する。
4. GRCh38の主染色体（1–22、X、Y、MT）のVCFだけをRefSeq accessionへ変換する。
5. Variant Recoderが有効なVCFを返したケースから再度均等に100件を選ぶ。

複数アレルまたは複数座標が返った場合はすべてを `expected.vcf` に含め、
`expected.ambiguous` を `true` にする。VCFを解釈できない候補はgoldに入れず、
`quarantine.jsonl` に理由と応答SHA-256を記録する。

## 入力データの固定

同じClinVarリリースの2ファイルを保存し、リリース名をコマンドへ渡す。

```bash
mkdir -p sources/clinvar/2026-07-02
curl -fL -o sources/clinvar/2026-07-02/variant_summary.txt.gz \
  https://ftp.ncbi.nlm.nih.gov/pub/clinvar/tab_delimited/variant_summary.txt.gz
curl -fL -o sources/clinvar/2026-07-02/hgvs4variation.txt.gz \
  https://ftp.ncbi.nlm.nih.gov/pub/clinvar/tab_delimited/hgvs4variation.txt.gz
```

生成レポートには両ファイルのSHA-256、ClinVarリリース、Ensemblリリース、
Variant RecoderのURLとオプションが入る。`rest.ensembl.org` は更新されるため、
完全な再現性が必要な場合は、対象リリースのEnsembl archive REST URLを
`--server` に指定する。

## 約100件の正解セットを生成

```bash
python3 tools/build_truth_set.py \
  --variant-summary sources/clinvar/2026-07-02/variant_summary.txt.gz \
  --hgvs4variation sources/clinvar/2026-07-02/hgvs4variation.txt.gz \
  --clinvar-release 2026-07-02 \
  --ensembl-release 116 \
  --target-count 100 \
  --cache build/variant-recoder-cache.jsonl \
  --output truth/gold.jsonl \
  --quarantine truth/quarantine.jsonl \
  --report truth/build-report.json
```

デフォルトでは、失敗を見込んで目標数の3倍まで候補を問い合わせる。100件に
届かない場合は終了コード1となるので、`--candidate-multiplier 5` のように増やす。
REST通信や不正な応答は終了コード2となる。

EnsemblのPOST上限は200件であり、`--batch-size` は1–200に制限される。
通常はデフォルトの100件のままでよい。

## キャッシュから再生成

正式生成時のキャッシュを保存すれば、APIを再度呼ばずに同じ応答から再構築できる。

```bash
python3 tools/build_truth_set.py \
  --variant-summary sources/clinvar/2026-07-02/variant_summary.txt.gz \
  --hgvs4variation sources/clinvar/2026-07-02/hgvs4variation.txt.gz \
  --clinvar-release 2026-07-02 \
  --ensembl-release 116 \
  --mode cache \
  --cache build/variant-recoder-cache.jsonl \
  --output truth/gold.jsonl \
  --quarantine truth/quarantine.jsonl \
  --report truth/build-report.json
```

キャッシュミスは正解として扱わない。候補数、Variant Recoder採用数、最終件数、
カテゴリ別件数は `build-report.json` で確認できる。

## 対象APIの評価

```bash
python3 tools/evaluate_hgvs2vcf.py \
  --truth-set truth/gold.jsonl \
  --base-url http://localhost:4567 \
  --json-report evaluation/result.json \
  --markdown-report evaluation/result.md
```

評価コードはデフォルトで `confidence: ensembl_variant_recoder` のケースだけを
goldとして受け付ける。VCF集合、transcript、`ambiguous` を比較し、順序には依存
しない。

これは座標変換実装の回帰試験用データであり、臨床判断には使用しない。
