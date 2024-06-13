#!/usr/bin/env python
import csv
import sys
from collections import defaultdict

infile = sys.argv[1]
outfile = open(sys.argv[2], 'w')

numExons2count = defaultdict(int)
nrow = 0
with open(infile) as in_handle:
    csvreader = csv.reader(in_handle, delimiter='\t')
    for row in csvreader:
        nrow+=1
        exons = int(row[9])
        numExons2count[exons]+=1
        
outfile.write("Number transcripts: " + f"{nrow:,}" + "\n")
for exons in sorted(numExons2count.keys()):
    outfile.write(str(exons) + " Exons: " + f"{numExons2count[exons]:,}" + "\n")