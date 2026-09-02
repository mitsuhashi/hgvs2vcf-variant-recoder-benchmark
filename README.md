# hgvs2vcf-variant-recoder-benchmark

HGVS→GRCh38 VCF変換を、Ensembl Variant Recoder由来の正解セットで評価する
ツールです。

## 全体の流れ

```text
ClinVar（HGVS・gene symbol） ─┐
                              ├─ 入力候補を生成
MANE Select（代表transcript）─┘
  │
  ▼
3つの入力形式と変異操作で分類し、偏りなく抽出
  │ Ensembl Variant Recoderの返却VCFを取得
  │
  ▼
正解セット（JSONL）
  │ ゲノムVCF集合を比較
  ▼
評価対象のAPI（cdotまたはmarshal）
  ▼
評価レポート（JSON / Markdown）
```

ClinVarはHGVS入力候補の収集にだけ使い、正解VCFにはEnsembl Variant Recoderの
`vcf_string` だけを使います。gene symbol入力は固定したMANE Selectに限定します。

| データソース | このプロジェクトでの用途 |
|---|---|
| ClinVar | HGVS、gene symbol、GRCh38主染色体accessionによる入力候補の抽出 |
| MANE Select | gene symbol入力に対応する代表RefSeq transcriptの固定 |
| Ensembl Variant Recoder | 正解VCFと、versionなしRefSeq入力のtranscript versionの決定 |

ClinVarの `PositionVCF`、`ReferenceAlleleVCF`、`AlternateAlleleVCF` は読み取らず、
正解値にも候補の座標判定にも使いません。

Variant Recoderが解釈できないHGVSや、GRCh38主染色体のVCFを返さないケースは
正解セットから除外し、quarantineへ記録します。

## 利用するAPI

正解セットの生成にはEnsembl Variant Recoderを使い、評価対象にはcdotまたはmarshal
のいずれかを選択します。

| API | URL | 用途 |
|---|---|---|
| Ensembl Variant Recoder | `https://rest.ensembl.org/variant_recoder/homo_sapiens` | 正解VCFの生成 |
| hgvs2vcf-cdot | `--base-url` で指定したURLの `/decode` | 正解セットとの比較 |
| hgvs2vcf-marshal | `--base-url` で指定したURLの `/v1/convert-batch` | 正解セットとの比較 |

Variant Recoderのデフォルトサーバーは `https://rest.ensembl.org` です。別のEnsembl
RESTサーバーを使う場合は、正解セット生成時に `--server` で指定します。

評価対象は `--api-type` で選択します。このレポジトリ自身はHGVS→VCF APIサーバーを
起動しません。公開または別環境のサーバーを評価する場合は、`--base-url` を実際の
URLへ変更してください。

## 必要なもの

- Python 3.11以上（外部Pythonパッケージ不要）
- 同一ClinVarリリースの次のファイル
  - `variant_summary.txt.gz`
  - `hgvs4variation.txt.gz`
- MANE summary
  - `MANE.GRCh38.v1.5.summary.txt.gz`
- Ensembl REST APIへのHTTPS接続

## 1. ClinVar・MANEデータを取得

通常はダウンロードスクリプトを実行します。

```bash
scripts/download_sources.sh
```

リリースを変更する場合は、buildスクリプトと同じ環境変数を指定します。

```bash
CLINVAR_RELEASE=2026-07-02 \
MANE_RELEASE=1.5 \
scripts/download_sources.sh
```

既存ファイルは再利用します。再取得する場合は `FORCE_DOWNLOAD=1` を指定します。

```bash
FORCE_DOWNLOAD=1 scripts/download_sources.sh
```

ClinVarは公式のtab-delimited配布先、MANEは指定リリースの公式summaryから取得します。
保存先は `CLINVAR_DIR`、`MANE_DIR`、または `SOURCES_DIR` で変更できます。

## 2. Variant Recoderから正解セットを生成

通常は実行スクリプトを使います。

```bash
scripts/build_truth_set.sh
```

デフォルトはClinVar `2026-07-02`、Ensembl `116`、MANE `1.5`、目標100件です。
異なるリリースや件数は環境変数で指定できます。

```bash
CLINVAR_RELEASE=2026-07-02 \
ENSEMBL_RELEASE=116 \
MANE_RELEASE=1.5 \
TARGET_COUNT=100 \
scripts/build_truth_set.sh
```

主な環境変数:

| 変数 | デフォルト |
|---|---|
| `CLINVAR_RELEASE` | `2026-07-02` |
| `ENSEMBL_RELEASE` | `116` |
| `MANE_RELEASE` | `1.5` |
| `TARGET_COUNT` | `100` |
| `CANDIDATE_MULTIPLIER` | `5` |
| `ENSEMBL_SERVER` | `https://rest.ensembl.org` |
| `BATCH_SIZE` | `20` |
| `VARIANT_RECODER_TIMEOUT` | `60`秒 |
| `VARIANT_RECODER_WORKERS` | `1` |
| `CANDIDATE_CACHE` | `build/candidate-selection-cache.json` |
| `CLINVAR_DIR` | `sources/clinvar/$CLINVAR_RELEASE` |
| `MANE_SUMMARY` | `sources/mane/$MANE_RELEASE/MANE.GRCh38.v$MANE_RELEASE.summary.txt.gz` |

入力・出力パスは `VARIANT_SUMMARY`、`HGVS4VARIATION`、`TRUTH_DIR`、`BUILD_DIR`
でも上書きできます。追加引数はPythonプログラムへ渡されます。

```bash
BATCH_SIZE=10 VARIANT_RECODER_TIMEOUT=120 VARIANT_RECODER_WORKERS=4 scripts/build_truth_set.sh
```

Variant Recoderへの大きなバッチがタイムアウトした場合は、自動的に半分へ分割して
再実行します。単一入力がタイムアウトする場合は、その入力だけを一時的な
quarantine対象として残りの処理を続け、応答キャッシュには保存しません。
`VARIANT_RECODER_WORKERS` で独立したバッチを並列取得できます（1–8）。
通常はVCFに加えて軽量な `spdi` だけを要求し、versionなしRefSeq入力のみtranscript
versionの決定に必要な `hgvsc` を要求します。

次の3形式をほぼ同数にし、各形式の中でも変異操作が偏らないよう抽出します。

| 入力形式 | 例 | transcriptの決定 |
|---|---|---|
| gene symbol HGVSp | `ALDH2:p.Glu504Lys` | MANE Select |
| gene symbol HGVSc | `ALDH2:c.1510G>A` | MANE Select |
| versionなしRefSeq HGVSc | `NM_000690:c.1510G>A` | Variant Recoderの解決結果 |

gene symbol形式は、ClinVar HGVSのaccessionがMANE summaryの `RefSeq_nuc` または
`RefSeq_prot` と一致する場合だけ生成します。Variant Recoderへgene symbol表記と
MANE表記の両方を問い合わせ、MANE由来VCFがgene symbolの結果に含まれる場合だけ
goldへ採用します。

固定seedを使うため、同じClinVar・MANEファイルとVariant Recoder応答から同じセットを
再生成できます。100件に届かない場合は `--candidate-multiplier 7` のように、
問い合わせる候補数を増やします（デフォルトは目標数の5倍）。
大規模なClinVar全候補をメモリへ保持せず、入力形式・変異カテゴリごとに安定ハッシュで
必要数だけ保持します。候補総数はbuild reportへ記録されます。
選定済み候補はローカルキャッシュへ保存され、入力ファイルのパス・サイズ・更新時刻、
seed、候補数が同じ再実行では約4,480万行の再走査を省略します。

生成物:

| パス | 内容 |
|---|---|
| `truth/gold.jsonl` | Variant Recoder由来の正解セット |
| `truth/quarantine.jsonl` | 応答なし、解釈不能、主染色体VCFなしのケース |
| `truth/build-report.json` | 件数、カテゴリ分布、SHA-256、実行設定 |
| `build/variant-recoder-cache.jsonl` | Variant Recoderの応答キャッシュ |

保存済みキャッシュだけで再生成する場合は、スクリプトに `--mode cache` を
追加します。キャッシュミスは正解として採用されません。

```bash
scripts/build_truth_set.sh --mode cache
```

## 3. HGVS→VCF APIを評価

デフォルトでは公開 `hgvs2vcf-marshal` APIを評価します。

```bash
scripts/evaluate.sh
```

デフォルトでは `truth/gold500.jsonl` を使い、JSONとMarkdownのレポートをそれぞれ
`evaluation/marshal-result.json`、`evaluation/marshal-result.md` へ出力します。
現在のmarshal評価については、`evaluation/marshal-analysis.md` に原因分析をまとめて
います。

`hgvs2vcf-cdot` を評価する場合は、API種別を切り替えます。cdotとmarshalは同じ
FQDNを使い、それぞれ `/decode` と `/v1/convert-batch` へリクエストします。

```bash
API_TYPE=cdot scripts/evaluate.sh
```

公開または別環境のAPIを評価する場合は `BASE_URL` を指定します。これはVariant
RecoderのURLではありません。

```bash
API_TYPE=marshal BASE_URL=https://hgvs2vcf.example.org scripts/evaluate.sh
```

主な環境変数:

| 変数 | デフォルト |
|---|---|
| `API_TYPE` | `marshal` |
| `BASE_URL` | `https://hgvs2vcf.togovar.org` |
| `TRUTH_SET` | `truth/gold500.jsonl` |
| `EVALUATION_DIR` | `evaluation` |
| `JSON_REPORT` | `evaluation/<API_TYPE>-result.json` |
| `MARKDOWN_REPORT` | `evaluation/<API_TYPE>-result.md` |
| `EVALUATION_BATCH_SIZE` | `100` |
| `EVALUATION_TIMEOUT` | `60`秒 |
| `PYTHON_BIN` | `python3` |

追加引数は評価プログラムへそのまま渡せます。

```bash
EVALUATION_BATCH_SIZE=20 EVALUATION_TIMEOUT=120 scripts/evaluate.sh
```

cdotの `POST /decode` またはmarshalの `POST /v1/convert-batch` の結果について、
次を比較します。

- VCF集合の `chrom`、`pos`、`ref`、`alt`（順序は無視）

合否はゲノムVCF集合だけで決定します。transcript、gene、`ambiguous` の表記差は
合否に影響しません。

終了コードは、全件一致が0、変換結果に差分ありが1、通信・応答形式エラーが2です。
バッチがHTTP 5xxを返した場合は自動的に分割して原因入力を特定し、その入力だけを
APIエラーとして記録して残りの評価を継続します。

## 再現性

Ensembl REST APIの内容はリリースとともに更新されます。同じ正解セットを再構築
できるよう、以下を保存してください。

- 2つのClinVar入力ファイルとMANE summary
- Variant Recoder応答キャッシュ、`truth/gold.jsonl`、build report

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
入力取得は `scripts/download_sources.sh`、正解セット生成は
`scripts/build_truth_set.sh`、評価は `scripts/evaluate.sh` から実行します。

この正解セットは回帰試験用です。臨床判断には使用しないでください。
