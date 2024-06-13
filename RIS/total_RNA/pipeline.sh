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
source ${SCRATCH_PATH}/${DATA_SET_NAME}/total_RNA/scripts/config.sh

# Submit LSF jobs
jid1=$(get_jobid bsub < $SCRIPT_PATH/align.bsub)
echo Submitted align job for $DATA_SET_NAME with ID: $jid1

jid2=$(get_jobid bsub -w "ended($jid1)" < $SCRIPT_PATH/align_concat.bsub)
echo Submitted align_concat job for $DATA_SET_NAME with ID: $jid2

jid3=$(get_jobid bsub -w "ended($jid2)" < $SCRIPT_PATH/align_qc.bsub)
echo Submitted align_qc job for $DATA_SET_NAME with ID: $jid3

jid4=$(get_jobid bsub -w "ended($jid3)" < $SCRIPT_PATH/reads.bsub)
echo Submitted reads job for $DATA_SET_NAME with ID: $jid4

jid5=$(get_jobid bsub -w "ended($jid4)" < $SCRIPT_PATH/split.bsub)
echo Submitted split job for $DATA_SET_NAME with ID: $jid5

jid6=$(get_jobid bsub -w "ended($jid5)" < $SCRIPT_PATH/collapse.bsub)
echo Submitted collapse job for $DATA_SET_NAME with ID: $jid6

jid7=$(get_jobid bsub -w "ended($jid6)" < $SCRIPT_PATH/collapse_concat.bsub)
echo Submitted collapse_concat job for $DATA_SET_NAME with ID: $jid7

jid8=$(get_jobid bsub -w "ended($jid7)" < $SCRIPT_PATH/collapse_qc.bsub)
echo Submitted collapse_qc job for $DATA_SET_NAME with ID: $jid8

jid9=$(get_jobid bsub -w "ended($jid8)" < $SCRIPT_PATH/sqanti.bsub)
echo Submitted sqanti job for $DATA_SET_NAME with ID: $jid9

jid10=$(get_jobid bsub -w "ended($jid9)" < $SCRIPT_PATH/blast_index.bsub)
echo Submitted blast_index job for $DATA_SET_NAME with ID: $jid10

jid11=$(get_jobid bsub -w "ended($jid10)" < $SCRIPT_PATH/translate.bsub)
echo Submitted translate job for $DATA_SET_NAME with ID: $jid11

jid12=$(get_jobid bsub -w "ended($jid11)" < $SCRIPT_PATH/rename.bsub)
echo Submitted rename job for $DATA_SET_NAME with ID: $jid12

jid13=$(get_jobid bsub -w "ended($jid12)" < $SCRIPT_PATH/rename_qc.bsub)
echo Submitted rename job for $DATA_SET_NAME with ID: $jid13

jid14=$(get_jobid bsub -w "ended($jid12)" < $SCRIPT_PATH/domains.bsub)
echo Submitted domains job for $DATA_SET_NAME with ID: $jid14

jid15=$(get_jobid bsub -w "ended($jid14)" < $SCRIPT_PATH/format_domains.bsub)
echo Submitted format_domains job for $DATA_SET_NAME with ID: $jid15

jid16=$(get_jobid bsub -w "ended($jid15)" < $SCRIPT_PATH/domains_qc.bsub)
echo Submitted domains_qc job for $DATA_SET_NAME with ID: $jid16

# jid17=$(get_jobid bsub -w "ended($jid15)" < $SCRIPT_PATH/index.bsub)
# echo Submitted index job for $DATA_SET_NAME with ID: $jid17











# jid11=$(get_jobid bsub -w "ended($jid10)" < $SCRIPT_PATH/isoform_collapse.bsub)
# echo Submitted isoform_collapse job for $DATA_SET_NAME with ID: $jid11