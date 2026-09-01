# hgvs2vcf-cdot-lmdb evaluation

- Total: 100
- Passed: 75
- Failed: 25
- Pass rate: 75.00%
- Elapsed: 0.448 s

## Results by category

| Category | Passed | Failed | Pass rate |
|---|---:|---:|---:|
| coding_del | 3 | 2 | 60.00% |
| coding_delins | 4 | 4 | 50.00% |
| coding_dup | 2 | 4 | 33.33% |
| coding_ins | 4 | 0 | 100.00% |
| coding_other | 1 | 0 | 100.00% |
| coding_substitution | 7 | 0 | 100.00% |
| intronic_del | 4 | 2 | 66.67% |
| intronic_delins | 2 | 2 | 50.00% |
| intronic_dup | 2 | 3 | 40.00% |
| intronic_ins | 1 | 1 | 50.00% |
| intronic_other | 1 | 0 | 100.00% |
| intronic_substitution | 6 | 0 | 100.00% |
| protein_del | 6 | 4 | 60.00% |
| protein_other | 13 | 0 | 100.00% |
| protein_substitution | 12 | 0 | 100.00% |
| utr_del | 1 | 1 | 50.00% |
| utr_delins | 2 | 0 | 100.00% |
| utr_dup | 0 | 2 | 0.00% |
| utr_ins | 2 | 0 | 100.00% |
| utr_substitution | 2 | 0 | 100.00% |

## Successful results

### coding_del

- **HGVS:** <code>NM_000720:c.2151_2152del</code>
  - **Variant Recoder:**<br><code>NC_000003.12:53723989<br>REF: CAG<br>ALT: C</code>
  - **hgvs2vcf:**<br><code>NC_000003.12:53723989<br>REF: CAG<br>ALT: C</code>

- **HGVS:** <code>NM_001374828:c.6504del</code>
  - **Variant Recoder:**<br><code>NC_000006.12:157207275<br>REF: GC<br>ALT: G</code>
  - **hgvs2vcf:**<br><code>NC_000006.12:157207275<br>REF: GC<br>ALT: G</code>

- **HGVS:** <code>SLC5A1:c.1566del</code>
  - **Variant Recoder:**<br><code>NC_000022.11:32102137<br>REF: GT<br>ALT: G</code>
  - **hgvs2vcf:**<br><code>NC_000022.11:32102137<br>REF: GT<br>ALT: G</code>

### coding_delins

- **HGVS:** <code>MYH14:c.2337_2338delinsA<wbr>A</code>
  - **Variant Recoder:**<br><code>NC_000019.10:50259248<br>REF: CC<br>ALT: AA</code>
  - **hgvs2vcf:**<br><code>NC_000019.10:50259248<br>REF: CC<br>ALT: AA</code>

- **HGVS:** <code>NM_001368038:c.835_837de<wbr>linsTGC</code>
  - **Variant Recoder:**<br><code>NC_000012.12:94375982<br>REF: ACG<br>ALT: GCA</code>
  - **hgvs2vcf:**<br><code>NC_000012.12:94375982<br>REF: ACG<br>ALT: GCA</code>

- **HGVS:** <code>NM_133437:c.73258_73259d<wbr>elinsGT</code>
  - **Variant Recoder:**<br><code>NC_000002.12:178537231<br>REF: TT<br>ALT: AC</code>
  - **hgvs2vcf:**<br><code>NC_000002.12:178537231<br>REF: TT<br>ALT: AC</code>

- **HGVS:** <code>ALPL:c.608_609delinsTT</code>
  - **Variant Recoder:**<br><code>NC_000001.11:21564176<br>REF: AC<br>ALT: TT</code>
  - **hgvs2vcf:**<br><code>NC_000001.11:21564176<br>REF: AC<br>ALT: TT</code>

### coding_dup

- **HGVS:** <code>VIM:c.1374_1375dup</code>
  - **Variant Recoder:**<br><code>NC_000010.11:17237243<br>REF: C<br>ALT: CTT</code>
  - **hgvs2vcf:**<br><code>NC_000010.11:17237243<br>REF: C<br>ALT: CTT</code>

- **HGVS:** <code>GAN:c.1690dup</code>
  - **Variant Recoder:**<br><code>NC_000016.10:81377491<br>REF: C<br>ALT: CG</code>
  - **hgvs2vcf:**<br><code>NC_000016.10:81377491<br>REF: C<br>ALT: CG</code>

### coding_ins

- **HGVS:** <code>MMUT:c.96_97insGG</code>
  - **Variant Recoder:**<br><code>NC_000006.12:49459370<br>REF: G<br>ALT: GCC</code>
  - **hgvs2vcf:**<br><code>NC_000006.12:49459370<br>REF: G<br>ALT: GCC</code>

- **HGVS:** <code>NM_018136:c.5101_5102ins<wbr>G</code>
  - **Variant Recoder:**<br><code>NC_000001.11:197104149<br>REF: A<br>ALT: AC</code>
  - **hgvs2vcf:**<br><code>NC_000001.11:197104149<br>REF: A<br>ALT: AC</code>

- **HGVS:** <code>NPHS1:c.2354_2355insTCGT<wbr>CGTGCTGCT</code>
  - **Variant Recoder:**<br><code>NC_000019.10:35842530<br>REF: C<br>ALT: CAGCAGCACGACGA</code>
  - **hgvs2vcf:**<br><code>NC_000019.10:35842530<br>REF: C<br>ALT: CAGCAGCACGACGA</code>

- **HGVS:** <code>HGSNAT:c.1054_1055insATC<wbr>AATTTCTAATGGGATTTCCAGAGT<wbr>TGAAAAAGACAAATATTCAGCTTT<wbr>AGGAAGCACAGTTGAGTCCTGAGC<wbr>AGTACAAATAAAAATATAGGCTGG<wbr>GCACAGTGGCTCACATGTGTAATC<wbr>CCAGCACTTTCGGAGGCTGAGGTG<wbr>GGTGGATTGCTGGAGTCCAGCAGT<wbr>TTGAAAACAGCCTGAGCAACATGG<wbr>CAAGACCCCATCTCTACAAAAAAT<wbr>ACAACAATTATCCGGGCATGGTGG<wbr>CACAAGCCCGTAGTCCCAGCTACT<wbr>CAGGAAGCTGAGGTGGATCGCTTG<wbr>AGCCCGGGAGGTGGAGGTTGCAGT<wbr>GAGCCAAGATCACACCATTGCACT<wbr>CCACACTGAATGACAGAGTGAGAC<wbr>TGTCTTAATAAAAAATATGAGTCA<wbr>GCGTATAAGTTAAAAGGAGTTTTA<wbr>AAAGATACTAATCCAAAAGAAGGC<wbr>AGAAAAGGAGAAACATAATAGACT<wbr>TACCAGCCCAATTTAAAAGTCAGG<wbr>GATTATAAACATGAATTGAAGAAG<wbr>TGAGACCCAGTTA</code>
  - **Variant Recoder:**<br><code>NC_000008.11:43182186<br>REF: T<br>ALT: TATCAATTTCTAATGGGATTTCCA<wbr>GAGTTGAAAAAGACAAATATTCAG<wbr>CTTTAGGAAGCACAGTTGAGTCCT<wbr>GAGCAGTACAAATAAAAATATAGG<wbr>CTGGGCACAGTGGCTCACATGTGT<wbr>AATCCCAGCACTTTCGGAGGCTGA<wbr>GGTGGGTGGATTGCTGGAGTCCAG<wbr>CAGTTTGAAAACAGCCTGAGCAAC<wbr>ATGGCAAGACCCCATCTCTACAAA<wbr>AAATACAACAATTATCCGGGCATG<wbr>GTGGCACAAGCCCGTAGTCCCAGC<wbr>TACTCAGGAAGCTGAGGTGGATCG<wbr>CTTGAGCCCGGGAGGTGGAGGTTG<wbr>CAGTGAGCCAAGATCACACCATTG<wbr>CACTCCACACTGAATGACAGAGTG<wbr>AGACTGTCTTAATAAAAAATATGA<wbr>GTCAGCGTATAAGTTAAAAGGAGT<wbr>TTTAAAAGATACTAATCCAAAAGA<wbr>AGGCAGAAAAGGAGAAACATAATA<wbr>GACTTACCAGCCCAATTTAAAAGT<wbr>CAGGGATTATAAACATGAATTGAA<wbr>GAAGTGAGACCCAGTTA</code>
  - **hgvs2vcf:**<br><code>NC_000008.11:43182186<br>REF: T<br>ALT: TATCAATTTCTAATGGGATTTCCA<wbr>GAGTTGAAAAAGACAAATATTCAG<wbr>CTTTAGGAAGCACAGTTGAGTCCT<wbr>GAGCAGTACAAATAAAAATATAGG<wbr>CTGGGCACAGTGGCTCACATGTGT<wbr>AATCCCAGCACTTTCGGAGGCTGA<wbr>GGTGGGTGGATTGCTGGAGTCCAG<wbr>CAGTTTGAAAACAGCCTGAGCAAC<wbr>ATGGCAAGACCCCATCTCTACAAA<wbr>AAATACAACAATTATCCGGGCATG<wbr>GTGGCACAAGCCCGTAGTCCCAGC<wbr>TACTCAGGAAGCTGAGGTGGATCG<wbr>CTTGAGCCCGGGAGGTGGAGGTTG<wbr>CAGTGAGCCAAGATCACACCATTG<wbr>CACTCCACACTGAATGACAGAGTG<wbr>AGACTGTCTTAATAAAAAATATGA<wbr>GTCAGCGTATAAGTTAAAAGGAGT<wbr>TTTAAAAGATACTAATCCAAAAGA<wbr>AGGCAGAAAAGGAGAAACATAATA<wbr>GACTTACCAGCCCAATTTAAAAGT<wbr>CAGGGATTATAAACATGAATTGAA<wbr>GAAGTGAGACCCAGTTA</code>

### coding_other

- **HGVS:** <code>NM_001277115:c.12492_124<wbr>93inv</code>
  - **Variant Recoder:**<br><code>NC_000007.14:21884395<br>REF: CA<br>ALT: TG</code>
  - **hgvs2vcf:**<br><code>NC_000007.14:21884395<br>REF: CA<br>ALT: TG</code>

### coding_substitution

- **HGVS:** <code>EYS:c.1478G&gt;A</code>
  - **Variant Recoder:**<br><code>NC_000006.12:65344159<br>REF: C<br>ALT: T</code>
  - **hgvs2vcf:**<br><code>NC_000006.12:65344159<br>REF: C<br>ALT: T</code>

- **HGVS:** <code>NM_001376241:c.1011C&gt;A</code>
  - **Variant Recoder:**<br><code>NC_000002.12:159748301<br>REF: C<br>ALT: A</code>
  - **hgvs2vcf:**<br><code>NC_000002.12:159748301<br>REF: C<br>ALT: A</code>

- **HGVS:** <code>NM_004407:c.1339A&gt;G</code>
  - **Variant Recoder:**<br><code>NC_000004.12:87663117<br>REF: A<br>ALT: G</code>
  - **hgvs2vcf:**<br><code>NC_000004.12:87663117<br>REF: A<br>ALT: G</code>

- **HGVS:** <code>ZDHHC9:c.812A&gt;G</code>
  - **Variant Recoder:**<br><code>NC_000023.11:129811475<br>REF: T<br>ALT: C</code>
  - **hgvs2vcf:**<br><code>NC_000023.11:129811475<br>REF: T<br>ALT: C</code>

- **HGVS:** <code>NM_001287489:c.5565G&gt;A</code>
  - **Variant Recoder:**<br><code>NC_000002.12:26460999<br>REF: C<br>ALT: T</code>
  - **hgvs2vcf:**<br><code>NC_000002.12:26460999<br>REF: C<br>ALT: T</code>

- **HGVS:** <code>NM_001287:c.528G&gt;C</code>
  - **Variant Recoder:**<br><code>NC_000016.10:1460484<br>REF: C<br>ALT: G</code>
  - **hgvs2vcf:**<br><code>NC_000016.10:1460484<br>REF: C<br>ALT: G</code>

- **HGVS:** <code>ASXL3:c.4228C&gt;T</code>
  - **Variant Recoder:**<br><code>NC_000018.10:33744076<br>REF: C<br>ALT: T</code>
  - **hgvs2vcf:**<br><code>NC_000018.10:33744076<br>REF: C<br>ALT: T</code>

### intronic_del

- **HGVS:** <code>TMEM237:c.554-56del</code>
  - **Variant Recoder:**<br><code>NC_000002.12:201629907<br>REF: AT<br>ALT: A</code>
  - **hgvs2vcf:**<br><code>NC_000002.12:201629907<br>REF: AT<br>ALT: A</code>

- **HGVS:** <code>NM_033115:c.267-10220_26<wbr>7-10219del</code>
  - **Variant Recoder:**<br><code>NC_000004.12:106262225<br>REF: CAA<br>ALT: C</code>
  - **hgvs2vcf:**<br><code>NC_000004.12:106262225<br>REF: CAA<br>ALT: C</code>

- **HGVS:** <code>NM_001316329:c.2090+1_20<wbr>91-1del</code>
  - **Variant Recoder:**<br><code>NC_000019.10:53906891<br>REF: TGTAATCTCACCCGCCGCCACTAG<wbr>GTGTCCCCAACGTCCCCTCCGCCG<wbr>TGCCGGCGGCAGCCCCACTTCACC<wbr>CCCAACTTCACCACCCCCTGTCCC<wbr>ATTCTAG<br>ALT: T</code>
  - **hgvs2vcf:**<br><code>NC_000019.10:53906891<br>REF: TGTAATCTCACCCGCCGCCACTAG<wbr>GTGTCCCCAACGTCCCCTCCGCCG<wbr>TGCCGGCGGCAGCCCCACTTCACC<wbr>CCCAACTTCACCACCCCCTGTCCC<wbr>ATTCTAG<br>ALT: T</code>

- **HGVS:** <code>SLC39A4:c.805-3del</code>
  - **Variant Recoder:**<br><code>NC_000008.11:144414898<br>REF: TG<br>ALT: T</code>
  - **hgvs2vcf:**<br><code>NC_000008.11:144414898<br>REF: TG<br>ALT: T</code>

### intronic_delins

- **HGVS:** <code>CDH1:c.48+6_48+7delinsTG</code>
  - **Variant Recoder:**<br><code>NC_000016.10:68737469<br>REF: CC<br>ALT: TG</code>
  - **hgvs2vcf:**<br><code>NC_000016.10:68737469<br>REF: CC<br>ALT: TG</code>

- **HGVS:** <code>NM_000154:c.166-5_166-4d<wbr>elinsAT</code>
  - **Variant Recoder:**<br><code>NC_000017.11:75764090<br>REF: GC<br>ALT: AT</code>
  - **hgvs2vcf:**<br><code>NC_000017.11:75764090<br>REF: GC<br>ALT: AT</code>

### intronic_dup

- **HGVS:** <code>NM_032446:c.2362+2dupT</code>
  - **Variant Recoder:**<br><code>NC_000005.10:127440868<br>REF: G<br>ALT: GT</code>
  - **hgvs2vcf:**<br><code>NC_000005.10:127440868<br>REF: G<br>ALT: GT</code>

- **HGVS:** <code>GYG1:c.609-15dup</code>
  - **Variant Recoder:**<br><code>NC_000003.12:149024037<br>REF: T<br>ALT: TG</code>
  - **hgvs2vcf:**<br><code>NC_000003.12:149024037<br>REF: T<br>ALT: TG</code>

### intronic_ins

- **HGVS:** <code>SCN8A:c.2545-19_2545-18i<wbr>nsC</code>
  - **Variant Recoder:**<br><code>NC_000012.12:51765652<br>REF: G<br>ALT: GC</code>
  - **hgvs2vcf:**<br><code>NC_000012.12:51765652<br>REF: G<br>ALT: GC</code>

### intronic_other

- **HGVS:** <code>NM_000138:c.6617-9_6617-<wbr>8inv</code>
  - **Variant Recoder:**<br><code>NC_000015.10:48432996<br>REF: AG<br>ALT: CT</code>
  - **hgvs2vcf:**<br><code>NC_000015.10:48432996<br>REF: AG<br>ALT: CT</code>

### intronic_substitution

- **HGVS:** <code>LAMA3:c.7645-1G&gt;A</code>
  - **Variant Recoder:**<br><code>NC_000018.10:23915288<br>REF: G<br>ALT: A</code>
  - **hgvs2vcf:**<br><code>NC_000018.10:23915288<br>REF: G<br>ALT: A</code>

- **HGVS:** <code>NM_001352303:c.76+20C&gt;A</code>
  - **Variant Recoder:**<br><code>NC_000022.11:19931010<br>REF: G<br>ALT: T</code>
  - **hgvs2vcf:**<br><code>NC_000022.11:19931010<br>REF: G<br>ALT: T</code>

- **HGVS:** <code>NM_001167819:c.502-2A&gt;G</code>
  - **Variant Recoder:**<br><code>NC_000023.11:136208453<br>REF: A<br>ALT: G</code>
  - **hgvs2vcf:**<br><code>NC_000023.11:136208453<br>REF: A<br>ALT: G</code>

- **HGVS:** <code>MCM8:c.1255-10C&gt;T</code>
  - **Variant Recoder:**<br><code>NC_000020.11:5973046<br>REF: C<br>ALT: T</code>
  - **hgvs2vcf:**<br><code>NC_000020.11:5973046<br>REF: C<br>ALT: T</code>

- **HGVS:** <code>NM_018924:c.2415+26628A&gt;<wbr>T</code>
  - **Variant Recoder:**<br><code>NC_000005.10:141399437<br>REF: A<br>ALT: T</code>
  - **hgvs2vcf:**<br><code>NC_000005.10:141399437<br>REF: A<br>ALT: T</code>

- **HGVS:** <code>NM_001365677:c.331+2T&gt;C</code>
  - **Variant Recoder:**<br><code>NC_000005.10:132217195<br>REF: A<br>ALT: G</code>
  - **hgvs2vcf:**<br><code>NC_000005.10:132217195<br>REF: A<br>ALT: G</code>

### protein_del

- **HGVS:** <code>GRIN2B:p.Asn1366del</code>
  - **Variant Recoder:**<br><code>NC_000012.12:13563139<br>REF: GGTT<br>ALT: G</code>
  - **hgvs2vcf:**<br><code>NC_000012.12:13563139<br>REF: GGTT<br>ALT: G</code>

- **HGVS:** <code>EP400:p.Gln2748del</code>
  - **Variant Recoder:**<br><code>NC_000012.12:132062608<br>REF: ACAG<br>ALT: A</code>
  - **hgvs2vcf:**<br><code>NC_000012.12:132062608<br>REF: ACAG<br>ALT: A</code>

- **HGVS:** <code>HIVEP2:p.Asn1911_Asp1912<wbr>del</code>
  - **Variant Recoder:**<br><code>NC_000006.12:142760551<br>REF: CATCATT<br>ALT: C</code>
  - **hgvs2vcf:**<br><code>NC_000006.12:142760551<br>REF: CATCATT<br>ALT: C</code>

- **HGVS:** <code>ATRX:p.Leu821_Glu822del</code>
  - **Variant Recoder:**<br><code>NC_000023.11:77682789<br>REF: TTTCTAA<br>ALT: T</code>
  - **hgvs2vcf:**<br><code>NC_000023.11:77682789<br>REF: TTTCTAA<br>ALT: T</code>

- **HGVS:** <code>SLC25A12:p.Phe646_Thr677<wbr>del</code>
  - **Variant Recoder:**<br><code>NC_000002.12:171785279<br>REF: GAGTGGCTGCCACTGCTGCCTTTG<wbr>GCTGAACCACAGCAACACTAGGAG<wbr>ACTTAAATTTCGGGAGATAAAGGC<wbr>CAAATTTGTTTTCGATGCCTGCAA<wbr>A<br>ALT: G</code>
  - **hgvs2vcf:**<br><code>NC_000002.12:171785279<br>REF: GAGTGGCTGCCACTGCTGCCTTTG<wbr>GCTGAACCACAGCAACACTAGGAG<wbr>ACTTAAATTTCGGGAGATAAAGGC<wbr>CAAATTTGTTTTCGATGCCTGCAA<wbr>A<br>ALT: G</code>

- **HGVS:** <code>CITED2:p.His144_Gln145de<wbr>l</code>
  - **Variant Recoder:**<br><code>NC_000006.12:139373509<br>REF: TCTGGTG<br>ALT: T</code>
  - **hgvs2vcf:**<br><code>NC_000006.12:139373509<br>REF: TCTGGTG<br>ALT: T</code>

### protein_other

- **HGVS:** <code>MTR:p.Ile441=</code>
  - **Variant Recoder:**<br><code>NC_000001.11:236835681<br>REF: C<br>ALT: A</code><br><br><code>NC_000001.11:236835681<br>REF: C<br>ALT: T</code>
  - **hgvs2vcf:**<br><code>NC_000001.11:236835681<br>REF: C<br>ALT: T</code><br><br><code>NC_000001.11:236835681<br>REF: C<br>ALT: A</code>

- **HGVS:** <code>MS4A1:p.Leu61=</code>
  - **Variant Recoder:**<br><code>NC_000011.10:60463025<br>REF: C<br>ALT: A</code><br><br><code>NC_000011.10:60463025<br>REF: C<br>ALT: G</code><br><br><code>NC_000011.10:60463025<br>REF: C<br>ALT: T</code>
  - **hgvs2vcf:**<br><code>NC_000011.10:60463025<br>REF: C<br>ALT: T</code><br><br><code>NC_000011.10:60463025<br>REF: C<br>ALT: A</code><br><br><code>NC_000011.10:60463025<br>REF: C<br>ALT: G</code>

- **HGVS:** <code>CSF1:p.Arg404=</code>
  - **Variant Recoder:**<br><code>NC_000001.11:109923831<br>REF: A<br>ALT: C</code><br><br><code>NC_000001.11:109923833<br>REF: G<br>ALT: A</code>
  - **hgvs2vcf:**<br><code>NC_000001.11:109923831<br>REF: A<br>ALT: C</code><br><br><code>NC_000001.11:109923833<br>REF: G<br>ALT: A</code>

- **HGVS:** <code>CDH23:p.Pro463=</code>
  - **Variant Recoder:**<br><code>NC_000010.11:71646557<br>REF: A<br>ALT: C</code><br><br><code>NC_000010.11:71646557<br>REF: A<br>ALT: G</code><br><br><code>NC_000010.11:71646557<br>REF: A<br>ALT: T</code>
  - **hgvs2vcf:**<br><code>NC_000010.11:71646557<br>REF: A<br>ALT: T</code><br><br><code>NC_000010.11:71646557<br>REF: A<br>ALT: C</code><br><br><code>NC_000010.11:71646557<br>REF: A<br>ALT: G</code>

- **HGVS:** <code>CELSR2:p.His1300=</code>
  - **Variant Recoder:**<br><code>NC_000001.11:109259021<br>REF: C<br>ALT: T</code>
  - **hgvs2vcf:**<br><code>NC_000001.11:109259021<br>REF: C<br>ALT: T</code>

- **HGVS:** <code>GLI1:p.Pro631=</code>
  - **Variant Recoder:**<br><code>NC_000012.12:57470633<br>REF: C<br>ALT: A</code><br><br><code>NC_000012.12:57470633<br>REF: C<br>ALT: G</code><br><br><code>NC_000012.12:57470633<br>REF: C<br>ALT: T</code>
  - **hgvs2vcf:**<br><code>NC_000012.12:57470633<br>REF: C<br>ALT: T</code><br><br><code>NC_000012.12:57470633<br>REF: C<br>ALT: A</code><br><br><code>NC_000012.12:57470633<br>REF: C<br>ALT: G</code>

- **HGVS:** <code>COL4A4:p.Gly373=</code>
  - **Variant Recoder:**<br><code>NC_000002.12:227098779<br>REF: C<br>ALT: A</code><br><br><code>NC_000002.12:227098779<br>REF: C<br>ALT: G</code><br><br><code>NC_000002.12:227098779<br>REF: C<br>ALT: T</code>
  - **hgvs2vcf:**<br><code>NC_000002.12:227098779<br>REF: C<br>ALT: A</code><br><br><code>NC_000002.12:227098779<br>REF: C<br>ALT: G</code><br><br><code>NC_000002.12:227098779<br>REF: C<br>ALT: T</code>

- **HGVS:** <code>TBC1D15:p.Gly495=</code>
  - **Variant Recoder:**<br><code>NC_000012.12:71917781<br>REF: A<br>ALT: C</code><br><br><code>NC_000012.12:71917781<br>REF: A<br>ALT: G</code><br><br><code>NC_000012.12:71917781<br>REF: A<br>ALT: T</code>
  - **hgvs2vcf:**<br><code>NC_000012.12:71917781<br>REF: A<br>ALT: T</code><br><br><code>NC_000012.12:71917781<br>REF: A<br>ALT: C</code><br><br><code>NC_000012.12:71917781<br>REF: A<br>ALT: G</code>

- **HGVS:** <code>LRRK1:p.Thr1053=</code>
  - **Variant Recoder:**<br><code>NC_000015.10:101048517<br>REF: T<br>ALT: A</code><br><br><code>NC_000015.10:101048517<br>REF: T<br>ALT: C</code><br><br><code>NC_000015.10:101048517<br>REF: T<br>ALT: G</code>
  - **hgvs2vcf:**<br><code>NC_000015.10:101048517<br>REF: T<br>ALT: C</code><br><br><code>NC_000015.10:101048517<br>REF: T<br>ALT: A</code><br><br><code>NC_000015.10:101048517<br>REF: T<br>ALT: G</code>

- **HGVS:** <code>ZFYVE26:p.Glu1208=</code>
  - **Variant Recoder:**<br><code>NC_000014.9:67784336<br>REF: C<br>ALT: T</code>
  - **hgvs2vcf:**<br><code>NC_000014.9:67784336<br>REF: C<br>ALT: T</code>

- **HGVS:** <code>PCK2:p.Pro427=</code>
  - **Variant Recoder:**<br><code>NC_000014.9:24102799<br>REF: G<br>ALT: A</code><br><br><code>NC_000014.9:24102799<br>REF: G<br>ALT: C</code><br><br><code>NC_000014.9:24102799<br>REF: G<br>ALT: T</code>
  - **hgvs2vcf:**<br><code>NC_000014.9:24102799<br>REF: G<br>ALT: T</code><br><br><code>NC_000014.9:24102799<br>REF: G<br>ALT: C</code><br><br><code>NC_000014.9:24102799<br>REF: G<br>ALT: A</code>

- **HGVS:** <code>DDX6:p.Arg381=</code>
  - **Variant Recoder:**<br><code>NC_000011.10:118756291<br>REF: T<br>ALT: A</code><br><br><code>NC_000011.10:118756291<br>REF: T<br>ALT: C</code><br><br><code>NC_000011.10:118756291<br>REF: T<br>ALT: G</code><br><br><code>NC_000011.10:118756293<br>REF: G<br>ALT: T</code>
  - **hgvs2vcf:**<br><code>NC_000011.10:118756291<br>REF: T<br>ALT: A</code><br><br><code>NC_000011.10:118756291<br>REF: T<br>ALT: G</code><br><br><code>NC_000011.10:118756291<br>REF: T<br>ALT: C</code><br><br><code>NC_000011.10:118756293<br>REF: G<br>ALT: T</code>

- **HGVS:** <code>ASNS:p.Ile462=</code>
  - **Variant Recoder:**<br><code>NC_000007.14:97853150<br>REF: A<br>ALT: G</code><br><br><code>NC_000007.14:97853150<br>REF: A<br>ALT: T</code>
  - **hgvs2vcf:**<br><code>NC_000007.14:97853150<br>REF: A<br>ALT: G</code><br><br><code>NC_000007.14:97853150<br>REF: A<br>ALT: T</code>

### protein_substitution

- **HGVS:** <code>OR6A2:p.Thr44Ile</code>
  - **Variant Recoder:**<br><code>NC_000011.10:6795578<br>REF: G<br>ALT: A</code>
  - **hgvs2vcf:**<br><code>NC_000011.10:6795578<br>REF: G<br>ALT: A</code>

- **HGVS:** <code>CLDN19:p.Ala14Asp</code>
  - **Variant Recoder:**<br><code>NC_000001.11:42740023<br>REF: G<br>ALT: T</code>
  - **hgvs2vcf:**<br><code>NC_000001.11:42740023<br>REF: G<br>ALT: T</code>

- **HGVS:** <code>IGDCC3:p.Ile98Thr</code>
  - **Variant Recoder:**<br><code>NC_000015.10:65375213<br>REF: A<br>ALT: G</code>
  - **hgvs2vcf:**<br><code>NC_000015.10:65375213<br>REF: A<br>ALT: G</code>

- **HGVS:** <code>MITF:p.Gly462Glu</code>
  - **Variant Recoder:**<br><code>NC_000003.12:69965052<br>REF: G<br>ALT: A</code>
  - **hgvs2vcf:**<br><code>NC_000003.12:69965052<br>REF: G<br>ALT: A</code>

- **HGVS:** <code>ZNF407:p.Arg1227His</code>
  - **Variant Recoder:**<br><code>NC_000018.10:74634699<br>REF: G<br>ALT: A</code>
  - **hgvs2vcf:**<br><code>NC_000018.10:74634699<br>REF: G<br>ALT: A</code>

- **HGVS:** <code>RP2:p.Thr56Met</code>
  - **Variant Recoder:**<br><code>NC_000023.11:46853540<br>REF: C<br>ALT: T</code>
  - **hgvs2vcf:**<br><code>NC_000023.11:46853540<br>REF: C<br>ALT: T</code>

- **HGVS:** <code>ARHGEF5:p.Glu918Lys</code>
  - **Variant Recoder:**<br><code>NC_000007.14:144365421<br>REF: G<br>ALT: A</code>
  - **hgvs2vcf:**<br><code>NC_000007.14:144365421<br>REF: G<br>ALT: A</code>

- **HGVS:** <code>KALRN:p.Arg1799Gln</code>
  - **Variant Recoder:**<br><code>NC_000003.12:124632633<br>REF: G<br>ALT: A</code>
  - **hgvs2vcf:**<br><code>NC_000003.12:124632633<br>REF: G<br>ALT: A</code>

- **HGVS:** <code>CYP2A6:p.Arg76Trp</code>
  - **Variant Recoder:**<br><code>NC_000019.10:40849935<br>REF: G<br>ALT: A</code>
  - **hgvs2vcf:**<br><code>NC_000019.10:40849935<br>REF: G<br>ALT: A</code>

- **HGVS:** <code>COG6:p.Lys58Glu</code>
  - **Variant Recoder:**<br><code>NC_000013.11:39659382<br>REF: A<br>ALT: G</code>
  - **hgvs2vcf:**<br><code>NC_000013.11:39659382<br>REF: A<br>ALT: G</code>

- **HGVS:** <code>VN1R1:p.Asn151Thr</code>
  - **Variant Recoder:**<br><code>NC_000019.10:57456035<br>REF: T<br>ALT: G</code>
  - **hgvs2vcf:**<br><code>NC_000019.10:57456035<br>REF: T<br>ALT: G</code>

- **HGVS:** <code>CACNA1E:p.Gln870Lys</code>
  - **Variant Recoder:**<br><code>NC_000001.11:181732694<br>REF: C<br>ALT: A</code>
  - **hgvs2vcf:**<br><code>NC_000001.11:181732694<br>REF: C<br>ALT: A</code>

### utr_del

- **HGVS:** <code>NAGA:c.*1789del</code>
  - **Variant Recoder:**<br><code>NC_000022.11:42058489<br>REF: GA<br>ALT: G</code>
  - **hgvs2vcf:**<br><code>NC_000022.11:42058489<br>REF: GA<br>ALT: G</code>

### utr_delins

- **HGVS:** <code>GMPPB:c.-5_-4delinsTT</code>
  - **Variant Recoder:**<br><code>NC_000003.12:49723730<br>REF: GC<br>ALT: AA</code>
  - **hgvs2vcf:**<br><code>NC_000003.12:49723730<br>REF: GC<br>ALT: AA</code>

- **HGVS:** <code>ALPK3:c.-84_-83delinsAA</code>
  - **Variant Recoder:**<br><code>NC_000015.10:84817369<br>REF: GC<br>ALT: AA</code>
  - **hgvs2vcf:**<br><code>NC_000015.10:84817369<br>REF: GC<br>ALT: AA</code>

### utr_ins

- **HGVS:** <code>ZFYVE26:c.-84+209_-84+21<wbr>0insGG</code>
  - **Variant Recoder:**<br><code>NC_000014.9:67816324<br>REF: G<br>ALT: GCC</code>
  - **hgvs2vcf:**<br><code>NC_000014.9:67816324<br>REF: G<br>ALT: GCC</code>

- **HGVS:** <code>ADRB2:c.*25_*26insG</code>
  - **Variant Recoder:**<br><code>NC_000005.10:148828098<br>REF: C<br>ALT: CG</code>
  - **hgvs2vcf:**<br><code>NC_000005.10:148828098<br>REF: C<br>ALT: CG</code>

### utr_substitution

- **HGVS:** <code>ATP5F1A:c.-59G&gt;T</code>
  - **Variant Recoder:**<br><code>NC_000018.10:46098290<br>REF: C<br>ALT: A</code>
  - **hgvs2vcf:**<br><code>NC_000018.10:46098290<br>REF: C<br>ALT: A</code>

- **HGVS:** <code>IGF1R:c.*5092C&gt;G</code>
  - **Variant Recoder:**<br><code>NC_000015.10:98962534<br>REF: C<br>ALT: G</code>
  - **hgvs2vcf:**<br><code>NC_000015.10:98962534<br>REF: C<br>ALT: G</code>

## Failed results

### coding_del

- **HGVS:** <code>VHL:c.402_428del</code>
  - **Variant Recoder:**<br><code>NC_000003.12:10146574<br>REF: AATTATTTGTGCCATCTCTCAATG<wbr>TTGA<br>ALT: A</code>
  - **hgvs2vcf:**<br><code>NC_000003.12:10146571<br>REF: CTGAATTATTTGTGCCATCTCTCA<wbr>ATGT<br>ALT: C</code>
  - **Difference:** VCF mismatch

- **HGVS:** <code>NM_001370404:c.4944_4972<wbr>del</code>
  - **Variant Recoder:**<br><code>NC_000016.10:2088054<br>REF: AGGGCCTTGTGGACACCAGCGTGG<wbr>CCAAGA<br>ALT: A</code>
  - **hgvs2vcf:**<br><code>NC_000016.10:2088052<br>REF: GGAGGGCCTTGTGGACACCAGCGT<wbr>GGCCAA<br>ALT: G</code>
  - **Difference:** VCF mismatch

### coding_delins

- **HGVS:** <code>NM_001258274:c.409_411de<wbr>linsA</code>
  - **Variant Recoder:**<br><code>NC_000003.12:37025729<br>REF: GGTC<br>ALT: GA</code>
  - **hgvs2vcf:**<br><code>NC_000003.12:37025730<br>REF: GTC<br>ALT: A</code>
  - **Difference:** VCF mismatch

- **HGVS:** <code>PCSK9:c.1378_1380delinsT<wbr>G</code>
  - **Variant Recoder:**<br><code>NC_000001.11:55058521<br>REF: TGTA<br>ALT: TTG</code>
  - **hgvs2vcf:**<br><code>NC_000001.11:55058522<br>REF: GTA<br>ALT: TG</code>
  - **Difference:** VCF mismatch

- **HGVS:** <code>NM_004020:c.90delinsAA</code>
  - **Variant Recoder:**<br><code>NC_000023.11:31774031<br>REF: GA<br>ALT: GTT</code>
  - **hgvs2vcf:**<br><code>NC_000023.11:31774032<br>REF: A<br>ALT: TT</code>
  - **Difference:** VCF mismatch

- **HGVS:** <code>NM_001165412:c.1673_1676<wbr>delinsCTTAC</code>
  - **Variant Recoder:**<br><code>NC_000004.12:102600932<br>REF: CTTGT<br>ALT: CCTTAC</code>
  - **hgvs2vcf:**<br><code>NC_000004.12:102600933<br>REF: TTGT<br>ALT: CTTAC</code>
  - **Difference:** VCF mismatch

### coding_dup

- **HGVS:** <code>NM_000546:c.875_876dup</code>
  - **Variant Recoder:**<br><code>NC_000017.11:7673745<br>REF: T<br>ALT: TTT</code>
  - **hgvs2vcf:**<br><code>NC_000017.11:7673743<br>REF: C<br>ALT: CTT</code>
  - **Difference:** VCF mismatch

- **HGVS:** <code>NM_145862:c.933_934dup</code>
  - **Variant Recoder:**<br><code>NC_000022.11:28699913<br>REF: G<br>ALT: GTG</code>
  - **hgvs2vcf:**<br><code>NC_000022.11:28699911<br>REF: T<br>ALT: TTG</code>
  - **Difference:** VCF mismatch

- **HGVS:** <code>NM_201572:c.1754dup</code>
  - **Variant Recoder:**<br><code>NC_000010.11:18539650<br>REF: A<br>ALT: AA</code>
  - **hgvs2vcf:**<br><code>NC_000010.11:18539647<br>REF: G<br>ALT: GA</code>
  - **Difference:** VCF mismatch

- **HGVS:** <code>NR3C1:c.1248dup</code>
  - **Variant Recoder:**<br><code>NC_000005.10:143314105<br>REF: T<br>ALT: TT</code>
  - **hgvs2vcf:**<br><code>NC_000005.10:143314104<br>REF: G<br>ALT: GT</code>
  - **Difference:** VCF mismatch

### intronic_del

- **HGVS:** <code>NM_001353119:c.1330-3076<wbr>_1330-2999del</code>
  - **Variant Recoder:**<br><code>NC_000003.12:134558300<br>REF: TAAACCAACACACAGCAGAACAAC<wbr>TGAGTTCAAGAATACAGAGTTCAA<wbr>GTAAAATTTTTTAAAAGTTTATTT<wbr>AAAATGT<br>ALT: T</code>
  - **hgvs2vcf:**<br><code>NC_000003.12:134558299<br>REF: TTAAACCAACACACAGCAGAACAA<wbr>CTGAGTTCAAGAATACAGAGTTCA<wbr>AGTAAAATTTTTTAAAAGTTTATT<wbr>TAAAATG<br>ALT: T</code>
  - **Difference:** VCF mismatch

- **HGVS:** <code>AK7:c.1556-9_1556-7del</code>
  - **Variant Recoder:**<br><code>NC_000014.9:96478455<br>REF: TTCT<br>ALT: T</code>
  - **hgvs2vcf:**<br><code>NC_000014.9:96478453<br>REF: CCTT<br>ALT: C</code>
  - **Difference:** VCF mismatch

### intronic_delins

- **HGVS:** <code>NM_001330368:c.640+20485<wbr>_640+20491delinsA</code>
  - **Variant Recoder:**<br><code>NC_000011.10:108365428<br>REF: CAAGTGAA<br>ALT: CT</code>
  - **hgvs2vcf:**<br><code>NC_000011.10:108365429<br>REF: AAGTGAA<br>ALT: T</code>
  - **Difference:** VCF mismatch

- **HGVS:** <code>MIA2:c.3180+11delinsGTGT<wbr>G</code>
  - **Variant Recoder:**<br><code>NC_000014.9:39314809<br>REF: TA<br>ALT: TGTGTG</code>
  - **hgvs2vcf:**<br><code>NC_000014.9:39314810<br>REF: A<br>ALT: GTGTG</code>
  - **Difference:** VCF mismatch

### intronic_dup

- **HGVS:** <code>EXT1:c.1417+2dup</code>
  - **Variant Recoder:**<br><code>NC_000008.11:117822463<br>REF: A<br>ALT: AA</code>
  - **hgvs2vcf:**<br><code>NC_000008.11:117822462<br>REF: T<br>ALT: TA</code>
  - **Difference:** VCF mismatch

- **HGVS:** <code>NM_001378457:c.8604+8_86<wbr>04+12dup</code>
  - **Variant Recoder:**<br><code>NC_000015.10:51455143<br>REF: A<br>ALT: AAGTGA</code>
  - **hgvs2vcf:**<br><code>NC_000015.10:51455138<br>REF: T<br>ALT: TAGTGA</code>
  - **Difference:** VCF mismatch

- **HGVS:** <code>NM_001206927:c.611-140_6<wbr>11-139dup</code>
  - **Variant Recoder:**<br><code>NC_000006.12:38734333<br>REF: C<br>ALT: CCC</code>
  - **hgvs2vcf:**<br><code>NC_000006.12:38734326<br>REF: A<br>ALT: ACC</code>
  - **Difference:** VCF mismatch

### intronic_ins

- **HGVS:** <code>DCAF15:c.1440+33_1440+34<wbr>insGGGCAGGGTGGGCCCAGGGCG<wbr>GGCAGGGTGGGCCCAGGGC</code>
  - **Variant Recoder:**<br><code>NC_000019.10:13959928<br>REF: C<br>ALT: CGGGCAGGGTGGGCCCAGGGCGGG<wbr>CAGGGTGGGCCCAGGGC</code>
  - **hgvs2vcf:**<br><code>NC_000019.10:13959894<br>REF: A<br>ALT: AGGTGGGCCCAGGGCGGGCAGGGT<wbr>GGGCCCAGGGCGGGCAG</code>
  - **Difference:** VCF mismatch

### protein_del

- **HGVS:** <code>TUBB2A:p.Glu440del</code>
  - **Variant Recoder:**<br><code>NC_000006.12:3153880<br>REF: CCTC<br>ALT: C</code>
  - **hgvs2vcf:**<br><code>NC_000006.12:3153879<br>REF: CCCT<br>ALT: C</code>
  - **Difference:** VCF mismatch

- **HGVS:** <code>GLS:p.Asn351del</code>
  - **Variant Recoder:**<br><code>NC_000002.12:190921035<br>REF: TAAT<br>ALT: T</code>
  - **hgvs2vcf:**<br><code>NC_000002.12:190921032<br>REF: AAAT<br>ALT: A</code>
  - **Difference:** VCF mismatch

- **HGVS:** <code>FOXE1:p.Ala177_Ala179del</code>
  - **Variant Recoder:**<br><code>NC_000009.12:97854442<br>REF: CGCCGCCGCC<br>ALT: C</code>
  - **hgvs2vcf:**<br><code>NC_000009.12:97854418<br>REF: AGCCGCCGCC<br>ALT: A</code>
  - **Difference:** VCF mismatch

- **HGVS:** <code>RNF213:p.Gly405del</code>
  - **Variant Recoder:**<br><code>NC_000017.11:80290669<br>REF: AGGA<br>ALT: A</code>
  - **hgvs2vcf:**<br><code>NC_000017.11:80290664<br>REF: AGAG<br>ALT: A</code>
  - **Difference:** VCF mismatch

### utr_del

- **HGVS:** <code>ARL13B:c.*1_*4delACAA</code>
  - **Variant Recoder:**<br><code>NC_000003.12:94053263<br>REF: AACAA<br>ALT: A</code>
  - **hgvs2vcf:**<br><code>NC_000003.12:94053261<br>REF: TAAAC<br>ALT: T</code>
  - **Difference:** VCF mismatch

### utr_dup

- **HGVS:** <code>DNAAF4:c.-255-340dup</code>
  - **Variant Recoder:**<br><code>NC_000015.10:55498924<br>REF: A<br>ALT: AA</code>
  - **hgvs2vcf:**<br><code>NC_000015.10:55498911<br>REF: C<br>ALT: CA</code>
  - **Difference:** VCF mismatch

- **HGVS:** <code>SPTA1:c.-121dup</code>
  - **Variant Recoder:**<br><code>NC_000001.11:158686638<br>REF: G<br>ALT: GG</code>
  - **hgvs2vcf:**<br><code>NC_000001.11:158686637<br>REF: T<br>ALT: TG</code>
  - **Difference:** VCF mismatch
