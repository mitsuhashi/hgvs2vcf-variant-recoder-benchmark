# テスト内容

テストは `tests/test_tools.py` にあり、次のコマンドで実行する。

```bash
python3 -m unittest discover -s tests -v
```

現在は、正解セット生成側7件、評価ツール側3件の合計10件である。

## 正解セット生成側

### 1. `test_fixture_join_and_filter`

ClinVarの `variant_summary` と `hgvs4variation` をVariation IDで結合できることを
確認する。

確認項目:

- transcript HGVSが正しく抽出される
- GRCh38 VCF候補が読み取られる
- genomic HGVSが同じVariation IDへ関連付けられる
- HGVSが適切なカテゴリへ分類される

ClinVarのVCFは候補の絞り込みにだけ使い、最終的な正解VCFには使用しない。

### 2. `test_protein_and_old_build_are_not_candidates`

正解セットの入力候補として不適切な行を除外できることを確認する。

確認項目:

- protein HGVSを候補にしない
- GRCh37の行を候補にしない

### 3. `test_parse_variant_recoder_vcf_formats`

Variant Recoderが返すVCF文字列を正規化できることを確認する。

確認項目:

- `7-150999023-T-G` 形式を解釈できる
- 空白区切りの通常VCF形式を解釈できる
- `X` をGRCh38 RefSeq accession `NC_000023.11` へ変換できる
- `GL000220.1` など主染色体以外の配列を採用しない

### 4. `test_extracts_all_primary_assembly_alleles`

Variant Recoderの入れ子になったJSON応答から、すべての有効な主染色体アレルを
抽出できることを確認する。

確認項目:

- 複数の代替アレルをすべて抽出する
- 重複するVCFを一つにまとめる
- LRGなど主染色体以外のVCFをgoldへ入れない
- 解釈できなかったVCF文字列を記録する

複数の異なるVCFが得られたケースは、正解セットで
`expected.ambiguous: true` となる。

### 5. `test_balanced_order_round_robins_categories`

入力候補が特定カテゴリへ偏らないよう、カテゴリ間をラウンドロビンで選択できる
ことを確認する。

例えばカテゴリAとBが十分に存在する場合、先頭はA、B、A、Bのように並ぶ。
実際の分類軸は次の組み合わせである。

- 位置: coding、intronic、UTR、non-coding transcript
- 操作: substitution、deletion、insertion、duplication、delins

### 6. `test_fetch_recoder_uses_post_and_associates_echoed_input`

Ensembl Variant Recoderへのリクエストと応答の対応付けを確認する。

確認項目:

- HTTP POSTを使用する
- `vcf_string=1` を指定する
- 複数のHGVSをJSONの `ids` 配列として送る
- API応答の順序が入力順と異なっても、応答内の `input` で正しく対応付ける

### 7. `test_fetch_recoder_bisects_all_invalid_batch`

Variant Recoderがバッチに対してエラーオブジェクトを返した場合の隔離処理を確認する。

確認項目:

- エラーになったバッチを分割する
- 問題のある入力を個別に特定する
- エラー応答を正解値として採用しない

## 評価ツール側

### 8. `test_equal_vcf_ignores_candidate_order`

期待VCFと観測VCFの配列順が異なっても、VCF集合の内容が同じであれば合格になる
ことを確認する。

比較するVCF項目:

- `chrom`
- `pos`
- `ref`
- `alt`

### 9. `test_coordinate_difference_is_reported`

期待値と観測値の座標が1塩基でも異なれば不合格となり、VCF差分が結果に記録される
ことを確認する。

### 10. `test_post_batch_contract`

評価対象である `hgvs2vcf-cdot-lmdb` のHTTP APIとの基本契約を確認する。

確認項目:

- `POST /decode` を呼び出す
- `{"hgvs": [...]}` 形式のJSONを送る
- JSON配列として返された変換結果を読み取る

## モックと実API確認の範囲

上記10件は、外部サービスに依存せず高速かつ安定して実行できるユニットテストである。
HTTP通信にはモックを使用しているため、テスト実行時にEnsembl REST APIや評価対象
サーバーへ接続しない。

実装時には別途、Ensembl Variant Recoderの実APIを使って次を手動確認した。

- `POST /variant_recoder/homo_sapiens` が利用できる
- `vcf_string=1` によりVCFが返る
- VCF文字列が `1-230710021-G-A` 形式で返る
- 無効なtranscriptではエラーまたは応答からの省略が起こり得る

この実API確認は現在の10件には含まれない。Ensemblの稼働状態や最新リリースとの
互換性を継続的に検査する統合テストを追加する場合は、通常のユニットテストとは
分離し、明示的に実行する構成とする。

