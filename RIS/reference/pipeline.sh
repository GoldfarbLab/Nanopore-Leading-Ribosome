#!/bin/bash

# Function to extract job ID from console output
function get_jobid {
    output=$($*)
    echo $output | tail -n 1 | cut -d'<' -f2 | cut -d'>' -f1
}

# Read config template to get initial paths
source ../config_template.sh

# Read command line arguments
DATA_SET_NAME=$1
DATA_PATH=$2

# Execute scripts with command line arguments
./prepare.sh $DATA_SET_NAME $DATA_PATH

# Read final config
source ${SCRATCH_PATH}/${DATA_SET_NAME}/reference/scripts/config.sh

# Submit LSF jobs
jid1=$(get_jobid bsub < $SCRIPT_PATH/utr.bsub)
echo Submitted utr job for $DATA_SET_NAME with ID: $jid1

jid2=$(get_jobid bsub -w "ended($jid1)" < $SCRIPT_PATH/bed.bsub)
echo Submitted bed job for $DATA_SET_NAME with ID: $jid2