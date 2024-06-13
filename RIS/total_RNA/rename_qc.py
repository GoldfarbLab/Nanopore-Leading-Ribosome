#!/usr/bin/env python
import sys
import os
from Bio import SeqIO
from collections import defaultdict

isoforms_protein_infile = sys.argv[1]
out_path = sys.argv[2]


gene2transcript = defaultdict(list)
transcript_count = 0
no_gene_count = 0
newly_translated_count = 0

transcripts_prot = SeqIO.parse(isoforms_protein_infile, 'fasta')
for transcript in transcripts_prot:
    transcript_count+=1
    
    if "Gene=" in transcript.description:
        gene = transcript.description.split("Gene=")[-1]
        gene2transcript[gene].append(transcript)
    else:
        no_gene_count+=1
        
    if "BLAST" in transcript.description:
        newly_translated_count+=1
        


iso2count = defaultdict(int)
for gene in gene2transcript:
    iso2count[len(gene2transcript[gene])] +=1

with open(out_path, 'w') as file_handle:
    file_handle.write(f"{transcript_count:,}".rjust(6, ' ') + " transcripts\n")
    file_handle.write(f"{transcript_count-no_gene_count:,}".rjust(6, ' ') + " annotated with genes \n")
    file_handle.write(f"{no_gene_count:,}".rjust(6, ' ') + " not annotated with genes \n")
    file_handle.write(f"{newly_translated_count:,}".rjust(6, ' ') + " translated with BLAST validation \n")
    
    for iso in sorted(iso2count.keys()):
        file_handle.write(f"{iso2count[iso]:,}".rjust(6, ' ') + " genes with " + str(iso) + " transcripts\n")
    
    
