#!/usr/bin/env python
import sys
import csv
from collections import defaultdict
from Bio import SeqIO

def writeEntries(gff_csvwriter, output_handleDNA, output_handlePROT, transcript_DNA, transcript_Prot):
    # Write dna
    SeqIO.write(transcript_DNA, output_handleDNA, "fasta")
    # Write protein
    SeqIO.write(transcript_Prot, output_handlePROT, "fasta")
    # Write cds
    accession = transcript_Prot.id
    [_, _, _, strand, start, end] = transcript_Prot.description.split()[1].split("|")
    name = accession
    if accession != gene:
        name = gene+"-"+accession
        gff_csvwriter.writerow([accession, ".", "CDS", start, end, ".", strand, ".", "ID="+gene+";Name="+name]) 
    gff_csvwriter.writerow([accession, ".", "CDS", start, end, ".", strand, ".", "ID="+accession+";Name="+name])

isoforms_DNA_infile = sys.argv[1]
isoforms_protein_infile = sys.argv[2]
out_dir = sys.argv[3]

out_DNA_fasta = out_dir + "/isoforms.fa"
out_protein_fasta = out_dir + "/isoforms.faa"
out_cds_gff = out_dir + "/isoforms.cds.gff"

toTranslate = []

gene2DNAentry = defaultdict(list)
transcripts_DNA = SeqIO.parse(isoforms_DNA_infile, 'fasta')
for transcript in transcripts_DNA:
    if "Gene=" not in transcript.description:
        gene2DNAentry[transcript.id].append(transcript)
    else:
        gene = transcript.description.split("=")[-1]
        gene2DNAentry[gene].append(transcript)
 
gene2PROTentry = defaultdict(list)
transcripts_prot = SeqIO.parse(isoforms_protein_infile, 'fasta')
for transcript in transcripts_prot:
    if "Gene=" not in transcript.description:
        gene2PROTentry[transcript.id].append(transcript)
    else:
        gene = transcript.description.split("=")[-1]
        gene2PROTentry[gene].append(transcript)    

    

with open(out_cds_gff, "w") as output_gff_handle:
    csvwriter = csv.writer(output_gff_handle, delimiter='\t')
    with open(out_DNA_fasta, "w") as output_handleDNA:
        with open(out_protein_fasta, "w") as output_handlePROT:
            for gene in gene2DNAentry:
                # single transcript
                if len(gene2DNAentry[gene]) == 1:
                    # Write dna
                    if gene in gene2PROTentry:
                        writeEntries(csvwriter, output_handleDNA, output_handlePROT, gene2DNAentry[gene][0], gene2PROTentry[gene][0])
                    else:
                        toTranslate.append(gene2DNAentry[gene][0])
                
                # look for multiple transcripts
                elif len(gene2DNAentry[gene]) > 1:
                    if gene in gene2PROTentry:
                        # find unique
                        redundant = []
                        for i, t1 in enumerate(gene2PROTentry[gene]):
                            isUnique = True
                            for j, t2 in enumerate(gene2PROTentry[gene]):
                                if i != j:
                                    if t1.seq == t2.seq:
                                        isUnique = False
                            if isUnique:
                                writeEntries(csvwriter, output_handleDNA, output_handlePROT, gene2DNAentry[gene][0], gene2PROTentry[gene][0])
                            else:
                                redundant.append([i,j])
                        if len(redundant) > 0:
                            print(len(redundant))
                    else:
                        # take longest TODO
                        toTranslate.append(gene2DNAentry[gene][0])

        
