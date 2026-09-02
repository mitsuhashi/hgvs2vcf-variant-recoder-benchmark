# hgvs2vcf-marshal gold500評価の原因分析

## 概要

`truth/gold500.jsonl` の469件について、Ensembl Variant Recoder由来の
`expected.vcf` と `hgvs2vcf-marshal` の結果を比較した。

| 結果 | 件数 |
|---|---:|
| 完全一致 | 279 |
| 正規化同値として一致 | 75 |
| 判定が残るVCF不一致 | 53 |
| APIエラー | 62 |
| 合計 | 469 |
| 合格 | 354 |
| 合格率 | 75.48% |

生の `chrom`、`pos`、`ref`、`alt` の完全一致率は59.49%だったが、VCF不一致128件
には同じ変異を異なる位置やアレルで表現したケースが多数含まれていた。評価器を変更し、
VCFから再構成できる共通参照配列へ両alleleを適用して一致する75件も合格としている。

詳細な各入力の結果は `evaluation/marshal-result.json` と
`evaluation/marshal-result.md` に記録している。

## 1. 当初VCF不一致だった128件

### 全体的な特徴

128件はすべて次の条件を満たした。

- genomic accessionは同一
- REFとALTの長さの差は同一
- coding substitutionは52件すべて完全一致
- 不一致はdel、dup、ins、delinsに限定
- marshalの位置がVariant Recoderより左側: 113件
- marshalの位置がVariant Recoderより1塩基右側: 15件
- 同じ位置でアレルだけが異なるケース: 0件

位置差の最頻値は-1塩基の42件で、最大の左方向への差は45塩基だった。

### 同値と確認できた75件

15件ではVariant Recoder側のREFとALTに共通prefixが1塩基残っており、marshalは
その共通prefixを除去していた。15件すべてで、Variant Recoder側のREF/ALTから先頭
1塩基を除くとmarshal側と一致した。この15件は同じVCF alleleである。

残る左方向へ移動した113件のうち60件は、両VCFのREFが覆う範囲から参照配列を
再構成し、それぞれのALTを適用した結果が一致した。この60件も同じ変異である。

したがって、75件は表記差による偽陰性である。現在の評価器ではこの75件を
`match_type: equivalent` として合格にし、次の一致率になった。

```text
(279 + 75) / 469 = 75.48%
```

### NCBI Variation Servicesによる確認例

`BRCA2:c.2192_2196del` は次のように異なっていた。

```text
Variant Recoder: NC_000013.11 32336546 GAAGAG > G
marshal:         NC_000013.11 32336544 AAGAAG > A
```

NCBI Variation Servicesで両方をcontextual SPDIへ変換すると、どちらも次の表現になった。

```text
NC_000013.11:32336544:AGAAGAG:AG
```

これは反復配列内で位置だけが異なる同一変異である。

`CFAP410:c.689_722dup` も34塩基の位置差があったが、NCBIでcontextual SPDIへ
変換すると同一になった。

一方、`NM_001372044:c.3069_3076dup` は45塩基の位置差があり、NCBIで正規化しても
異なるSPDIになった。このケースは単なる左正規化差ではなく、transcript version、
transcript-genome alignment、またはduplication対象配列の違いを調べる必要がある。

NCBIのSPDIとcontextual alleleについては、次を参照した。

- [SPDI: data model for variants and applications at NCBI](https://pmc.ncbi.nlm.nih.gov/articles/PMC7523648/)
- [NCBI Variation Services API](https://api.ncbi.nlm.nih.gov/variation/v0/var_service.yaml)

### 評価方法の問題

現在の評価器は、生のVCFタプルが一致しない場合、両VCFのREFが覆う連続範囲から
参照配列を再構成し、ALT適用後の配列が一致すれば合格にする。VCFだけでは間の参照
配列を再構成できない53件は、同じ染色体・同じ長さの変化という理由だけでは合格に
していない。この53件を判定するには、両方を同じGRCh38 FASTAで正規化する必要がある。

## 2. marshalの未対応入力53件

APIエラー62件のうち53件は、marshalの対応範囲または変換方針によるものだった。

| エラー | 件数 | 原因 |
|---|---:|---|
| `INVALID_HGVS` | 25 | protein deletion構文が未対応 |
| `INVALID_HGVS` | 1 | `SRP54:c.1327+15_1327+32del18` の長さ付きdelが未対応 |
| `UNSUPPORTED_PROTEIN_EDIT` | 26 | `p.Val300=` などのprotein identity |
| `DATA_NOT_FOUND` | 1 | `MARVELD2:p.Pro97His` の `cds_sequence` 欠落 |

### Protein deletion

marshalのproteinパーサは、単一アミノ酸の置換または `=` を受け付けるが、
`p.Gly2765del` や `p.Leu262_Val264del` のようなprotein deletionを受け付けない。

- [hgvs_parser.rb](https://github.com/ktym/hgvs2vcf-marshal/blob/main/lib/hgvs_vcf/hgvs_parser.rb)

### Protein identity

`p.=` はパースされるが、converterは `protein identity is not a DNA allele` として
明示的に拒否する。一方、Variant Recoderは同じアミノ酸になる候補DNA変異を返す。
これは単純なパースエラーではなく、両実装の変換方針の違いである。

- [converter.rbのprotein変換](https://github.com/ktym/hgvs2vcf-marshal/blob/main/lib/hgvs_vcf/converter.rb#L43-L75)

Variant Recoder互換を目指す場合は、同じアミノ酸を生成する最小の非ゼロ塩基置換を
候補として列挙する必要がある。そうしない場合は、protein identityをベンチマークの
対象外として明示する必要がある。

## 3. HTTP 500の9件

HTTP 500になった入力は次の9件だった。

```text
CDSN:c.164_167dup
KCNQ2:c.1149-6_1149-5dup
NM_000314:c.31del
NM_172107:c.2333del
PKD1:c.5883_5929del
PKD1:c.99del
ALMS1:c.790dup
NM_005993:c.3480-19G>T
COL18A1:c.*30G>A
```

最初の再現時には、marshalから次の例外が返った。

```text
undefined method '+' for nil (NoMethodError)
converter.rb:124 または converter.rb:127
```

`transcript_position` はcoding座標で `cds_start_n`、`*` 座標で `cds_end_n` に値を
加算する。対象transcriptではキーが存在していても値が `nil` のため、`KeyError` では
なく `NoMethodError` になっている。

- [converter.rbのtranscript_position](https://github.com/ktym/hgvs2vcf-marshal/blob/main/lib/hgvs_vcf/converter.rb#L121-L129)

さらに、バッチAPIの `convert_one` は `ConversionError` だけを捕捉するため、
`NoMethodError` がバッチ全体へ伝播してHTTP 500になる。

- [api.rbのconvert_one](https://github.com/ktym/hgvs2vcf-marshal/blob/main/lib/hgvs_vcf/api.rb#L47-L50)

原因は次の2層に分かれる。

1. index内のcoding transcriptに `cds_start_n`、`cds_end_n`、または
   `cds_sequence` が欠落している
2. converterとAPIが不完全なindex recordを安定した `DATA_NOT_FOUND` として扱わない

評価器側では、HTTP 5xxになったバッチを二分して原因入力を特定し、その入力だけを
APIエラーとして記録して残りの評価を継続するよう対応した。ただし、これはmarshalの
データ欠落や例外処理を修正するものではない。

## 修正の優先順位

1. 評価器で両VCFを同一のGRCh38 FASTAにより正規化してから比較する
2. index生成時にcoding transcriptのCDS関連フィールドを検証する
3. CDS情報欠落を `DATA_NOT_FOUND` として返し、バッチ全体のHTTP 500を防ぐ
4. protein deletionを実装する
5. protein identityをVariant Recoder互換にするか、評価対象外にするか決定する
6. 正規化後も異なるduplicationについてtranscript versionとalignmentを比較する

## 結論

厳密なVCF文字列表現の一致率は59.49%だったが、同値と証明できた75件を合格にした
現在の合格率は75.48%である。残る53件は参照配列による追加判定が必要であり、その
中には実際に異なるduplicationも含まれる。

marshal側の明確な修正対象は、CDSメタデータ欠落によるHTTP 500、protein deletion
未対応、およびprotein identityの方針差である。
