#!/bin/bash

# parameters
DATA_NAME=hel2ski2_polysomes
DATA_PATH=/storage1/fs1/d.goldfarb/Active/Projects/Nanopore//data/batch1/fastq_pass_hel2ski2_polysomes/*.gz

# setup paths
PROJECT_PATH=/storage1/fs1/d.goldfarb/Active/Projects/Nanopore/
REF_PATH=${PROJECT_PATH}/reference
SRC_PATH=${PROJECT_PATH}/source
SCRATCH_PATH=/scratch1/fs1/d.goldfarb/Nanopore/

OUT_PATH=${SCRATCH_PATH}/${DATA_NAME}
RESULTS_PATH=${OUT_PATH}/results
LOG_PATH=${OUT_PATH}/logs
SCRIPT_PATH=${OUT_PATH}/scripts

# reference files
GENOME=${REF_PATH}/sacCer3.fa
INTRONS=${REF_PATH}/introns.bed
CHROMSIZE=${REF_PATH}/chrom.sizes

