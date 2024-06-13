#!/usr/bin/env python
import sys
import pandas as pd
import numpy as np
import csv

tsv_in_path = sys.argv[1]
gff_in_path = sys.argv[2]
fasta_in_path = sys.argv[3]
out_base = sys.argv[4]

cds_df = pd.read_csv(gff_in_path, sep="\t", comment="#", header=None)
id2start = dict(zip(cds_df.iloc[:,0], cds_df.iloc[:,3]))
id2end = dict(zip(cds_df.iloc[:,0], cds_df.iloc[:,4]))
domains_df = pd.read_csv(tsv_in_path, sep="\t", comment="#", header=None)
id2strand = dict()
for line in open(fasta_in_path):
    if line[0] == ">":
        id = line.split(" ")[0][1:]
        strand = line.split(" ")[1].split("|")[3]
        id2strand[id] = strand

# convert to DNA index
for ind in domains_df.index:
    strand = id2strand[domains_df[0][ind]]
    if strand == "+":
        domains_df[6][ind] = (domains_df[6][ind]-1)*3 + id2start[domains_df[0][ind]]
        domains_df[7][ind] = (domains_df[7][ind]-1)*3 + id2start[domains_df[0][ind]] - 1
    else:
        domain_start = (domains_df[6][ind]-1)*3 + id2start[domains_df[0][ind]]
        domain_end = ((domains_df[7][ind]-1)*3) + id2start[domains_df[0][ind]]
        domains_df[6][ind] = (id2end[domains_df[0][ind]] - domain_end) + id2start[domains_df[0][ind]]-2
        domains_df[7][ind] = 2 + domains_df[6][ind] + domain_end - domain_start
        
        
        

# drop columns
domains_df = domains_df.iloc[:,[0, 3, 6, 7, 8, 5]]

#print(domains_df.iloc[0].to_string())
# add new columns
domains_df.insert(2, "protein_match", ["protein_match"]*len(domains_df.index))
domains_df.insert(6, "strand", ["+"]*len(domains_df.index))
#print(domains_df.iloc[0].to_string())
domains_df["strand"] = [id2strand[id] for id in domains_df[0]]
#print(domains_df.iloc[0].to_string())
domains_df.insert(7, ".", ["."]*len(domains_df.index))
domains_df[5] = ["Description " + x for x in domains_df[5]]

domains_df.to_csv(out_base + "/all_domains.gff", sep="\t", index=False, header=False, quoting=3, quotechar="",  escapechar="\\")

for source in domains_df[3].unique():
    source_domains_df = domains_df[domains_df[3] == source]
    source_domains_df.to_csv(out_base + "/" + source + ".gff", sep="\t", index=False, header=False, quoting=3, quotechar="",  escapechar="\\")
    
    