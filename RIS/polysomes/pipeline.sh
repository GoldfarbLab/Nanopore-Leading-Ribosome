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

DATA_BASE_NAME=$(basename -- "$DATA_PATH")

# Read final config
source ${SCRATCH_PATH}/${DATA_SET_NAME}/polysomes/${DATA_BASE_NAME}/scripts/config.sh

# Submit LSF jobs
#jid1=$(get_jobid bsub < $SCRIPT_PATH/align.bsub)
#echo Submitted align job for $DATA_BASE_NAME with ID: $jid1

#jid2=$(get_jobid bsub -w "ended($jid1)" < $SCRIPT_PATH/bam.bsub)
#echo Submitted bam job for $DATA_BASE_NAME with ID: $jid2

#jid3=$(get_jobid bsub -w "ended($jid2)" < $SCRIPT_PATH/bed.bsub)
#echo Submitted bed job for $DATA_BASE_NAME with ID: $jid3

#jid4=$(get_jobid bsub -w "ended($jid3)" < $SCRIPT_PATH/bigwig.bsub)
#echo Submitted bigwig job for $DATA_BASE_NAME with ID: $jid4

#jid5=$(get_jobid bsub -w "ended($jid4)" < $SCRIPT_PATH/pause.bsub)
#echo Submitted pause job for $DATA_BASE_NAME with ID: $jid5

#jid6=$(get_jobid bsub -w "ended($jid5)" < $SCRIPT_PATH/translate.bsub)
#echo Submitted translate job for $DATA_BASE_NAME with ID: $jid6

#jid7=$(get_jobid bsub -w "ended($jid6)" < $SCRIPT_PATH/domains.bsub)
#echo Submitted domain job for $DATA_BASE_NAME with ID: $jid7

#jid8=$(get_jobid bsub -w "ended($jid7)" < $SCRIPT_PATH/format_domains.bsub)
#echo Submitted format_domain job for $DATA_BASE_NAME with ID: $jid8


#jid1=$(get_jobid bsub < $SCRIPT_PATH/bed.bsub)
#jid1=$(get_jobid bsub < $SCRIPT_PATH/translate.bsub)
#jid1=$(get_jobid bsub < $SCRIPT_PATH/bigwig.bsub)


