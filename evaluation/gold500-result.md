# hgvs2vcf-cdot-lmdb evaluation

- Total: 469
- Passed: 322
- Failed: 147
- Pass rate: 68.66%

Alleles are printed in groups of ten bases. A failure here means the VCF
rows are not byte-identical, which for an indel is usually a left-alignment
or anchor-base difference rather than a different variant.

## Results by category

| Category              | Passed | Failed | Pass rate |
|-----------------------|-------:|-------:|----------:|
| coding_del            |     32 |     21 |    60.38% |
| coding_delins         |      9 |     12 |    42.86% |
| coding_dup            |     11 |     41 |    21.15% |
| coding_ins            |      9 |      2 |    81.82% |
| coding_other          |      1 |      0 |   100.00% |
| coding_substitution   |     52 |      0 |   100.00% |
| intronic_del          |     31 |     21 |    59.62% |
| intronic_delins       |      3 |      2 |    60.00% |
| intronic_dup          |      1 |     26 |     3.70% |
| intronic_ins          |      3 |      1 |    75.00% |
| intronic_substitution |     52 |      0 |   100.00% |
| protein_del           |      9 |     16 |    36.00% |
| protein_other         |     26 |      0 |   100.00% |
| protein_substitution  |     26 |      0 |   100.00% |
| utr_del               |      4 |      1 |    80.00% |
| utr_delins            |      0 |      1 |     0.00% |
| utr_dup               |      1 |      3 |    25.00% |
| utr_substitution      |     52 |      0 |   100.00% |

## Excluded from scoring (31)

候補 500 件のうち **31 件は Variant Recoder が
HTTP エラーを返し、応答そのものが得られなかった**。期待値 VCF が作れないため
真値セットは 469 件になっており、上のスコアの母数から外れている。
**本ツールの失敗ではない。**

| Category       | 件数 |
|----------------|-----:|
| protein_ins    |   13 |
| protein_dup    |    8 |
| protein_delins |    7 |
| coding_other   |    2 |
| protein_del    |    1 |

オラクルの応答: HTTP 400 が 30 件、HTTP 500 が 1 件

### 本ツールでの可否: 24/31 は答えを返せる

オラクルが答えられなかったものを本ツールに同じ内容で投げた結果。
**ただし正解が存在しないので、これらの答えが正しいかは検証されていない。**
採点結果ではなく、カバレッジの記録として読むこと。

```
NAGLU:p.Gly71dup
    -> NC_000017.11:42536473  G > GGGC
CFTR:p.Leu1368delinsCysLeuMet
    -> NC_000007.14:117664826  C > TGTTTAA  (ambiguous)
RFWD3:p.Thr535_Tyr536insTer
    -> NC_000016.10:74630927  A > ATAT  (ambiguous)
AR:p.Gly821_Leu822insTer
    -> NC_000023.11:67722840  G > GTAA  (ambiguous)
NHS:p.Ala117dup
    -> NC_000023.11:17376105  G > GGCC
HPS3:p.Leu614_Tyr615insTer
    -> NC_000003.12:149158816  T > TTAA  (ambiguous)
TBX18:p.Thr82_Pro85dup
    -> NC_000006.12:84763926  C > CCGGCCCAGACGT
BRCA2:p.Thr399_Leu400delinsIle
    -> NC_000013.11:32332673  ACCC > A  (ambiguous)
... 他 16 件
```

### 本ツールでも返せない 7 件

```
CIC:p.Pro2483_Leu2484insGlnAlaAlaProPro
    QAAPP has 512 possible codon combinations (limit 64); the nucleotide change cannot be pinned down from HGVSp alone
MUC5B:p.Thr4870_Leu4871insProGlyThrThrTrpIleLeuThrGluSerSerThrThrAlaThrValThrValProThrSerSerThrAlaThrAlaSerSerThr
    PGTTWILTESSTTATVTVPTSSTATASST has 461689330549653504 possible codon combinations (limit 64); the nucleotide change cannot be pinned down from HGVSp alone
CRYGC:p.Asn138_Tyr139delinsArgArgArgGlyAsnThrLeuValAspGlyGlnTyrLeuValAspGlyAlaIleProSerTer
    RRRGNTLVDGQYLVDGAIPS* has 880602513408 possible codon combinations (limit 64); the nucleotide change cannot be pinned down from HGVSp alone
APC:p.Ala193_Gln195delinsValArgLeu
    VRL has 144 possible codon combinations (limit 64); the nucleotide change cannot be pinned down from HGVSp alone
NM_001077365:c.1047=
    unsupported cDNA change "c.1047="
PHOX2B:p.Ala260_Gly261insAlaAlaAlaAlaAlaAlaAlaAlaAlaAlaAla
    AAAAAAAAAAA has 4194304 possible codon combinations (limit 64); the nucleotide change cannot be pinned down from HGVSp alone
JRK:c.1382_1383=
    unsupported cDNA change "c.1382_1383="
```

## Failed results (147)

判定は表記の比較ではなく、**両者の対立遺伝子を GRCh38 に実際に適用して
配列を突き合わせた**結果。内訳:

- 左寄せの違い: 131 件
- アンカー塩基のトリミング差: 15 件
- 別の変異: 1 件

「別の変異」は両者が食い違うという事実のみを示す。**どちらが正しいかは
別途の検証が必要**で、オラクル側が誤っている場合もこの判定になる。

### `BRCA2:c.2192_2196del` — coding_del

**Variant としては同一。** 左寄せの違い — hgvs2vcf は VCF 規約どおり 2 塩基左に寄せ、Variant Recoder は HGVS の 3′ シフト位置のまま。

```
Variant Recoder:
  NC_000013.11:32336546
    REF  GAAGAG
    ALT  G

hgvs2vcf:
  NC_000013.11:32336544
    REF  AAGAAG
    ALT  A
```

### `HSD3B2:c.792_796del` — coding_del

**Variant としては同一。** 左寄せの違い — hgvs2vcf は VCF 規約どおり 2 塩基左に寄せ、Variant Recoder は HGVS の 3′ シフト位置のまま。

```
Variant Recoder:
  NC_000001.11:119422292
    REF  ATGATA
    ALT  A

hgvs2vcf:
  NC_000001.11:119422290
    REF  CTATGA
    ALT  C
```

### `ITGB3:c.2068_2069del` — coding_del

**Variant としては同一。** 左寄せの違い — hgvs2vcf は VCF 規約どおり 3 塩基左に寄せ、Variant Recoder は HGVS の 3′ シフト位置のまま。

```
Variant Recoder:
  NC_000017.11:47302773
    REF  TGT
    ALT  T

hgvs2vcf:
  NC_000017.11:47302770
    REF  CTG
    ALT  C
```

### `LDLRAP1:c.112_113del` — coding_del

**Variant としては同一。** 左寄せの違い — hgvs2vcf は VCF 規約どおり 2 塩基左に寄せ、Variant Recoder は HGVS の 3′ シフト位置のまま。

```
Variant Recoder:
  NC_000001.11:25553944
    REF  CAC
    ALT  C

hgvs2vcf:
  NC_000001.11:25553942
    REF  GAC
    ALT  G
```

### `LMNA:c.991_992del` — coding_del

**Variant としては同一。** 左寄せの違い — hgvs2vcf は VCF 規約どおり 1 塩基左に寄せ、Variant Recoder は HGVS の 3′ シフト位置のまま。

```
Variant Recoder:
  NC_000001.11:156135954
    REF  GCG
    ALT  G

hgvs2vcf:
  NC_000001.11:156135953
    REF  AGC
    ALT  A
```

### `NF1:c.2284_2296del` — coding_del

**Variant としては同一。** 左寄せの違い — hgvs2vcf は VCF 規約どおり 3 塩基左に寄せ、Variant Recoder は HGVS の 3′ シフト位置のまま。

```
Variant Recoder:
  NC_000017.11:31227249
    REF  ACTGCTGAGG CGCA
    ALT  A

hgvs2vcf:
  NC_000017.11:31227246
    REF  GGCACTGCTG AGGC
    ALT  G
```

### `NF1:c.7319_7321delCAG` — coding_del

**Variant としては同一。** 左寄せの違い — hgvs2vcf は VCF 規約どおり 2 塩基左に寄せ、Variant Recoder は HGVS の 3′ シフト位置のまま。

```
Variant Recoder:
  NC_000017.11:31349248
    REF  GCAG
    ALT  G

hgvs2vcf:
  NC_000017.11:31349246
    REF  TAGC
    ALT  T
```

### `NM_000251:c.1369del` — coding_del

**Variant としては同一。** 左寄せの違い — hgvs2vcf は VCF 規約どおり 1 塩基左に寄せ、Variant Recoder は HGVS の 3′ シフト位置のまま。

```
Variant Recoder:
  NC_000002.12:47445639
    REF  AA
    ALT  A

hgvs2vcf:
  NC_000002.12:47445638
    REF  CA
    ALT  C
```

### `NM_000252:c.1088_1089del` — coding_del

**Variant としては同一。** 左寄せの違い — hgvs2vcf は VCF 規約どおり 1 塩基左に寄せ、Variant Recoder は HGVS の 3′ シフト位置のまま。

```
Variant Recoder:
  NC_000023.11:150657854
    REF  AAA
    ALT  A

hgvs2vcf:
  NC_000023.11:150657853
    REF  CAA
    ALT  C
```

### `NM_000548:c.3270del` — coding_del

**Variant としては同一。** 左寄せの違い — hgvs2vcf は VCF 規約どおり 1 塩基左に寄せ、Variant Recoder は HGVS の 3′ シフト位置のまま。

```
Variant Recoder:
  NC_000016.10:2079413
    REF  CC
    ALT  C

hgvs2vcf:
  NC_000016.10:2079412
    REF  TC
    ALT  T
```

### `NM_001018115:c.2794del` — coding_del

**Variant としては同一。** 左寄せの違い — hgvs2vcf は VCF 規約どおり 1 塩基左に寄せ、Variant Recoder は HGVS の 3′ シフト位置のまま。

```
Variant Recoder:
  NC_000003.12:10074607
    REF  GG
    ALT  G

hgvs2vcf:
  NC_000003.12:10074606
    REF  AG
    ALT  A
```

### `NM_001130438:c.4458del` — coding_del

**Variant としては同一。** 左寄せの違い — hgvs2vcf は VCF 規約どおり 5 塩基左に寄せ、Variant Recoder は HGVS の 3′ シフト位置のまま。

```
Variant Recoder:
  NC_000009.12:128608242
    REF  AA
    ALT  A

hgvs2vcf:
  NC_000009.12:128608237
    REF  CA
    ALT  C
```

### `NM_014049:c.504del` — coding_del

**Variant としては同一。** 左寄せの違い — hgvs2vcf は VCF 規約どおり 2 塩基左に寄せ、Variant Recoder は HGVS の 3′ シフト位置のまま。

```
Variant Recoder:
  NC_000003.12:128896485
    REF  AA
    ALT  A

hgvs2vcf:
  NC_000003.12:128896483
    REF  TA
    ALT  T
```

### `NM_030632:c.1191_1192del` — coding_del

**Variant としては同一。** 左寄せの違い — hgvs2vcf は VCF 規約どおり 1 塩基左に寄せ、Variant Recoder は HGVS の 3′ シフト位置のまま。

```
Variant Recoder:
  NC_000018.10:33738594
    REF  AGA
    ALT  A

hgvs2vcf:
  NC_000018.10:33738593
    REF  CAG
    ALT  C
```

### `NM_030973:c.1438del` — coding_del

**Variant としては同一。** 左寄せの違い — hgvs2vcf は VCF 規約どおり 1 塩基左に寄せ、Variant Recoder は HGVS の 3′ シフト位置のまま。

```
Variant Recoder:
  NC_000019.10:49832370
    REF  CC
    ALT  C

hgvs2vcf:
  NC_000019.10:49832369
    REF  AC
    ALT  A
```

### `NM_198576:c.1668del` — coding_del

**Variant としては同一。** 左寄せの違い — hgvs2vcf は VCF 規約どおり 3 塩基左に寄せ、Variant Recoder は HGVS の 3′ シフト位置のまま。

```
Variant Recoder:
  NC_000001.11:1043601
    REF  CC
    ALT  C

hgvs2vcf:
  NC_000001.11:1043598
    REF  GC
    ALT  G
```

### `SERPINB8:c.947del` — coding_del

**Variant としては同一。** 左寄せの違い — hgvs2vcf は VCF 規約どおり 1 塩基左に寄せ、Variant Recoder は HGVS の 3′ シフト位置のまま。

```
Variant Recoder:
  NC_000018.10:63987099
    REF  AA
    ALT  A

hgvs2vcf:
  NC_000018.10:63987098
    REF  CA
    ALT  C
```

### `SZT2:c.841del` — coding_del

**Variant としては同一。** 左寄せの違い — hgvs2vcf は VCF 規約どおり 1 塩基左に寄せ、Variant Recoder は HGVS の 3′ シフト位置のまま。

```
Variant Recoder:
  NC_000001.11:43416602
    REF  CC
    ALT  C

hgvs2vcf:
  NC_000001.11:43416601
    REF  AC
    ALT  A
```

### `TSC2:c.3294del` — coding_del

**Variant としては同一。** 左寄せの違い — hgvs2vcf は VCF 規約どおり 3 塩基左に寄せ、Variant Recoder は HGVS の 3′ シフト位置のまま。

```
Variant Recoder:
  NC_000016.10:2079565
    REF  CC
    ALT  C

hgvs2vcf:
  NC_000016.10:2079562
    REF  GC
    ALT  G
```

### `VCL:c.176_177del` — coding_del

**Variant としては同一。** 左寄せの違い — hgvs2vcf は VCF 規約どおり 2 塩基左に寄せ、Variant Recoder は HGVS の 3′ シフト位置のまま。

```
Variant Recoder:
  NC_000010.11:74043089
    REF  AAA
    ALT  A

hgvs2vcf:
  NC_000010.11:74043087
    REF  GAA
    ALT  G
```

### `WNT1:c.1060del` — coding_del

**Variant としては同一。** 左寄せの違い — hgvs2vcf は VCF 規約どおり 1 塩基左に寄せ、Variant Recoder は HGVS の 3′ シフト位置のまま。

```
Variant Recoder:
  NC_000012.12:48981586
    REF  CC
    ALT  C

hgvs2vcf:
  NC_000012.12:48981585
    REF  GC
    ALT  G
```

### `ACTN2:c.1167_1169delinsA` — coding_delins

**Variant としては同一。** アンカー塩基のトリミング差 — Variant Recoder は REF/ALT 共通の先頭 1 塩基を残し、hgvs2vcf は削っている。

```
Variant Recoder:
  NC_000001.11:236742954
    REF  TGCT
    ALT  TA

hgvs2vcf:
  NC_000001.11:236742955
    REF  GCT
    ALT  A
```

### `COL6A1:c.206_214delinsCCT` — coding_delins

**Variant としては同一。** アンカー塩基のトリミング差 — Variant Recoder は REF/ALT 共通の先頭 1 塩基を残し、hgvs2vcf は削っている。

```
Variant Recoder:
  NC_000021.9:45982741
    REF  TTCATCGACA
    ALT  TCCT

hgvs2vcf:
  NC_000021.9:45982742
    REF  TCATCGACA
    ALT  CCT
```

### `DRD4:c.810_824delinsA` — coding_delins

**Variant としては同一。** アンカー塩基のトリミング差 — Variant Recoder は REF/ALT 共通の先頭 1 塩基を残し、hgvs2vcf は削っている。

```
Variant Recoder:
  NC_000011.10:640058
    REF  CCCGGGGTCC CTGCGG
    ALT  CA

hgvs2vcf:
  NC_000011.10:640059
    REF  CCGGGGTCCC TGCGG
    ALT  A
```

### `HNF1A:c.864delinsCC` — coding_delins

**Variant としては同一。** アンカー塩基のトリミング差 — Variant Recoder は REF/ALT 共通の先頭 1 塩基を残し、hgvs2vcf は削っている。

```
Variant Recoder:
  NC_000012.12:120994313
    REF  GG
    ALT  GCC

hgvs2vcf:
  NC_000012.12:120994314
    REF  G
    ALT  CC
```

### `KRT1:c.1609_1610delinsA` — coding_delins

**Variant としては同一。** アンカー塩基のトリミング差 — Variant Recoder は REF/ALT 共通の先頭 1 塩基を残し、hgvs2vcf は削っている。

```
Variant Recoder:
  NC_000012.12:52675517
    REF  ACC
    ALT  AT

hgvs2vcf:
  NC_000012.12:52675518
    REF  CC
    ALT  T
```

### `MTTP:c.2299_2300delinsA` — coding_delins

**Variant としては同一。** アンカー塩基のトリミング差 — Variant Recoder は REF/ALT 共通の先頭 1 塩基を残し、hgvs2vcf は削っている。

```
Variant Recoder:
  NC_000004.12:99619054
    REF  GTT
    ALT  GA

hgvs2vcf:
  NC_000004.12:99619055
    REF  TT
    ALT  A
```

### `NM_000049:c.241_242delinsT` — coding_delins

**Variant としては同一。** アンカー塩基のトリミング差 — Variant Recoder は REF/ALT 共通の先頭 1 塩基を残し、hgvs2vcf は削っている。

```
Variant Recoder:
  NC_000017.11:3481606
    REF  AAA
    ALT  AT

hgvs2vcf:
  NC_000017.11:3481607
    REF  AA
    ALT  T
```

### `NM_000435:c.4476_4487delinsTGGGC` — coding_delins

**Variant としては同一。** アンカー塩基のトリミング差 — Variant Recoder は REF/ALT 共通の先頭 1 塩基を残し、hgvs2vcf は削っている。

```
Variant Recoder:
  NC_000019.10:15174316
    REF  ATCCCAGCCG CAC
    ALT  AGCCCA

hgvs2vcf:
  NC_000019.10:15174317
    REF  TCCCAGCCGC AC
    ALT  GCCCA
```

### `NM_000441:c.735_739delinsTGTTTCA` — coding_delins

**Variant としては同一。** アンカー塩基のトリミング差 — Variant Recoder は REF/ALT 共通の先頭 1 塩基を残し、hgvs2vcf は削っている。

```
Variant Recoder:
  NC_000007.14:107675078
    REF  AAAACT
    ALT  ATGTTTCA

hgvs2vcf:
  NC_000007.14:107675079
    REF  AAACT
    ALT  TGTTTCA
```

### `NM_007294:c.5534_5539delinsGTCCTGCTGTCCTGGCACTG` — coding_delins

**Variant としては同一。** アンカー塩基のトリミング差 — Variant Recoder は REF/ALT 共通の先頭 1 塩基を残し、hgvs2vcf は削っている。

```
Variant Recoder:
  NC_000017.11:43045730
    REF  CACTGGT
    ALT  CCAGTGCCAG GACAGCAGGA C

hgvs2vcf:
  NC_000017.11:43045731
    REF  ACTGGT
    ALT  CAGTGCCAGG ACAGCAGGAC
```

### `NM_020989:c.411_417delinsTCGTAGACGGGGCAATACCCTCGTAGACGGGCAATACCTCGTAGACGGGGCAATACCCTCGTAGA` — coding_delins

**Variant としては同一。** アンカー塩基のトリミング差 — Variant Recoder は REF/ALT 共通の先頭 1 塩基を残し、hgvs2vcf は削っている。

```
Variant Recoder:
  NC_000002.12:208128310
    REF  GGTAGTTG
    ALT  GTCTACGAGG GTATTGCCCC GTCTACGAGG TATTGCCCGT CTACGAGGGT ATTGCCCCGT
         CTACGA

hgvs2vcf:
  NC_000002.12:208128311
    REF  GTAGTTG
    ALT  TCTACGAGGG TATTGCCCCG TCTACGAGGT ATTGCCCGTC TACGAGGGTA TTGCCCCGTC
         TACGA
```

### `TFR2:c.754_763delinsGCGTAC` — coding_delins

**Variant としては同一。** アンカー塩基のトリミング差 — Variant Recoder は REF/ALT 共通の先頭 1 塩基を残し、hgvs2vcf は削っている。

```
Variant Recoder:
  NC_000007.14:100633086
    REF  TCTTCGGGCC G
    ALT  TGTACGC

hgvs2vcf:
  NC_000007.14:100633087
    REF  CTTCGGGCCG
    ALT  GTACGC
```

### `APC:c.518dup` — coding_dup

**Variant としては同一。** 左寄せの違い — hgvs2vcf は VCF 規約どおり 1 塩基左に寄せ、Variant Recoder は HGVS の 3′ シフト位置のまま。

```
Variant Recoder:
  NC_000005.10:112775723
    REF  C
    ALT  CC

hgvs2vcf:
  NC_000005.10:112775722
    REF  T
    ALT  TC
```

### `BAP1:c.1508dup` — coding_dup

**Variant としては同一。** 左寄せの違い — hgvs2vcf は VCF 規約どおり 1 塩基左に寄せ、Variant Recoder は HGVS の 3′ シフト位置のまま。

```
Variant Recoder:
  NC_000003.12:52403637
    REF  A
    ALT  AA

hgvs2vcf:
  NC_000003.12:52403636
    REF  G
    ALT  GA
```

### `BRCA1:c.4754dup` — coding_dup

**Variant としては同一。** 左寄せの違い — hgvs2vcf は VCF 規約どおり 1 塩基左に寄せ、Variant Recoder は HGVS の 3′ シフト位置のまま。

```
Variant Recoder:
  NC_000017.11:43071160
    REF  G
    ALT  GG

hgvs2vcf:
  NC_000017.11:43071159
    REF  T
    ALT  TG
```

### `CDSN:c.164_167dup` — coding_dup

**Variant としては同一。** 左寄せの違い — hgvs2vcf は VCF 規約どおり 4 塩基左に寄せ、Variant Recoder は HGVS の 3′ シフト位置のまま。

```
Variant Recoder:
  NC_000006.12:31117451
    REF  C
    ALT  CAGGC

hgvs2vcf:
  NC_000006.12:31117447
    REF  G
    ALT  GAGGC
```

### `CFAP410:c.689_722dup` — coding_dup

**Variant としては同一。** 左寄せの違い — hgvs2vcf は VCF 規約どおり 34 塩基左に寄せ、Variant Recoder は HGVS の 3′ シフト位置のまま。

```
Variant Recoder:
  NC_000021.9:44330280
    REF  T
    ALT  TCTGCCCACA GTCTGCTGCA CGGCCTCCAG CCCCT

hgvs2vcf:
  NC_000021.9:44330246
    REF  G
    ALT  GCTGCCCACA GTCTGCTGCA CGGCCTCCAG CCCCT
```

### `DNAH5:c.1988dup` — coding_dup

**Variant としては同一。** 左寄せの違い — hgvs2vcf は VCF 規約どおり 1 塩基左に寄せ、Variant Recoder は HGVS の 3′ シフト位置のまま。

```
Variant Recoder:
  NC_000005.10:13901316
    REF  T
    ALT  TT

hgvs2vcf:
  NC_000005.10:13901315
    REF  G
    ALT  GT
```

### `DOCK6:c.2520dup` — coding_dup

**Variant としては同一。** 左寄せの違い — hgvs2vcf は VCF 規約どおり 1 塩基左に寄せ、Variant Recoder は HGVS の 3′ シフト位置のまま。

```
Variant Recoder:
  NC_000019.10:11235632
    REF  A
    ALT  AA

hgvs2vcf:
  NC_000019.10:11235631
    REF  G
    ALT  GA
```

### `EYA1:c.1381_1387dup` — coding_dup

**Variant としては同一。** 左寄せの違い — hgvs2vcf は VCF 規約どおり 7 塩基左に寄せ、Variant Recoder は HGVS の 3′ シフト位置のまま。

```
Variant Recoder:
  NC_000008.11:71215708
    REF  T
    ALT  TCTTCCCT

hgvs2vcf:
  NC_000008.11:71215701
    REF  G
    ALT  GCTTCCCT
```

### `IRF7:c.1024_1028dup` — coding_dup

**Variant としては同一。** 左寄せの違い — hgvs2vcf は VCF 規約どおり 5 塩基左に寄せ、Variant Recoder は HGVS の 3′ シフト位置のまま。

```
Variant Recoder:
  NC_000011.10:613419
    REF  G
    ALT  GAGCTG

hgvs2vcf:
  NC_000011.10:613414
    REF  C
    ALT  CAGCTG
```

### `KAT6A:c.4968_4982dup` — coding_dup

**Variant としては同一。** 左寄せの違い — hgvs2vcf は VCF 規約どおり 15 塩基左に寄せ、Variant Recoder は HGVS の 3′ シフト位置のまま。

```
Variant Recoder:
  NC_000008.11:41933252
    REF  T
    ALT  TGGCTGTGGC TGCTGT

hgvs2vcf:
  NC_000008.11:41933237
    REF  C
    ALT  CGGCTGTGGC TGCTGT
```

### `LYST:c.8425dup` — coding_dup

**Variant としては同一。** 左寄せの違い — hgvs2vcf は VCF 規約どおり 1 塩基左に寄せ、Variant Recoder は HGVS の 3′ シフト位置のまま。

```
Variant Recoder:
  NC_000001.11:235734593
    REF  C
    ALT  CC

hgvs2vcf:
  NC_000001.11:235734592
    REF  T
    ALT  TC
```

### `MYO5B:c.3163_3165dup` — coding_dup

**Variant としては同一。** 左寄せの違い — hgvs2vcf は VCF 規約どおり 3 塩基左に寄せ、Variant Recoder は HGVS の 3′ シフト位置のまま。

```
Variant Recoder:
  NC_000018.10:49879058
    REF  G
    ALT  GGAG

hgvs2vcf:
  NC_000018.10:49879055
    REF  T
    ALT  TGAG
```

### `MYORG:c.337_348dup` — coding_dup

**Variant としては同一。** 左寄せの違い — hgvs2vcf は VCF 規約どおり 12 塩基左に寄せ、Variant Recoder は HGVS の 3′ シフト位置のまま。

```
Variant Recoder:
  NC_000009.12:34372607
    REF  G
    ALT  GGCGGAAGGC CAG

hgvs2vcf:
  NC_000009.12:34372595
    REF  A
    ALT  AGCGGAAGGC CAG
```

### `NEBL:c.2497dup` — coding_dup

**Variant としては同一。** 左寄せの違い — hgvs2vcf は VCF 規約どおり 1 塩基左に寄せ、Variant Recoder は HGVS の 3′ シフト位置のまま。

```
Variant Recoder:
  NC_000010.11:20812790
    REF  T
    ALT  TT

hgvs2vcf:
  NC_000010.11:20812789
    REF  C
    ALT  CT
```

### `NM_000176:c.1248dup` — coding_dup

**Variant としては同一。** 左寄せの違い — hgvs2vcf は VCF 規約どおり 1 塩基左に寄せ、Variant Recoder は HGVS の 3′ シフト位置のまま。

```
Variant Recoder:
  NC_000005.10:143314105
    REF  T
    ALT  TT

hgvs2vcf:
  NC_000005.10:143314104
    REF  G
    ALT  GT
```

### `NM_000321:c.19dup` — coding_dup

**Variant としては同一。** 左寄せの違い — hgvs2vcf は VCF 規約どおり 5 塩基左に寄せ、Variant Recoder は HGVS の 3′ シフト位置のまま。

```
Variant Recoder:
  NC_000013.11:48303930
    REF  C
    ALT  CC

hgvs2vcf:
  NC_000013.11:48303925
    REF  A
    ALT  AC
```

### `NM_000368:c.2239dup` — coding_dup

**Variant としては同一。** 左寄せの違い — hgvs2vcf は VCF 規約どおり 1 塩基左に寄せ、Variant Recoder は HGVS の 3′ シフト位置のまま。

```
Variant Recoder:
  NC_000009.12:132902757
    REF  T
    ALT  TT

hgvs2vcf:
  NC_000009.12:132902756
    REF  A
    ALT  AT
```

### `NM_000494:c.2723dup` — coding_dup

**Variant としては同一。** 左寄せの違い — hgvs2vcf は VCF 規約どおり 1 塩基左に寄せ、Variant Recoder は HGVS の 3′ シフト位置のまま。

```
Variant Recoder:
  NC_000010.11:104040389
    REF  G
    ALT  GG

hgvs2vcf:
  NC_000010.11:104040388
    REF  T
    ALT  TG
```

### `NM_000518:c.287dupA` — coding_dup

**Variant としては同一。** 左寄せの違い — hgvs2vcf は VCF 規約どおり 1 塩基左に寄せ、Variant Recoder は HGVS の 3′ シフト位置のまま。

```
Variant Recoder:
  NC_000011.10:5226605
    REF  T
    ALT  TT

hgvs2vcf:
  NC_000011.10:5226604
    REF  C
    ALT  CT
```

### `NM_000528:c.89dup` — coding_dup

**Variant としては同一。** 左寄せの違い — hgvs2vcf は VCF 規約どおり 1 塩基左に寄せ、Variant Recoder は HGVS の 3′ シフト位置のまま。

```
Variant Recoder:
  NC_000019.10:12666613
    REF  G
    ALT  GG

hgvs2vcf:
  NC_000019.10:12666612
    REF  T
    ALT  TG
```

### `NM_000665:c.11dup` — coding_dup

**Variant としては同一。** 左寄せの違い — hgvs2vcf は VCF 規約どおり 1 塩基左に寄せ、Variant Recoder は HGVS の 3′ シフト位置のまま。

```
Variant Recoder:
  NC_000007.14:100894222
    REF  G
    ALT  GG

hgvs2vcf:
  NC_000007.14:100894221
    REF  C
    ALT  CG
```

### `NM_001127222:c.3925dup` — coding_dup

**Variant としては同一。** 左寄せの違い — hgvs2vcf は VCF 規約どおり 1 塩基左に寄せ、Variant Recoder は HGVS の 3′ シフト位置のまま。

```
Variant Recoder:
  NC_000019.10:13275914
    REF  G
    ALT  GG

hgvs2vcf:
  NC_000019.10:13275913
    REF  C
    ALT  CG
```

### `NM_001135998:c.196_197dup` — coding_dup

**Variant としては同一。** 左寄せの違い — hgvs2vcf は VCF 規約どおり 2 塩基左に寄せ、Variant Recoder は HGVS の 3′ シフト位置のまま。

```
Variant Recoder:
  NC_000023.11:47144484
    REF  A
    ALT  AAA

hgvs2vcf:
  NC_000023.11:47144482
    REF  C
    ALT  CAA
```

### `NM_001200:c.231dup` — coding_dup

**Variant としては同一。** 左寄せの違い — hgvs2vcf は VCF 規約どおり 5 塩基左に寄せ、Variant Recoder は HGVS の 3′ シフト位置のまま。

```
Variant Recoder:
  NC_000020.11:6770356
    REF  C
    ALT  CC

hgvs2vcf:
  NC_000020.11:6770351
    REF  G
    ALT  GC
```

### `NM_001291415:c.1552_1555dup` — coding_dup

**Variant としては同一。** 左寄せの違い — hgvs2vcf は VCF 規約どおり 4 塩基左に寄せ、Variant Recoder は HGVS の 3′ シフト位置のまま。

```
Variant Recoder:
  NC_000023.11:45061389
    REF  T
    ALT  TTCAT

hgvs2vcf:
  NC_000023.11:45061385
    REF  C
    ALT  CTCAT
```

### `NM_001367624:c.10332dup` — coding_dup

**Variant としては同一。** 左寄せの違い — hgvs2vcf は VCF 規約どおり 7 塩基左に寄せ、Variant Recoder は HGVS の 3′ シフト位置のまま。

```
Variant Recoder:
  NC_000016.10:88437801
    REF  G
    ALT  GG

hgvs2vcf:
  NC_000016.10:88437794
    REF  A
    ALT  AG
```

### `NM_001372044:c.3069_3076dup` — coding_dup

**別の変異。** 参照配列に適用した結果が一致しない。

```
Variant Recoder:
  NC_000022.11:50720715
    REF  A
    ALT  AGGACGCGC

hgvs2vcf:
  NC_000022.11:50720670
    REF  A
    ALT  AGCCGCAGC
```

### `NM_001386298:c.7436_7450dup` — coding_dup

**Variant としては同一。** 左寄せの違い — hgvs2vcf は VCF 規約どおり 1 塩基左に寄せ、Variant Recoder は HGVS の 3′ シフト位置のまま。

```
Variant Recoder:
  NC_000019.10:42295072
    REF  C
    ALT  CAGGCTGCCC CGCCAC

hgvs2vcf:
  NC_000019.10:42295071
    REF  C
    ALT  CCAGGCTGCC CCGCCA
```

### `NM_003924:c.735_767dup` — coding_dup

**Variant としては同一。** 左寄せの違い — hgvs2vcf は VCF 規約どおり 33 塩基左に寄せ、Variant Recoder は HGVS の 3′ シフト位置のまま。

```
Variant Recoder:
  NC_000004.12:41746017
    REF  C
    ALT  CGCCGCTGCC GCCGCCGCCG CTGCCGCGGC CGCC

hgvs2vcf:
  NC_000004.12:41745984
    REF  T
    ALT  TGCCGCTGCC GCCGCCGCCG CTGCCGCGGC CGCC
```

### `NM_013275:c.6552_6558dup` — coding_dup

**Variant としては同一。** 左寄せの違い — hgvs2vcf は VCF 規約どおり 7 塩基左に寄せ、Variant Recoder は HGVS の 3′ シフト位置のまま。

```
Variant Recoder:
  NC_000016.10:89279990
    REF  A
    ALT  ACTCCTCA

hgvs2vcf:
  NC_000016.10:89279983
    REF  G
    ALT  GCTCCTCA
```

### `NM_015272:c.1158dup` — coding_dup

**Variant としては同一。** 左寄せの違い — hgvs2vcf は VCF 規約どおり 1 塩基左に寄せ、Variant Recoder は HGVS の 3′ シフト位置のまま。

```
Variant Recoder:
  NC_000016.10:53664955
    REF  T
    ALT  TT

hgvs2vcf:
  NC_000016.10:53664954
    REF  C
    ALT  CT
```

### `NM_015909:c.2817dup` — coding_dup

**Variant としては同一。** 左寄せの違い — hgvs2vcf は VCF 規約どおり 1 塩基左に寄せ、Variant Recoder は HGVS の 3′ シフト位置のまま。

```
Variant Recoder:
  NC_000002.12:15415666
    REF  A
    ALT  AA

hgvs2vcf:
  NC_000002.12:15415665
    REF  G
    ALT  GA
```

### `NM_182931:c.4829dup` — coding_dup

**Variant としては同一。** 左寄せの違い — hgvs2vcf は VCF 規約どおり 5 塩基左に寄せ、Variant Recoder は HGVS の 3′ シフト位置のまま。

```
Variant Recoder:
  NC_000007.14:105112584
    REF  T
    ALT  TT

hgvs2vcf:
  NC_000007.14:105112579
    REF  A
    ALT  AT
```

### `NOTCH3:c.1561_1569dup` — coding_dup

**Variant としては同一。** 左寄せの違い — hgvs2vcf は VCF 規約どおり 9 塩基左に寄せ、Variant Recoder は HGVS の 3′ シフト位置のまま。

```
Variant Recoder:
  NC_000019.10:15187926
    REF  T
    ALT  TCACGCATTT

hgvs2vcf:
  NC_000019.10:15187917
    REF  C
    ALT  CCACGCATTT
```

### `PADI6:c.441dupA` — coding_dup

**Variant としては同一。** 左寄せの違い — hgvs2vcf は VCF 規約どおり 5 塩基左に寄せ、Variant Recoder は HGVS の 3′ シフト位置のまま。

```
Variant Recoder:
  NC_000001.11:17381051
    REF  A
    ALT  AA

hgvs2vcf:
  NC_000001.11:17381046
    REF  G
    ALT  GA
```

### `PKP2:c.604dup` — coding_dup

**Variant としては同一。** 左寄せの違い — hgvs2vcf は VCF 規約どおり 1 塩基左に寄せ、Variant Recoder は HGVS の 3′ シフト位置のまま。

```
Variant Recoder:
  NC_000012.12:32878276
    REF  C
    ALT  CC

hgvs2vcf:
  NC_000012.12:32878275
    REF  A
    ALT  AC
```

### `POT1:c.161dup` — coding_dup

**Variant としては同一。** 左寄せの違い — hgvs2vcf は VCF 規約どおり 1 塩基左に寄せ、Variant Recoder は HGVS の 3′ シフト位置のまま。

```
Variant Recoder:
  NC_000007.14:124871005
    REF  T
    ALT  TT

hgvs2vcf:
  NC_000007.14:124871004
    REF  A
    ALT  AT
```

### `RAX2:c.337dup` — coding_dup

**Variant としては同一。** 左寄せの違い — hgvs2vcf は VCF 規約どおり 1 塩基左に寄せ、Variant Recoder は HGVS の 3′ シフト位置のまま。

```
Variant Recoder:
  NC_000019.10:3770839
    REF  C
    ALT  CC

hgvs2vcf:
  NC_000019.10:3770838
    REF  G
    ALT  GC
```

### `RPGR:c.2819_2838dup` — coding_dup

**Variant としては同一。** 左寄せの違い — hgvs2vcf は VCF 規約どおり 20 塩基左に寄せ、Variant Recoder は HGVS の 3′ シフト位置のまま。

```
Variant Recoder:
  NC_000023.11:38286180
    REF  T
    ALT  TCCCTTCTCC ATCCTCCCCT T

hgvs2vcf:
  NC_000023.11:38286160
    REF  C
    ALT  CCCCTTCTCC ATCCTCCCCT T
```

### `SPTAN1:c.6923_6928dup` — coding_dup

**Variant としては同一。** 左寄せの違い — hgvs2vcf は VCF 規約どおり 6 塩基左に寄せ、Variant Recoder は HGVS の 3′ シフト位置のまま。

```
Variant Recoder:
  NC_000009.12:128632286
    REF  C
    ALT  CGCATGC

hgvs2vcf:
  NC_000009.12:128632280
    REF  G
    ALT  GGCATGC
```

### `WNT10A:c.495_502dup` — coding_dup

**Variant としては同一。** 左寄せの違い — hgvs2vcf は VCF 規約どおり 5 塩基左に寄せ、Variant Recoder は HGVS の 3′ シフト位置のまま。

```
Variant Recoder:
  NC_000002.12:218890101
    REF  G
    ALT  GGGACGAGG

hgvs2vcf:
  NC_000002.12:218890096
    REF  G
    ALT  GCGAGGGGA
```

### `ALG13:c.2797_2798insGAC` — coding_ins

**Variant としては同一。** 左寄せの違い — hgvs2vcf は VCF 規約どおり 2 塩基左に寄せ、Variant Recoder は HGVS の 3′ シフト位置のまま。

```
Variant Recoder:
  NC_000023.11:111744769
    REF  C
    ALT  CGAC

hgvs2vcf:
  NC_000023.11:111744767
    REF  C
    ALT  CACG
```

### `NM_002458:c.14609_14610insCCCAGGGACCACCTGGATCCTCACAGAGTCGAGCACTACAGCCACCGTGACGGTGCCCACCAGCTCCACGGCCACCGCCTCCTCCAC` — coding_ins

**Variant としては同一。** 左寄せの違い — hgvs2vcf は VCF 規約どおり 23 塩基左に寄せ、Variant Recoder は HGVS の 3′ シフト位置のまま。

```
Variant Recoder:
  NC_000011.10:1251489
    REF  C
    ALT  CCCCAGGGAC CACCTGGATC CTCACAGAGT CGAGCACTAC AGCCACCGTG ACGGTGCCCA
         CCAGCTCCAC GGCCACCGCC TCCTCCAC

hgvs2vcf:
  NC_000011.10:1251466
    REF  T
    ALT  TTCCACGGCC ACCGCCTCCT CCACCCCAGG GACCACCTGG ATCCTCACAG AGTCGAGCAC
         TACAGCCACC GTGACGGTGC CCACCAGC
```

### `APH1A:c.609_610-2del` — intronic_del

**Variant としては同一。** 左寄せの違い — hgvs2vcf は VCF 規約どおり 1 塩基左に寄せ、Variant Recoder は HGVS の 3′ シフト位置のまま。

```
Variant Recoder:
  NC_000001.11:150266657
    REF  CTAGGAAGGA GGGTAAGAGT AGGAAAGAGA TTAGATTCTC CCTCGACCTA ATCCCCATAT
         TCTCTCTGTA CCTTTCTGAC TCCCAGATAT CTCTCTCAAA TTCTCCAGTC TTTCCCTTCA
         GAGCACCAAC ATCTTGTGGT TAAGGGGACT TTTGATTTTC AGCTCCTCAG AAACTCAAAG
         GTTTCTGCCG CTCCTGCTCA CCTCAGGCCC TCTGCATTAC AGTTTGACTA ATCCTTTCAA
         CCTCCTCCCC AGAGCAGGTG ATAGAAATGA TGCTGAGGTG AGAGACCTTG AAAGACTCAC
         CTTTCCTCCT CCTCCCAGGT AAGTTAAAAA TGTTAAGAAG TGAGGATACC CTTTCCCCCA
         CATCCCACTC ACCATTAAAT GCTTTTCTCC CTAACTCAGG CCCCTGTCTC CAACTCACC
    ALT  C

hgvs2vcf:
  NC_000001.11:150266656
    REF  TCTAGGAAGG AGGGTAAGAG TAGGAAAGAG ATTAGATTCT CCCTCGACCT AATCCCCATA
         TTCTCTCTGT ACCTTTCTGA CTCCCAGATA TCTCTCTCAA ATTCTCCAGT CTTTCCCTTC
         AGAGCACCAA CATCTTGTGG TTAAGGGGAC TTTTGATTTT CAGCTCCTCA GAAACTCAAA
         GGTTTCTGCC GCTCCTGCTC ACCTCAGGCC CTCTGCATTA CAGTTTGACT AATCCTTTCA
         ACCTCCTCCC CAGAGCAGGT GATAGAAATG ATGCTGAGGT GAGAGACCTT GAAAGACTCA
         CCTTTCCTCC TCCTCCCAGG TAAGTTAAAA ATGTTAAGAA GTGAGGATAC CCTTTCCCCC
         ACATCCCACT CACCATTAAA TGCTTTTCTC CCTAACTCAG GCCCCTGTCT CCAACTCAC
    ALT  T
```

### `BAP1:c.2053_2056+10del` — intronic_del

**Variant としては同一。** 左寄せの違い — hgvs2vcf は VCF 規約どおり 1 塩基左に寄せ、Variant Recoder は HGVS の 3′ シフト位置のまま。

```
Variant Recoder:
  NC_000003.12:52402591
    REF  CATCCCCTCA CCTTC
    ALT  C

hgvs2vcf:
  NC_000003.12:52402590
    REF  GCATCCCCTC ACCTT
    ALT  G
```

### `KCNT1:c.675+17_676-22del` — intronic_del

**Variant としては同一。** 左寄せの違い — hgvs2vcf は VCF 規約どおり 10 塩基左に寄せ、Variant Recoder は HGVS の 3′ シフト位置のまま。

```
Variant Recoder:
  NC_000009.12:135757246
    REF  CTGCCAGGAG TGCGGGCCCT GGAGCCCCAG C
    ALT  C

hgvs2vcf:
  NC_000009.12:135757236
    REF  TGAGCCCCAG CTGCCAGGAG TGCGGGCCCT G
    ALT  T
```

### `NF1:c.2851-21_2851-17del` — intronic_del

**Variant としては同一。** 左寄せの違い — hgvs2vcf は VCF 規約どおり 2 塩基左に寄せ、Variant Recoder は HGVS の 3′ シフト位置のまま。

```
Variant Recoder:
  NC_000017.11:31229813
    REF  AATGTA
    ALT  A

hgvs2vcf:
  NC_000017.11:31229811
    REF  TTAATG
    ALT  T
```

### `NM_000338:c.2485+15del` — intronic_del

**Variant としては同一。** 左寄せの違い — hgvs2vcf は VCF 規約どおり 2 塩基左に寄せ、Variant Recoder は HGVS の 3′ シフト位置のまま。

```
Variant Recoder:
  NC_000015.10:48274667
    REF  TT
    ALT  T

hgvs2vcf:
  NC_000015.10:48274665
    REF  CT
    ALT  C
```

### `NM_000501:c.470-37_470del` — intronic_del

**Variant としては同一。** 左寄せの違い — hgvs2vcf は VCF 規約どおり 3 塩基左に寄せ、Variant Recoder は HGVS の 3′ シフト位置のまま。

```
Variant Recoder:
  NC_000007.14:74045184
    REF  GCCTGCCTTC CTACACTCAC TGCTTTGTCC CCCGGCAGG
    ALT  G

hgvs2vcf:
  NC_000007.14:74045181
    REF  AAGGCCTGCC TTCCTACACT CACTGCTTTG TCCCCCGGC
    ALT  A
```

### `NM_001023570:c.1279-15del` — intronic_del

**Variant としては同一。** 左寄せの違い — hgvs2vcf は VCF 規約どおり 7 塩基左に寄せ、Variant Recoder は HGVS の 3′ シフト位置のまま。

```
Variant Recoder:
  NC_000003.12:121781888
    REF  AA
    ALT  A

hgvs2vcf:
  NC_000003.12:121781881
    REF  GA
    ALT  G
```

### `NM_001271:c.62+18_62+21del` — intronic_del

**Variant としては同一。** 左寄せの違い — hgvs2vcf は VCF 規約どおり 3 塩基左に寄せ、Variant Recoder は HGVS の 3′ シフト位置のまま。

```
Variant Recoder:
  NC_000015.10:92901316
    REF  TTCTT
    ALT  T

hgvs2vcf:
  NC_000015.10:92901313
    REF  ACTTT
    ALT  A
```

### `NM_004211:c.1436_1737+314del` — intronic_del

**Variant としては同一。** 左寄せの違い — hgvs2vcf は VCF 規約どおり 2 塩基左に寄せ、Variant Recoder は HGVS の 3′ シフト位置のまま。

```
Variant Recoder:
  NC_000011.10:20628019
    REF  TCTGCTGCAT GGGGAGGCCT GATCACTCTC TCTTCTTACA ACAAATTCCA CAACAACTGC
         TACAGGTATG TAGAGGTACT ACAAGATCTG GGCATAGCTG GTGAGTGGGA CAGAAGAATG
         GACTGAGTTA TCAGACACCT GAGGCCACAT CCTCACATTT CATCTTAGGG AGAGCTAAAG
         ATTTGCCTCT GGCCTAGGAG AAACCACCTG CTAAGGCCTA GGCACTATCT TCTGAAGGCC
         TGGACCCTCA CTTACACACC TGGCTCTGAC ACATGGGGGA GGCTCAGTGG CTATTTACAG
         GATGGAAGCA AGTTTGTCTG CAGGTCACTG TGCAGTTGGC TGTGTTCTGT GACAGTCATT
         TGTGAGCTAC CTAGTCTGTG GATACAATGG ACTGTGCCTT CAGATGGTCT TCCCTCTGTG
         TGGGGCTGTG ACCTAATCTC CTCTTCTTAT AAAGACCCCA GTCATATCAG TCACATTGGA
         TCAGGGACCA CTCTAATGAC TTCATTTAAC TTAATTACCT CTTTAAAGGC CCTATCTCCA
         AATACAGTCA CGTTATGAGA TGCTAGTGAT TAGGATGACA AAATATGAAT TTGGTAGTGA
         TAGGGGAGTG GTAGGAAGAC ACAATTCAGT TCAAAATGAC CTTGAGTAAC AGACTATGGT
         ATTTAAACTT CATTAGTCAC AACTGCTCAT TAACCATTGA CCCAAATCAG TCTGAACACC
         ATTAAAGGGT GAAGCATTGC TATCTTCTTT ATTAGAAATG AGGCTGTGGT GTGGCAGAAA
         TAACCCAGGC TGAGAGCTTG AAAATCTAGA TTCATATCCT GGCCCACACT ATTAATTAGT
         CCATTACCTT TCCCTGGGCC TCAGTTTCCT CTTCAGTAAA CTAAGGGGTC AGACAAGGTG
         GATCATTTGC TGCACACTTG CTCTGTGCTA GGCGGTGCAT AGTACAGGTA TCATCTCATT
         CTCTCCTGGC AACAGCCTAT GACAGATAGA CTCATTGCTG CCATTTCAAA TCAGAGTGGA
         AAGGAAGTGG ATTGCTCAAG GTCATGCCAC TAAAAGGCAG GAGAACCAGG ATTTCAGTGT
         AGCCCTGGGT TACAGTGTAG CCCGTCTAGC TGTGACCTCA CATTTGAATC TAGGATGACT
         GAAGGTAGAC TGGGAAACCC TGGCTATCTT ACCAGCAGCA GGCTCTGCGA TGAAGGTAGA
         GACACTGGGC TCTCTTCCCT CCCCTGCCCC TTTGTCCTTC TCAACCCTGT GTGTCCCAAC
         TCCAGGCTAC CCTCACATTT TAGGGTCATT TGACTTTCCC ACTGCCTTCT CTTCCCTCAC
         ACATAGTTCC TGTCCTGGAG CCGACCAAGG CCCCATCTCC TCAATTTCTG TTCTGATGAA
         CAGATTTACC TCTGCCCCTG GAATAATGTC TTAGTTTGTT CAGATTGTCT AACAAAATGC
         CATAGACTGA GTAATATTTT TTCTTTATAC GTTTTTTGCT TTTATTATTT TTAAATGACA
         CATAGTAATT ATGCATATTT ATGGAGTACA GTATGATATT TCGGTACATG TATACAATGT
         GTAATGATCA AATCAGGGTA ATTAGCATAT CTACTACCTC AAACATTTAT CATTTCTTTG
         TGTTGAAAAC ACTGACAGTT CATTCTTCTA GCTGTTTGAA AACATAAAAT AAATTGTTGT
         TAATATAGTC ATCTCATAGT GCTGTAGGAT GATTTTTTTT TTTTTTTTTG AGATGGAGTT
         TCGCTCTTGT TGCCCAGGCT GGAGTGCAAT GGCCAATCTC AGCTCACTGC AACCTCCACC
         TCCCAGGTTC AAGCAATTCA AGTAGCTGGG ATTGCGGGCA TGTGCCACCA TGCCCCGCTA
         ATTTTTTTTT TTGTGTGTGT ATTGGGTAGA CACGGGGTTT CACCATGTTG GTGAGGCTGG
         TCTCGAACTC CTGACCTCAG GTGATCCACC TGCCTTGGCC TCCCAAAGTG CCGGGATTAC
         AGGTATGAGC CACCGTGCCC GGCTGGGATG GTTGTTAATA TAGTCATCCT ATAGTGCTAT
         AGAATACTAG AGTTTATTTC TCCTACCTAG CTATATTTTT GTATCTTTAA CTGACTTTTG
         GCTATAAACA ACAGAAATTT ATTGCTCACT GCTCTAGGGG CTGGGAAGTC CAAGTTCAAG
         GTGCCAGAAT ATTCAGTGTC TGGAGGGCTG CTCTCTGTTT CAAAGATGGC ACCTTGTTGC
         TGTGTCTTCA TATGGTGGAA GAGGCAGACA CATTCCCTTC AGCCTATTTT ATAAGGGCAC
         TAATCCCATG AGTTGGCTCT GTCTTCATGA CTTAATCACT TTTCTAAAGC CTCCACCTCT
         TAATACTATC AAATTGTGGA TTAAGTTTCA GCCAATGAAT TTGAGATGGG GGGATTCAGA
         CCACAGCAGA TGAGTTGAGA CCCATTTATA TAGATCGTGG AGTCAGAGCT TTGGCCCACA
         GGCCCTGAAT CAGGGCTATT AGGGGATATC GTCTGAGCCT TTTGGTGCTT TTTAAGTGAG
         CCCAAGGGAG CCTGTGGTTA GGACATGAAC GTACACGTAT ATGCCTACAC ATGTGCAGAC
         AAACATGTGG GCACACATTT GTGTGTCCTT CCCCTTGTCC CTTTCCACTC ACCAAGCACA
         CCTAATGGAA AACTCTGGTC TCTTCCTTCC AGGGACACTC TAATTGTCAC CTGCACCAAC
         AGTGCCACAA GCATCTTTGC CGGCTTCGTC ATCTTCTCCG TTATCGGCTT CATGGCCAAT
         GAACGCAAAG TCAACATTGA GAATGTGGCA GACCAAGGTA CAGGACAGTT GTTACCCTGC
         TGTTGCAGGG CAGGTCCCAG GCTCATGTCA CAAGCTCCTA ATTTAGACTA TGCTGGGAAG
         CTGGCCTTCT GGAACAGGAT AGAGGGTGGA GGAGCCCAGG TCCTTCTTTA CAGAGGGACC
         AAGGCAGGCT CAAGTAGGAA GCTCACTGCA GAGTCAGAAC TGGCTGGTCT CTAACTGGAG
         GGATTGCTTT AAAAGCCCTC TTTCCTTCTC CTTGCCTCTC CTTCCTCTTA CCTTGCCCCT
         CTTAATTTAG CTCCAGTCTA TAGAAATAAG GGTTATACCT GTTAGGTATG AGTAGAGAAT
         TTATTAGGCA AACCATTGCC TCAGGAGCTG ATGTGGGCAC AGGCTGCTGT AGGATGACAT
         TCATTGCAGA AGGCCCTGTC GAAACCAAGG CTTAGTGAGA GAACTGACTT CAGAGGAGCA
         TTTTCCTTAC AAAGCACTTT TCTGATTGTT AGGTCAAATG TGCTTTCAGG GCCTTCTGCT
         TAGTTAGCAA TGCAGACCTG CAGTTTTTTT CCCCAGTGGG TAGAAATGTT GGATCGTGCT
         GGGTGGGTGG AGAGGCATGT GGAATAAATG TTTACTCTCT ACCCAAATGA TCTTTTTATT
         AATGGCTAAC ATTTGTATGG TGCTTTCAAG TTGACAAAGA GCTTTCATTT TTATTTCACT
         TAATCCATAT TACTAGGACA GCATTTTGCA GAGAAAGCAT TCAAGATTTT AGTTTAACTC
         TTCATTTTCA CCCAGCCTGG TTCCACAAAG GATTTGTATA TTTAGTAGGT TTCAGTGATC
         AAGGGATTTC ATTGTGTCTG TTGTTTACCA TTATGATCTC ATTCTCAATT CAGACATTTA
         TGGGATGCGT AGTGTGTTGG TCATGTGCCT CATGCTGTGG GGCATGACTG TGGCCCTGGA
         CAACCAAGGG GCGTACCTGT GAGAGGCTTG TCTGGGCAGT TATCTTCCTT CAAGGAGCTG
         ACTGCAATTC TCAGATAATG GCTCAGATGT GGTGAGAGAA CTAAGCCCTG GAAATGTCAC
         CTTCTTGGAT ACTAAGATTT CTTCTGGCTC CCCAAGGATA ATTCATTACT GCGCCAATTC
         ATGCTGATGG TGCACCAGGG GCCTCAAAGA GTTAAAGAGC CAGCACTTTC CAGGGGTGCA
         ATTATCTCTC CCTGGAGAGA GTGTAAAACC CTGAGGGGTG TTTGGTTCCG CAGCAATGCA
         CTAAATTAGA GGGGCCCCAG GAGATAAGCA ATGGCTCTCC CTGGTTGAGA ATTCTCAGAT
         ACCCTGGGAG GCAGGGAGGG AAAGTGAGAG GGTAAACGGG TTTTGTCCTT AGAGGTACTG
         GAGTCACTTC CAGCTGTCCT GTAACCTCAT TTCCTCCTAG CAGAGTGGTT GGAGCAGATA
         GGTTCTGTCC CATTTTCTAG AAGATCTTAG GCATTTTGCT TTTTGTGACA TTACTGAGTT
         CTTTTGGAAC CAGTGGCCAA CCTGCTAGAG ACTGTGAATC CTGAGATGTG GGCCAGGTTA
         GTAAATGATT CTGAACTCTT TTCTGCTCCA GGAAACGGAT TTCTGGGGAG ATATTGCAAA
         AACTCAAACA GAATGTTGTT TATCTGGTGT GTAAAATTGC CAACAAATTG CCCATGTTTT
         CCTCTGAAAT TTCTCCTTTC CAATGTTTTT TCACTTCCTT TGATTTGAAC AAGGGTAGGG
         GCACTTCTAA CAGGTTCTAA CCTGTTGTGT TAATTCTTGT CTCTGGCACA GGGACGGGTG
         GGCCTCATCT CTCACAGGAG AAGGCCCATG AGATCTTCTC CCAGACCCAC TGGGGAAGCT
         TTCCTGCTCA TCTGAACCTG GATGTATTTT TATATGTGCT TTACAGGCTT GTCTTACTTG
         CCTTGATATA ATGGAGGCTC TGCAGAATAC AGGACAGAGA TTTGGGGTCA GGCCTGCATT
         CAACCTGAGC CCCACTTCCT CCTTGCTGGG CAACACTGGC ATATAGACAT TCAGGACATT
         TTTGCTGACC CAACTTTGGT AACTAAGTTT TGATCTTTAG TCAAATAGAG GTTCTCTTTA
         ATGACCTAAC ACTATGCGAT TTAGTTTACC ACTCCCTTCT AAAAGAGGCA TTTCTACCAA
         AATGATCATC TTAAATCTTG GTCTTATCAA AATTTTGAGG GGCTGAGGAT GGGATTGGTG
         AAGAGACCAA GCTGTGTTTT GCTTTTATGA TAGGCATAGG GAAGGGGGCA TGTTCTCGGG
         GAACTACTCT AGAAAAGCAG CTTCCAGGAA AGTTAGCCCT TCAGAGCCAT CTCGCCACCA
         TATGCATTAC CACCTATGGA GCGGTGACTC ATGTTCAGAA TCTATCCTGA AGCCAAACAA
         AGATGCTTAT CCAATAGCAG AAACACTGAG TTATACCAGA GTAGATAAGC AGAAATTTGC
         ATATTTATTT AGCATTCCCA GGTGTAGGTA ACTCTCAGCT AACCGGAGCA CTAGAAATAC
         TACTTTGGTT CCCTTGCCCC TTAATAGTTC AGATACCTTA CTAATCAAAA TAAGCATTCT
         CAAACAGCAC TGATGTCCCA CTTCCATGCA GCCATCTGTC TGTCACCTGT ATCCCAATCC
         TTCTGCCCAA AGGCACAGAG GTCCAGGTGG CATATCCTCA GAGAGCTCAT TCAATTTGTA
         ATAGTTATCA CAGCAGAGTG GCTACCCAAG CTGTGCCATG GGCCTTGATG CATTGCACTG
         ACCAGAGCCC CTTGCTGTGT CTTTAGTGGC ACTCTAGGAT AAAGGAGGCT CTCATGGTAG
         GATCTCTGGG GACTCTGCTC AAGTTACTGA AATGAAGAGC CCCTTTGATC CCTTCTCATA
         AGAAGACTAA TAATGGTCTA TGTTTTCTGA GTTCATAGTA TGTCCAGGCA TTGTTCTAAG
         CCTTTTACTT GTGTTGATGC ATTTAATTCT CACGGAAGCT CTATAAAGGT AGGTACTATT
         ACTATTTCCA TTGTGTGGAT AAAGAAACTA AAGTTTGTCT AGAGAGAACA AGTGACCCCC
         TAAGTCCTCG GCTAGCAAGA GGTACAGCCA GTTTGTTTTT TGTTTCTTTT TGAGATGGAG
         TCTTGCTCTG TCACCCAGGC TGGAGTGCAG TGGTGCCATC TTGGCTCACT GCAACTTCTG
         CCTCCCGGGT TCACACCATT CTCCTGCCTC AGCCTCCTGA GTAGCTGGGA CTACAGGCGC
         CCCCCACTAC GCCCGGCTAA TTTTTGTATT TTTAGTAGAG ACGGGGTTTC ACCATATTGG
         CCAGGCTGGT CTTGAACTCC TCACCTTGTG ATCTGCCCAC CTTGGCCTCC CAAAGTGTGG
         GGATTACAGG CGTGAGCCAC CGCACCTGGC TGCCAGTTTT TTAATCCATG AGGAAGAGAG
         CCTGTACTCC AGCCACTGGG CTCTACTGCC TCCCAGTGGG AGAGGAGAGA GGCAGAACTT
         GGCCTTCATC AGACTGGCCA TATACTCTTT TAAACATCTA ACGATGTTAT TCTCTAGATG
         ACTCCGCTCC CCATCTGCCT TGGGTAAGTG GAGTCTGCTG TAATTTAGCT TGCAAAGAAT
         GCCTTCACCT GGGTGCTTTA GGGAGGCAGC TGAAATGGAA GCAGACTGAA TATTTTGAAA
         TCACTTGTTT CCTCTAAAAA AGCTGTAAAG CCCAAAGGGT AGAATCCTGT TAAAGTGAGC
         AGCTGAGGAC CTCTGGTAGT GGCCATTCAA GATCTTCTTG TCGGCTTTAC GGGCCTGACT
         GTCGCCAGAA CATTAAACTG ACTTCCTTGT TGTTCTGCAT TTGAGACCTA TTTTGAACTT
         TAGTTTAATA CAGACTTTTC TTTTACGGTT CACATAGGGA GCCTTCAGAG GCTGGCTCTA
         CAGTCTGTTC AATAAATGCG TAAAGCGGGG GTATTTCTGG CATTTGAGGC TTTATATTTT
         AAATACACAA AGGCCCTAGG CAACATTAGG AACTAACAAC CTGATAAATT CCAGTTTAAA
         AAAGTGCTGT TATGCTTGAG TTATAAACAT TCTAGGTGCT GTGATTGCTG ATTGTGGACG
         TGTGCTGGCT GTGGATTATC CCGGCGCCCA CATTCACTTG TCTCTGCCCA TTATCATTTA
         GTTTTCTACT TACAGGAAAA TTCACAACTG CTGTGTCTTT AGCTACCTTT GATTACAGTA
         ATCTTCCCAG TGAGACCGTG AGGCAGGGAG AATGGCTGGC AGAGCTTTAC GATAGCAGAG
         AAAACTGCCG CTCAGACTTC CCCACCAAGA CCACATGAAG TGTTCTAGAG AAAACCTGAA
         TCAGAACCGC TAACTTCCAA GTTCATAGTC CACTCATAAT AGAAGATAAT ATTCTGTGGG
         TGTTGATGAT GTAGGGGGTA CTGGGCTCAG TGTTTTACCT GCGTTTTCTC ATTTGTTTAT
         TGTAACCACC TTGTGAGGTC CTATTTTTGT CCCCATTTTA CAGATGGACA AAATTGAGGC
         TTACAGAAAT TAAATAACTT GTCTAGGGTT GCACAGATGG TAAGTCACGG AATCTGGATT
         TGGACCAGAT CTAACCCTTA GAGACTGAAC CCTCTTAACC CTTACATGAT GTTTCATGCG
         CCGCCCCCCC GCAACCCGAC TAACTACTAG GACTGATGTA GCCCCATTTA TACCAATAGT
         GCAAGATCCT GAAAGTGTTA GATTCATATT TTATGTGAAT GTTTTCTCCT GGAGGACTAA
         ATAGGAGGAA GGGTAGTTAA AGGAAGAAAT ACTAATGCAT GCCAGACTTA ATACTTAGGT
         GATGGGGTGA TCTGTGCAGC AAACCACAAT GACACACGTT TACCTATGTA ACAAACCTGC
         ACATGCACCC CAGAACTTAA TAAAATAAAT AAAGGAAGAA ATGATGTCAT TCTGGTCATG
         TTCCAACTTT TAGAGCGGGG ATTCTCAAAC CTCAGCACTA TTGACATTTG AGACAGGATA
         ATTCTTTGTT GGCAAGAAGC TCTCTTGTGC ATTGTAAGAG GCTTACCAGC ATCCCTTGCC
         TCCACCCCAC TAGATGCCAG TAGTTATCCT ACCCCTACCC CCAGCTCACC CGTGAGAATA
         AAAAATGTCT GCAGACATTG CCAAATATCC CAAACATGGC AAAATCACTG CTGGTTGAGT
         ACTACTGCTG TAAAGGCTAA TTAATTACAT TTTCCTTTAA TTCATCCAAT ACAAAGATCC
         TATGTACATG GTACACAGCC TAGCCGTGGA GTCCAGTAGA GTTGCCTCTG AGTCTCTGCT
         TAGACACTAT TTTTAGGCCT CTCCTGTGAG TTCTCCTAGC TGTTGACCTA ATTCCTTTGG
         TCTTCCCCTT CAAGGAGCCT AAGGTCTAAT TGAGGAAATG GATAGAGATG AGTAAAAAAT
         AACCAACAGT GGAAGCAGCA TATAAGAAGT AATAAATGAG GATCTCAGCA GAGAGAAGGC
         CCTCTGGGCT CTGGGAAGAG CAGCCTTGAG TAGGGCCTGC CTGCAATCAT CTGTCTTGTT
         CCTTCCAGGG CCAGGCATTG CATTTGTGGT TTACCCGGAA GCCTTAACCA GGCTGCCTCT
         CTCTCCGTTC TGGGCCATCA TCTTTTTCCT GATGCTCCTC ACTCTTGGAC TTGACACTAT
         GGTGAGCCCC TTTTCCATCA GTCTCTATCC CATGCTCCTC TTGAAGACTC CCCCTCTCCT
         GGGTCCTGGG TTCACCCTTC AGGAGAGGGG TAGGCTTACG GGTGTCTGAA TGTTTCTCCC
         GAGAGATCTA GAGATGCTGA AGTGCCTGTG TAGGGCTCAG GATCACCTTG TATTTTGGGT
         GCTCATGTAA TGGTGCAAGA GAGTCATCCT CTCTCCTTCC TTCTCCCTCT GTTCTATGTG
         GCAACTTTTA GCCTGTGTAT CTCCTGCCTT CGTGTCATTT TGCCAAAGCA AATTCTTTAG
         GGCTGGATAA AGAAT
    ALT  T

hgvs2vcf:
  NC_000011.10:20628017
    REF  TATCTGCTGC ATGGGGAGGC CTGATCACTC TCTCTTCTTA CAACAAATTC CACAACAACT
         GCTACAGGTA TGTAGAGGTA CTACAAGATC TGGGCATAGC TGGTGAGTGG GACAGAAGAA
         TGGACTGAGT TATCAGACAC CTGAGGCCAC ATCCTCACAT TTCATCTTAG GGAGAGCTAA
         AGATTTGCCT CTGGCCTAGG AGAAACCACC TGCTAAGGCC TAGGCACTAT CTTCTGAAGG
         CCTGGACCCT CACTTACACA CCTGGCTCTG ACACATGGGG GAGGCTCAGT GGCTATTTAC
         AGGATGGAAG CAAGTTTGTC TGCAGGTCAC TGTGCAGTTG GCTGTGTTCT GTGACAGTCA
         TTTGTGAGCT ACCTAGTCTG TGGATACAAT GGACTGTGCC TTCAGATGGT CTTCCCTCTG
         TGTGGGGCTG TGACCTAATC TCCTCTTCTT ATAAAGACCC CAGTCATATC AGTCACATTG
         GATCAGGGAC CACTCTAATG ACTTCATTTA ACTTAATTAC CTCTTTAAAG GCCCTATCTC
         CAAATACAGT CACGTTATGA GATGCTAGTG ATTAGGATGA CAAAATATGA ATTTGGTAGT
         GATAGGGGAG TGGTAGGAAG ACACAATTCA GTTCAAAATG ACCTTGAGTA ACAGACTATG
         GTATTTAAAC TTCATTAGTC ACAACTGCTC ATTAACCATT GACCCAAATC AGTCTGAACA
         CCATTAAAGG GTGAAGCATT GCTATCTTCT TTATTAGAAA TGAGGCTGTG GTGTGGCAGA
         AATAACCCAG GCTGAGAGCT TGAAAATCTA GATTCATATC CTGGCCCACA CTATTAATTA
         GTCCATTACC TTTCCCTGGG CCTCAGTTTC CTCTTCAGTA AACTAAGGGG TCAGACAAGG
         TGGATCATTT GCTGCACACT TGCTCTGTGC TAGGCGGTGC ATAGTACAGG TATCATCTCA
         TTCTCTCCTG GCAACAGCCT ATGACAGATA GACTCATTGC TGCCATTTCA AATCAGAGTG
         GAAAGGAAGT GGATTGCTCA AGGTCATGCC ACTAAAAGGC AGGAGAACCA GGATTTCAGT
         GTAGCCCTGG GTTACAGTGT AGCCCGTCTA GCTGTGACCT CACATTTGAA TCTAGGATGA
         CTGAAGGTAG ACTGGGAAAC CCTGGCTATC TTACCAGCAG CAGGCTCTGC GATGAAGGTA
         GAGACACTGG GCTCTCTTCC CTCCCCTGCC CCTTTGTCCT TCTCAACCCT GTGTGTCCCA
         ACTCCAGGCT ACCCTCACAT TTTAGGGTCA TTTGACTTTC CCACTGCCTT CTCTTCCCTC
         ACACATAGTT CCTGTCCTGG AGCCGACCAA GGCCCCATCT CCTCAATTTC TGTTCTGATG
         AACAGATTTA CCTCTGCCCC TGGAATAATG TCTTAGTTTG TTCAGATTGT CTAACAAAAT
         GCCATAGACT GAGTAATATT TTTTCTTTAT ACGTTTTTTG CTTTTATTAT TTTTAAATGA
         CACATAGTAA TTATGCATAT TTATGGAGTA CAGTATGATA TTTCGGTACA TGTATACAAT
         GTGTAATGAT CAAATCAGGG TAATTAGCAT ATCTACTACC TCAAACATTT ATCATTTCTT
         TGTGTTGAAA ACACTGACAG TTCATTCTTC TAGCTGTTTG AAAACATAAA ATAAATTGTT
         GTTAATATAG TCATCTCATA GTGCTGTAGG ATGATTTTTT TTTTTTTTTT TGAGATGGAG
         TTTCGCTCTT GTTGCCCAGG CTGGAGTGCA ATGGCCAATC TCAGCTCACT GCAACCTCCA
         CCTCCCAGGT TCAAGCAATT CAAGTAGCTG GGATTGCGGG CATGTGCCAC CATGCCCCGC
         TAATTTTTTT TTTTGTGTGT GTATTGGGTA GACACGGGGT TTCACCATGT TGGTGAGGCT
         GGTCTCGAAC TCCTGACCTC AGGTGATCCA CCTGCCTTGG CCTCCCAAAG TGCCGGGATT
         ACAGGTATGA GCCACCGTGC CCGGCTGGGA TGGTTGTTAA TATAGTCATC CTATAGTGCT
         ATAGAATACT AGAGTTTATT TCTCCTACCT AGCTATATTT TTGTATCTTT AACTGACTTT
         TGGCTATAAA CAACAGAAAT TTATTGCTCA CTGCTCTAGG GGCTGGGAAG TCCAAGTTCA
         AGGTGCCAGA ATATTCAGTG TCTGGAGGGC TGCTCTCTGT TTCAAAGATG GCACCTTGTT
         GCTGTGTCTT CATATGGTGG AAGAGGCAGA CACATTCCCT TCAGCCTATT TTATAAGGGC
         ACTAATCCCA TGAGTTGGCT CTGTCTTCAT GACTTAATCA CTTTTCTAAA GCCTCCACCT
         CTTAATACTA TCAAATTGTG GATTAAGTTT CAGCCAATGA ATTTGAGATG GGGGGATTCA
         GACCACAGCA GATGAGTTGA GACCCATTTA TATAGATCGT GGAGTCAGAG CTTTGGCCCA
         CAGGCCCTGA ATCAGGGCTA TTAGGGGATA TCGTCTGAGC CTTTTGGTGC TTTTTAAGTG
         AGCCCAAGGG AGCCTGTGGT TAGGACATGA ACGTACACGT ATATGCCTAC ACATGTGCAG
         ACAAACATGT GGGCACACAT TTGTGTGTCC TTCCCCTTGT CCCTTTCCAC TCACCAAGCA
         CACCTAATGG AAAACTCTGG TCTCTTCCTT CCAGGGACAC TCTAATTGTC ACCTGCACCA
         ACAGTGCCAC AAGCATCTTT GCCGGCTTCG TCATCTTCTC CGTTATCGGC TTCATGGCCA
         ATGAACGCAA AGTCAACATT GAGAATGTGG CAGACCAAGG TACAGGACAG TTGTTACCCT
         GCTGTTGCAG GGCAGGTCCC AGGCTCATGT CACAAGCTCC TAATTTAGAC TATGCTGGGA
         AGCTGGCCTT CTGGAACAGG ATAGAGGGTG GAGGAGCCCA GGTCCTTCTT TACAGAGGGA
         CCAAGGCAGG CTCAAGTAGG AAGCTCACTG CAGAGTCAGA ACTGGCTGGT CTCTAACTGG
         AGGGATTGCT TTAAAAGCCC TCTTTCCTTC TCCTTGCCTC TCCTTCCTCT TACCTTGCCC
         CTCTTAATTT AGCTCCAGTC TATAGAAATA AGGGTTATAC CTGTTAGGTA TGAGTAGAGA
         ATTTATTAGG CAAACCATTG CCTCAGGAGC TGATGTGGGC ACAGGCTGCT GTAGGATGAC
         ATTCATTGCA GAAGGCCCTG TCGAAACCAA GGCTTAGTGA GAGAACTGAC TTCAGAGGAG
         CATTTTCCTT ACAAAGCACT TTTCTGATTG TTAGGTCAAA TGTGCTTTCA GGGCCTTCTG
         CTTAGTTAGC AATGCAGACC TGCAGTTTTT TTCCCCAGTG GGTAGAAATG TTGGATCGTG
         CTGGGTGGGT GGAGAGGCAT GTGGAATAAA TGTTTACTCT CTACCCAAAT GATCTTTTTA
         TTAATGGCTA ACATTTGTAT GGTGCTTTCA AGTTGACAAA GAGCTTTCAT TTTTATTTCA
         CTTAATCCAT ATTACTAGGA CAGCATTTTG CAGAGAAAGC ATTCAAGATT TTAGTTTAAC
         TCTTCATTTT CACCCAGCCT GGTTCCACAA AGGATTTGTA TATTTAGTAG GTTTCAGTGA
         TCAAGGGATT TCATTGTGTC TGTTGTTTAC CATTATGATC TCATTCTCAA TTCAGACATT
         TATGGGATGC GTAGTGTGTT GGTCATGTGC CTCATGCTGT GGGGCATGAC TGTGGCCCTG
         GACAACCAAG GGGCGTACCT GTGAGAGGCT TGTCTGGGCA GTTATCTTCC TTCAAGGAGC
         TGACTGCAAT TCTCAGATAA TGGCTCAGAT GTGGTGAGAG AACTAAGCCC TGGAAATGTC
         ACCTTCTTGG ATACTAAGAT TTCTTCTGGC TCCCCAAGGA TAATTCATTA CTGCGCCAAT
         TCATGCTGAT GGTGCACCAG GGGCCTCAAA GAGTTAAAGA GCCAGCACTT TCCAGGGGTG
         CAATTATCTC TCCCTGGAGA GAGTGTAAAA CCCTGAGGGG TGTTTGGTTC CGCAGCAATG
         CACTAAATTA GAGGGGCCCC AGGAGATAAG CAATGGCTCT CCCTGGTTGA GAATTCTCAG
         ATACCCTGGG AGGCAGGGAG GGAAAGTGAG AGGGTAAACG GGTTTTGTCC TTAGAGGTAC
         TGGAGTCACT TCCAGCTGTC CTGTAACCTC ATTTCCTCCT AGCAGAGTGG TTGGAGCAGA
         TAGGTTCTGT CCCATTTTCT AGAAGATCTT AGGCATTTTG CTTTTTGTGA CATTACTGAG
         TTCTTTTGGA ACCAGTGGCC AACCTGCTAG AGACTGTGAA TCCTGAGATG TGGGCCAGGT
         TAGTAAATGA TTCTGAACTC TTTTCTGCTC CAGGAAACGG ATTTCTGGGG AGATATTGCA
         AAAACTCAAA CAGAATGTTG TTTATCTGGT GTGTAAAATT GCCAACAAAT TGCCCATGTT
         TTCCTCTGAA ATTTCTCCTT TCCAATGTTT TTTCACTTCC TTTGATTTGA ACAAGGGTAG
         GGGCACTTCT AACAGGTTCT AACCTGTTGT GTTAATTCTT GTCTCTGGCA CAGGGACGGG
         TGGGCCTCAT CTCTCACAGG AGAAGGCCCA TGAGATCTTC TCCCAGACCC ACTGGGGAAG
         CTTTCCTGCT CATCTGAACC TGGATGTATT TTTATATGTG CTTTACAGGC TTGTCTTACT
         TGCCTTGATA TAATGGAGGC TCTGCAGAAT ACAGGACAGA GATTTGGGGT CAGGCCTGCA
         TTCAACCTGA GCCCCACTTC CTCCTTGCTG GGCAACACTG GCATATAGAC ATTCAGGACA
         TTTTTGCTGA CCCAACTTTG GTAACTAAGT TTTGATCTTT AGTCAAATAG AGGTTCTCTT
         TAATGACCTA ACACTATGCG ATTTAGTTTA CCACTCCCTT CTAAAAGAGG CATTTCTACC
         AAAATGATCA TCTTAAATCT TGGTCTTATC AAAATTTTGA GGGGCTGAGG ATGGGATTGG
         TGAAGAGACC AAGCTGTGTT TTGCTTTTAT GATAGGCATA GGGAAGGGGG CATGTTCTCG
         GGGAACTACT CTAGAAAAGC AGCTTCCAGG AAAGTTAGCC CTTCAGAGCC ATCTCGCCAC
         CATATGCATT ACCACCTATG GAGCGGTGAC TCATGTTCAG AATCTATCCT GAAGCCAAAC
         AAAGATGCTT ATCCAATAGC AGAAACACTG AGTTATACCA GAGTAGATAA GCAGAAATTT
         GCATATTTAT TTAGCATTCC CAGGTGTAGG TAACTCTCAG CTAACCGGAG CACTAGAAAT
         ACTACTTTGG TTCCCTTGCC CCTTAATAGT TCAGATACCT TACTAATCAA AATAAGCATT
         CTCAAACAGC ACTGATGTCC CACTTCCATG CAGCCATCTG TCTGTCACCT GTATCCCAAT
         CCTTCTGCCC AAAGGCACAG AGGTCCAGGT GGCATATCCT CAGAGAGCTC ATTCAATTTG
         TAATAGTTAT CACAGCAGAG TGGCTACCCA AGCTGTGCCA TGGGCCTTGA TGCATTGCAC
         TGACCAGAGC CCCTTGCTGT GTCTTTAGTG GCACTCTAGG ATAAAGGAGG CTCTCATGGT
         AGGATCTCTG GGGACTCTGC TCAAGTTACT GAAATGAAGA GCCCCTTTGA TCCCTTCTCA
         TAAGAAGACT AATAATGGTC TATGTTTTCT GAGTTCATAG TATGTCCAGG CATTGTTCTA
         AGCCTTTTAC TTGTGTTGAT GCATTTAATT CTCACGGAAG CTCTATAAAG GTAGGTACTA
         TTACTATTTC CATTGTGTGG ATAAAGAAAC TAAAGTTTGT CTAGAGAGAA CAAGTGACCC
         CCTAAGTCCT CGGCTAGCAA GAGGTACAGC CAGTTTGTTT TTTGTTTCTT TTTGAGATGG
         AGTCTTGCTC TGTCACCCAG GCTGGAGTGC AGTGGTGCCA TCTTGGCTCA CTGCAACTTC
         TGCCTCCCGG GTTCACACCA TTCTCCTGCC TCAGCCTCCT GAGTAGCTGG GACTACAGGC
         GCCCCCCACT ACGCCCGGCT AATTTTTGTA TTTTTAGTAG AGACGGGGTT TCACCATATT
         GGCCAGGCTG GTCTTGAACT CCTCACCTTG TGATCTGCCC ACCTTGGCCT CCCAAAGTGT
         GGGGATTACA GGCGTGAGCC ACCGCACCTG GCTGCCAGTT TTTTAATCCA TGAGGAAGAG
         AGCCTGTACT CCAGCCACTG GGCTCTACTG CCTCCCAGTG GGAGAGGAGA GAGGCAGAAC
         TTGGCCTTCA TCAGACTGGC CATATACTCT TTTAAACATC TAACGATGTT ATTCTCTAGA
         TGACTCCGCT CCCCATCTGC CTTGGGTAAG TGGAGTCTGC TGTAATTTAG CTTGCAAAGA
         ATGCCTTCAC CTGGGTGCTT TAGGGAGGCA GCTGAAATGG AAGCAGACTG AATATTTTGA
         AATCACTTGT TTCCTCTAAA AAAGCTGTAA AGCCCAAAGG GTAGAATCCT GTTAAAGTGA
         GCAGCTGAGG ACCTCTGGTA GTGGCCATTC AAGATCTTCT TGTCGGCTTT ACGGGCCTGA
         CTGTCGCCAG AACATTAAAC TGACTTCCTT GTTGTTCTGC ATTTGAGACC TATTTTGAAC
         TTTAGTTTAA TACAGACTTT TCTTTTACGG TTCACATAGG GAGCCTTCAG AGGCTGGCTC
         TACAGTCTGT TCAATAAATG CGTAAAGCGG GGGTATTTCT GGCATTTGAG GCTTTATATT
         TTAAATACAC AAAGGCCCTA GGCAACATTA GGAACTAACA ACCTGATAAA TTCCAGTTTA
         AAAAAGTGCT GTTATGCTTG AGTTATAAAC ATTCTAGGTG CTGTGATTGC TGATTGTGGA
         CGTGTGCTGG CTGTGGATTA TCCCGGCGCC CACATTCACT TGTCTCTGCC CATTATCATT
         TAGTTTTCTA CTTACAGGAA AATTCACAAC TGCTGTGTCT TTAGCTACCT TTGATTACAG
         TAATCTTCCC AGTGAGACCG TGAGGCAGGG AGAATGGCTG GCAGAGCTTT ACGATAGCAG
         AGAAAACTGC CGCTCAGACT TCCCCACCAA GACCACATGA AGTGTTCTAG AGAAAACCTG
         AATCAGAACC GCTAACTTCC AAGTTCATAG TCCACTCATA ATAGAAGATA ATATTCTGTG
         GGTGTTGATG ATGTAGGGGG TACTGGGCTC AGTGTTTTAC CTGCGTTTTC TCATTTGTTT
         ATTGTAACCA CCTTGTGAGG TCCTATTTTT GTCCCCATTT TACAGATGGA CAAAATTGAG
         GCTTACAGAA ATTAAATAAC TTGTCTAGGG TTGCACAGAT GGTAAGTCAC GGAATCTGGA
         TTTGGACCAG ATCTAACCCT TAGAGACTGA ACCCTCTTAA CCCTTACATG ATGTTTCATG
         CGCCGCCCCC CCGCAACCCG ACTAACTACT AGGACTGATG TAGCCCCATT TATACCAATA
         GTGCAAGATC CTGAAAGTGT TAGATTCATA TTTTATGTGA ATGTTTTCTC CTGGAGGACT
         AAATAGGAGG AAGGGTAGTT AAAGGAAGAA ATACTAATGC ATGCCAGACT TAATACTTAG
         GTGATGGGGT GATCTGTGCA GCAAACCACA ATGACACACG TTTACCTATG TAACAAACCT
         GCACATGCAC CCCAGAACTT AATAAAATAA ATAAAGGAAG AAATGATGTC ATTCTGGTCA
         TGTTCCAACT TTTAGAGCGG GGATTCTCAA ACCTCAGCAC TATTGACATT TGAGACAGGA
         TAATTCTTTG TTGGCAAGAA GCTCTCTTGT GCATTGTAAG AGGCTTACCA GCATCCCTTG
         CCTCCACCCC ACTAGATGCC AGTAGTTATC CTACCCCTAC CCCCAGCTCA CCCGTGAGAA
         TAAAAAATGT CTGCAGACAT TGCCAAATAT CCCAAACATG GCAAAATCAC TGCTGGTTGA
         GTACTACTGC TGTAAAGGCT AATTAATTAC ATTTTCCTTT AATTCATCCA ATACAAAGAT
         CCTATGTACA TGGTACACAG CCTAGCCGTG GAGTCCAGTA GAGTTGCCTC TGAGTCTCTG
         CTTAGACACT ATTTTTAGGC CTCTCCTGTG AGTTCTCCTA GCTGTTGACC TAATTCCTTT
         GGTCTTCCCC TTCAAGGAGC CTAAGGTCTA ATTGAGGAAA TGGATAGAGA TGAGTAAAAA
         ATAACCAACA GTGGAAGCAG CATATAAGAA GTAATAAATG AGGATCTCAG CAGAGAGAAG
         GCCCTCTGGG CTCTGGGAAG AGCAGCCTTG AGTAGGGCCT GCCTGCAATC ATCTGTCTTG
         TTCCTTCCAG GGCCAGGCAT TGCATTTGTG GTTTACCCGG AAGCCTTAAC CAGGCTGCCT
         CTCTCTCCGT TCTGGGCCAT CATCTTTTTC CTGATGCTCC TCACTCTTGG ACTTGACACT
         ATGGTGAGCC CCTTTTCCAT CAGTCTCTAT CCCATGCTCC TCTTGAAGAC TCCCCCTCTC
         CTGGGTCCTG GGTTCACCCT TCAGGAGAGG GGTAGGCTTA CGGGTGTCTG AATGTTTCTC
         CCGAGAGATC TAGAGATGCT GAAGTGCCTG TGTAGGGCTC AGGATCACCT TGTATTTTGG
         GTGCTCATGT AATGGTGCAA GAGAGTCATC CTCTCTCCTT CCTTCTCCCT CTGTTCTATG
         TGGCAACTTT TAGCCTGTGT ATCTCCTGCC TTCGTGTCAT TTTGCCAAAG CAAATTCTTT
         AGGGCTGGAT AAAGA
    ALT  T
```

### `NM_014425:c.273+13del` — intronic_del

**Variant としては同一。** 左寄せの違い — hgvs2vcf は VCF 規約どおり 3 塩基左に寄せ、Variant Recoder は HGVS の 3′ シフト位置のまま。

```
Variant Recoder:
  NC_000009.12:100126561
    REF  AA
    ALT  A

hgvs2vcf:
  NC_000009.12:100126558
    REF  TA
    ALT  T
```

### `NM_017668:c.948-2680_948-2670del` — intronic_del

**Variant としては同一。** 左寄せの違い — hgvs2vcf は VCF 規約どおり 1 塩基左に寄せ、Variant Recoder は HGVS の 3′ シフト位置のまま。

```
Variant Recoder:
  NC_000016.10:15721510
    REF  TCCAAGGCCT CT
    ALT  T

hgvs2vcf:
  NC_000016.10:15721509
    REF  TTCCAAGGCC TC
    ALT  T
```

### `NM_025077:c.753-9_753-7del` — intronic_del

**Variant としては同一。** 左寄せの違い — hgvs2vcf は VCF 規約どおり 1 塩基左に寄せ、Variant Recoder は HGVS の 3′ シフト位置のまま。

```
Variant Recoder:
  NC_000001.11:45342833
    REF  GCTG
    ALT  G

hgvs2vcf:
  NC_000001.11:45342832
    REF  CGCT
    ALT  C
```

### `NM_033034:c.768-26_768-24del` — intronic_del

**Variant としては同一。** 左寄せの違い — hgvs2vcf は VCF 規約どおり 14 塩基左に寄せ、Variant Recoder は HGVS の 3′ シフト位置のまま。

```
Variant Recoder:
  NC_000011.10:5666104
    REF  AAAA
    ALT  A

hgvs2vcf:
  NC_000011.10:5666090
    REF  TAAA
    ALT  T
```

### `NM_170682:c.774+123del` — intronic_del

**Variant としては同一。** 左寄せの違い — hgvs2vcf は VCF 規約どおり 3 塩基左に寄せ、Variant Recoder は HGVS の 3′ シフト位置のまま。

```
Variant Recoder:
  NC_000012.12:132620705
    REF  AA
    ALT  A

hgvs2vcf:
  NC_000012.12:132620702
    REF  GA
    ALT  G
```

### `NM_181523:c.1815-17_1815-16del` — intronic_del

**Variant としては同一。** 左寄せの違い — hgvs2vcf は VCF 規約どおり 1 塩基左に寄せ、Variant Recoder は HGVS の 3′ シフト位置のまま。

```
Variant Recoder:
  NC_000005.10:68296153
    REF  TCT
    ALT  T

hgvs2vcf:
  NC_000005.10:68296152
    REF  TTC
    ALT  T
```

### `NM_203447:c.1679+11_1679+12del` — intronic_del

**Variant としては同一。** 左寄せの違い — hgvs2vcf は VCF 規約どおり 3 塩基左に寄せ、Variant Recoder は HGVS の 3′ シフト位置のまま。

```
Variant Recoder:
  NC_000009.12:340331
    REF  ACA
    ALT  A

hgvs2vcf:
  NC_000009.12:340328
    REF  AAC
    ALT  A
```

### `PEX14:c.677+6_677+8del` — intronic_del

**Variant としては同一。** 左寄せの違い — hgvs2vcf は VCF 規約どおり 3 塩基左に寄せ、Variant Recoder は HGVS の 3′ シフト位置のまま。

```
Variant Recoder:
  NC_000001.11:10627368
    REF  GAGG
    ALT  G

hgvs2vcf:
  NC_000001.11:10627365
    REF  TAGG
    ALT  T
```

### `SMARCAL1:c.811+38del` — intronic_del

**Variant としては同一。** 左寄せの違い — hgvs2vcf は VCF 規約どおり 14 塩基左に寄せ、Variant Recoder は HGVS の 3′ シフト位置のまま。

```
Variant Recoder:
  NC_000002.12:216415552
    REF  TT
    ALT  T

hgvs2vcf:
  NC_000002.12:216415538
    REF  GT
    ALT  G
```

### `SRP54:c.1327+15_1327+32del18` — intronic_del

**Variant としては同一。** 左寄せの違い — hgvs2vcf は VCF 規約どおり 2 塩基左に寄せ、Variant Recoder は HGVS の 3′ シフト位置のまま。

```
Variant Recoder:
  NC_000014.9:35023094
    REF  GCTTGTTATT AGTTAACAG
    ALT  G

hgvs2vcf:
  NC_000014.9:35023092
    REF  AAGCTTGTTA TTAGTTAAC
    ALT  A
```

### `TARDBP:c.544-17_544-14del` — intronic_del

**Variant としては同一。** 左寄せの違い — hgvs2vcf は VCF 規約どおり 3 塩基左に寄せ、Variant Recoder は HGVS の 3′ シフト位置のまま。

```
Variant Recoder:
  NC_000001.11:11020411
    REF  TCCTT
    ALT  T

hgvs2vcf:
  NC_000001.11:11020408
    REF  TCTTC
    ALT  T
```

### `ZFC3H1:c.5730-22_5730-20del` — intronic_del

**Variant としては同一。** 左寄せの違い — hgvs2vcf は VCF 規約どおり 12 塩基左に寄せ、Variant Recoder は HGVS の 3′ シフト位置のまま。

```
Variant Recoder:
  NC_000012.12:71611116
    REF  AAAA
    ALT  A

hgvs2vcf:
  NC_000012.12:71611104
    REF  GAAA
    ALT  G
```

### `NM_000051:c.7629_7629+1delinsA` — intronic_delins

**Variant としては同一。** アンカー塩基のトリミング差 — Variant Recoder は REF/ALT 共通の先頭 1 塩基を残し、hgvs2vcf は削っている。

```
Variant Recoder:
  NC_000011.10:108331556
    REF  ATG
    ALT  AA

hgvs2vcf:
  NC_000011.10:108331557
    REF  TG
    ALT  A
```

### `NM_006363:c.1233+9_1233+12delinsGAC` — intronic_delins

**Variant としては同一。** アンカー塩基のトリミング差 — Variant Recoder は REF/ALT 共通の先頭 1 塩基を残し、hgvs2vcf は削っている。

```
Variant Recoder:
  NC_000020.11:18530811
    REF  AAACT
    ALT  AGAC

hgvs2vcf:
  NC_000020.11:18530812
    REF  AACT
    ALT  GAC
```

### `ADAMTSL4:c.1861+16dup` — intronic_dup

**Variant としては同一。** 左寄せの違い — hgvs2vcf は VCF 規約どおり 3 塩基左に寄せ、Variant Recoder は HGVS の 3′ シフト位置のまま。

```
Variant Recoder:
  NC_000001.11:150557065
    REF  C
    ALT  CC

hgvs2vcf:
  NC_000001.11:150557062
    REF  A
    ALT  AC
```

### `AIP:c.645+23dup` — intronic_dup

**Variant としては同一。** 左寄せの違い — hgvs2vcf は VCF 規約どおり 4 塩基左に寄せ、Variant Recoder は HGVS の 3′ シフト位置のまま。

```
Variant Recoder:
  NC_000011.10:67490236
    REF  G
    ALT  GG

hgvs2vcf:
  NC_000011.10:67490232
    REF  A
    ALT  AG
```

### `ASPM:c.2936+132dup` — intronic_dup

**Variant としては同一。** 左寄せの違い — hgvs2vcf は VCF 規約どおり 15 塩基左に寄せ、Variant Recoder は HGVS の 3′ シフト位置のまま。

```
Variant Recoder:
  NC_000001.11:197128358
    REF  A
    ALT  AA

hgvs2vcf:
  NC_000001.11:197128343
    REF  G
    ALT  GA
```

### `BLNK:c.205-19_205-16dup` — intronic_dup

**Variant としては同一。** 左寄せの違い — hgvs2vcf は VCF 規約どおり 4 塩基左に寄せ、Variant Recoder は HGVS の 3′ シフト位置のまま。

```
Variant Recoder:
  NC_000010.11:96227585
    REF  A
    ALT  ACAGA

hgvs2vcf:
  NC_000010.11:96227581
    REF  G
    ALT  GCAGA
```

### `COL4A3:c.144+11dup` — intronic_dup

**Variant としては同一。** 左寄せの違い — hgvs2vcf は VCF 規約どおり 2 塩基左に寄せ、Variant Recoder は HGVS の 3′ シフト位置のまま。

```
Variant Recoder:
  NC_000002.12:227238034
    REF  A
    ALT  AA

hgvs2vcf:
  NC_000002.12:227238032
    REF  C
    ALT  CA
```

### `DICER1:c.4206+8dup` — intronic_dup

**Variant としては同一。** 左寄せの違い — hgvs2vcf は VCF 規約どおり 1 塩基左に寄せ、Variant Recoder は HGVS の 3′ シフト位置のまま。

```
Variant Recoder:
  NC_000014.9:95099772
    REF  A
    ALT  AA

hgvs2vcf:
  NC_000014.9:95099771
    REF  C
    ALT  CA
```

### `DIS3L2:c.1659+18dup` — intronic_dup

**Variant としては同一。** 左寄せの違い — hgvs2vcf は VCF 規約どおり 6 塩基左に寄せ、Variant Recoder は HGVS の 3′ シフト位置のまま。

```
Variant Recoder:
  NC_000002.12:232263457
    REF  T
    ALT  TT

hgvs2vcf:
  NC_000002.12:232263451
    REF  G
    ALT  GT
```

### `KCNQ2:c.1149-6_1149-5dup` — intronic_dup

**Variant としては同一。** 左寄せの違い — hgvs2vcf は VCF 規約どおり 4 塩基左に寄せ、Variant Recoder は HGVS の 3′ シフト位置のまま。

```
Variant Recoder:
  NC_000020.11:63428441
    REF  G
    ALT  GGG

hgvs2vcf:
  NC_000020.11:63428437
    REF  T
    ALT  TGG
```

### `NM_000481:c.878-228dup` — intronic_dup

**Variant としては同一。** 左寄せの違い — hgvs2vcf は VCF 規約どおり 14 塩基左に寄せ、Variant Recoder は HGVS の 3′ シフト位置のまま。

```
Variant Recoder:
  NC_000003.12:49418201
    REF  T
    ALT  TT

hgvs2vcf:
  NC_000003.12:49418187
    REF  C
    ALT  CT
```

### `NM_000546:c.994-35_994-18dup` — intronic_dup

**Variant としては同一。** 左寄せの違い — hgvs2vcf は VCF 規約どおり 18 塩基左に寄せ、Variant Recoder は HGVS の 3′ シフト位置のまま。

```
Variant Recoder:
  NC_000017.11:7670750
    REF  T
    ALT  TGGGGAGAAG TAAGTATAT

hgvs2vcf:
  NC_000017.11:7670732
    REF  G
    ALT  GGGGGAGAAG TAAGTATAT
```

### `NM_000551:c.340+172_340+174dup` — intronic_dup

**Variant としては同一。** 左寄せの違い — hgvs2vcf は VCF 規約どおり 17 塩基左に寄せ、Variant Recoder は HGVS の 3′ シフト位置のまま。

```
Variant Recoder:
  NC_000003.12:10142358
    REF  T
    ALT  TTTT

hgvs2vcf:
  NC_000003.12:10142341
    REF  C
    ALT  CTTT
```

### `NM_001015880:c.381+24dup` — intronic_dup

**Variant としては同一。** 左寄せの違い — hgvs2vcf は VCF 規約どおり 21 塩基左に寄せ、Variant Recoder は HGVS の 3′ シフト位置のまま。

```
Variant Recoder:
  NC_000010.11:87713333
    REF  A
    ALT  AA

hgvs2vcf:
  NC_000010.11:87713312
    REF  T
    ALT  TA
```

### `NM_001164508:c.13369-20_13369-12dup` — intronic_dup

**Variant としては同一。** 左寄せの違い — hgvs2vcf は VCF 規約どおり 9 塩基左に寄せ、Variant Recoder は HGVS の 3′ シフト位置のまま。

```
Variant Recoder:
  NC_000002.12:151602028
    REF  T
    ALT  TGAGTGCAAT

hgvs2vcf:
  NC_000002.12:151602019
    REF  A
    ALT  AGAGTGCAAT
```

### `NM_001267550:c.1398+216_1398+237dup` — intronic_dup

**Variant としては同一。** 左寄せの違い — hgvs2vcf は VCF 規約どおり 22 塩基左に寄せ、Variant Recoder は HGVS の 3′ シフト位置のまま。

```
Variant Recoder:
  NC_000002.12:178794183
    REF  C
    ALT  CTATAGCCCA GGTATTTCTG GCC

hgvs2vcf:
  NC_000002.12:178794161
    REF  A
    ALT  ATATAGCCCA GGTATTTCTG GCC
```

### `NM_001330700:c.2863-7dup` — intronic_dup

**Variant としては同一。** 左寄せの違い — hgvs2vcf は VCF 規約どおり 3 塩基左に寄せ、Variant Recoder は HGVS の 3′ シフト位置のまま。

```
Variant Recoder:
  NC_000003.12:25620069
    REF  A
    ALT  AA

hgvs2vcf:
  NC_000003.12:25620066
    REF  T
    ALT  TA
```

### `NM_006939:c.3490-13dup` — intronic_dup

**Variant としては同一。** 左寄せの違い — hgvs2vcf は VCF 規約どおり 10 塩基左に寄せ、Variant Recoder は HGVS の 3′ シフト位置のまま。

```
Variant Recoder:
  NC_000014.9:50118866
    REF  A
    ALT  AA

hgvs2vcf:
  NC_000014.9:50118856
    REF  C
    ALT  CA
```

### `NM_007098:c.3601-1dup` — intronic_dup

**Variant としては同一。** 左寄せの違い — hgvs2vcf は VCF 規約どおり 2 塩基左に寄せ、Variant Recoder は HGVS の 3′ シフト位置のまま。

```
Variant Recoder:
  NC_000022.11:19201494
    REF  C
    ALT  CC

hgvs2vcf:
  NC_000022.11:19201492
    REF  A
    ALT  AC
```

### `NM_016284:c.3202-3dup` — intronic_dup

**Variant としては同一。** 左寄せの違い — hgvs2vcf は VCF 規約どおり 1 塩基左に寄せ、Variant Recoder は HGVS の 3′ シフト位置のまま。

```
Variant Recoder:
  NC_000016.10:58551275
    REF  A
    ALT  AA

hgvs2vcf:
  NC_000016.10:58551274
    REF  T
    ALT  TA
```

### `PIK3C2A:c.2232-11dup` — intronic_dup

**Variant としては同一。** 左寄せの違い — hgvs2vcf は VCF 規約どおり 1 塩基左に寄せ、Variant Recoder は HGVS の 3′ シフト位置のまま。

```
Variant Recoder:
  NC_000011.10:17129478
    REF  A
    ALT  AA

hgvs2vcf:
  NC_000011.10:17129477
    REF  G
    ALT  GA
```

### `RIPOR2:c.886-163dup` — intronic_dup

**Variant としては同一。** 左寄せの違い — hgvs2vcf は VCF 規約どおり 16 塩基左に寄せ、Variant Recoder は HGVS の 3′ シフト位置のまま。

```
Variant Recoder:
  NC_000006.12:24850113
    REF  T
    ALT  TT

hgvs2vcf:
  NC_000006.12:24850097
    REF  C
    ALT  CT
```

### `SCN1A:c.602+2dup` — intronic_dup

**Variant としては同一。** 左寄せの違い — hgvs2vcf は VCF 規約どおり 1 塩基左に寄せ、Variant Recoder は HGVS の 3′ シフト位置のまま。

```
Variant Recoder:
  NC_000002.12:166054636
    REF  A
    ALT  AA

hgvs2vcf:
  NC_000002.12:166054635
    REF  T
    ALT  TA
```

### `SCN5A:c.703+19dup` — intronic_dup

**Variant としては同一。** 左寄せの違い — hgvs2vcf は VCF 規約どおり 1 塩基左に寄せ、Variant Recoder は HGVS の 3′ シフト位置のまま。

```
Variant Recoder:
  NC_000003.12:38613724
    REF  T
    ALT  TT

hgvs2vcf:
  NC_000003.12:38613723
    REF  G
    ALT  GT
```

### `SFXN4:c.112-87_112-84dup` — intronic_dup

**Variant としては同一。** 左寄せの違い — hgvs2vcf は VCF 規約どおり 15 塩基左に寄せ、Variant Recoder は HGVS の 3′ シフト位置のまま。

```
Variant Recoder:
  NC_000010.11:119164283
    REF  T
    ALT  TTTTT

hgvs2vcf:
  NC_000010.11:119164268
    REF  C
    ALT  CTTTT
```

### `SLC25A12:c.930+3dup` — intronic_dup

**Variant としては同一。** 左寄せの違い — hgvs2vcf は VCF 規約どおり 1 塩基左に寄せ、Variant Recoder は HGVS の 3′ シフト位置のまま。

```
Variant Recoder:
  NC_000002.12:171826795
    REF  T
    ALT  TT

hgvs2vcf:
  NC_000002.12:171826794
    REF  A
    ALT  AT
```

### `VIPAS39:c.913-36_913-35dup` — intronic_dup

**Variant としては同一。** 左寄せの違い — hgvs2vcf は VCF 規約どおり 14 塩基左に寄せ、Variant Recoder は HGVS の 3′ シフト位置のまま。

```
Variant Recoder:
  NC_000014.9:77435429
    REF  A
    ALT  AAA

hgvs2vcf:
  NC_000014.9:77435415
    REF  G
    ALT  GAA
```

### `WDR1:c.229+9_229+10dup` — intronic_dup

**Variant としては同一。** 左寄せの違い — hgvs2vcf は VCF 規約どおり 2 塩基左に寄せ、Variant Recoder は HGVS の 3′ シフト位置のまま。

```
Variant Recoder:
  NC_000004.12:10103887
    REF  A
    ALT  ACA

hgvs2vcf:
  NC_000004.12:10103885
    REF  C
    ALT  CCA
```

### `NM_007078:c.93+272_93+273insGAGG` — intronic_ins

**Variant としては同一。** 左寄せの違い — hgvs2vcf は VCF 規約どおり 3 塩基左に寄せ、Variant Recoder は HGVS の 3′ シフト位置のまま。

```
Variant Recoder:
  NC_000010.11:86669056
    REF  G
    ALT  GGAGG

hgvs2vcf:
  NC_000010.11:86669053
    REF  C
    ALT  CAGGG
```

### `AARS1:p.Leu262_Val264del` — protein_del

**Variant としては同一。** 左寄せの違い — hgvs2vcf は VCF 規約どおり 1 塩基左に寄せ、Variant Recoder は HGVS の 3′ シフト位置のまま。

```
Variant Recoder:
  NC_000016.10:70270219
    REF  GGACAAAAAG
    ALT  G

hgvs2vcf:
  NC_000016.10:70270218
    REF  GGGACAAAAA
    ALT  G
```

### `ATM:p.Gly2765del` — protein_del

**Variant としては同一。** 左寄せの違い — hgvs2vcf は VCF 規約どおり 2 塩基左に寄せ、Variant Recoder は HGVS の 3′ シフト位置のまま。

```
Variant Recoder:
  NC_000011.10:108343245
    REF  TGGT
    ALT  T

hgvs2vcf:
  NC_000011.10:108343243
    REF  AGTG
    ALT  A
```

### `CBS:p.Met173del` — protein_del

**Variant としては同一。** 左寄せの違い — hgvs2vcf は VCF 規約どおり 1 塩基左に寄せ、Variant Recoder は HGVS の 3′ シフト位置のまま。

```
Variant Recoder:
  NC_000021.9:43065627
    REF  TCAT
    ALT  T

hgvs2vcf:
  NC_000021.9:43065626
    REF  CTCA
    ALT  C
```

### `CEBPA:p.Pro192_His205del` — protein_del

**Variant としては同一。** 左寄せの違い — hgvs2vcf は VCF 規約どおり 1 塩基左に寄せ、Variant Recoder は HGVS の 3′ シフト位置のまま。

```
Variant Recoder:
  NC_000019.10:33301799
    REF  GGTGCGGGGC GGCCAGGTGC GCGGGCGGCG GGTGCGGGTG CGG
    ALT  G

hgvs2vcf:
  NC_000019.10:33301798
    REF  AGGTGCGGGG CGGCCAGGTG CGCGGGCGGC GGGTGCGGGT GCG
    ALT  A
```

### `CFB:p.Glu243del` — protein_del

**Variant としては同一。** 左寄せの違い — hgvs2vcf は VCF 規約どおり 1 塩基左に寄せ、Variant Recoder は HGVS の 3′ シフト位置のまま。

```
Variant Recoder:
  NC_000006.12:31947809
    REF  AGAA
    ALT  A

hgvs2vcf:
  NC_000006.12:31947808
    REF  TAGA
    ALT  T
```

### `CLCN1:p.Gly482_Gly483del` — protein_del

**Variant としては同一。** 左寄せの違い — hgvs2vcf は VCF 規約どおり 2 塩基左に寄せ、Variant Recoder は HGVS の 3′ シフト位置のまま。

```
Variant Recoder:
  NC_000007.14:143339294
    REF  CGGAGGC
    ALT  C

hgvs2vcf:
  NC_000007.14:143339292
    REF  TGCGGAG
    ALT  T
```

### `HCFC1:p.Thr712del` — protein_del

**Variant としては同一。** 左寄せの違い — hgvs2vcf は VCF 規約どおり 1 塩基左に寄せ、Variant Recoder は HGVS の 3′ シフト位置のまま。

```
Variant Recoder:
  NC_000023.11:153957530
    REF  TGGT
    ALT  T

hgvs2vcf:
  NC_000023.11:153957529
    REF  TTGG
    ALT  T
```

### `MYT1:p.Glu306del` — protein_del

**Variant としては同一。** 左寄せの違い — hgvs2vcf は VCF 規約どおり 12 塩基左に寄せ、Variant Recoder は HGVS の 3′ シフト位置のまま。

```
Variant Recoder:
  NC_000020.11:64208111
    REF  GGAG
    ALT  G

hgvs2vcf:
  NC_000020.11:64208099
    REF  AGAG
    ALT  A
```

### `NHP2:p.Arg42del` — protein_del

**Variant としては同一。** 左寄せの違い — hgvs2vcf は VCF 規約どおり 1 塩基左に寄せ、Variant Recoder は HGVS の 3′ シフト位置のまま。

```
Variant Recoder:
  NC_000005.10:178153691
    REF  GGCG
    ALT  G

hgvs2vcf:
  NC_000005.10:178153690
    REF  AGGC
    ALT  A
```

### `PSEN1:p.Leu174del` — protein_del

**Variant としては同一。** 左寄せの違い — hgvs2vcf は VCF 規約どおり 2 塩基左に寄せ、Variant Recoder は HGVS の 3′ シフト位置のまま。

```
Variant Recoder:
  NC_000014.9:73186891
    REF  GCTG
    ALT  G

hgvs2vcf:
  NC_000014.9:73186889
    REF  TTGC
    ALT  T
```

### `RAI1:p.Ser1249del` — protein_del

**Variant としては同一。** 左寄せの違い — hgvs2vcf は VCF 規約どおり 14 塩基左に寄せ、Variant Recoder は HGVS の 3′ シフト位置のまま。

```
Variant Recoder:
  NC_000017.11:17796692
    REF  CAGC
    ALT  C

hgvs2vcf:
  NC_000017.11:17796678
    REF  CGCA
    ALT  C
```

### `SPI1:p.Gly148del` — protein_del

**Variant としては同一。** 左寄せの違い — hgvs2vcf は VCF 規約どおり 1 塩基左に寄せ、Variant Recoder は HGVS の 3′ シフト位置のまま。

```
Variant Recoder:
  NC_000011.10:47358892
    REF  CGCC
    ALT  C

hgvs2vcf:
  NC_000011.10:47358891
    REF  TCGC
    ALT  T
```

### `TGFBR1:p.Ala25_Ala26del` — protein_del

**Variant としては同一。** 左寄せの違い — hgvs2vcf は VCF 規約どおり 22 塩基左に寄せ、Variant Recoder は HGVS の 3′ シフト位置のまま。

```
Variant Recoder:
  NC_000009.12:99105277
    REF  GGCGGCG
    ALT  G

hgvs2vcf:
  NC_000009.12:99105255
    REF  TGGCGGC
    ALT  T
```

### `TLR7:p.Thr221del` — protein_del

**Variant としては同一。** 左寄せの違い — hgvs2vcf は VCF 規約どおり 2 塩基左に寄せ、Variant Recoder は HGVS の 3′ シフト位置のまま。

```
Variant Recoder:
  NC_000023.11:12886168
    REF  TACT
    ALT  T

hgvs2vcf:
  NC_000023.11:12886166
    REF  CCTA
    ALT  C
```

### `TTN:p.Asp17396del` — protein_del

**Variant としては同一。** 左寄せの違い — hgvs2vcf は VCF 規約どおり 1 塩基左に寄せ、Variant Recoder は HGVS の 3′ シフト位置のまま。

```
Variant Recoder:
  NC_000002.12:178608822
    REF  CATC
    ALT  C

hgvs2vcf:
  NC_000002.12:178608821
    REF  CCAT
    ALT  C
```

### `ZC4H2:p.Ile73del` — protein_del

**Variant としては同一。** 左寄せの違い — hgvs2vcf は VCF 規約どおり 1 塩基左に寄せ、Variant Recoder は HGVS の 3′ シフト位置のまま。

```
Variant Recoder:
  NC_000023.11:64921822
    REF  TGAT
    ALT  T

hgvs2vcf:
  NC_000023.11:64921821
    REF  TTGA
    ALT  T
```

### `NM_004329:c.-268+6699_-268+6706del` — utr_del

**Variant としては同一。** 左寄せの違い — hgvs2vcf は VCF 規約どおり 3 塩基左に寄せ、Variant Recoder は HGVS の 3′ シフト位置のまま。

```
Variant Recoder:
  NC_000010.11:86763617
    REF  GTACCAAAG
    ALT  G

hgvs2vcf:
  NC_000010.11:86763614
    REF  CAAGTACCA
    ALT  C
```

### `NM_000444:c.-14_8delinsTGGGAGCAGCGTGG` — utr_delins

**Variant としては同一。** アンカー塩基のトリミング差 — Variant Recoder は REF/ALT 共通の先頭 1 塩基を残し、hgvs2vcf は削っている。

```
Variant Recoder:
  NC_000023.11:22032991
    REF  TCTACGGCCC TTCTGATGGA AGC
    ALT  TTGGGAGCAG CGTGG

hgvs2vcf:
  NC_000023.11:22032992
    REF  CTACGGCCCT TCTGATGGAA GC
    ALT  TGGGAGCAGC GTGG
```

### `NM_000127:c.*144dup` — utr_dup

**Variant としては同一。** 左寄せの違い — hgvs2vcf は VCF 規約どおり 1 塩基左に寄せ、Variant Recoder は HGVS の 3′ シフト位置のまま。

```
Variant Recoder:
  NC_000008.11:117799568
    REF  T
    ALT  TT

hgvs2vcf:
  NC_000008.11:117799567
    REF  C
    ALT  CT
```

### `NM_001370348:c.*7810dup` — utr_dup

**Variant としては同一。** 左寄せの違い — hgvs2vcf は VCF 規約どおり 3 塩基左に寄せ、Variant Recoder は HGVS の 3′ シフト位置のまま。

```
Variant Recoder:
  NC_000006.12:63721517
    REF  T
    ALT  TT

hgvs2vcf:
  NC_000006.12:63721514
    REF  A
    ALT  AT
```

### `NM_019032:c.-84-299dup` — utr_dup

**Variant としては同一。** 左寄せの違い — hgvs2vcf は VCF 規約どおり 14 塩基左に寄せ、Variant Recoder は HGVS の 3′ シフト位置のまま。

```
Variant Recoder:
  NC_000001.11:150551905
    REF  A
    ALT  AA

hgvs2vcf:
  NC_000001.11:150551891
    REF  C
    ALT  CA
```

## Successful results (322)

### `BRCA2:c.7563del` — coding_del

```
Variant Recoder = hgvs2vcf:
  NC_000013.11:32356554
    REF  TC
    ALT  T
```

### `CACNA1A:c.6657_6659del` — coding_del

```
Variant Recoder = hgvs2vcf:
  NC_000019.10:13208876
    REF  GGGA
    ALT  G
```

### `FGA:c.1113del` — coding_del

```
Variant Recoder = hgvs2vcf:
  NC_000004.12:154586315
    REF  GC
    ALT  G
```

### `HLCS:c.2212_2213del` — coding_del

```
Variant Recoder = hgvs2vcf:
  NC_000021.9:36759749
    REF  TCC
    ALT  T
```

### `NM_000080:c.510_511del` — coding_del

```
Variant Recoder = hgvs2vcf:
  NC_000017.11:4901614
    REF  TAC
    ALT  T
```

### `NM_000314:c.31del` — coding_del

```
Variant Recoder = hgvs2vcf:
  NC_000010.11:87864499
    REF  CA
    ALT  C
```

### `NM_000517:c.340_351del` — coding_del

```
Variant Recoder = hgvs2vcf:
  NC_000016.10:173510
    REF  CCTCCCCGCC GAG
    ALT  C
```

### `NM_000546:c.388delC` — coding_del

```
Variant Recoder = hgvs2vcf:
  NC_000017.11:7675223
    REF  AG
    ALT  A
```

### `NM_001040616:c.1116del` — coding_del

```
Variant Recoder = hgvs2vcf:
  NC_000015.10:100573756
    REF  GT
    ALT  G
```

### `NM_001261826:c.2489_2490del` — coding_del

```
Variant Recoder = hgvs2vcf:
  NC_000019.10:2114235
    REF  CAG
    ALT  C
```

### `NM_001353214:c.1177_1178del` — coding_del

```
Variant Recoder = hgvs2vcf:
  NC_000018.10:49272250
    REF  ATG
    ALT  A
```

### `NM_004713:c.2943_2950del` — coding_del

```
Variant Recoder = hgvs2vcf:
  NC_000014.9:49785298
    REF  GTCAAAGAA
    ALT  G
```

### `NM_004714:c.1058del` — coding_del

```
Variant Recoder = hgvs2vcf:
  NC_000019.10:39827321
    REF  AC
    ALT  A
```

### `NM_005334:c.2135_2137del` — coding_del

```
Variant Recoder = hgvs2vcf:
  NC_000023.11:153957529
    REF  TTGG
    ALT  T
```

### `NM_006231:c.2756_2759del` — coding_del

```
Variant Recoder = hgvs2vcf:
  NC_000012.12:132661631
    REF  GGTGA
    ALT  G
```

### `NM_015910:c.512_515del` — coding_del

```
Variant Recoder = hgvs2vcf:
  NC_000002.12:63437538
    REF  ACTGT
    ALT  A
```

### `NM_018192:c.722del` — coding_del

```
Variant Recoder = hgvs2vcf:
  NC_000003.12:189994194
    REF  GA
    ALT  G
```

### `NM_018417:c.4477del` — coding_del

```
Variant Recoder = hgvs2vcf:
  NC_000001.11:167818076
    REF  AG
    ALT  A
```

### `NM_020779:c.1468del` — coding_del

```
Variant Recoder = hgvs2vcf:
  NC_000002.12:19951416
    REF  TG
    ALT  T
```

### `NM_172107:c.2333del` — coding_del

```
Variant Recoder = hgvs2vcf:
  NC_000020.11:63406929
    REF  CT
    ALT  C
```

### `NM_206933:c.6225_6227del` — coding_del

```
Variant Recoder = hgvs2vcf:
  NC_000001.11:216046528
    REF  GTTC
    ALT  G
```

### `NOTCH1:c.456_458del` — coding_del

```
Variant Recoder = hgvs2vcf:
  NC_000009.12:136523133
    REF  GCCA
    ALT  G
```

### `PALB2:c.2127_2128del` — coding_del

```
Variant Recoder = hgvs2vcf:
  NC_000016.10:23630025
    REF  GTA
    ALT  G
```

### `PKD1:c.5883_5929del` — coding_del

```
Variant Recoder = hgvs2vcf:
  NC_000016.10:2109237
    REF  GGCACCTGCA GCCCACTCAC GGCCTCCAGC ACCACGATGC GCACCTGC
    ALT  G
```

### `PKD1:c.99del` — coding_del

```
Variant Recoder = hgvs2vcf:
  NC_000016.10:2135590
    REF  CG
    ALT  C
```

### `SCN1A:c.3305del` — coding_del

```
Variant Recoder = hgvs2vcf:
  NC_000002.12:166036171
    REF  GT
    ALT  G
```

### `SPI1:c.443_445del` — coding_del

```
Variant Recoder = hgvs2vcf:
  NC_000011.10:47358891
    REF  TCGC
    ALT  T
```

### `SPTB:c.3332del` — coding_del

```
Variant Recoder = hgvs2vcf:
  NC_000014.9:64786632
    REF  GT
    ALT  G
```

### `ST3GAL5:c.374_381del` — coding_del

```
Variant Recoder = hgvs2vcf:
  NC_000002.12:85848141
    REF  ATGTCTTGG
    ALT  A
```

### `TBL1XR1:c.1189del` — coding_del

```
Variant Recoder = hgvs2vcf:
  NC_000003.12:177034258
    REF  AT
    ALT  A
```

### `USH2A:c.10714del` — coding_del

```
Variant Recoder = hgvs2vcf:
  NC_000001.11:215782067
    REF  AC
    ALT  A
```

### `ZC4H2:c.218_220del` — coding_del

```
Variant Recoder = hgvs2vcf:
  NC_000023.11:64921821
    REF  TTGA
    ALT  T
```

### `APC:c.578_584delinsTAAGGCT` — coding_delins

```
Variant Recoder = hgvs2vcf:
  NC_000005.10:112780836
    REF  CAAGGCA
    ALT  TAAGGCT
```

### `NM_001365999:c.7466_7467delinsTT` — coding_delins

```
Variant Recoder = hgvs2vcf:
  NC_000001.11:43441335
    REF  GA
    ALT  TT
```

### `NM_004656:c.2124_2125delinsTA` — coding_delins

```
Variant Recoder = hgvs2vcf:
  NC_000003.12:52402353
    REF  GC
    ALT  TA
```

### `NM_005876:c.259_260delinsAA` — coding_delins

```
Variant Recoder = hgvs2vcf:
  NC_000002.12:219435236
    REF  GC
    ALT  AA
```

### `NM_015311:c.2577_2578delinsTT` — coding_delins

```
Variant Recoder = hgvs2vcf:
  NC_000002.12:219563457
    REF  GC
    ALT  AA
```

### `NM_017617:c.5273_5274delinsAA` — coding_delins

```
Variant Recoder = hgvs2vcf:
  NC_000009.12:136502382
    REF  GC
    ALT  TT
```

### `NM_182961:c.17386_17387delinsAA` — coding_delins

```
Variant Recoder = hgvs2vcf:
  NC_000006.12:152302023
    REF  GC
    ALT  TT
```

### `NM_198075:c.728_729delinsTA` — coding_delins

```
Variant Recoder = hgvs2vcf:
  NC_000011.10:551234
    REF  CG
    ALT  TA
```

### `TTN:c.63303_63304delinsTT` — coding_delins

```
Variant Recoder = hgvs2vcf:
  NC_000002.12:178588103
    REF  CC
    ALT  AA
```

### `ALMS1:c.790dup` — coding_dup

```
Variant Recoder = hgvs2vcf:
  NC_000002.12:73424454
    REF  T
    ALT  TA
```

### `ARID1A:c.750_771dup` — coding_dup

```
Variant Recoder = hgvs2vcf:
  NC_000001.11:26697152
    REF  A
    ALT  AGCCGCCTCC CTCCTCCAGC GCC
```

### `BEST1:c.194dup` — coding_dup

```
Variant Recoder = hgvs2vcf:
  NC_000011.10:61955147
    REF  C
    ALT  CT
```

### `NIPBL:c.3547dup` — coding_dup

```
Variant Recoder = hgvs2vcf:
  NC_000005.10:37000860
    REF  A
    ALT  AG
```

### `NM_000051:c.5524dup` — coding_dup

```
Variant Recoder = hgvs2vcf:
  NC_000011.10:108304701
    REF  A
    ALT  AC
```

### `NM_000179:c.692_693dup` — coding_dup

```
Variant Recoder = hgvs2vcf:
  NC_000002.12:47798674
    REF  G
    ALT  GTA
```

### `NM_000327:c.180dup` — coding_dup

```
Variant Recoder = hgvs2vcf:
  NC_000011.10:62613460
    REF  C
    ALT  CT
```

### `NM_001042492:c.4051dup` — coding_dup

```
Variant Recoder = hgvs2vcf:
  NC_000017.11:31249059
    REF  C
    ALT  CA
```

### `NM_001177316:c.1467_1477dup` — coding_dup

```
Variant Recoder = hgvs2vcf:
  NC_000009.12:137236082
    REF  G
    ALT  GGGTCTACCT GC
```

### `NM_006767:c.112dup` — coding_dup

```
Variant Recoder = hgvs2vcf:
  NC_000022.11:20982482
    REF  T
    ALT  TG
```

### `NM_014956:c.4255_4262dup` — coding_dup

```
Variant Recoder = hgvs2vcf:
  NC_000011.10:117411885
    REF  G
    ALT  GTGGCTGGA
```

### `ATM:c.8059_8060insT` — coding_ins

```
Variant Recoder = hgvs2vcf:
  NC_000011.10:108335017
    REF  A
    ALT  AT
```

### `BICRA:c.1509_1510insA` — coding_ins

```
Variant Recoder = hgvs2vcf:
  NC_000019.10:47680679
    REF  C
    ALT  CA
```

### `CPT2:c.28_29insAGCAAG` — coding_ins

```
Variant Recoder = hgvs2vcf:
  NC_000001.11:53196971
    REF  T
    ALT  TAGCAAG
```

### `MYBPC3:c.3228_3229insT` — coding_ins

```
Variant Recoder = hgvs2vcf:
  NC_000011.10:47333295
    REF  C
    ALT  CA
```

### `NM_001369369:c.1910_1911insG` — coding_ins

```
Variant Recoder = hgvs2vcf:
  NC_000017.11:28537399
    REF  A
    ALT  AG
```

### `NM_007294:c.3814_3815insT` — coding_ins

```
Variant Recoder = hgvs2vcf:
  NC_000017.11:43091716
    REF  T
    ALT  TA
```

### `NM_007294:c.770_771insGA` — coding_ins

```
Variant Recoder = hgvs2vcf:
  NC_000017.11:43094760
    REF  A
    ALT  ATC
```

### `PALB2:c.521_522insCA` — coding_ins

```
Variant Recoder = hgvs2vcf:
  NC_000016.10:23636024
    REF  T
    ALT  TTG
```

### `PAX3:c.422_423insTCCTTTCTCTGTCTCCACAAGCAGCAGTGCCTGTGTCACCTGTTACATCTTGGGACAGAGACCACAGCAGCGGCAGG` — coding_ins

```
Variant Recoder = hgvs2vcf:
  NC_000002.12:222295556
    REF  C
    ALT  CCCTGCCGCT GCTGTGGTCT CTGTCCCAAG ATGTAACAGG TGACACAGGC ACTGCTGCTT
         GTGGAGACAG AGAAAGGA
```

### `NM_018389:c.717_718inv` — coding_other

```
Variant Recoder = hgvs2vcf:
  NC_000011.10:45810957
    REF  CA
    ALT  TG
```

### `ADGRV1:c.12008T>C` — coding_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000005.10:90759476
    REF  T
    ALT  C
```

### `AKAP9:c.7023G>A` — coding_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000007.14:92079156
    REF  G
    ALT  A
```

### `CFTR:c.4335C>G` — coding_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000007.14:117667000
    REF  C
    ALT  G
```

### `DEF6:c.891G>A` — coding_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000006.12:35317974
    REF  G
    ALT  A
```

### `DNAH5:c.12210C>T` — coding_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000005.10:13721069
    REF  G
    ALT  A
```

### `FDX2:c.111G>A` — coding_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000019.10:10315886
    REF  C
    ALT  T
```

### `GALNT12:c.1386C>A` — coding_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000009.12:98844137
    REF  C
    ALT  A
```

### `GPI:c.1574T>C` — coding_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000019.10:34399933
    REF  T
    ALT  C
```

### `HPS3:c.2877A>G` — coding_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000003.12:149167973
    REF  A
    ALT  G
```

### `ITGB4:c.3463A>G` — coding_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000017.11:75750257
    REF  A
    ALT  G
```

### `JMJD1C:c.1399C>G` — coding_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000010.11:63214768
    REF  G
    ALT  C
```

### `KIF7:c.1485G>A` — coding_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000015.10:89647671
    REF  C
    ALT  T
```

### `KRT5:c.58G>A` — coding_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000012.12:52520239
    REF  C
    ALT  T
```

### `LCA5:c.634G>C` — coding_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000006.12:79513298
    REF  C
    ALT  G
```

### `LDB1:c.607C>T` — coding_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000010.11:102109962
    REF  G
    ALT  A
```

### `LITAF:c.429C>T` — coding_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000016.10:11549694
    REF  G
    ALT  A
```

### `LONP1:c.1924A>G` — coding_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000019.10:5696143
    REF  T
    ALT  C
```

### `MYOM1:c.2125T>C` — coding_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000018.10:3135631
    REF  A
    ALT  G
```

### `NM_000038:c.6883T>G` — coding_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000005.10:112842477
    REF  T
    ALT  G
```

### `NM_000391:c.840G>C` — coding_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000011.10:6616707
    REF  C
    ALT  G
```

### `NM_001004471:c.254T>C` — coding_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000011.10:58228622
    REF  A
    ALT  G
```

### `NM_001098484:c.2051A>T` — coding_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000004.12:71497577
    REF  A
    ALT  T
```

### `NM_001161417:c.787C>T` — coding_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000002.12:127651522
    REF  C
    ALT  T
```

### `NM_001267550:c.28434C>T` — coding_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000002.12:178710663
    REF  G
    ALT  A
```

### `NM_001271696:c.1492G>A` — coding_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000023.11:75069328
    REF  C
    ALT  T
```

### `NM_002386:c.96A>G` — coding_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000016.10:89919354
    REF  A
    ALT  G
```

### `NM_002637:c.2062C>T` — coding_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000023.11:72620800
    REF  G
    ALT  A
```

### `NM_003014:c.760G>A` — coding_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000007.14:37912150
    REF  C
    ALT  T
```

### `NM_004136:c.313G>A` — coding_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000015.10:78465291
    REF  G
    ALT  A
```

### `NM_004984:c.767A>G` — coding_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000012.12:57569015
    REF  A
    ALT  G
```

### `NM_006947:c.378T>C` — coding_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000004.12:56474077
    REF  T
    ALT  C
```

### `NM_007294:c.2913T>G` — coding_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000017.11:43092618
    REF  A
    ALT  C
```

### `NM_013339:c.665G>A` — coding_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000001.11:63411316
    REF  G
    ALT  A
```

### `NM_015450:c.896C>T` — coding_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000007.14:124851925
    REF  G
    ALT  A
```

### `NM_015512:c.12198G>A` — coding_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000003.12:52398958
    REF  G
    ALT  A
```

### `NM_018121:c.2650C>G` — coding_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000010.11:100938732
    REF  C
    ALT  G
```

### `NM_018946:c.219G>A` — coding_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000009.12:98060868
    REF  G
    ALT  A
```

### `NM_020207:c.4061C>T` — coding_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000009.12:96012611
    REF  C
    ALT  T
```

### `NM_020759:c.10946G>A` — coding_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000015.10:42692524
    REF  G
    ALT  A
```

### `NM_024535:c.578G>A` — coding_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000016.10:4395326
    REF  C
    ALT  T
```

### `NM_031935:c.9035T>C` — coding_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000001.11:186086396
    REF  T
    ALT  C
```

### `NM_033109:c.1033A>G` — coding_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000002.12:55667902
    REF  T
    ALT  C
```

### `NM_144646:c.58G>A` — coding_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000004.12:70666433
    REF  C
    ALT  T
```

### `NM_182476:c.24A>G` — coding_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000014.9:73950356
    REF  A
    ALT  G
```

### `ORC1:c.271C>T` — coding_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000001.11:52397816
    REF  G
    ALT  A
```

### `PLA2R1:c.439A>G` — coding_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000002.12:160044828
    REF  T
    ALT  C
```

### `PSAT1:c.173A>G` — coding_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000009.12:78302005
    REF  A
    ALT  G
```

### `QDPR:c.48C>G` — coding_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000004.12:17512007
    REF  G
    ALT  C
```

### `RYR1:c.10207C>T` — coding_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000019.10:38519402
    REF  C
    ALT  T
```

### `SAMHD1:c.78T>C` — coding_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000020.11:36951566
    REF  A
    ALT  G
```

### `SLC4A9:c.829C>T` — coding_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000005.10:140362933
    REF  C
    ALT  T
```

### `SOAT1:c.550G>A` — coding_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000001.11:179341080
    REF  G
    ALT  A
```

### `DICER1:c.1752+14_1752+15del` — intronic_del

```
Variant Recoder = hgvs2vcf:
  NC_000014.9:95116437
    REF  AAT
    ALT  A
```

### `DICER1:c.904-5del` — intronic_del

```
Variant Recoder = hgvs2vcf:
  NC_000014.9:95124672
    REF  CA
    ALT  C
```

### `DNAH5:c.3263-3del` — intronic_del

```
Variant Recoder = hgvs2vcf:
  NC_000005.10:13876819
    REF  TA
    ALT  T
```

### `HNRNPA2B1:c.658+7_658+8del` — intronic_del

```
Variant Recoder = hgvs2vcf:
  NC_000007.14:26196392
    REF  GAA
    ALT  G
```

### `HPS5:c.109-10_109-9del` — intronic_del

```
Variant Recoder = hgvs2vcf:
  NC_000011.10:18312032
    REF  CAT
    ALT  C
```

### `IQCB1:c.767-228_767-226del` — intronic_del

```
Variant Recoder = hgvs2vcf:
  NC_000003.12:121797452
    REF  TAAA
    ALT  T
```

### `MECP2:c.413+6_413+9del` — intronic_del

```
Variant Recoder = hgvs2vcf:
  NC_000023.11:154032197
    REF  TCTTA
    ALT  T
```

### `MYLK:c.5369-14_5369-12del` — intronic_del

```
Variant Recoder = hgvs2vcf:
  NC_000003.12:123618781
    REF  GAGA
    ALT  G
```

### `NM_000187:c.87+8_88-31del` — intronic_del

```
Variant Recoder = hgvs2vcf:
  NC_000003.12:120675019
    REF  ACTCCCATCC GAAAAGCATC CCACCTTCCC ACCAACCAAC TCAGTAGGGG GATGGGGATG
         CTCTGGGCGA CTGCACATGA CCATCTGCAA CCCGATATGT TTCTTGTAAC AACTTTTGAT
         GTGACTTGCC CCCCGATTAT AAAAGTAATA TATATTTATT GTAGAAAATG TATAAACTAT
         ATGATAACAC CCATTATCTC ACAACCAGAA ATAACCAAGC GTTCACATGT TGGTATTTTT
         CCTTGCATTC TTATCCTCCA AAATTGTGAC CCTATCATAC CTGTAACCCT GTAATAATCA
         GGCATTTTTT CCTTTTTTTT TTTAAGAAAT GAGGATTTTT TTATGCTATG ATACGGCCTG
         CAAAAAGTTT TGAAAATATT TTTGTTTCCC GTGTTGTTGC TTTTCTAACC AGCACTAGTA
         TGAACATCTT TGTGCATACA TGTGAAAGCA CCTTGTTATT TTATCATAAT GCTCACATCC
         ATGGTGTTCA AGGGGAATAT GAGGGATTCT CTTTAACTCT GGATTTTTGG GGATCCTACT
         GGAAACCCTA CAGTTAATTT CACTAGTTTG GATTGGCTGC TGTGCCACCA ATCCAATTTT
         AATCTTTGTG TTGTCATTGC TCTGTATCTT CATTGCCCCT ATGACTTGGG AAACCTCTAG
         ACAGTTCACA GGCTAGATTG GAAGAGCCAC GGTGGGTGGA GGCACTTTGG CCTGAAAGCT
         AGTCATCCAG GAATAGGATT CAGAGCTCTT CTAAGCACTT TATTTG
    ALT  A
```

### `NM_000257:c.4953+11del` — intronic_del

```
Variant Recoder = hgvs2vcf:
  NC_000014.9:23415992
    REF  CT
    ALT  C
```

### `NM_001080449:c.442-768_587+648del` — intronic_del

```
Variant Recoder = hgvs2vcf:
  NC_000010.11:68465018
    REF  ATTTTTTTTT TTTTTTTTTG AGATGGAGTC TTGCTTTGTC ACCCAGGCTG GAGTGCAGTG
         GTGTGATCTC GGCTCACTGC AAGCTCTACC TCCCGGGTTC ACACCATTCT CCTGCCTCAG
         CCTTCCGAGT AGCTGGGACT ACAGGCGCCT GCCACCATGC CCTGCTAATT TTTTGTATTT
         TTAGTAGAGA CGGGGTTTCA CCATGTTAGC CAGGATGGTC TCGATTTCCT GACTTCTGAT
         CCGCCCACCT CGGCCTCCCA AAGTGCTGGG ATTACAGGCG TGAGCCACCG CACCTGGCCG
         TAAAGATGCA CTTTGAAACC AGTTTCATCT TCTTCCCAAC CCCATATAAT TCTCAGTATA
         TCACACTGTT TCTAGAACTA ATGCAAAAAA GTTCTTTATA CATTCTCTGA AAGTACTTAA
         GGAATCTGTT ATGCACATGT ACAAAATATT TAGGTATTTT TACCCAAAAA GTTCCTGTTG
         AGCAATTTCA GAAACTCTTC ACAGAGTTCC AACAATGTAC TAGAACTATG AAATCTGCAT
         TTTAGATTAC ACTAATTTAT ATTGGATAGT CTACACAAAT ACTTTATAGT TTCTAGGACA
         GAAGTTATAT AATAAAATTA TACCTGCAGT TCTTCTTATA ACTACTTACA TTTCCTTCAA
         ATGTCTTATT TCTTGAATTG TTTGAAAAGC AAGTTCTTGT AGCTTTTCTG GGGCAAAGCT
         ATTATTTATG GCTTTTTGAA ACACCTCATG GAGAACCGTA CCAATTAGCA TTTGGCGTGT
         GGCTGGATCA GAGCTCTACA AAAGCAAATC ACACAGTTTA TTTCACAACA TATTAACAGA
         CACAATTGTA TATTTATTAC CTAATCTATT AAACCACCAT AGCCAAAATG CACTGGTAAG
         ACAAATGCCA AAATATTAAA AAAATTTTTT TCTGGTGCGT GGAATTATAA GTGACTTTCA
         CTTTCTTCTA TCCAGAATTG TCTGAATTAC TGTATGAGTT ATCCTTTTTT TTTTCTTTTT
         TGAGACAGAG TCTTGCTCTG TCACCCAGGC TGGAGCACAG TGGCACAATC TCAGCTCACT
         GCAACCTTCA TCTCCCAGGT TCAAATGATT CTCATGCCTC AACCTCCCAA GTAGCTGGAA
         TTACAGGTGT GTGCTATCAT GCCCGGCTAA CTTTTATTTT TTGTATTTTT AGTAGAGGCA
         GGGTTTCACC ATGTTGGCCA GGCTGATATG AATTACTTTT AAAATCAATG TTCTCCATTT
         TGAAAAAAAT TAAAATAACC AATATTTTAA AATTCAAAAT ATTCTCAAAT AATTAATATT
         TAAAGTATTG TTCTCTTATT TCACTTGATA ATCCACCCAA TAGAAAAGTC AATAAAGGCA
         TAGCTGATAA ACTCATGTAA GTAAAAGATA CCATTCAAAC ATAAAATGTA AACCTACTTA
         GCAGTAATGT TTGGGAAGAA AAAAAATTTT TTTAACCTAC AGCAGAGATT TTTGGCAAGG
         AATTTTTCTC CACTCAAAAA GAAACACTAC ATTTCTTGAT TAACTCTTGT ATTAGCCTAG
         ACC
    ALT  A
```

### `NM_001278116:c.2431+300_2431+311del` — intronic_del

```
Variant Recoder = hgvs2vcf:
  NC_000023.11:153866337
    REF  GAAAAGAAAA GAA
    ALT  G
```

### `NM_001660:c.259-7del` — intronic_del

```
Variant Recoder = hgvs2vcf:
  NC_000003.12:57577393
    REF  GA
    ALT  G
```

### `NM_003292:c.790-4del` — intronic_del

```
Variant Recoder = hgvs2vcf:
  NC_000001.11:186361872
    REF  GA
    ALT  G
```

### `NM_004268:c.860-17del` — intronic_del

```
Variant Recoder = hgvs2vcf:
  NC_000011.10:93794890
    REF  AT
    ALT  A
```

### `NM_004656:c.438-7del` — intronic_del

```
Variant Recoder = hgvs2vcf:
  NC_000003.12:52407322
    REF  GA
    ALT  G
```

### `NM_004963:c.1930+1del` — intronic_del

```
Variant Recoder = hgvs2vcf:
  NC_000012.12:14643572
    REF  AC
    ALT  A
```

### `NM_006231:c.2026+18_2026+62del` — intronic_del

```
Variant Recoder = hgvs2vcf:
  NC_000012.12:132668572
    REF  AAGGCGGCCG ACACTCACCC ACCCGTTTCC CACCGAGTGC CCACCC
    ALT  A
```

### `NM_014291:c.815-2_815-1del` — intronic_del

```
Variant Recoder = hgvs2vcf:
  NC_000022.11:37815660
    REF  CAG
    ALT  C
```

### `NM_015662:c.4815+10del` — intronic_del

```
Variant Recoder = hgvs2vcf:
  NC_000002.12:27445918
    REF  TC
    ALT  T
```

### `NM_016122:c.1812-9_1812-5del` — intronic_del

```
Variant Recoder = hgvs2vcf:
  NC_000012.12:94310111
    REF  AAAAAG
    ALT  A
```

### `NM_018100:c.1492+175_1492+176del` — intronic_del

```
Variant Recoder = hgvs2vcf:
  NC_000006.12:52479424
    REF  CTT
    ALT  C
```

### `PCDH15:c.4368-2189_4368-2154del` — intronic_del

```
Variant Recoder = hgvs2vcf:
  NC_000010.11:53822383
    REF  GGGAGGAGGA CAAAAAAGAG AAAAAGGAGA AATGTCA
    ALT  G
```

### `PFKM:c.85+16del` — intronic_del

```
Variant Recoder = hgvs2vcf:
  NC_000012.12:48122874
    REF  AC
    ALT  A
```

### `PLEC:c.4045-7_4045-5del` — intronic_del

```
Variant Recoder = hgvs2vcf:
  NC_000008.11:143925888
    REF  TGGC
    ALT  T
```

### `SCRIB:c.4770+8del` — intronic_del

```
Variant Recoder = hgvs2vcf:
  NC_000008.11:143791657
    REF  GC
    ALT  G
```

### `SKA3:c.829+1_830-1del` — intronic_del

```
Variant Recoder = hgvs2vcf:
  NC_000013.11:21159987
    REF  TCTAAAAGAC ACATAAAATG GTCATTAAAA AACTATAACT ATAGTATGCT TAACTGGACA
         GGAAGAAAAT CTCATATTTA CATATGTAAT TATCATTAGC ACTACTAAAA TTCAGCAAGG
         ATGCAAGAGT AATACACAAT AACAAATAGT TGTGTTGTAA TATATATTAA ACATAAAAGC
         AACAAACTAT TACACATATA ATTTGAAAAA AGATACTTTT CACAGTAGCA AGAAAGACAA
         GATACCTACA AATATATCTA TTAAAAATGG TGTAAAACCT TTATGAAGAA AATTATCAAA
         CTTCTGACAA AGGAGGAGGA AGACGGAGAA CAGGTCACTT GTCTTCCAAG ATGGCAGGAC
         TTACTCCAAA GGTACAGTAG TTAAAAACAG TGTAACATTA ACCAGGGATG GAAAAATTAA
         AGATAAGAAC AAGAGAGACC CATGCATATA TAGACAAGAG AGACCCATGC ATATATAGAC
         AATTGCTATC TAGAACACAT AGTATCATCG AGGCAACCTT AAAAAACAAC AAAGAGAAAA
         GGTAAATATG TTAGAAAAAC AATCTGACTG GCAAAATATC TGAAGTCTAA AAATCATCAA
         GTACTGGAAA AGACGGAGAA ACAGGAACTC AATACCACTA GTGAGAAGAT AAATCTTAAC
         AGCTACTCTT AGCTGACTAT TCAGCATTTT CTAGAATAAG TAAAAATGTG CATGCCCTTT
         GACCTGGCAA TTCTACTCCT AGATATGAGA AACACGCATA TGCACAAGGG AAAATTTCCT
         TAAGGCACTG CCTATAATAA TAAAAAATGA AAACACTACC TCCTAATCAG CAAATGAATA
         TGGCTCATAT ATACAGTAGA ATACTATTTA TCAATTAAAA AGGATGAAGT GCTTTGGGAG
         GCCAAGGTGG GCAGATCGCT TGAGTCCAGG AGTTTGAGGC CAGCATTGGC AACATGGTGA
         AACCCCTCTA CCAAAAAAAT ACAAACATTA GCTGGGCATG GTGGTGTAAG CCTGTAGTCC
         CTGCTACGTG GGGGCTGAGG TGGGAGGACT GGTTGAGCCC AAGAGGCGGA GGTTGCAATG
         AGTTGTCTAC AGTTGTGACC AGCCTGGGCA ACATGGCGAA ACCCCATCTA TACAAAAAAT
         ACAAAAATTA GCTGGACGTC GTGGTGTGTG CCTATAGTCT CGGATACTTG AGAGGATTGC
         TTGAGCCTGG GAAGTTGAGG CTGCAGTGAG CCAAGATCGT GCCACTACAC TCCAGTCTGG
         GCAACAGAGT GAGACCCTGT CTCAAAGAAA ACAAAACAAA AAAATCATAA AACTCTAGGA
         TTTTTTTATC TTGCTTTTTC ATGAACACCA ATGTTTTCAT GTTTGCTGGG ACAAATATGA
         AAACACTGTA TGAAAATTTT CTTTAAGTTA CTGAGCTATT TAAAAGAAAC CAAAATTTAA
         ATTGGCAGCT GATGTATTCC GTGCGTGGTT TATATAAGAT AATGTACAAC TCTAATCAAT
         AGGTTAAAAG AAAAAGTACT AAGGCTCTAC ATCAAAATAT TGGTGAATAT GTAAGTTTCA
         AATTAAAATG TTAATAACAA GCTGACAGAT ATTGAACATA ATCAAGAGTA TTAAAAACAT
         ACCAGAAAAT TTTCTTTCTC TTGGACAAAA TCATGCTGAA TGAAATGGTA CTTAATGTAA
         TCCAATGTTA GGAATTAAAC AGATGAAGAA AACTATTAGA ATGTCTAAGA TGATGAAATC
         AATTTTGTTC AAAGATAGTT TGGGAAAAAT GTTCCTGAGA AGTAACTTGA TTCTTATACT
         TAC
    ALT  T
```

### `SUFU:c.318-22_318-19del` — intronic_del

```
Variant Recoder = hgvs2vcf:
  NC_000010.11:102549947
    REF  CACTT
    ALT  C
```

### `TBCE:c.898+6del` — intronic_del

```
Variant Recoder = hgvs2vcf:
  NC_000001.11:235436455
    REF  AT
    ALT  A
```

### `TRERF1:c.2746-6del` — intronic_del

```
Variant Recoder = hgvs2vcf:
  NC_000006.12:42243366
    REF  CG
    ALT  C
```

### `WDR83OS:c.255-4_260del` — intronic_del

```
Variant Recoder = hgvs2vcf:
  NC_000019.10:12668419
    REF  GGACAGCCTG A
    ALT  G
```

### `ALDH7A1:c.193-15_193-9delinsCCCTTTG` — intronic_delins

```
Variant Recoder = hgvs2vcf:
  NC_000005.10:126593413
    REF  AAAAGGA
    ALT  CAAAGGG
```

### `NM_004984:c.129+6_129+7delinsCC` — intronic_delins

```
Variant Recoder = hgvs2vcf:
  NC_000012.12:57550406
    REF  TG
    ALT  CC
```

### `SATB1:c.1779+680_1779+681delinsAA` — intronic_delins

```
Variant Recoder = hgvs2vcf:
  NC_000003.12:18351311
    REF  AC
    ALT  TT
```

### `NM_000019:c.580-5dup` — intronic_dup

```
Variant Recoder = hgvs2vcf:
  NC_000011.10:108140059
    REF  T
    ALT  TA
```

### `MAP3K7:c.483-8_483-7insC` — intronic_ins

```
Variant Recoder = hgvs2vcf:
  NC_000006.12:90556631
    REF  A
    ALT  AG
```

### `NM_145207:c.289-8_289-7insAACATTTATTTC` — intronic_ins

```
Variant Recoder = hgvs2vcf:
  NC_000004.12:122929032
    REF  T
    ALT  TAACATTTAT TTC
```

### `PNKP:c.1298+13_1298+14insA` — intronic_ins

```
Variant Recoder = hgvs2vcf:
  NC_000019.10:49861758
    REF  C
    ALT  CT
```

### `ATM:c.7308-15A>G` — intronic_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000011.10:108330199
    REF  A
    ALT  G
```

### `ATP13A3:c.2421+8C>G` — intronic_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000003.12:194431709
    REF  G
    ALT  C
```

### `ATP1A3:c.6+9T>C` — intronic_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000019.10:41994062
    REF  A
    ALT  G
```

### `CCDC39:c.930+12C>A` — intronic_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000003.12:180654750
    REF  G
    ALT  T
```

### `CDH23:c.337-16G>A` — intronic_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000010.11:71511104
    REF  G
    ALT  A
```

### `CEP95:c.367+12A>T` — intronic_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000017.11:64514370
    REF  A
    ALT  T
```

### `COL17A1:c.4357+18G>A` — intronic_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000010.11:104032888
    REF  C
    ALT  T
```

### `COL5A2:c.97+10C>T` — intronic_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000002.12:189179498
    REF  G
    ALT  A
```

### `COQ7:c.73+36T>G` — intronic_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000016.10:19067773
    REF  T
    ALT  G
```

### `CTNNA1:c.1062+3189T>C` — intronic_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000005.10:138830907
    REF  T
    ALT  C
```

### `CYBC1:c.128-150G>T` — intronic_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000017.11:82446846
    REF  C
    ALT  A
```

### `DICER1:c.4051-5T>A` — intronic_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000014.9:95099940
    REF  A
    ALT  T
```

### `FASN:c.2100+6C>T` — intronic_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000017.11:82089244
    REF  G
    ALT  A
```

### `IARS1:c.1305-5T>G` — intronic_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000009.12:92268305
    REF  A
    ALT  C
```

### `KCNMA1:c.1334+12C>G` — intronic_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000010.11:77090388
    REF  G
    ALT  C
```

### `KMT2B:c.6960-4C>T` — intronic_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000019.10:35733593
    REF  C
    ALT  T
```

### `LRP5:c.4001-18C>G` — intronic_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000011.10:68436871
    REF  C
    ALT  G
```

### `MLH1:c.1897-3C>T` — intronic_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000003.12:37048514
    REF  C
    ALT  T
```

### `NM_000260:c.5856+13C>T` — intronic_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000011.10:77207415
    REF  C
    ALT  T
```

### `NM_000310:c.234+7C>A` — intronic_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000001.11:40092391
    REF  G
    ALT  T
```

### `NM_000435:c.5362+20C>T` — intronic_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000019.10:15167229
    REF  G
    ALT  A
```

### `NM_001037283:c.1290-5C>G` — intronic_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000007.14:2366520
    REF  C
    ALT  G
```

### `NM_001244008:c.1769-11C>T` — intronic_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000002.12:240763357
    REF  G
    ALT  A
```

### `NM_001290223:c.2847+47707G>A` — intronic_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000010.11:127175471
    REF  G
    ALT  A
```

### `NM_001363:c.513+20G>A` — intronic_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000023.11:154767081
    REF  G
    ALT  A
```

### `NM_001384140:c.876+2T>C` — intronic_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000010.11:54317269
    REF  A
    ALT  G
```

### `NM_001384474:c.3619+10C>A` — intronic_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000018.10:46545307
    REF  G
    ALT  T
```

### `NM_001556:c.1364+5C>T` — intronic_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000008.11:42318680
    REF  C
    ALT  T
```

### `NM_002150:c.324+8A>G` — intronic_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000012.12:121856316
    REF  T
    ALT  C
```

### `NM_002224:c.627+5G>C` — intronic_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000006.12:33659124
    REF  G
    ALT  C
```

### `NM_002474:c.1749+17C>T` — intronic_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000016.10:15756324
    REF  G
    ALT  A
```

### `NM_003070:c.4461+195T>C` — intronic_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000009.12:2182437
    REF  T
    ALT  C
```

### `NM_003072:c.3382+17G>A` — intronic_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000019.10:11027967
    REF  G
    ALT  A
```

### `NM_005751:c.11686+4C>T` — intronic_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000007.14:92108637
    REF  C
    ALT  T
```

### `NM_005993:c.3480-19G>T` — intronic_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000017.11:82941380
    REF  G
    ALT  T
```

### `NM_017617:c.5168-5C>G` — intronic_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000009.12:136502493
    REF  G
    ALT  C
```

### `NM_018288:c.195-17T>A` — intronic_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000006.12:169718935
    REF  A
    ALT  T
```

### `NM_022458:c.424-15649G>C` — intronic_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000007.14:156779444
    REF  C
    ALT  G
```

### `NM_022475:c.630-177G>T` — intronic_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000004.12:144659460
    REF  G
    ALT  T
```

### `NM_058216:c.572-16T>G` — intronic_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000017.11:58703180
    REF  T
    ALT  G
```

### `NM_133459:c.655-155A>T` — intronic_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000018.10:59448258
    REF  T
    ALT  A
```

### `NM_153704:c.1861-13A>G` — intronic_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000008.11:93797121
    REF  A
    ALT  G
```

### `NM_206933:c.2809+2T>A` — intronic_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000001.11:216246583
    REF  A
    ALT  T
```

### `NM_206943:c.4985-57G>T` — intronic_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000002.12:33398307
    REF  G
    ALT  T
```

### `OBSCN:c.21533-2384G>T` — intronic_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000001.11:228360192
    REF  G
    ALT  T
```

### `PHKB:c.1514+1G>T` — intronic_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000016.10:47641091
    REF  G
    ALT  T
```

### `PLCD1:c.790+92C>G` — intronic_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000003.12:38011122
    REF  G
    ALT  C
```

### `PLEKHN1:c.1294-11C>G` — intronic_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000001.11:973489
    REF  C
    ALT  G
```

### `PTPRC:c.658+16G>C` — intronic_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000001.11:198703388
    REF  G
    ALT  C
```

### `SOS2:c.3337+20C>T` — intronic_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000014.9:50130481
    REF  G
    ALT  A
```

### `TCIRG1:c.504-15C>A` — intronic_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000011.10:68043356
    REF  C
    ALT  A
```

### `TOP2B:c.640-7T>C` — intronic_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000003.12:25636155
    REF  A
    ALT  G
```

### `CNOT1:p.Cys2125del` — protein_del

```
Variant Recoder = hgvs2vcf:
  NC_000016.10:58528552
    REF  TACA
    ALT  T
```

### `COL6A3:p.Val1219_Pro1222del` — protein_del

```
Variant Recoder = hgvs2vcf:
  NC_000002.12:237374424
    REF  GAGGCTGCAA CAC
    ALT  G
```

### `DYNC1H1:p.Pro2628del` — protein_del

```
Variant Recoder = hgvs2vcf:
  NC_000014.9:102017120
    REF  TCCA
    ALT  T
```

### `FOXG1:p.Ala62_Pro69del` — protein_del

```
Variant Recoder = hgvs2vcf:
  NC_000014.9:28767462
    REF  CGCCCCGCAA CCGCCGCCGC CGCCG
    ALT  C
```

### `NAF1:p.Asp159del` — protein_del

```
Variant Recoder = hgvs2vcf:
  NC_000004.12:163164279
    REF  AATC
    ALT  A
```

### `PKD1:p.Ile1374del` — protein_del

```
Variant Recoder = hgvs2vcf:
  NC_000016.10:2111044
    REF  AGAT
    ALT  A
```

### `PKP2:p.Arg534del` — protein_del

```
Variant Recoder = hgvs2vcf:
  NC_000012.12:32824116
    REF  ATCT
    ALT  A
```

### `SYNGAP1:p.Trp1315_Pro1321del` — protein_del

```
Variant Recoder = hgvs2vcf:
  NC_000006.12:33451816
    REF  GTGGAATGGC CTGGCCCCCC CA
    ALT  G
```

### `TBX5:p.His220del` — protein_del

```
Variant Recoder = hgvs2vcf:
  NC_000012.12:114394743
    REF  TGTG
    ALT  T
```

### `ACTA2:p.Val300=` — protein_other

```
Variant Recoder = hgvs2vcf:
  NC_000010.11:88938151
    REF  G
    ALT  A
  NC_000010.11:88938151
    REF  G
    ALT  T
  NC_000010.11:88938151
    REF  G
    ALT  C
```

### `ANLN:p.Thr1018=` — protein_other

```
Variant Recoder = hgvs2vcf:
  NC_000007.14:36443838
    REF  T
    ALT  C
  NC_000007.14:36443838
    REF  T
    ALT  A
  NC_000007.14:36443838
    REF  T
    ALT  G
```

### `ASGR2:p.Gly303=` — protein_other

```
Variant Recoder = hgvs2vcf:
  NC_000017.11:7101587
    REF  G
    ALT  A
  NC_000017.11:7101587
    REF  G
    ALT  T
  NC_000017.11:7101587
    REF  G
    ALT  C
```

### `B3GALNT2:p.Pro28=` — protein_other

```
Variant Recoder = hgvs2vcf:
  NC_000001.11:235504169
    REF  G
    ALT  A
  NC_000001.11:235504169
    REF  G
    ALT  T
  NC_000001.11:235504169
    REF  G
    ALT  C
```

### `BRCA1:p.Glu575=` — protein_other

```
Variant Recoder = hgvs2vcf:
  NC_000017.11:43093806
    REF  T
    ALT  C
```

### `CLN3:p.Glu257=` — protein_other

```
Variant Recoder = hgvs2vcf:
  NC_000016.10:28484025
    REF  C
    ALT  T
```

### `DEF6:p.Thr297=` — protein_other

```
Variant Recoder = hgvs2vcf:
  NC_000006.12:35317974
    REF  G
    ALT  T
  NC_000006.12:35317974
    REF  G
    ALT  C
  NC_000006.12:35317974
    REF  G
    ALT  A
```

### `EDC3:p.His470=` — protein_other

```
Variant Recoder = hgvs2vcf:
  NC_000015.10:74632729
    REF  G
    ALT  A
```

### `EIF2B2:p.Gly94=` — protein_other

```
Variant Recoder = hgvs2vcf:
  NC_000014.9:75003393
    REF  C
    ALT  T
  NC_000014.9:75003393
    REF  C
    ALT  A
  NC_000014.9:75003393
    REF  C
    ALT  G
```

### `ERCC2:p.Arg369=` — protein_other

```
Variant Recoder = hgvs2vcf:
  NC_000019.10:45363754
    REF  G
    ALT  A
  NC_000019.10:45363754
    REF  G
    ALT  T
  NC_000019.10:45363754
    REF  G
    ALT  C
```

### `ERG:p.Asn121=` — protein_other

```
Variant Recoder = hgvs2vcf:
  NC_000021.9:38423435
    REF  G
    ALT  A
```

### `GHR:p.Ser65=` — protein_other

```
Variant Recoder = hgvs2vcf:
  NC_000005.10:42688948
    REF  A
    ALT  T
  NC_000005.10:42688948
    REF  A
    ALT  C
  NC_000005.10:42688948
    REF  A
    ALT  G
```

### `INPP5E:p.Arg97=` — protein_other

```
Variant Recoder = hgvs2vcf:
  NC_000009.12:136439129
    REF  T
    ALT  A
  NC_000009.12:136439129
    REF  T
    ALT  G
  NC_000009.12:136439129
    REF  T
    ALT  C
  NC_000009.12:136439131
    REF  G
    ALT  T
```

### `KARS1:p.Phe391=` — protein_other

```
Variant Recoder = hgvs2vcf:
  NC_000016.10:75631495
    REF  G
    ALT  A
```

### `LAMP2:p.Glu334=` — protein_other

```
Variant Recoder = hgvs2vcf:
  NC_000023.11:120441821
    REF  C
    ALT  T
```

### `MYB:p.Lys109=` — protein_other

```
Variant Recoder = hgvs2vcf:
  NC_000006.12:135190147
    REF  A
    ALT  G
```

### `PALLD:p.Ser426=` — protein_other

```
Variant Recoder = hgvs2vcf:
  NC_000004.12:168685502
    REF  A
    ALT  T
  NC_000004.12:168685502
    REF  A
    ALT  C
  NC_000004.12:168685502
    REF  A
    ALT  G
```

### `PCDH19:p.Pro984=` — protein_other

```
Variant Recoder = hgvs2vcf:
  NC_000023.11:100296772
    REF  A
    ALT  G
  NC_000023.11:100296772
    REF  A
    ALT  T
  NC_000023.11:100296772
    REF  A
    ALT  C
```

### `PDE6C:p.Arg623=` — protein_other

```
Variant Recoder = hgvs2vcf:
  NC_000010.11:93645979
    REF  A
    ALT  C
  NC_000010.11:93645981
    REF  A
    ALT  G
```

### `PGM3:p.Glu81=` — protein_other

```
Variant Recoder = hgvs2vcf:
  NC_000006.12:83188760
    REF  T
    ALT  C
```

### `POLE:p.Ile1890=` — protein_other

```
Variant Recoder = hgvs2vcf:
  NC_000012.12:132638022
    REF  G
    ALT  A
  NC_000012.12:132638022
    REF  G
    ALT  T
```

### `POLQ:p.Gly2225=` — protein_other

```
Variant Recoder = hgvs2vcf:
  NC_000003.12:121472033
    REF  T
    ALT  A
  NC_000003.12:121472033
    REF  T
    ALT  G
  NC_000003.12:121472033
    REF  T
    ALT  C
```

### `RTEL1:p.Arg1188=` — protein_other

```
Variant Recoder = hgvs2vcf:
  NC_000020.11:63695390
    REF  A
    ALT  C
  NC_000020.11:63695392
    REF  G
    ALT  A
```

### `SPEN:p.Val2549=` — protein_other

```
Variant Recoder = hgvs2vcf:
  NC_000001.11:15933887
    REF  C
    ALT  T
  NC_000001.11:15933887
    REF  C
    ALT  A
  NC_000001.11:15933887
    REF  C
    ALT  G
```

### `TTN:p.Ala15599=` — protein_other

```
Variant Recoder = hgvs2vcf:
  NC_000002.12:178618753
    REF  A
    ALT  G
  NC_000002.12:178618753
    REF  A
    ALT  T
  NC_000002.12:178618753
    REF  A
    ALT  C
```

### `ZFPM2:p.Phe370=` — protein_other

```
Variant Recoder = hgvs2vcf:
  NC_000008.11:105801192
    REF  C
    ALT  T
```

### `ADAM22:p.Ala266Val` — protein_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000007.14:88130431
    REF  C
    ALT  T
```

### `ARHGEF4:p.Leu1680Ser` — protein_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000002.12:131043465
    REF  T
    ALT  C
```

### `ATF6:p.Lys370Glu` — protein_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000001.11:161821082
    REF  A
    ALT  G
```

### `COX11:p.Pro13Arg` — protein_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000017.11:54968609
    REF  G
    ALT  C
```

### `DHDDS:p.Lys147Arg` — protein_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000001.11:26446432
    REF  A
    ALT  G
```

### `FHDC1:p.Arg580Gln` — protein_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000004.12:152975030
    REF  G
    ALT  A
```

### `GPR149:p.Pro29Leu` — protein_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000003.12:154429530
    REF  G
    ALT  A
```

### `LAMC2:p.Gln992Ter` — protein_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000001.11:183239468
    REF  C
    ALT  T
```

### `LTN1:p.Tyr830Cys` — protein_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000021.9:28959562
    REF  T
    ALT  C
```

### `MARVELD2:p.Pro97His` — protein_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000005.10:69419675
    REF  C
    ALT  A
```

### `MATR3:p.Gln34Arg` — protein_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000005.10:139307516
    REF  A
    ALT  G
```

### `MEGF6:p.Cys296Ser` — protein_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000001.11:3512095
    REF  C
    ALT  G
  NC_000001.11:3512096
    REF  A
    ALT  T
```

### `NAB1:p.Ala166Thr` — protein_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000002.12:190659672
    REF  G
    ALT  A
```

### `NLRP3:p.Arg673Gln` — protein_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000001.11:247425467
    REF  G
    ALT  A
```

### `OTX2:p.Ala234Val` — protein_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000014.9:56801928
    REF  G
    ALT  A
```

### `PCM1:p.Glu136Lys` — protein_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000008.11:17938803
    REF  G
    ALT  A
```

### `PLXNA3:p.Ile320Val` — protein_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000023.11:154461462
    REF  A
    ALT  G
```

### `SBF1:p.Arg1885Trp` — protein_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000022.11:50447171
    REF  G
    ALT  A
```

### `SLC15A5:p.Thr281Arg` — protein_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000012.12:16244713
    REF  G
    ALT  C
```

### `SLC5A4:p.Gly196Ala` — protein_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000022.11:32237321
    REF  C
    ALT  G
```

### `SRPX:p.Val259Phe` — protein_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000023.11:38160933
    REF  C
    ALT  A
```

### `ST18:p.Gln953Arg` — protein_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000008.11:52118339
    REF  T
    ALT  C
```

### `SYNE2:p.Leu5486Phe` — protein_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000014.9:64163558
    REF  C
    ALT  T
```

### `TSC2:p.Phe966Val` — protein_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000016.10:2077656
    REF  T
    ALT  G
```

### `WWP2:p.Leu725Pro` — protein_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000016.10:69937174
    REF  T
    ALT  C
```

### `ZFHX3:p.His1380Asp` — protein_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000016.10:72798544
    REF  G
    ALT  C
```

### `HABP2:c.*599del` — utr_del

```
Variant Recoder = hgvs2vcf:
  NC_000010.11:113588967
    REF  GA
    ALT  G
```

### `NM_000059:c.-39-89del` — utr_del

```
Variant Recoder = hgvs2vcf:
  NC_000013.11:32316332
    REF  AC
    ALT  A
```

### `NM_015599:c.*2675del` — utr_del

```
Variant Recoder = hgvs2vcf:
  NC_000006.12:83166558
    REF  CA
    ALT  C
```

### `PTCH1:c.-6_-5del` — utr_del

```
Variant Recoder = hgvs2vcf:
  NC_000009.12:95508365
    REF  GCC
    ALT  G
```

### `ATRIP:c.*2003dup` — utr_dup

```
Variant Recoder = hgvs2vcf:
  NC_000003.12:48467556
    REF  G
    ALT  GT
```

### `AGPS:c.*1364A>G` — utr_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000002.12:177539559
    REF  A
    ALT  G
```

### `AZIN2:c.-72-11T>C` — utr_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000001.11:33082167
    REF  T
    ALT  C
```

### `BBS7:c.-9G>A` — utr_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000004.12:121870322
    REF  C
    ALT  T
```

### `C19orf44:c.*335C>T` — utr_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000019.10:16520388
    REF  C
    ALT  T
```

### `COL18A1:c.*30G>A` — utr_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000021.9:45512428
    REF  G
    ALT  A
```

### `DES:c.*662G>A` — utr_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000002.12:219426652
    REF  G
    ALT  A
```

### `EFCAB10:c.*115C>T` — utr_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000007.14:105565332
    REF  G
    ALT  A
```

### `ERCC4:c.*2710C>T` — utr_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000016.10:13951057
    REF  C
    ALT  T
```

### `HLCS:c.*1484A>G` — utr_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000021.9:36752762
    REF  T
    ALT  C
```

### `IFT80:c.*104G>A` — utr_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000003.12:160258421
    REF  C
    ALT  T
```

### `IGF1R:c.*6092G>A` — utr_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000015.10:98963534
    REF  G
    ALT  A
```

### `IVD:c.*2235G>A` — utr_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000015.10:40420498
    REF  G
    ALT  A
```

### `KIF1A:c.*120C>A` — utr_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000002.12:240717244
    REF  G
    ALT  T
```

### `LMLN:c.*3256A>T` — utr_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000003.12:198041923
    REF  A
    ALT  T
```

### `MMP13:c.*13A>T` — utr_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000011.10:102944253
    REF  T
    ALT  A
```

### `NM_000033:c.*668C>T` — utr_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000023.11:153744403
    REF  C
    ALT  T
```

### `NM_000129:c.*934G>A` — utr_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000006.12:6144685
    REF  C
    ALT  T
```

### `NM_000136:c.*593C>G` — utr_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000009.12:95101114
    REF  G
    ALT  C
```

### `NM_000294:c.*1744G>A` — utr_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000016.10:30758841
    REF  G
    ALT  A
```

### `NM_001009925:c.-16G>A` — utr_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000020.11:5112961
    REF  C
    ALT  T
```

### `NM_001017995:c.*1862G>T` — utr_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000005.10:172336507
    REF  C
    ALT  A
```

### `NM_001039844:c.*2308A>T` — utr_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000010.11:15076222
    REF  T
    ALT  A
```

### `NM_001113525:c.*1291C>G` — utr_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000016.10:89739537
    REF  C
    ALT  G
```

### `NM_001135091:c.*1334A>T` — utr_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000011.10:26559731
    REF  T
    ALT  A
```

### `NM_001361:c.*144G>A` — utr_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000016.10:72024343
    REF  G
    ALT  A
```

### `NM_001621:c.*2091A>T` — utr_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000007.14:17345155
    REF  A
    ALT  T
```

### `NM_004004:c.*979A>G` — utr_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000013.11:20187922
    REF  T
    ALT  C
```

### `NM_004744:c.*3654T>C` — utr_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000004.12:154752790
    REF  T
    ALT  C
```

### `NM_005589:c.*309G>A` — utr_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000014.9:74060333
    REF  C
    ALT  T
```

### `NM_006580:c.-90C>T` — utr_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000003.12:190388240
    REF  C
    ALT  T
```

### `NM_006824:c.-14G>T` — utr_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000001.11:43172132
    REF  C
    ALT  A
```

### `NM_007294:c.-19-6T>A` — utr_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000017.11:43124121
    REF  A
    ALT  T
```

### `NM_014431:c.*1422G>T` — utr_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000010.11:70568155
    REF  G
    ALT  T
```

### `NM_014748:c.*766G>A` — utr_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000002.12:27377485
    REF  G
    ALT  A
```

### `NM_016156:c.*1822T>G` — utr_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000011.10:95833468
    REF  A
    ALT  C
```

### `NM_024838:c.-215-38A>C` — utr_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000010.11:25021704
    REF  A
    ALT  C
```

### `NM_031433:c.*951C>T` — utr_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000011.10:119340343
    REF  G
    ALT  A
```

### `NM_032638:c.-4G>C` — utr_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000003.12:128487035
    REF  C
    ALT  G
```

### `NM_153252:c.*3083G>T` — utr_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000023.11:80673526
    REF  C
    ALT  A
```

### `NM_194255:c.*2918G>C` — utr_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000021.9:45512740
    REF  C
    ALT  G
```

### `NM_198252:c.-9-2025G>T` — utr_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000009.12:121299938
    REF  G
    ALT  T
```

### `NRXN1:c.-28A>C` — utr_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000002.12:51028301
    REF  T
    ALT  G
```

### `PLEKHA6:c.-13-256G>T` — utr_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000001.11:204273996
    REF  C
    ALT  A
```

### `RPE65:c.*630C>T` — utr_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000001.11:68429146
    REF  G
    ALT  A
```

### `RRM2B:c.*2035A>G` — utr_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000008.11:102206098
    REF  T
    ALT  C
```

### `SLC37A4:c.-195-136A>C` — utr_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000011.10:119029700
    REF  T
    ALT  G
```

### `SMARCA4:c.*19C>T` — utr_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000019.10:11061835
    REF  C
    ALT  T
```

### `TMEM106B:c.*1276G>T` — utr_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000007.14:12233251
    REF  G
    ALT  T
```

### `TRIP11:c.-335G>A` — utr_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000014.9:92040020
    REF  C
    ALT  T
```

### `VANGL1:c.*5993C>G` — utr_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000001.11:115697372
    REF  C
    ALT  G
```

### `VLDLR:c.-303C>G` — utr_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000009.12:2621887
    REF  C
    ALT  G
```

### `ZNF276:c.*438C>G` — utr_substitution

```
Variant Recoder = hgvs2vcf:
  NC_000016.10:89738684
    REF  C
    ALT  G
```
