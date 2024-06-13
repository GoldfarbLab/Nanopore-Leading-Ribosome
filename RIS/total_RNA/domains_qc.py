#!/usr/bin/env python
import sys
import pandas as pd

gff_in_path = sys.argv[1]
fasta_in_path = sys.argv[2]
out_path = sys.argv[3]


# count transcripts
num_transcripts = 0
with open(fasta_in_path) as infile:
    for line in infile:
        if line[0] == ">":
            num_transcripts+=1
            
# read domains.gff
domains = pd.read_csv(gff_in_path, sep="\t", comment="#", header=None)

with open(out_path, "w") as outfile:
    # domains per transcript
    transcript_domains = domains.groupby([0])[0].count().reset_index(name='Domains per transcript')
    transcript_domains = transcript_domains.groupby(['Domains per transcript'])['Domains per transcript'].count()
    transcript_domains.loc[0] = num_transcripts - len(domains[0].unique())
    #transcript_domains.index = transcript_domains.index + 1  # shifting index
    transcript_domains.sort_index(inplace=True) 

    outfile.write(transcript_domains.to_string() + "\n")

    # domains per source
    domain_counts = domains.groupby([1])[1].count().reset_index(name='Domains per source')

    outfile.write(domain_counts.to_string() + "\n")
    
    
