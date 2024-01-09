#!/usr/bin/python3
import pandas as pd
import sys

gtf_path = sys.argv[1]
bed_path = sys.argv[2]
out_path = sys.argv[3]

# Read annotations gtf file
gtf_df = pd.read_csv(gtf_path, sep="\t", comment="#", header=None)

# Get the unique values of chromosome column
for chromosome in gtf_df[0].unique():
    # Filter for chromosome
    gtf_chromo_df = gtf_df[gtf_df[0] == chromosome]
    # Write chromosome specific file
    gtf_chromo_df.to_csv(out_path + "/" + chromosome + ".gtf", sep="\t", index=False, header=False, quoting=3, quotechar="",  escapechar="\\")

# Read reads bed file
bed_df = pd.read_csv(bed_path, sep="\t", comment="#", header=None)

# Get the unique values of chromosome column
for chromosome in bed_df[0].unique():
    # Filter for chromosome
    bed_chromo_df = bed_df[bed_df[0] == chromosome]
    # Write chromosome specific file
    bed_chromo_df.to_csv(out_path + "/" + chromosome + ".bed", sep="\t", index=False, header=False, quoting=3, quotechar="",  escapechar="\\")

