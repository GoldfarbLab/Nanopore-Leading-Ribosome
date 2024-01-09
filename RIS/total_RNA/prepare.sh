#!/bin/bash

# Read command line arguments
DATA_SET_NAME=$1
DATA_PATH=$2

# Create config file from template and command line arguments
sed "s+DATA_NAME=+DATA_NAME=$DATA_SET_NAME+g" < ../config_template.sh > config.sh
sed -i "s+DATA_PATH=+DATA_PATH=$DATA_PATH/+g" config.sh
sed -i "s+ANALYSIS_TYPE+total_RNA+g" config.sh

# Read config
source ./config.sh

# Create output folders
mkdir -p $OUT_PATH
mkdir -p $RESULTS_PATH
mkdir -p $LOG_PATH
mkdir -p $SCRIPT_PATH

# Move config to output scripts folder
mv ./config.sh $SCRIPT_PATH

# Update scripts with dataset specific parameters
declare -a scripts=("align.bsub" "split.bsub" "collapse.bsub" "index.bsub" "blast_index.bsub" "translate.bsub" "domains.bsub" "format_domains.bsub")

for val in ${scripts[@]}; do
    sed "s+LSF_g+$LSF_g+g" < $val > $SCRIPT_PATH/$val
    sed -i "s+LSF_G+$LSF_G+g" $SCRIPT_PATH/$val
    sed -i "s+LSF_LOG_PATH+$LOG_PATH/+g" $SCRIPT_PATH/$val
    sed -i "s+LSF_SCRIPT_PATH+$SCRIPT_PATH/+g" $SCRIPT_PATH/$val
done

# Copy python scripts
cp *.py $SCRIPT_PATH/

