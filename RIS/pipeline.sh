#!/bin/bash

# Function to extract job ID from console output
function get_jobid {
    output=$($*)
    echo $output | tail -n 1 | cut -d'<' -f2 | cut -d'>' -f1
}

# Read command line arguments
DATA_NAME=$1
DATA_PATH=$2

# Execute scripts with command line arguments
./prepare.sh $DATA_NAME $DATA_PATH

# Read config 
source ./config.sh

# Move config to output scripts folder
mv ./config.sh $SCRIPT_PATH

# Submit LSF jobs
jid1=$(get_jobid bsub < $SCRIPT_PATH/align.bsub)
echo Submitted align job for $DATA_NAME with ID: $jid1

jid2=$(get_jobid bsub -w "ended($jid1)" < $SCRIPT_PATH/bam.bsub)
echo Submitted bam job for $DATA_NAME with ID: $jid2

jid3=$(get_jobid bsub -w "ended($jid2)" < $SCRIPT_PATH/bedgraph.bsub)
echo Submitted bedgraph job for $DATA_NAME with ID: $jid3

jid4=$(get_jobid bsub -w "ended($jid3)" < $SCRIPT_PATH/bigwig.bsub)
echo Submitted bigwig job for $DATA_NAME with ID: $jid4

jid5=$(get_jobid bsub -w "ended($jid2)" < $SCRIPT_PATH/bamtobed.bsub)
echo Submitted bamtobed job for $DATA_NAME with ID: $jid5

jid6=$(get_jobid bsub -w "ended($jid5)" < $SCRIPT_PATH/ribosome_bam.bsub)
echo Submitted ribosome_bam job for $DATA_NAME with ID: $jid6
