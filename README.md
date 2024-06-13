### Reference Pipeline

1) utr
2) bed

### All RNA Pipeline

This generates a reference transcriptome using SQANTI. It uses both the total RNA and nanopore ribosomal profiling reads to construct it. Afterwards, the standard domain hidden markov models are applied to each transcript to get perfectly aligned domains.

1) align
2) align_concat
3) align_qc
4) reads
5) split
6) collapse
7) collapse_concat
8) collapse_qc
9) sqanti
10) blast_index
11) translate
12) rename
13) rename_qc
14) domains
15) format_domains
16) domains_qc
17) index

### Polysome Pipeline

This aligns the nanopore reads to the transcriptome and computes pause scores.

1) align
2) bam
3) bed
4) pause
5) bigwig
6) translate

