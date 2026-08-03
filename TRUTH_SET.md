# HGVS→VCF正解セットの生成仕様

このプロジェクトは、Ensembl Variant Recoder由来とClinVar由来の正解セットを
別々に生成する。両者を混ぜず、provenanceと出力先で区別する。gene symbol表記では、
固定したMANE Selectを代表transcriptとする。

## 共通の入力候補

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
以降の正解VCF決定だけが出典によって異なる。

## Variant Recoder版

1. Ensembl REST APIの `POST /variant_recoder/homo_sapiens` を最大200件ずつ呼び、
   `vcf_string=1` の結果を取得する。
2. GRCh38の主染色体（1–22、X、Y、MT）のVCFだけをRefSeq accessionへ変換する。
3. Variant Recoderが有効なVCFを返したケースから再度均等に100件を選ぶ。

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

## Variant Recoder版を約100件生成

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

デフォルトでは、失敗を見込んで目標数の3倍まで候補を問い合わせる。100件に
届かない場合は終了コード1となるので、`--candidate-multiplier 5` のように増やす。
REST通信や不正な応答は終了コード2となる。

EnsemblのPOST上限は200件であり、`--batch-size` は1–200に制限される。
デフォルトは20件とし、タイムアウトしたバッチは成功する大きさまで自動分割する。
単一入力もタイムアウトする場合は終了コード2となる。応答量を抑えるため、通常は
`spdi`、versionなしRefSeq入力だけはversion解決用の `hgvsc` を要求する。

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
  --output truth/gold.jsonl \
  --quarantine truth/quarantine.jsonl \
  --report truth/build-report.json
```

キャッシュミスは正解として扱わない。候補数、Variant Recoder採用数、最終件数、
カテゴリ別件数は `build-report.json` で確認できる。

## ClinVar版

`tools/build_clinvar_truth_set.py` は、共通候補へ結合済みのClinVar GRCh38行から
`PositionVCF`、`ReferenceAlleleVCF`、`AlternateAlleleVCF` を取得する。`Start`、
`Stop`、`ReferenceAllele`、`AlternateAllele` はHGVS寄りの表現になり得るため
正解VCFには使わない。

CHROMには `Chromosome` の数値表記ではなく `ChromosomeAccession` を使う。
たとえばClinVarの `NC_000001.11` は、FASTAヘッダー
`>NC_000001.11 Homo sapiens chromosome 1, ...` の空白より前の配列IDと一致する。

VCF用3列もそのまま採用せず、NCBI GRCh38.p14 genomic FASTAに対して次の処理を行う。

1. accession付き染色体名で一時VCFを作る。
2. `bcftools norm --fasta-ref ... --check-ref x --multiallelics -any` を実行する。
3. left-align・最小表現化された `CHROM/POS/REF/ALT` を正解にする。
4. REF不一致や正規化結果のない候補をquarantineへ送る。
5. 有効な候補から入力形式と変異カテゴリを均等に約100件選ぶ。

```bash
REFERENCE_FASTA=sources/reference/grch38-p14/GCF_000001405.40_GRCh38.p14_genomic.fna \
scripts/build_clinvar_truth_set.sh
```

出力は `truth/clinvar/` に分離する。build reportにはClinVar・MANE・FASTAのSHA-256、
bcftools version、正規化オプション、採否件数を記録する。これはHGVSから座標を
再計算した正解ではなく、ClinVarのVCF表現を独立に再正規化した正解である。

## 対象APIの評価

```bash
python3 tools/evaluate_hgvs2vcf.py \
  --truth-set truth/gold.jsonl \
  --base-url http://localhost:4567 \
  --json-report evaluation/result.json \
  --markdown-report evaluation/result.md
```

評価コードは `confidence: ensembl_variant_recoder` と
`confidence: clinvar_bcftools_normalized` をgoldとして受け付ける。VCF集合、
transcript、`ambiguous` を比較し、順序には依存しない。

これは座標変換実装の回帰試験用データであり、臨床判断には使用しない。
