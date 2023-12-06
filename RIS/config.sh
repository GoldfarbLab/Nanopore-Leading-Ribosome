#!/bin/bash

# setup paths
BASE_PATH="/storage1/fs1/d.goldfarb/Active/Projects/Nanopore/"
REF_PATH=${BASE_PATH}/reference
SRC_PATH=${BASE_PATH}/source
SCRATCH_PATH="/scratch1/fs1/d.goldfarb/Nanopore/"

# reference files
GENOME=${REF_PATH}/sacCer3.fa
INTRONS=${REF_PATH}/introns.bed

# parameters
DATA_NAME="hel2ski2_polysomes"
DATA_PATH=${BASE_PATH}/data/batch1/fastq_pass_hel2ski2_polysomes/*.gz