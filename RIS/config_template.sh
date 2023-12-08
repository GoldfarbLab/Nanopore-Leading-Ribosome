#!/bin/bash

# parameters
DATA_NAME=
DATA_PATH=

# LSF parameters
LSF_g=/d.goldfarb/compute
LSF_G=compute-d.goldfarb

# setup paths
PROJECT_PATH=/storage1/fs1/d.goldfarb/Active/Projects/Nanopore/
REF_PATH=${PROJECT_PATH}/reference
SRC_PATH=${PROJECT_PATH}/source
SCRATCH_PATH=/scratch1/fs1/d.goldfarb/Nanopore/

# output paths
OUT_PATH=${SCRATCH_PATH}/${DATA_NAME}
RESULTS_PATH=${OUT_PATH}/results
LOG_PATH=${OUT_PATH}/logs
SCRIPT_PATH=${OUT_PATH}/scripts

# reference files
GENOME=${REF_PATH}/sacCer3.fa
INTRONS=${REF_PATH}/introns.bed
CHROMSIZE=${REF_PATH}/chrom.sizes

