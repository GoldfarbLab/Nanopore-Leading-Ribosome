#!/usr/bin/env python
import sys
import pandas as pd
import numpy as np
import csv
from functools import partial
from multiprocessing import Pool
np.set_printoptions(threshold=sys.maxsize)

def convert_to_long_format(bg_transcript_df, size):
    read_counts = np.zeros(size, dtype = int)
    for index in range(len(bg_transcript_df.index)):
        for pos in range(bg_transcript_df.iloc[index, 1], bg_transcript_df.iloc[index, 2]):
            read_counts[pos] = bg_transcript_df.iloc[index, 3]
    return read_counts

def moving_average(x, w):
    return np.convolve(x, np.ones(w), 'same') / w

def get_transcript_density(bg_transcript_df, size):
    return sum((bg_transcript_df[2] - bg_transcript_df[1]) * bg_transcript_df[3]) / size

def get_local_densities(read_counts, motif_length):    
    return moving_average(read_counts, motif_length)

def get_prefix_densities(read_counts):
    return np.divide((read_counts+1).cumsum(axis=0), np.arange(len(read_counts)) + 1)

def compute_leading_pause_scores(local_densities, transcript_density):
    return local_densities / transcript_density

def compute_toeprinting_pause_scores(local_densities, prefix_densities):
    scores = []
    for i in range(len(local_densities)):
        local = local_densities[i]
        prefix = prefix_densities[i]
        if prefix <= 0:
            scores.append(0)
        else:
            scores.append(local / prefix)
    return scores

def write_scores_bg(out_path, transcript2scores, result_index):
    with open(out_path, 'w') as csvfile: 
        csvwriter = csv.writer(csvfile, delimiter='\t')
        for entry in transcript2scores:
            transcript = entry[0]
            current_start = -1
            current_end = -1
            current_score = -1
            for i, score in enumerate(entry[result_index]):
                if score == current_score:
                    current_end = i+1
                else:
                    if current_start > -1 and current_score > 0:
                        csvwriter.writerow([transcript, str(current_start), str(current_end), str(current_score)]) 
                    current_start = i
                    current_end = i+1
                    current_score = score
                    
def write_scores_tsv(out_path, transcript2scores, result_index):
    with open(out_path, 'w') as csvfile: 
        csvwriter = csv.writer(csvfile, delimiter='\t')
        csvwriter.writerow(["Transcript", "index", "pause_score", "read_count", "local_density", "transcript_density"])
        for entry in transcript2scores:
            
            transcript = entry[0]
            for i, score in enumerate(entry[result_index]):
                csvwriter.writerow([transcript, str(i), str(score), str(entry[3][i]), str(entry[4][i]), str(entry[5])]) 
                
def process_transcripts(transcript):
    #if ("0021b0cb" not in transcript): return ['', '', '']
    #print(transcript)
    bg_transcript_df = bg_df[bg_df[0] == transcript]
    size = sizes_df[sizes_df[0] == transcript].iloc[0][1]
    read_counts = convert_to_long_format(bg_transcript_df, size)
    # Compute densities
    transcript_density = get_transcript_density(bg_transcript_df, size)
    local_densities = get_local_densities(read_counts, motif_length)
    prefix_densities = get_prefix_densities(read_counts)
    # Compute scores
    leading_pause_scores = compute_leading_pause_scores(local_densities, transcript_density)
    toeprinting_pause_scores = compute_toeprinting_pause_scores(local_densities, prefix_densities)
    # Filter for depth
    #filtered_leading_pause_scores = filter_for_depth(leading_pause_scores, read_counts, 10)
    
    return [transcript, leading_pause_scores, toeprinting_pause_scores, read_counts, local_densities, transcript_density]




bg_file = sys.argv[1]
transcriptome_length_file = sys.argv[2]
motif_length = int(sys.argv[3])
num_threads = int(sys.argv[4])
out_base = sys.argv[5]


# Read bedgraph file which has read counts at each position
bg_df = pd.read_csv(bg_file, sep="\t", comment="#", header=None)
# Read trancript length file
sizes_df = pd.read_csv(transcriptome_length_file, sep="\t", comment="#", header=None)

pool = Pool(num_threads)
partial_process=partial(process_transcripts)
result_list = pool.map(partial_process, bg_df[0].unique())

print("Writing leading pause scores")
write_scores_bg(out_base + "_leading_pause.bg", result_list, 1)
write_scores_tsv(out_base + "_leading_pause.tsv", result_list, 1)
print("Writing toeprinting pause scores")
write_scores_bg(out_base + "_toe_pause.bg", result_list, 2)
write_scores_tsv(out_base + "_toe_pause.tsv", result_list, 2)