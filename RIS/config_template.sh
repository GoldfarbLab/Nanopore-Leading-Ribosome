#!/bin/bash

# parameters automatically filled in
DATA_NAME=
DATA_PATH=
DATA_BASE_NAME=

# user parameters
# note NT must be 1 greater than how many you want (e.g. 30 NT means you should put 31)
NUM_UPSTREAM_NT=34 
NUM_UPSTREAM_AA=5

# LSF parameters
LSF_g=/d.goldfarb/compute
LSF_G=compute-d.goldfarb

# setup paths
PROJECT_PATH=/storage1/fs1/d.goldfarb/Active/Projects/Nanopore/
REF_PATH=${PROJECT_PATH}/reference
SRC_PATH=${PROJECT_PATH}/source
SCRATCH_PATH=/scratch1/fs1/d.goldfarb/Nanopore/

# output paths
OUT_PATH=${SCRATCH_PATH}/${DATA_NAME}/ANALYSIS_TYPE/${DATA_BASE_NAME}
RESULTS_PATH=${OUT_PATH}/results
LOG_PATH=${OUT_PATH}/logs
SCRIPT_PATH=${OUT_PATH}/scripts

# reference files
GENOME=${REF_PATH}/sacCer3.fa
INTRONS=${REF_PATH}/introns.bed6
CHROMSIZE=${REF_PATH}/chrom.sizes
TRANSCRIPTS=${REF_PATH}/transcripts.gff
ANNOTATIONS=${REF_PATH}/Saccharomyces_cerevisiae.R64-1-1.110_v3.gtf
PROTEOME=${REF_PATH}/ref_proteome.fasta
# Transcriptome generation results
TRANSCRIPTOME=${REF_PATH}/isoforms.fa
TRANSCRIPTOME_SIZES=${REF_PATH}/isoforms.fa.sizes
TRANSCRIPTOME_AA=${REF_PATH}/isoforms_aa.fasta
