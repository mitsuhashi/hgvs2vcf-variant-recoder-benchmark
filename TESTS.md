# テスト内容

```bash
python3 -m unittest discover -s tests -v
```

現在は、正解セット生成側16件、評価側4件の合計20件である。外部HTTP通信は
モックし、ネットワークなしで実行する。

## 正解セット生成

### 1. `test_fixture_join_and_filter`

ClinVar 2ファイルとMANE summaryを結合し、次の3形式を生成できることを確認する。
`hgvs4variation` fixtureは実データと同様に説明行を含み、protein HGVSを
`Type=coding` 行の `ProteinExpression` 列に保持する。
`variant_summary` fixtureはVCF座標・REF・ALT列を持たず、それらに依存せず候補を
生成できることも確認する。

- `GENE:p.`（例: `NOS3:p.Asp298Glu`）
- `GENE:c.`（例: `NOS3:c.894T>G`）
- versionなし `NM_:c.`（例: `NM_000603:c.894T>G`）

### 2. `test_inputs_use_mane_and_old_build_is_excluded`

gene symbol形式がMANE Selectの `RefSeq_nuc`／`RefSeq_prot` から生成され、GRCh37や
accessionをそのまま使った入力が混入しないことを確認する。

### 3. `test_candidate_retention_is_bounded_per_group`

実データから生成される候補総数は統計へ残しつつ、メモリ上には入力形式・変異カテゴリ
ごとに指定上限までしか保持しないことを確認する。

### 4. `test_candidate_cache_round_trip_preserves_sets_and_stats`

選定済み候補と全件統計をローカルキャッシュへ保存・復元でき、set型のgenomic HGVSも
失われないことを確認する。

### 5. `test_balanced_order_round_robins_categories`

3つの入力形式を最優先でラウンドロビンし、各形式の中でも変異カテゴリを均等に
並べることを確認する。

### 6. `test_gene_record_uses_only_mane_vcf`

gene symbol入力が複数VCFを返しても、正解にはMANE Select表記をVariant Recoderへ
入力して得たVCFだけを採用することを確認する。

### 7. `test_gene_record_rejects_mane_vcf_missing_from_gene_response`

MANE由来VCFがgene symbol入力の返却VCFに含まれない場合、goldへ入れずquarantineへ
送ることを確認する。

### 8. `test_unversioned_refseq_resolves_version_from_recoder`

versionなし `NM_:c.` の期待transcriptを、Variant Recoderが返すversion付き `hgvsc`
から決定することを確認する。

### 9. `test_parse_variant_recoder_vcf_formats`

Variant Recoderの `CHROM-POS-REF-ALT` と通常VCF列形式を解釈し、GRCh38主染色体を
RefSeq accessionへ変換することを確認する。主染色体以外は採用しない。

### 10. `test_extracts_all_primary_assembly_alleles`

入れ子になったVariant Recoder応答から複数アレルを抽出・重複除去し、解釈できない
VCF文字列を記録することを確認する。

### 11. `test_fetch_recoder_uses_post_and_associates_echoed_input`

`vcf_string=1` を指定してPOSTし、応答順が変わっても応答内の `input` で元のHGVSへ
対応付けることを確認する。

### 12. `test_fetch_recoder_requests_hgvsc_for_unversioned_refseq`

versionなしRefSeq入力にはversion解決用の `hgvsc` を要求し、それ以外の入力では
応答量の小さい `spdi` だけを要求することを確認する。

### 13. `test_fetch_recoder_bisects_all_invalid_batch`

バッチ全体がエラーになった場合に入力を分割し、問題入力を個別に隔離することを
確認する。

### 14. `test_fetch_recoder_bisects_timed_out_batch`

複数入力のバッチが読み取りタイムアウトした場合に半分ずつへ分割し、正常な個別入力を
取得できることを確認する。

### 15. `test_fetch_recoder_bisects_http_400_and_quarantines_singleton`

無効入力を含むバッチがHTTP 400になった場合も半分ずつへ分割し、正常入力を取得して
不正な単一入力だけをquarantine用エラーとして保持することを確認する。

### 16. `test_fetch_recoder_quarantines_timed_out_singleton`

単一入力がタイムアウトした場合、処理全体を止めずにその入力をquarantine用エラー
として保持し、応答キャッシュには保存しないことを確認する。

## 評価ツール

### 17. `test_equal_vcf_ignores_candidate_order`

VCF集合の順序が異なっても、`chrom`、`pos`、`ref`、`alt` が同じなら合格になる
ことを確認する。

### 18. `test_coordinate_difference_is_reported`

座標が1塩基でも異なれば不合格となり、VCF差分がレポートへ記録されることを確認する。

### 19. `test_markdown_report_lists_passed_and_failed_vcfs`

Markdownレポートに成功・失敗の両方と、期待VCF・観測VCFが表示されることを確認する。

### 20. `test_post_batch_contract`

評価対象の `POST /decode` へ `{"hgvs": [...]}` を送り、JSON配列の応答を読み取る
ことを確認する。

## 実APIで確認した範囲

ユニットテストとは別に、Ensembl Variant Recoderの実APIで次を確認した。

- `ALDH2:p.Glu504Lys` を受理する
- `ALDH2:c.1510G>A` を受理する
- `NM_000690:c.1510G>A` を `NM_000690.4` へ解決する
- gene symbol形式は複数VCFを返し得る
- MANE protein `NP_000681.2:p.Glu504Lys` は対象VCF
  `12-111803962-G-A` に限定される
- `vcf_string` は `12-111803962-G-A` 形式で返る

実API確認は通常のテスト実行には含まれない。
