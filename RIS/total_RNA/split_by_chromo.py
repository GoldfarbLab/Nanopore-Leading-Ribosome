#!/usr/bin/python3
import csv
import sys
import os

def decomment(csvfile):
    for row in csvfile:
        row = row.split('#')[0].strip()
        if row: yield row

gtf_path = sys.argv[1]
bed_path = sys.argv[2]
out_path = sys.argv[3]

chrom2gtf_csvwriter= dict()
chrom2bed_csvwriter = dict()

with open(gtf_path) as in_handle:
    gtf_reader = csv.reader(decomment(in_handle), delimiter='\t')
    for row in gtf_reader:
        chromosome = row[0]
        if chromosome not in chrom2gtf_csvwriter:
            outfile = open(os.path.join(out_path, chromosome)+".gtf", 'w')
            chrom2gtf_csvwriter[chromosome] = csv.writer(outfile, delimiter='\t', quoting=csv.QUOTE_NONE, quotechar="", escapechar="\\")
        chrom2gtf_csvwriter[chromosome].writerow(row)      

with open(bed_path) as in_handle:
    bed_reader = csv.reader(decomment(in_handle), delimiter='\t')
    for row in bed_reader:
        chromosome = row[0]
        if chromosome not in chrom2bed_csvwriter:
            outfile = open(os.path.join(out_path, chromosome)+".bed", 'w')
            chrom2bed_csvwriter[chromosome] = csv.writer(outfile, delimiter='\t', quoting=csv.QUOTE_NONE, quotechar="", escapechar="\\")
        chrom2bed_csvwriter[chromosome].writerow(row)   
