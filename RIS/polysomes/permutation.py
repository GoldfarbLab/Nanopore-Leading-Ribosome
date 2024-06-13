#!/usr/bin/env python
import sys
import pandas as pd
import numpy as np
import csv
from collections import defaultdict

cds_infile = sys.argv[1]
pause_infile = sys.argv[2]
domain_infile = sys.argv[3]
out_path = sys.argv[4]
job_index = int(sys.argv[5])
data_base_name = sys.argv[6]

cds_df = pd.read_csv(cds_infile, sep="\t", comment="#", header=None)
pause_df = pd.read_csv(pause_infile, sep="\t", comment="#", header=None)
domains_df = pd.read_csv(domain_infile, sep="\t", comment="#", header=None)

distanceStart2stats = defaultdict(list) # pause_score, read_count, frequency
distanceEnd2stats = defaultdict(list) # pause_score, read_count, frequency
CDS_distanceStart2stats = defaultdict(list)

if job_index >= len(domains_df[1].unique()):
    domain_source = "CDS"
    transcripts = cds_df[0].unique()
else:
    domain_source = domains_df[1].unique()[job_index-1]
    transcripts = domains_df[domains_df[1] == domain_source][0].unique()
domains_df = domains_df[domains_df[1] == domain_source]

print(domain_source)
for transcript in transcripts:
    print(transcript)
    transcript_domains_df = domains_df[domains_df[0] == transcript]
    transcript_cds_df = cds_df[cds_df[0] == transcript]
    cds_start = transcript_cds_df.iloc[0,3]
    cds_end = transcript_cds_df.iloc[0,4]
    strand = transcript_cds_df.iloc[0,6]
    
    transcript_pause_df = pause_df[pause_df[0] == transcript]
    if len(transcript_pause_df.index) == 0: continue
    transcript_length = max(pd.to_numeric(transcript_pause_df[1]))
    
    for index, row in transcript_domains_df.iterrows():
        max_score = 0
        max_dist = 0
        dist_from_CDS_end = 0
        for index2, row2 in transcript_pause_df.iterrows():
            transcript_index = int(row2[1])
            
            if strand == "+":
                domain_start_index = int(row[3])
                domain_end_index = int(row[4])
                distance_start = transcript_index - domain_start_index
                distance_end = transcript_index - domain_end_index
            else:
                domain_start_index = int(row[4])
                domain_end_index = int(row[3])
                distance_start = domain_start_index - transcript_index
                distance_end = domain_end_index - transcript_index
            
        
            pause = float(row2[2])
            read_count = int(row2[3])
            
            if pause > max_score:
                max_score = pause
                max_dist = distance_end
                dist_from_CDS_end = cds_end - transcript_index
            
            if distance_end not in distanceEnd2stats:
                distanceEnd2stats[distance_end] = [0, 0, 0]
            if distance_start not in distanceStart2stats:
                distanceStart2stats[distance_start] = [0, 0, 0]
                
            distanceEnd2stats[distance_end][0] += pause
            distanceEnd2stats[distance_end][1] += read_count
            distanceEnd2stats[distance_end][2] += 1
            
            distanceStart2stats[distance_start][0] += pause
            distanceStart2stats[distance_start][1] += read_count
            distanceStart2stats[distance_start][2] += 1
            
        if -200 > max_dist > -250 and dist_from_CDS_end > 500:
            print("EXAMPLE:", transcript, max_dist, max_score, dist_from_CDS_end)
            
    if domain_source == "CDS":  
        max_score = 0
        max_dist = 0
        for index2, row2 in transcript_pause_df.iterrows():
            transcript_index = int(row2[1])
            
            if strand == "+":
                distance_end = transcript_index - cds_end
            else:
                distance_end = cds_start - transcript_index
            
            pause = float(row2[2])
            read_count = int(row2[3])
            
            if pause > max_score:
                max_score = pause
                max_dist = distance_end
            
            if distance_end not in CDS_distanceStart2stats:
                CDS_distanceStart2stats[distance_end] = [0, 0, 0]
                
            CDS_distanceStart2stats[distance_end][0] += pause
            CDS_distanceStart2stats[distance_end][1] += read_count
            CDS_distanceStart2stats[distance_end][2] += 1
            
        
            
if domain_source != "CDS":
    with open(out_path+"_" + domain_source + "_dist_start.tsv", "w") as output_handle:
        csvwriter = csv.writer(output_handle, delimiter='\t')
        csvwriter.writerow(["exp", "source", "distance", "total_pause_score", "total_reads", "frequency", "avg_pause_score", "avg_reads"])
            
        for distance in sorted(distanceStart2stats.keys()):
            csvwriter.writerow([data_base_name, domain_source, distance, distanceStart2stats[distance][0], distanceStart2stats[distance][1], distanceStart2stats[distance][2], distanceStart2stats[distance][0]/distanceStart2stats[distance][2], distanceStart2stats[distance][1]/distanceStart2stats[distance][2]])


    with open(out_path+"_" + domain_source + "_dist_end.tsv", "w") as output_handle:
        csvwriter = csv.writer(output_handle, delimiter='\t')
        csvwriter.writerow(["exp", "source", "distance", "total_pause_score", "total_reads", "frequency", "avg_pause_score", "avg_reads"])
                        
        for distance in sorted(distanceEnd2stats.keys()):
            csvwriter.writerow([data_base_name, domain_source, distance, distanceEnd2stats[distance][0], distanceEnd2stats[distance][1], distanceEnd2stats[distance][2], distanceEnd2stats[distance][0]/distanceEnd2stats[distance][2], distanceEnd2stats[distance][1]/distanceEnd2stats[distance][2]])

else:
    with open(out_path+"_" + domain_source + "_dist_end.tsv", "w") as output_handle:
        csvwriter = csv.writer(output_handle, delimiter='\t')
        csvwriter.writerow(["exp", "source", "distance", "total_pause_score", "total_reads", "frequency", "avg_pause_score", "avg_reads"])
                        
        for distance in sorted(CDS_distanceStart2stats.keys()):
            csvwriter.writerow([data_base_name, domain_source, distance, CDS_distanceStart2stats[distance][0], CDS_distanceStart2stats[distance][1], CDS_distanceStart2stats[distance][2], CDS_distanceStart2stats[distance][0]/CDS_distanceStart2stats[distance][2], CDS_distanceStart2stats[distance][1]/CDS_distanceStart2stats[distance][2]])



