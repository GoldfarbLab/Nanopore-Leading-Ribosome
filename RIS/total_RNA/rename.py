#!/usr/bin/env python
import sys
import csv
from collections import defaultdict
from Bio import SeqIO

isoforms_DNA_infile = sys.argv[1]
isoforms_protein_infile = sys.argv[2]
isoforms_gtf = sys.argv[3]
isoforms_genePred = sys.argv[4]
out_dir = sys.argv[5]

out_DNA_fasta = out_dir + "/isoforms.fa"
out_protein_fasta = out_dir + "/isoforms.faa"
out_cds_gff = out_dir + "/isoforms.cds.gff"

# Read gtf to map transcript_id to accession
transcript2accession = dict()
with open(isoforms_gtf) as in_handle:
    gtf_reader = csv.reader(in_handle, delimiter='\t')
    for row in gtf_reader:
        attributes = row[8].split(";")
        transcript_id = attributes[0].split("transcript_id ")[-1].strip('"').strip()
        accession = attributes[1].split("gene_id ")[-1].strip('"').strip()
        transcript2accession[transcript_id] = accession

# Read genePred to map accession to gene name
accession2gene = dict()
with open(isoforms_genePred) as in_handle:
    gtf_reader = csv.reader(in_handle, delimiter='\t')
    for row in gtf_reader:
        accession = row[0].split("_")[0].strip()
        gene = row[11].strip()
        if gene != "":
            accession2gene[accession] = gene
        
# read DNA fasta, update id and description, and write
accession2count = defaultdict(int)
transcripts_DNA = SeqIO.parse(isoforms_DNA_infile, 'fasta')
with open(out_DNA_fasta, "w") as output_handle:
    for transcript in transcripts_DNA:
        accession = transcript2accession[transcript.id]
        gene = ""
        if accession in accession2gene:
            gene = accession2gene[accession]
        
        accession2count[accession] += 1
        
        if accession2count[accession] > 1: 
                accessionIso = accession + "_" + str(accession2count[accession])
        else: 
            accessionIso = accession
        
        transcript.id = accessionIso
        
        if gene != "":
            transcript.description = "Gene=" + gene
        else:
            transcript.description = ""
        
        SeqIO.write(transcript, output_handle, "fasta")

# read protein fasta, update id and description, and write
accession2count = defaultdict(int)
transcripts_prot = SeqIO.parse(isoforms_protein_infile, 'fasta')
with open(out_cds_gff, "w") as output_gff_handle:
    csvwriter = csv.writer(output_gff_handle, delimiter='\t')
    with open(out_protein_fasta, "w") as output_handle:
        for transcript in transcripts_prot:
            accession = transcript2accession[transcript.id]
            gene = ""
            if accession in accession2gene:
                gene = accession2gene[accession]
            
            accession2count[accession] += 1
            
            if accession2count[accession] > 1: 
                    accessionIso = accession + "_" + str(accession2count[accession])
            else: 
                accessionIso = accession
            
            transcript.id = accessionIso
            name = accessionIso
            
            transcript.description = transcript.description.split()[-1]
            
            [_, _, _, strand, start, end] = transcript.description.split("|")
            
            if gene != "":
                transcript.description += " Gene=" + gene
            
            SeqIO.write(transcript, output_handle, "fasta")

            if gene != "":
                name = gene+"-"+accessionIso
                csvwriter.writerow([transcript.id, ".", "CDS", start, end, ".", strand, ".", "ID="+gene+";Name="+name]) 
            csvwriter.writerow([transcript.id, ".", "CDS", start, end, ".", strand, ".", "ID="+accessionIso+";Name="+name])
