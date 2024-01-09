#!/usr/bin/env python
import sys
import pandas as pd
import numpy as np
import csv

gff_in_path = sys.argv[1]
tsv_in_path = sys.argv[2]
out_base = sys.argv[3]

domains_df = pd.read_csv(tsv_in_path, sep="\t", comment="#", header=None)

# convert to DNA index
domains_df[6] = (domains_df[6]-1)*3
domains_df[7] = (domains_df[7]-1)*3

# drop columns
domains_df = domains_df.iloc[:,[0, 3, 6, 7, 8, 5]]
domains_df.insert(2, "protein_match", ["protein_match"]*len(domains_df.index))
domains_df.insert(6, "+", ["+"]*len(domains_df.index))
domains_df.insert(7, ".", ["."]*len(domains_df.index))
domains_df[5] = ["Description " + x for x in domains_df[5]]

domains_df.to_csv(out_base + "/all_domains.gff", sep="\t", index=False, header=False, quoting=3, quotechar="",  escapechar="\\")

for source in domains_df[3].unique():
    source_domains_df = domains_df[domains_df[3] == source]
    source_domains_df.to_csv(out_base + "/" + source + ".gff", sep="\t", index=False, header=False, quoting=3, quotechar="",  escapechar="\\")
    
    