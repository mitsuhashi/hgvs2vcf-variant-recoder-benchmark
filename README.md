# hgvs2vcf-variant-recoder-benchmark

Ensembl Variant Recoderを正解として、HGVS→GRCh38 VCF変換を評価するツールです。

## 全体の流れ

```text
ClinVar
  │ バージョン付きtranscript HGVSを収集
  ▼
位置と変異操作で分類し、偏りなく抽出
  ▼
Ensembl Variant Recoder
  │ HGVSを変換
  ▼
正解セット（JSONL）
  │ VCF・transcript・ambiguousを比較
  ▼
評価対象の POST /decode
  ▼
評価レポート（JSON / Markdown）
```

ClinVarはHGVS入力候補の収集にだけ使います。ClinVarの座標やREF/ALTは正解にせず、
Variant Recoderが返す `vcf_string` を正解VCFへ変換します。

Variant Recoderが解釈できないHGVSや、GRCh38主染色体のVCFを返さないケースは
正解セットから除外し、quarantineへ記録します。

## 利用する2つのAPI

このツールでは、目的の異なる2つのAPIを使います。

| API | URL | 用途 |
|---|---|---|
| Ensembl Variant Recoder | `https://rest.ensembl.org/variant_recoder/homo_sapiens` | 正解VCFの生成 |
| 評価対象のHGVS→VCF API | `--base-url` で指定したURLの `/decode` | 正解セットとの比較 |

Variant Recoderのデフォルトサーバーは `https://rest.ensembl.org` です。別のEnsembl
RESTサーバーを使う場合は、正解セット生成時に `--server` で指定します。

`http://localhost:4567` は、評価対象の `hgvs2vcf-cdot-lmdb` をローカルで起動した
場合の例です。このレポジトリ自身はHGVS→VCF APIサーバーを起動しません。公開または
別環境のサーバーを評価する場合は、`--base-url` を実際のURLへ変更してください。

## 必要なもの

- Python 3.11以上（外部Pythonパッケージ不要）
- Ensembl REST APIへのHTTPS接続
- 同一ClinVarリリースの次のファイル
  - `variant_summary.txt.gz`
  - `hgvs4variation.txt.gz`

## 1. ClinVarデータを取得

```bash
mkdir -p sources/clinvar/2026-07-02

curl -fL -o sources/clinvar/2026-07-02/variant_summary.txt.gz \
  https://ftp.ncbi.nlm.nih.gov/pub/clinvar/tab_delimited/variant_summary.txt.gz

curl -fL -o sources/clinvar/2026-07-02/hgvs4variation.txt.gz \
  https://ftp.ncbi.nlm.nih.gov/pub/clinvar/tab_delimited/hgvs4variation.txt.gz
```

ディレクトリ名と `--clinvar-release` には、実際に使用したリリース日を指定します。

## 2. 約100件の正解セットを生成

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

候補は次の2軸で分類し、存在するカテゴリからラウンドロビンで抽出します。

- 位置: coding、intronic、UTR、non-coding transcript
- 操作: substitution、deletion、insertion、duplication、delins

固定seedを使うため、同じClinVarファイルとVariant Recoder応答から同じセットを
再生成できます。100件に届かない場合は `--candidate-multiplier 5` のように、
問い合わせる候補数を増やします（デフォルトは目標数の3倍）。

生成物:

| パス | 内容 |
|---|---|
| `truth/gold.jsonl` | Variant Recoder由来の正解セット |
| `truth/quarantine.jsonl` | 応答なし、解釈不能、主染色体VCFなしのケース |
| `truth/build-report.json` | 件数、カテゴリ分布、SHA-256、実行設定 |
| `build/variant-recoder-cache.jsonl` | Variant Recoderの応答キャッシュ |

保存済みキャッシュだけで再生成する場合は、同じコマンドに `--mode cache` を
追加します。キャッシュミスは正解として採用されません。

## 3. HGVS→VCF APIを評価

評価対象の `hgvs2vcf-cdot-lmdb` サーバーを起動してから実行します。次は
`http://localhost:4567` でローカル起動している場合の例です。

```bash
python3 tools/evaluate_hgvs2vcf.py \
  --truth-set truth/gold.jsonl \
  --base-url http://localhost:4567 \
  --json-report evaluation/result.json \
  --markdown-report evaluation/result.md
```

`--base-url` には評価対象サーバーのURLを指定します。これはVariant RecoderのURL
ではありません。

`POST /decode` の結果について、次を比較します。

- VCF集合の `chrom`、`pos`、`ref`、`alt`（順序は無視）
- transcript
- `ambiguous`
- `--check-gene` 指定時はgene

終了コードは、全件一致が0、変換結果に差分ありが1、通信・応答形式エラーが2です。

## 再現性

Ensembl REST APIの内容はリリースとともに更新されます。同じ正解セットを再構築
できるよう、以下を保存してください。

- 2つのClinVar入力ファイル
- Variant Recoder応答キャッシュ
- `truth/gold.jsonl`
- `truth/build-report.json`

Ensembl archive RESTサーバーを利用する場合は `--server` で指定できます。
固定方法と採否基準の詳細は [TRUTH_SET.md](TRUTH_SET.md) を参照してください。

## テスト

```bash
python3 -m unittest discover -s tests -v
```

テストの目的と、モック・実API確認の範囲は [TESTS.md](TESTS.md) に記載しています。

## ドキュメント

- `README.md` — 全体像と使い方（このファイル）
- `TRUTH_SET.md` — 正解セットの生成仕様
- `TESTS.md` — テスト内容と検証範囲

実装は `tools/`、ユニットテストとfixtureは `tests/` にあります。

この正解セットは回帰試験用です。臨床判断には使用しないでください。
