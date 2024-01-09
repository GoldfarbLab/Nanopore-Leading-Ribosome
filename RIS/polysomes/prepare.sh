#!/bin/bash

# Read command line arguments
DATA_SET_NAME=$1
DATA_PATH=$2
DATA_BASE_NAME=$(basename -- "$DATA_PATH")

# Create config file from template and command line arguments
sed "s+DATA_NAME=+DATA_NAME=$DATA_SET_NAME+g" < ../config_template.sh > config.sh
sed -i "s+DATA_PATH=+DATA_PATH=$DATA_PATH/*.gz+g" config.sh
sed -i "s+ANALYSIS_TYPE+polysomes+g" config.sh
sed -i "s+DATA_BASE_NAME=+DATA_BASE_NAME=$DATA_BASE_NAME+g" config.sh

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
declare -a scripts=("align.bsub" "bam.bsub" "bed.bsub" "translate.bsub" "bigwig.bsub" "pause.bsub")

for val in ${scripts[@]}; do
    sed "s+LSF_g+$LSF_g+g" < $val > $SCRIPT_PATH/$val
    sed -i "s+LSF_G+$LSF_G+g" $SCRIPT_PATH/$val
    sed -i "s+LSF_LOG_PATH+$LOG_PATH/+g" $SCRIPT_PATH/$val
    sed -i "s+LSF_SCRIPT_PATH+$SCRIPT_PATH/+g" $SCRIPT_PATH/$val
done

# Copy python scripts
cp *.py $SCRIPT_PATH/


