#!/bin/bash

# Read command line arguments
DATA_NAME=$1
DATA_PATH=$2

# Create config file from template and command line arguments
sed "s+DATA_NAME=+DATA_NAME=$DATA_NAME+g" < config_template.sh > config.sh
sed -i "s+DATA_PATH=+DATA_PATH=$DATA_PATH/*.gz+g" config.sh

# Read config
source ./config.sh

# Create output folders
mkdir -p $OUT_PATH
mkdir $RESULTS_PATH
mkdir $LOG_PATH
mkdir $SCRIPT_PATH

# Update scripts with dataset specific parameters
declare -a scripts=("align.bsub" "bam.bsub" "bedgraph.bsub" "bigwig.bsub" "bamtobed.bsub" "ribosome_bam.bsub")

for val in ${scripts[@]}; do
    sed "s+LSF_g+$LSF_g+g" < $val > $SCRIPT_PATH/$val
    sed -i "s+LSF_G+$LSF_G+g" $SCRIPT_PATH/$val
    sed -i "s+LSF_LOG_PATH+$LOG_PATH/+g" $SCRIPT_PATH/$val
    sed -i "s+LSF_SCRIPT_PATH+$SCRIPT_PATH/+g" $SCRIPT_PATH/$val
done




