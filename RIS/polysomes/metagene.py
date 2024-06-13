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
data_base_name = sys.argv[5]

cds_df = pd.read_csv(cds_infile, sep="\t", comment="#", header=None)
pause_df = pd.read_csv(pause_infile, sep="\t", comment="#")
domains_df = pd.read_csv(domain_infile, sep="\t", comment="#", header=None)

domains_df = domains_df[domains_df[1] == "Pfam"]
pause_df.set_index(pause_df.columns[0])
cds_df.set_index(cds_df.columns[0])
domains_df.set_index(domains_df.columns[0])

domainEnd2CDS_distanceEnd2stats = dict() # pause_score, read_count, frequency
domainEnd2CDS_distanceEnd2stats[True] = defaultdict(list)
domainEnd2CDS_distanceEnd2stats[False] = defaultdict(list)

domainEnd2transcript_distanceEnd2stats = dict() # pause_score, read_count, frequency
domainEnd2transcript_distanceEnd2stats[True] = defaultdict(list)
domainEnd2transcript_distanceEnd2stats[False] = defaultdict(list)

domainEnd2region2CDS_percent2stats = dict() # pause_score, read_count, frequency
domainEnd2region2CDS_percent2stats[True] = dict()
domainEnd2region2CDS_percent2stats[True]['fiveUTR'] = defaultdict(list)
domainEnd2region2CDS_percent2stats[True]['CDS'] = defaultdict(list)
domainEnd2region2CDS_percent2stats[True]['threeUTR'] = defaultdict(list)
domainEnd2region2CDS_percent2stats[False] = defaultdict(list)
domainEnd2region2CDS_percent2stats[False]['fiveUTR'] = defaultdict(list)
domainEnd2region2CDS_percent2stats[False]['CDS'] = defaultdict(list)
domainEnd2region2CDS_percent2stats[False]['threeUTR'] = defaultdict(list)

domain2CDS_percent2stats = dict() # pause_score, read_count, frequency
domain2CDS_percent2stats[True] = defaultdict(list)
domain2CDS_percent2stats[False] = defaultdict(list)

for transcript in cds_df[0].unique():
    print(transcript)
    transcript_pause_df = pause_df[pause_df['Transcript'] == transcript]
    if (len(transcript_pause_df.index) == 0): continue
    #if (len(transcript_pause_df.index) == 0) or (transcript_pause_df['read_count'].sum() < 3000): continue
    
    transcript_cds_df = cds_df[cds_df[0] == transcript]
    transcript_domains_df = domains_df[(domains_df[0] == transcript)]
    
    cds_start = transcript_cds_df.iloc[0,3]
    cds_end = transcript_cds_df.iloc[0,4]
    cds_length = cds_end - cds_start
    transcript_length = max(transcript_pause_df['index'])
    strand = transcript_cds_df.iloc[0,6]
    
    if strand == "+":
        utr5_length = cds_start
        utr3_length = transcript_length - cds_end
    else:
        utr3_length = cds_start
        utr5_length = transcript_length - cds_end
    
    # check if domain within 300 nt of CDS end (stand award)
    if strand == "+":
        domainEnd = any(transcript_domains_df[4] >= cds_end - 300)
    else:
        domainEnd = any(transcript_domains_df[3] <= cds_start + 300)
    
    total_domain_length = (transcript_domains_df[4]-transcript_domains_df[3]).sum()
    total_non_domain_length = cds_length - total_domain_length
    is_last_domain = False
    
    for index, row in transcript_pause_df.iterrows():
        transcript_index = int(row[1])
        
        if strand == "+":
            CDS_distance_end = transcript_index - cds_end
            transcript_distance_end = transcript_index - transcript_length
            if cds_start <= transcript_index <= cds_end: 
                region = "CDS"
                CDS_percent = (transcript_index - cds_start) / cds_length
            elif transcript_index < cds_start:
                region = "fiveUTR"
                CDS_percent = (transcript_index) / cds_start
            elif transcript_index > cds_end:
                region = "threeUTR"
                CDS_percent = (transcript_index-cds_end) / (transcript_length - cds_end)
        else:
            continue
            CDS_distance_end = cds_start - transcript_index
            transcript_distance_end = -transcript_index
            if cds_start <= transcript_index <= cds_end: 
                region = "CDS"
                CDS_percent = (cds_end - transcript_index) / cds_length
            elif transcript_index < cds_start:
                region = "threeUTR"
                CDS_percent = (cds_start - transcript_index) / (cds_start)
            elif transcript_index > cds_end:
                region = "fiveUTR"
                CDS_percent = (transcript_length - transcript_index) / (transcript_length - cds_end)
                
        if region == "CDS":
            CDS_percent = int(CDS_percent * 100)
            # check if in domain or not
            in_domain = any((transcript_domains_df[3] <= transcript_index) & (transcript_index  <= transcript_domains_df[4]))
            
            if in_domain:
                # determine which domain
                in_domains_df = transcript_domains_df[(transcript_domains_df[3] <= transcript_index) & (transcript_index  <= transcript_domains_df[4])]
                domain_start_index = in_domains_df.iloc[0,3]
                domain_end_index = in_domains_df.iloc[0,4]
                domain_length = domain_end_index - domain_start_index
                # determine percent
                domain_percent = int(((transcript_index - domain_start_index) / domain_length) * 100)
                # determine if last domain
                is_last_domain = domain_end_index == transcript_domains_df[4].max()
            else:
                # find domain after
                domains_after = transcript_domains_df[transcript_domains_df[3] > transcript_index]
                if len(domains_after.index) > 0:
                    nondomain_end_index = domains_after.iloc[0,3]-1
                else:
                    nondomain_end_index = cds_end
                # find domain before
                domains_before = transcript_domains_df[transcript_domains_df[4] < transcript_index]
                if len(domains_before.index) > 0:
                    nondomain_start_index = domains_before.iloc[len(domains_before.index)-1, 3]+1
                else:
                    nondomain_start_index = cds_start
                # determine percent
                nondomain_length = nondomain_end_index - nondomain_start_index
                # determine if last domain
                domain_percent = int(((transcript_index - nondomain_start_index) / nondomain_length) * 100)
        else:
            CDS_percent = int(CDS_percent * 10)*10
            
       
                
        pause = row['pause_score']
        read_count = row['read_count']
        
        if CDS_distance_end not in domainEnd2CDS_distanceEnd2stats[domainEnd]:
            domainEnd2CDS_distanceEnd2stats[domainEnd][CDS_distance_end] = [0, 0, 0]
            
        domainEnd2CDS_distanceEnd2stats[domainEnd][CDS_distance_end][0] += pause
        domainEnd2CDS_distanceEnd2stats[domainEnd][CDS_distance_end][1] += read_count
        domainEnd2CDS_distanceEnd2stats[domainEnd][CDS_distance_end][2] += 1
        
        if transcript_distance_end not in domainEnd2transcript_distanceEnd2stats[domainEnd]:
            domainEnd2transcript_distanceEnd2stats[domainEnd][transcript_distance_end] = [0, 0, 0]
            
        domainEnd2transcript_distanceEnd2stats[domainEnd][transcript_distance_end][0] += pause
        domainEnd2transcript_distanceEnd2stats[domainEnd][transcript_distance_end][1] += read_count
        domainEnd2transcript_distanceEnd2stats[domainEnd][transcript_distance_end][2] += 1
        
        if (region == "fiveUTR" and utr5_length >= 10) or (region == "threeUTR" and utr3_length >= 10) or (region == "CDS"):
            if CDS_percent not in domainEnd2region2CDS_percent2stats[domainEnd][region]:
                domainEnd2region2CDS_percent2stats[domainEnd][region][CDS_percent] = [0, 0, 0]
                
            domainEnd2region2CDS_percent2stats[domainEnd][region][CDS_percent][0] += pause
            domainEnd2region2CDS_percent2stats[domainEnd][region][CDS_percent][1] += read_count
            domainEnd2region2CDS_percent2stats[domainEnd][region][CDS_percent][2] += 1
        
        if region == "CDS": 
            if in_domain or nondomain_length > 100:
                if domain_percent not in domain2CDS_percent2stats[in_domain]:
                    domain2CDS_percent2stats[in_domain][domain_percent] = [0, 0, 0]
                    
                domain2CDS_percent2stats[in_domain][domain_percent][0] += pause
                domain2CDS_percent2stats[in_domain][domain_percent][1] += read_count
                domain2CDS_percent2stats[in_domain][domain_percent][2] += 1
   











with open(out_path+"_CDS_dist_end.tsv", "w") as output_handle:
    csvwriter = csv.writer(output_handle, delimiter='\t')
    csvwriter.writerow(["exp", "source", "domain_at_end", "region", "distance", "total_pause_score", "total_reads", "frequency", "avg_pause_score", "avg_reads"])
    
    for domainEnd in domainEnd2CDS_distanceEnd2stats:
        for distance in sorted(domainEnd2CDS_distanceEnd2stats[domainEnd].keys()):
            stats = domainEnd2CDS_distanceEnd2stats[domainEnd][distance]
            csvwriter.writerow([data_base_name, "Pfam", domainEnd, "transcript", distance, stats[0], stats[1], stats[2], stats[0]/stats[2], stats[1]/stats[2]])


with open(out_path+"_transcript_dist_end.tsv", "w") as output_handle:
    csvwriter = csv.writer(output_handle, delimiter='\t')
    csvwriter.writerow(["exp", "source", "domain_at_end", "region", "distance", "total_pause_score", "total_reads", "frequency", "avg_pause_score", "avg_reads"])
    
    for domainEnd in domainEnd2transcript_distanceEnd2stats:
        for distance in sorted(domainEnd2transcript_distanceEnd2stats[domainEnd].keys()):
            stats = domainEnd2transcript_distanceEnd2stats[domainEnd][distance]
            csvwriter.writerow([data_base_name, "Pfam", domainEnd, "transcript", distance, stats[0], stats[1], stats[2], stats[0]/stats[2], stats[1]/stats[2]])

with open(out_path+"_CDS_percent.tsv", "w") as output_handle:
    csvwriter = csv.writer(output_handle, delimiter='\t')
    csvwriter.writerow(["exp", "source", "domain_at_end", "region", "distance", "total_pause_score", "total_reads", "frequency", "avg_pause_score", "avg_reads"])
    
    for domainEnd in domainEnd2region2CDS_percent2stats:
        for region in domainEnd2region2CDS_percent2stats[domainEnd]:
            for distance in sorted(domainEnd2region2CDS_percent2stats[domainEnd][region].keys()):
                stats = domainEnd2region2CDS_percent2stats[domainEnd][region][distance]
                csvwriter.writerow([data_base_name, "Pfam", domainEnd, region, distance, stats[0], stats[1], stats[2], stats[0]/stats[2], stats[1]/stats[2]])

with open(out_path+"_domain_percent.tsv", "w") as output_handle:
    csvwriter = csv.writer(output_handle, delimiter='\t')
    csvwriter.writerow(["exp", "source", "region", "distance", "total_pause_score", "total_reads", "frequency", "avg_pause_score", "avg_reads"])
    
    for domain in domain2CDS_percent2stats:
        for distance in sorted(domain2CDS_percent2stats[domain].keys()):
            stats = domain2CDS_percent2stats[domain][distance]
            csvwriter.writerow([data_base_name, "Pfam", domain, distance, stats[0], stats[1], stats[2], stats[0]/stats[2], stats[1]/stats[2]])


