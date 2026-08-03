# HGVS→VCF正解セットの生成仕様

このプロジェクトは、Ensembl Variant Recoderの返却VCFだけから正解セットを生成する。
ClinVarはHGVS入力候補の収集に使うが、そのVCF列は正解値に使わない。gene symbol表記
では、固定したMANE Selectを代表transcriptとする。

## 入力候補

`tools/build_truth_set.py` は次を行う。

1. 同一リリースのClinVar `variant_summary.txt.gz` と
   `hgvs4variation.txt.gz` を結合し、version付きRefSeq HGVSとgene symbolを得る。
2. 固定したMANE summaryの `MANE Select` 行をgene symbolへ対応付ける。
3. 次の3形式を生成する。
   - `GENE:p.` — MANE Selectの `RefSeq_prot` と一致するprotein HGVSから生成
   - `GENE:c.` — MANE Selectの `RefSeq_nuc` と一致するtranscript HGVSから生成
   - versionなし `NM_:c.` — version付き `NM_:c.` から生成
4. 入力形式と変異カテゴリごとに、固定seedの安定ハッシュで必要数だけ候補を保持する。
5. 入力形式をほぼ同数にし、各形式内でも変異操作が偏らないよう固定seedで並べる。

`variant_summary` からはGRCh38主染色体候補を選ぶための `Assembly` と
`ChromosomeAccession` を使うが、`PositionVCF`、`ReferenceAlleleVCF`、
`AlternateAlleleVCF` は読み取らない。候補段階でClinVarの座標やアレルを正解値へ
持ち込まない。

## Variant Recoderによる正解VCFの決定

1. Ensembl REST APIの `POST /variant_recoder/homo_sapiens` を最大200件ずつ呼び、
   `vcf_string=1` の結果を取得する。
2. GRCh38の主染色体（1–22、X、Y、MT）のVCFだけをRefSeq accessionへ変換する。
3. Variant Recoderが有効なVCFを返したケースから再度均等に100件を選ぶ。

`expected.vcf` の `chrom`、`pos`、`ref`、`alt` はすべてこのVariant Recoder応答から
作成する。

gene symbol入力は複数transcriptへ解決され得るため、次の二段階で正解を限定する。

1. gene symbol表記をVariant Recoderへ入力し、解釈できることを確認する。
2. 対応するMANE Selectのversion付きRefSeq HGVSもVariant Recoderへ入力する。
3. MANE由来VCFがgene symbol表記の返却VCFに含まれる場合、MANE由来VCFだけを正解にする。

versionなし `NM_:c.` の期待transcriptは、Variant Recoder応答のversion付き `hgvsc`
から決定する。MANE表記が複数アレルを返した場合はすべてを `expected.vcf` に含め、
`expected.ambiguous` を `true` にする。不一致や解釈不能はgoldに入れず、
`quarantine.jsonl` に理由と応答SHA-256を記録する。

## 入力データの固定

同じClinVarリリースの2ファイルと、固定したMANE summaryを保存する。
通常はダウンロードスクリプトで3ファイルをまとめて取得する。

```bash
scripts/download_sources.sh
```

生成レポートには3ファイルのSHA-256、ClinVar・MANE・Ensemblリリース、
Variant RecoderのURLとオプションが入る。`rest.ensembl.org` は更新されるため、
完全な再現性が必要な場合は、対象リリースのEnsembl archive REST URLを
`--server` に指定する。

## 正解セットを約100件生成

```bash
python3 tools/build_truth_set.py \
  --variant-summary sources/clinvar/2026-07-02/variant_summary.txt.gz \
  --hgvs4variation sources/clinvar/2026-07-02/hgvs4variation.txt.gz \
  --mane-summary sources/mane/1.5/MANE.GRCh38.v1.5.summary.txt.gz \
  --clinvar-release 2026-07-02 \
  --ensembl-release 116 \
  --mane-release 1.5 \
  --target-count 100 \
  --cache build/variant-recoder-cache.jsonl \
  --output truth/gold.jsonl \
  --quarantine truth/quarantine.jsonl \
  --report truth/build-report.json
```

デフォルトでは、失敗を見込んで目標数の5倍まで候補を問い合わせる。100件に
届かない場合は終了コード1となるので、`--candidate-multiplier 7` のように増やす。
REST通信や不正な応答は終了コード2となる。

EnsemblのPOST上限は200件であり、`--batch-size` は1–200に制限される。
`--workers` は1–8で、独立したバッチの並列取得数を指定する。
デフォルトは20件とし、タイムアウトしたバッチは成功する大きさまで自動分割する。
単一入力がタイムアウトする場合は一時的なquarantine対象とし、応答キャッシュへ
保存せずに残りを続行する。
応答量を抑えるため、通常は `spdi`、versionなしRefSeq入力だけはversion解決用の
`hgvsc` を要求する。

## キャッシュから再生成

正式生成時のキャッシュを保存すれば、APIを再度呼ばずに同じ応答から再構築できる。

```bash
python3 tools/build_truth_set.py \
  --variant-summary sources/clinvar/2026-07-02/variant_summary.txt.gz \
  --hgvs4variation sources/clinvar/2026-07-02/hgvs4variation.txt.gz \
  --mane-summary sources/mane/1.5/MANE.GRCh38.v1.5.summary.txt.gz \
  --clinvar-release 2026-07-02 \
  --ensembl-release 116 \
  --mane-release 1.5 \
  --mode cache \
  --cache build/variant-recoder-cache.jsonl \
  --candidate-cache build/candidate-selection-cache.json \
  --output truth/gold.jsonl \
  --quarantine truth/quarantine.jsonl \
  --report truth/build-report.json
```

キャッシュミスは正解として扱わない。候補数、Variant Recoder採用数、最終件数、
カテゴリ別件数は `build-report.json` で確認できる。
候補選定キャッシュが入力ファイル情報・seed・候補数と一致する場合は、ClinVar全件の
再走査も省略する。

## 対象APIの評価

```bash
python3 tools/evaluate_hgvs2vcf.py \
  --truth-set truth/gold.jsonl \
  --base-url http://localhost:4567 \
  --json-report evaluation/result.json \
  --markdown-report evaluation/result.md
```

評価コードは `confidence: ensembl_variant_recoder` だけをgoldとして受け付ける。
VCF集合、transcript、`ambiguous` を比較し、順序には依存しない。

これは座標変換実装の回帰試験用データであり、臨床判断には使用しない。
