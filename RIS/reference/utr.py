#!/usr/bin/python3
import sys
import csv
from Bio import SeqIO

# input files
utr_path = sys.argv[1]
out_path = sys.argv[2]

# read sequences
utrs = SeqIO.parse(utr_path, 'fasta')

with open(out_path, "w") as out_handle:
    csvwriter = csv.writer(out_handle, delimiter='\t')
    for utr in utrs:
        [name, loc, _, _, strand, _] = utr.description.split(" ")
        chrom = loc.split("=")[-1].split(":")[0]
        [start, end] = loc.split("=")[-1].split(":")[-1].split("-")
        strand = strand[-1]
        csvwriter.writerow([chrom, start, end, name, "0", strand]) 
