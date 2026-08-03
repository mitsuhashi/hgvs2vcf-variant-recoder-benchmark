# hgvs2vcf-cdot-lmdb evaluation

- Total: 100
- Passed: 8
- Failed: 92
- Pass rate: 8.00%
- Elapsed: 2.296 s

## Results by category

| Category | Passed | Failed | Pass rate |
|---|---:|---:|---:|
| coding_del | 0 | 5 | 0.00% |
| coding_delins | 0 | 8 | 0.00% |
| coding_dup | 0 | 6 | 0.00% |
| coding_ins | 0 | 4 | 0.00% |
| coding_other | 0 | 1 | 0.00% |
| coding_substitution | 4 | 3 | 57.14% |
| intronic_del | 0 | 6 | 0.00% |
| intronic_delins | 0 | 4 | 0.00% |
| intronic_dup | 0 | 5 | 0.00% |
| intronic_ins | 0 | 2 | 0.00% |
| intronic_other | 0 | 1 | 0.00% |
| intronic_substitution | 4 | 2 | 66.67% |
| protein_del | 0 | 10 | 0.00% |
| protein_other | 0 | 13 | 0.00% |
| protein_substitution | 0 | 12 | 0.00% |
| utr_del | 0 | 2 | 0.00% |
| utr_delins | 0 | 2 | 0.00% |
| utr_dup | 0 | 2 | 0.00% |
| utr_ins | 0 | 2 | 0.00% |
| utr_substitution | 0 | 2 | 0.00% |

## All results

| Result | HGVS | Variant Recoder expected VCF | hgvs2vcf observed VCF | Differences |
|---|---|---|---|---|
| FAIL | `VHL:c.402_428del` | `NC_000003.12:10146574 AATTATTTGTGCCATCTCTCAATGTTGA>A` | Error: `edit type del not yet implemented in this prototype` | `{"error": {"expected": null, "observed": "edit type del not yet implemented in this prototype"}}` |
| FAIL | `TUBB2A:p.Glu440del` | `NC_000006.12:3153880 CCTC>C` | Error: `unsupported protein change "p.Glu440del" (only substitutions here)` | `{"error": {"expected": null, "observed": "unsupported protein change \"p.Glu440del\" (only substitutions here)"}}` |
| FAIL | `NM_000720:c.2151_2152del` | `NC_000003.12:53723989 CAG>C` | Error: `edit type del not yet implemented in this prototype` | `{"error": {"expected": null, "observed": "edit type del not yet implemented in this prototype"}}` |
| FAIL | `MYH14:c.2337_2338delinsAA` | `NC_000019.10:50259248 CC>AA` | Error: `edit type delins not yet implemented in this prototype` | `{"error": {"expected": null, "observed": "edit type delins not yet implemented in this prototype"}}` |
| FAIL | `MTR:p.Ile441=` | `NC_000001.11:236835681 C>A`<br>`NC_000001.11:236835681 C>T` | Error: `unsupported protein change "p.Ile441=" (only substitutions here)` | `{"error": {"expected": null, "observed": "unsupported protein change \"p.Ile441=\" (only substitutions here)"}}` |
| FAIL | `NM_001368038:c.835_837delinsTGC` | `NC_000012.12:94375982 ACG>GCA` | Error: `edit type delins not yet implemented in this prototype` | `{"error": {"expected": null, "observed": "edit type delins not yet implemented in this prototype"}}` |
| FAIL | `VIM:c.1374_1375dup` | `NC_000010.11:17237243 C>CTT` | Error: `edit type dup not yet implemented in this prototype` | `{"error": {"expected": null, "observed": "edit type dup not yet implemented in this prototype"}}` |
| FAIL | `OR6A2:p.Thr44Ile` | `NC_000011.10:6795578 G>A` | `NC_000011.10:6795578 G>A` | `{"transcript": {"expected": "NM_003696.3", "observed": "ENST00000641196.1"}}` |
| FAIL | `NM_000546:c.875_876dup` | `NC_000017.11:7673745 T>TTT` | Error: `edit type dup not yet implemented in this prototype` | `{"error": {"expected": null, "observed": "edit type dup not yet implemented in this prototype"}}` |
| FAIL | `MMUT:c.96_97insGG` | `NC_000006.12:49459370 G>GCC` | Error: `edit type ins not yet implemented in this prototype` | `{"error": {"expected": null, "observed": "edit type ins not yet implemented in this prototype"}}` |
| FAIL | `GLS:p.Asn351del` | `NC_000002.12:190921035 TAAT>T` | Error: `unsupported protein change "p.Asn351del" (only substitutions here)` | `{"error": {"expected": null, "observed": "unsupported protein change \"p.Asn351del\" (only substitutions here)"}}` |
| FAIL | `NM_018136:c.5101_5102insG` | `NC_000001.11:197104149 A>AC` | Error: `edit type ins not yet implemented in this prototype` | `{"error": {"expected": null, "observed": "edit type ins not yet implemented in this prototype"}}` |
| FAIL | `EYS:c.1478G>A` | `NC_000006.12:65344159 C>T` | `NC_000006.12:65344159 C>T` | `{"transcript": {"expected": "NM_001142800.2", "observed": "ENST00000503581.6"}}` |
| FAIL | `MS4A1:p.Leu61=` | `NC_000011.10:60463025 C>A`<br>`NC_000011.10:60463025 C>G`<br>`NC_000011.10:60463025 C>T` | Error: `unsupported protein change "p.Leu61=" (only substitutions here)` | `{"error": {"expected": null, "observed": "unsupported protein change \"p.Leu61=\" (only substitutions here)"}}` |
| FAIL | `NM_001277115:c.12492_12493inv` | `NC_000007.14:21884395 CA>TG` | Error: `unsupported cDNA change "c.12492_12493inv"` | `{"error": {"expected": null, "observed": "unsupported cDNA change \"c.12492_12493inv\""}}` |
| FAIL | `TMEM237:c.554-56del` | `NC_000002.12:201629907 AT>A` | Error: `edit type del not yet implemented in this prototype` | `{"error": {"expected": null, "observed": "edit type del not yet implemented in this prototype"}}` |
| FAIL | `CLDN19:p.Ala14Asp` | `NC_000001.11:42740023 G>T` | `NC_000001.11:42740023 G>T` | `{"transcript": {"expected": "NM_148960.3", "observed": "ENST00000296387.6"}}` |
| PASS | `NM_001376241:c.1011C>A` | `NC_000002.12:159748301 C>A` | `NC_000002.12:159748301 C>A` | — |
| FAIL | `CDH1:c.48+6_48+7delinsTG` | `NC_000016.10:68737469 CC>TG` | Error: `edit type delins not yet implemented in this prototype` | `{"error": {"expected": null, "observed": "edit type delins not yet implemented in this prototype"}}` |
| FAIL | `GRIN2B:p.Asn1366del` | `NC_000012.12:13563139 GGTT>G` | Error: `unsupported protein change "p.Asn1366del" (only substitutions here)` | `{"error": {"expected": null, "observed": "unsupported protein change \"p.Asn1366del\" (only substitutions here)"}}` |
| FAIL | `NM_033115:c.267-10220_267-10219del` | `NC_000004.12:106262225 CAA>C` | Error: `edit type del not yet implemented in this prototype` | `{"error": {"expected": null, "observed": "edit type del not yet implemented in this prototype"}}` |
| FAIL | `EXT1:c.1417+2dup` | `NC_000008.11:117822463 A>AA` | Error: `edit type dup not yet implemented in this prototype` | `{"error": {"expected": null, "observed": "edit type dup not yet implemented in this prototype"}}` |
| FAIL | `CSF1:p.Arg404=` | `NC_000001.11:109923831 A>C`<br>`NC_000001.11:109923833 G>A` | Error: `unsupported protein change "p.Arg404=" (only substitutions here)` | `{"error": {"expected": null, "observed": "unsupported protein change \"p.Arg404=\" (only substitutions here)"}}` |
| FAIL | `NM_000154:c.166-5_166-4delinsAT` | `NC_000017.11:75764090 GC>AT` | Error: `edit type delins not yet implemented in this prototype` | `{"error": {"expected": null, "observed": "edit type delins not yet implemented in this prototype"}}` |
| FAIL | `SCN8A:c.2545-19_2545-18insC` | `NC_000012.12:51765652 G>GC` | Error: `edit type ins not yet implemented in this prototype` | `{"error": {"expected": null, "observed": "edit type ins not yet implemented in this prototype"}}` |
| FAIL | `IGDCC3:p.Ile98Thr` | `NC_000015.10:65375213 A>G` | `NC_000015.10:65375213 A>G` | `{"transcript": {"expected": "NM_004884.4", "observed": "ENST00000327987.9"}}` |
| FAIL | `NM_032446:c.2362+2dupT` | `NC_000005.10:127440868 G>GT` | Error: `edit type dup not yet implemented in this prototype` | `{"error": {"expected": null, "observed": "edit type dup not yet implemented in this prototype"}}` |
| FAIL | `LAMA3:c.7645-1G>A` | `NC_000018.10:23915288 G>A` | `NC_000018.10:23915288 G>A` | `{"transcript": {"expected": "NM_198129.4", "observed": "ENST00000313654.14"}}` |
| FAIL | `EP400:p.Gln2748del` | `NC_000012.12:132062608 ACAG>A` | Error: `unsupported protein change "p.Gln2748del" (only substitutions here)` | `{"error": {"expected": null, "observed": "unsupported protein change \"p.Gln2748del\" (only substitutions here)"}}` |
| FAIL | `NM_000138:c.6617-9_6617-8inv` | `NC_000015.10:48432996 AG>CT` | Error: `unsupported cDNA change "c.6617-9_6617-8inv"` | `{"error": {"expected": null, "observed": "unsupported cDNA change \"c.6617-9_6617-8inv\""}}` |
| FAIL | `ARL13B:c.*1_*4delACAA` | `NC_000003.12:94053263 AACAA>A` | Error: `unsupported cDNA change "c.*1_*4delACAA"` | `{"error": {"expected": null, "observed": "unsupported cDNA change \"c.*1_*4delACAA\""}}` |
| FAIL | `CDH23:p.Pro463=` | `NC_000010.11:71646557 A>C`<br>`NC_000010.11:71646557 A>G`<br>`NC_000010.11:71646557 A>T` | Error: `unsupported protein change "p.Pro463=" (only substitutions here)` | `{"error": {"expected": null, "observed": "unsupported protein change \"p.Pro463=\" (only substitutions here)"}}` |
| PASS | `NM_001352303:c.76+20C>A` | `NC_000022.11:19931010 G>T` | `NC_000022.11:19931010 G>T` | — |
| FAIL | `GMPPB:c.-5_-4delinsTT` | `NC_000003.12:49723730 GC>AA` | Error: `unsupported cDNA change "c.-5_-4delinsTT"` | `{"error": {"expected": null, "observed": "unsupported cDNA change \"c.-5_-4delinsTT\""}}` |
| FAIL | `MITF:p.Gly462Glu` | `NC_000003.12:69965052 G>A` | `NC_000003.12:69965052 G>A` | `{"transcript": {"expected": "NM_001354604.2", "observed": "ENST00000352241.9"}}` |
| FAIL | `NM_001374828:c.6504del` | `NC_000006.12:157207275 GC>G` | Error: `edit type del not yet implemented in this prototype` | `{"error": {"expected": null, "observed": "edit type del not yet implemented in this prototype"}}` |
| FAIL | `DNAAF4:c.-255-340dup` | `NC_000015.10:55498924 A>AA` | Error: `unsupported cDNA change "c.-255-340dup"` | `{"error": {"expected": null, "observed": "unsupported cDNA change \"c.-255-340dup\""}}` |
| FAIL | `FOXE1:p.Ala177_Ala179del` | `NC_000009.12:97854442 CGCCGCCGCC>C` | Error: `unsupported protein change "p.Ala177_Ala179del" (only substitutions here)` | `{"error": {"expected": null, "observed": "unsupported protein change \"p.Ala177_Ala179del\" (only substitutions here)"}}` |
| FAIL | `NM_001258274:c.409_411delinsA` | `NC_000003.12:37025729 GGTC>GA` | Error: `edit type delins not yet implemented in this prototype` | `{"error": {"expected": null, "observed": "edit type delins not yet implemented in this prototype"}}` |
| FAIL | `ZFYVE26:c.-84+209_-84+210insGG` | `NC_000014.9:67816324 G>GCC` | Error: `unsupported cDNA change "c.-84+209_-84+210insGG"` | `{"error": {"expected": null, "observed": "unsupported cDNA change \"c.-84+209_-84+210insGG\""}}` |
| FAIL | `CELSR2:p.His1300=` | `NC_000001.11:109259021 C>T` | Error: `unsupported protein change "p.His1300=" (only substitutions here)` | `{"error": {"expected": null, "observed": "unsupported protein change \"p.His1300=\" (only substitutions here)"}}` |
| FAIL | `NM_145862:c.933_934dup` | `NC_000022.11:28699913 G>GTG` | Error: `edit type dup not yet implemented in this prototype` | `{"error": {"expected": null, "observed": "edit type dup not yet implemented in this prototype"}}` |
| FAIL | `ATP5F1A:c.-59G>T` | `NC_000018.10:46098290 C>A` | Error: `unsupported cDNA change "c.-59G>T"` | `{"error": {"expected": null, "observed": "unsupported cDNA change \"c.-59G>T\""}}` |
| FAIL | `ZNF407:p.Arg1227His` | `NC_000018.10:74634699 G>A` | `NC_000018.10:74634699 G>A` | `{"transcript": {"expected": "NM_017757.3", "observed": "ENST00000299687.10"}}` |
| PASS | `NM_004407:c.1339A>G` | `NC_000004.12:87663117 A>G` | `NC_000004.12:87663117 A>G` | — |
| FAIL | `SLC5A1:c.1566del` | `NC_000022.11:32102137 GT>G` | Error: `edit type del not yet implemented in this prototype` | `{"error": {"expected": null, "observed": "edit type del not yet implemented in this prototype"}}` |
| FAIL | `HIVEP2:p.Asn1911_Asp1912del` | `NC_000006.12:142760551 CATCATT>C` | Error: `unsupported protein change "p.Asn1911_Asp1912del" (only substitutions here)` | `{"error": {"expected": null, "observed": "unsupported protein change \"p.Asn1911_Asp1912del\" (only substitutions here)"}}` |
| FAIL | `NM_001316329:c.2090+1_2091-1del` | `NC_000019.10:53906891 TGTAATCTCACCCGCCGCCACTAGGTGTCCCCAACGTCCCCTCCGCCGTGCCGGCGGCAGCCCCACTTCACCCCCAACTTCACCACCCCCTGTCCCATTCTAG>T` | Error: `edit type del not yet implemented in this prototype` | `{"error": {"expected": null, "observed": "edit type del not yet implemented in this prototype"}}` |
| FAIL | `PCSK9:c.1378_1380delinsTG` | `NC_000001.11:55058521 TGTA>TTG` | Error: `edit type delins not yet implemented in this prototype` | `{"error": {"expected": null, "observed": "edit type delins not yet implemented in this prototype"}}` |
| FAIL | `GLI1:p.Pro631=` | `NC_000012.12:57470633 C>A`<br>`NC_000012.12:57470633 C>G`<br>`NC_000012.12:57470633 C>T` | Error: `unsupported protein change "p.Pro631=" (only substitutions here)` | `{"error": {"expected": null, "observed": "unsupported protein change \"p.Pro631=\" (only substitutions here)"}}` |
| FAIL | `NM_001330368:c.640+20485_640+20491delinsA` | `NC_000011.10:108365428 CAAGTGAA>CT` | Error: `edit type delins not yet implemented in this prototype` | `{"error": {"expected": null, "observed": "edit type delins not yet implemented in this prototype"}}` |
| FAIL | `GAN:c.1690dup` | `NC_000016.10:81377491 C>CG` | Error: `edit type dup not yet implemented in this prototype` | `{"error": {"expected": null, "observed": "edit type dup not yet implemented in this prototype"}}` |
| FAIL | `RP2:p.Thr56Met` | `NC_000023.11:46853540 C>T` | `NC_000023.11:46853540 C>T` | `{"transcript": {"expected": "NM_006915.3", "observed": "ENST00000218340.4"}}` |
| FAIL | `NM_001378457:c.8604+8_8604+12dup` | `NC_000015.10:51455143 A>AAGTGA` | Error: `edit type dup not yet implemented in this prototype` | `{"error": {"expected": null, "observed": "edit type dup not yet implemented in this prototype"}}` |
| FAIL | `NPHS1:c.2354_2355insTCGTCGTGCTGCT` | `NC_000019.10:35842530 C>CAGCAGCACGACGA` | Error: `edit type ins not yet implemented in this prototype` | `{"error": {"expected": null, "observed": "edit type ins not yet implemented in this prototype"}}` |
| FAIL | `ATRX:p.Leu821_Glu822del` | `NC_000023.11:77682789 TTTCTAA>T` | Error: `unsupported protein change "p.Leu821_Glu822del" (only substitutions here)` | `{"error": {"expected": null, "observed": "unsupported protein change \"p.Leu821_Glu822del\" (only substitutions here)"}}` |
| PASS | `NM_001167819:c.502-2A>G` | `NC_000023.11:136208453 A>G` | `NC_000023.11:136208453 A>G` | — |
| FAIL | `ZDHHC9:c.812A>G` | `NC_000023.11:129811475 T>C` | `NC_000023.11:129811475 T>C` | `{"transcript": {"expected": "NM_016032.4", "observed": "ENST00000357166.11"}}` |
| FAIL | `COL4A4:p.Gly373=` | `NC_000002.12:227098779 C>A`<br>`NC_000002.12:227098779 C>G`<br>`NC_000002.12:227098779 C>T` | Error: `unsupported protein change "p.Gly373=" (only substitutions here)` | `{"error": {"expected": null, "observed": "unsupported protein change \"p.Gly373=\" (only substitutions here)"}}` |
| FAIL | `NM_001370404:c.4944_4972del` | `NC_000016.10:2088054 AGGGCCTTGTGGACACCAGCGTGGCCAAGA>A` | Error: `edit type del not yet implemented in this prototype` | `{"error": {"expected": null, "observed": "edit type del not yet implemented in this prototype"}}` |
| FAIL | `SLC39A4:c.805-3del` | `NC_000008.11:144414898 TG>T` | Error: `edit type del not yet implemented in this prototype` | `{"error": {"expected": null, "observed": "edit type del not yet implemented in this prototype"}}` |
| FAIL | `ARHGEF5:p.Glu918Lys` | `NC_000007.14:144365421 G>A` | `NC_000007.14:144365421 G>A` | `{"transcript": {"expected": "NM_005435.4", "observed": "ENST00000056217.10"}}` |
| FAIL | `NM_004020:c.90delinsAA` | `NC_000023.11:31774031 GA>GTT` | Error: `edit type delins not yet implemented in this prototype` | `{"error": {"expected": null, "observed": "edit type delins not yet implemented in this prototype"}}` |
| FAIL | `MIA2:c.3180+11delinsGTGTG` | `NC_000014.9:39314809 TA>TGTGTG` | Error: `edit type delins not yet implemented in this prototype` | `{"error": {"expected": null, "observed": "edit type delins not yet implemented in this prototype"}}` |
| FAIL | `SLC25A12:p.Phe646_Thr677del` | `NC_000002.12:171785279 GAGTGGCTGCCACTGCTGCCTTTGGCTGAACCACAGCAACACTAGGAGACTTAAATTTCGGGAGATAAAGGCCAAATTTGTTTTCGATGCCTGCAAA>G` | Error: `unsupported protein change "p.Phe646_Thr677del" (only substitutions here)` | `{"error": {"expected": null, "observed": "unsupported protein change \"p.Phe646_Thr677del\" (only substitutions here)"}}` |
| FAIL | `NM_201572:c.1754dup` | `NC_000010.11:18539650 A>AA` | Error: `edit type dup not yet implemented in this prototype` | `{"error": {"expected": null, "observed": "edit type dup not yet implemented in this prototype"}}` |
| FAIL | `GYG1:c.609-15dup` | `NC_000003.12:149024037 T>TG` | Error: `edit type dup not yet implemented in this prototype` | `{"error": {"expected": null, "observed": "edit type dup not yet implemented in this prototype"}}` |
| FAIL | `TBC1D15:p.Gly495=` | `NC_000012.12:71917781 A>C`<br>`NC_000012.12:71917781 A>G`<br>`NC_000012.12:71917781 A>T` | Error: `unsupported protein change "p.Gly495=" (only substitutions here)` | `{"error": {"expected": null, "observed": "unsupported protein change \"p.Gly495=\" (only substitutions here)"}}` |
| PASS | `NM_001287489:c.5565G>A` | `NC_000002.12:26460999 C>T` | `NC_000002.12:26460999 C>T` | — |
| FAIL | `DCAF15:c.1440+33_1440+34insGGGCAGGGTGGGCCCAGGGCGGGCAGGGTGGGCCCAGGGC` | `NC_000019.10:13959928 C>CGGGCAGGGTGGGCCCAGGGCGGGCAGGGTGGGCCCAGGGC` | Error: `edit type ins not yet implemented in this prototype` | `{"error": {"expected": null, "observed": "edit type ins not yet implemented in this prototype"}}` |
| FAIL | `KALRN:p.Arg1799Gln` | `NC_000003.12:124632633 G>A` | `NC_000003.12:124632633 G>A` | `{"transcript": {"expected": "NM_001388419.1", "observed": "ENST00000682506.1"}}` |
| FAIL | `NM_001353119:c.1330-3076_1330-2999del` | `NC_000003.12:134558300 TAAACCAACACACAGCAGAACAACTGAGTTCAAGAATACAGAGTTCAAGTAAAATTTTTTAAAAGTTTATTTAAAATGT>T` | Error: `edit type del not yet implemented in this prototype` | `{"error": {"expected": null, "observed": "edit type del not yet implemented in this prototype"}}` |
| FAIL | `MCM8:c.1255-10C>T` | `NC_000020.11:5973046 C>T` | `NC_000020.11:5973046 C>T` | `{"transcript": {"expected": "NM_032485.6", "observed": "ENST00000610722.4"}}` |
| FAIL | `CITED2:p.His144_Gln145del` | `NC_000006.12:139373509 TCTGGTG>T` | Error: `unsupported protein change "p.His144_Gln145del" (only substitutions here)` | `{"error": {"expected": null, "observed": "unsupported protein change \"p.His144_Gln145del\" (only substitutions here)"}}` |
| FAIL | `NM_001206927:c.611-140_611-139dup` | `NC_000006.12:38734333 C>CCC` | Error: `edit type dup not yet implemented in this prototype` | `{"error": {"expected": null, "observed": "edit type dup not yet implemented in this prototype"}}` |
| FAIL | `NAGA:c.*1789del` | `NC_000022.11:42058489 GA>G` | Error: `unsupported cDNA change "c.*1789del"` | `{"error": {"expected": null, "observed": "unsupported cDNA change \"c.*1789del\""}}` |
| FAIL | `LRRK1:p.Thr1053=` | `NC_000015.10:101048517 T>A`<br>`NC_000015.10:101048517 T>C`<br>`NC_000015.10:101048517 T>G` | Error: `unsupported protein change "p.Thr1053=" (only substitutions here)` | `{"error": {"expected": null, "observed": "unsupported protein change \"p.Thr1053=\" (only substitutions here)"}}` |
| PASS | `NM_018924:c.2415+26628A>T` | `NC_000005.10:141399437 A>T` | `NC_000005.10:141399437 A>T` | — |
| FAIL | `ALPK3:c.-84_-83delinsAA` | `NC_000015.10:84817369 GC>AA` | Error: `unsupported cDNA change "c.-84_-83delinsAA"` | `{"error": {"expected": null, "observed": "unsupported cDNA change \"c.-84_-83delinsAA\""}}` |
| FAIL | `CYP2A6:p.Arg76Trp` | `NC_000019.10:40849935 G>A` | `NC_000019.10:40849935 G>A` | `{"transcript": {"expected": "NM_000762.6", "observed": "ENST00000301141.10"}}` |
| FAIL | `NM_001165412:c.1673_1676delinsCTTAC` | `NC_000004.12:102600932 CTTGT>CCTTAC` | Error: `edit type delins not yet implemented in this prototype` | `{"error": {"expected": null, "observed": "edit type delins not yet implemented in this prototype"}}` |
| FAIL | `SPTA1:c.-121dup` | `NC_000001.11:158686638 G>GG` | Error: `unsupported cDNA change "c.-121dup"` | `{"error": {"expected": null, "observed": "unsupported cDNA change \"c.-121dup\""}}` |
| FAIL | `RNF213:p.Gly405del` | `NC_000017.11:80290669 AGGA>A` | Error: `unsupported protein change "p.Gly405del" (only substitutions here)` | `{"error": {"expected": null, "observed": "unsupported protein change \"p.Gly405del\" (only substitutions here)"}}` |
| PASS | `NM_001287:c.528G>C` | `NC_000016.10:1460484 C>G` | `NC_000016.10:1460484 C>G` | — |
| FAIL | `ADRB2:c.*25_*26insG` | `NC_000005.10:148828098 C>CG` | Error: `unsupported cDNA change "c.*25_*26insG"` | `{"error": {"expected": null, "observed": "unsupported cDNA change \"c.*25_*26insG\""}}` |
| FAIL | `ZFYVE26:p.Glu1208=` | `NC_000014.9:67784336 C>T` | Error: `unsupported protein change "p.Glu1208=" (only substitutions here)` | `{"error": {"expected": null, "observed": "unsupported protein change \"p.Glu1208=\" (only substitutions here)"}}` |
| PASS | `NM_001365677:c.331+2T>C` | `NC_000005.10:132217195 A>G` | `NC_000005.10:132217195 A>G` | — |
| FAIL | `IGF1R:c.*5092C>G` | `NC_000015.10:98962534 C>G` | Error: `unsupported cDNA change "c.*5092C>G"` | `{"error": {"expected": null, "observed": "unsupported cDNA change \"c.*5092C>G\""}}` |
| FAIL | `COG6:p.Lys58Glu` | `NC_000013.11:39659382 A>G` | `NC_000013.11:39659382 A>G` | `{"transcript": {"expected": "NM_020751.3", "observed": "ENST00000455146.8"}}` |
| FAIL | `NM_133437:c.73258_73259delinsGT` | `NC_000002.12:178537231 TT>AC` | Error: `edit type delins not yet implemented in this prototype` | `{"error": {"expected": null, "observed": "edit type delins not yet implemented in this prototype"}}` |
| FAIL | `ALPL:c.608_609delinsTT` | `NC_000001.11:21564176 AC>TT` | Error: `edit type delins not yet implemented in this prototype` | `{"error": {"expected": null, "observed": "edit type delins not yet implemented in this prototype"}}` |
| FAIL | `PCK2:p.Pro427=` | `NC_000014.9:24102799 G>A`<br>`NC_000014.9:24102799 G>C`<br>`NC_000014.9:24102799 G>T` | Error: `unsupported protein change "p.Pro427=" (only substitutions here)` | `{"error": {"expected": null, "observed": "unsupported protein change \"p.Pro427=\" (only substitutions here)"}}` |
| FAIL | `NR3C1:c.1248dup` | `NC_000005.10:143314105 T>TT` | Error: `edit type dup not yet implemented in this prototype` | `{"error": {"expected": null, "observed": "edit type dup not yet implemented in this prototype"}}` |
| FAIL | `VN1R1:p.Asn151Thr` | `NC_000019.10:57456035 T>G` | `NC_000019.10:57456035 T>G` | `{"transcript": {"expected": "NM_020633.4", "observed": "ENST00000321039.5"}}` |
| FAIL | `HGSNAT:c.1054_1055insATCAATTTCTAATGGGATTTCCAGAGTTGAAAAAGACAAATATTCAGCTTTAGGAAGCACAGTTGAGTCCTGAGCAGTACAAATAAAAATATAGGCTGGGCACAGTGGCTCACATGTGTAATCCCAGCACTTTCGGAGGCTGAGGTGGGTGGATTGCTGGAGTCCAGCAGTTTGAAAACAGCCTGAGCAACATGGCAAGACCCCATCTCTACAAAAAATACAACAATTATCCGGGCATGGTGGCACAAGCCCGTAGTCCCAGCTACTCAGGAAGCTGAGGTGGATCGCTTGAGCCCGGGAGGTGGAGGTTGCAGTGAGCCAAGATCACACCATTGCACTCCACACTGAATGACAGAGTGAGACTGTCTTAATAAAAAATATGAGTCAGCGTATAAGTTAAAAGGAGTTTTAAAAGATACTAATCCAAAAGAAGGCAGAAAAGGAGAAACATAATAGACTTACCAGCCCAATTTAAAAGTCAGGGATTATAAACATGAATTGAAGAAGTGAGACCCAGTTA` | `NC_000008.11:43182186 T>TATCAATTTCTAATGGGATTTCCAGAGTTGAAAAAGACAAATATTCAGCTTTAGGAAGCACAGTTGAGTCCTGAGCAGTACAAATAAAAATATAGGCTGGGCACAGTGGCTCACATGTGTAATCCCAGCACTTTCGGAGGCTGAGGTGGGTGGATTGCTGGAGTCCAGCAGTTTGAAAACAGCCTGAGCAACATGGCAAGACCCCATCTCTACAAAAAATACAACAATTATCCGGGCATGGTGGCACAAGCCCGTAGTCCCAGCTACTCAGGAAGCTGAGGTGGATCGCTTGAGCCCGGGAGGTGGAGGTTGCAGTGAGCCAAGATCACACCATTGCACTCCACACTGAATGACAGAGTGAGACTGTCTTAATAAAAAATATGAGTCAGCGTATAAGTTAAAAGGAGTTTTAAAAGATACTAATCCAAAAGAAGGCAGAAAAGGAGAAACATAATAGACTTACCAGCCCAATTTAAAAGTCAGGGATTATAAACATGAATTGAAGAAGTGAGACCCAGTTA` | Error: `edit type ins not yet implemented in this prototype` | `{"error": {"expected": null, "observed": "edit type ins not yet implemented in this prototype"}}` |
| FAIL | `DDX6:p.Arg381=` | `NC_000011.10:118756291 T>A`<br>`NC_000011.10:118756291 T>C`<br>`NC_000011.10:118756291 T>G`<br>`NC_000011.10:118756293 G>T` | Error: `unsupported protein change "p.Arg381=" (only substitutions here)` | `{"error": {"expected": null, "observed": "unsupported protein change \"p.Arg381=\" (only substitutions here)"}}` |
| FAIL | `ASXL3:c.4228C>T` | `NC_000018.10:33744076 C>T` | `NC_000018.10:33744076 C>T` | `{"transcript": {"expected": "NM_030632.3", "observed": "ENST00000269197.12"}}` |
| FAIL | `CACNA1E:p.Gln870Lys` | `NC_000001.11:181732694 C>A` | `NC_000001.11:181732694 C>A` | `{"transcript": {"expected": "NM_001205293.3", "observed": "ENST00000367573.7"}}` |
| FAIL | `AK7:c.1556-9_1556-7del` | `NC_000014.9:96478455 TTCT>T` | Error: `edit type del not yet implemented in this prototype` | `{"error": {"expected": null, "observed": "edit type del not yet implemented in this prototype"}}` |
| FAIL | `ASNS:p.Ile462=` | `NC_000007.14:97853150 A>G`<br>`NC_000007.14:97853150 A>T` | Error: `unsupported protein change "p.Ile462=" (only substitutions here)` | `{"error": {"expected": null, "observed": "unsupported protein change \"p.Ile462=\" (only substitutions here)"}}` |
