#!/usr/bin/env python
import sys
import re as re
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
from Bio.Seq import Seq
from Bio.Alphabet import generic_protein
from Bio.Blast.Applications import NcbiblastpCommandline
from collections import defaultdict
    
isoforms_DNA_infile = sys.argv[1]
isoforms_protein_infile = sys.argv[2]
proteome_path = sys.argv[3]
min_length = int(sys.argv[4])
num_threads = int(sys.argv[5])
tmp_path = sys.argv[6]
out_dir = sys.argv[7]

out_DNA_fasta = out_dir + "/isoforms.fa"
out_protein_fasta = out_dir + "/isoforms.faa"

output_handleDNA = open(out_DNA_fasta, "w")
output_handlePROT = open(out_protein_fasta, "w")

toTranslate = []

id2PROTentry = defaultdict(list)
transcripts_prot = SeqIO.parse(isoforms_protein_infile, 'fasta')
for transcript in transcripts_prot:
    id2PROTentry[transcript.id].append(transcript)
 
transcripts_DNA = SeqIO.parse(isoforms_DNA_infile, 'fasta')
for transcript in transcripts_DNA:
    if transcript.id not in id2PROTentry:
        toTranslate.append(transcript)
    else:
        SeqIO.write(transcript, output_handleDNA, "fasta")
        SeqIO.write(id2PROTentry[transcript.id], output_handlePROT, "fasta")


cline = NcbiblastpCommandline(query=tmp_path, db=proteome_path, evalue=0.001, remote=False, outfmt=6, max_target_seqs=1, max_hsps=1, num_threads=num_threads)

for transcript in toTranslate:
    bestFrame = -1
    bestFrameEVal = 1e9
    bestPercent = 0
    bestMatch = ""
    bestLength = 0
    bestStrand = "-"
    bestStart = 0
    bestEnd = 0
    bestAA = ""
    for strand in ["-","+"]:
        for frame in range(0,3):
            if strand == "-":
                translated = transcript.seq.reverse_complement()[frame:].translate(table="Standard")
            else:
                translated = transcript.seq[frame:].translate(table="Standard")
            seqs = str(translated).split("*")
            start = 1 + frame
            for i, peptideOri in enumerate(seqs):
                if "M" in peptideOri and i < len(seqs)-1:
                    peptideSplit = peptideOri.split("M")
                    tmpStart = start + len(peptideSplit[0]*3)
                    peptide = "M" + "M".join(peptideSplit[1:])
                    if len(peptide) >= min_length:
                        with open(tmp_path, "w") as output_handle:
                            protRec = SeqRecord(Seq(str(peptide), generic_protein), id=transcript.id, description=transcript.description)
                            SeqIO.write(protRec, output_handle, "fasta")
                        stdout, stderr = cline()
                        
                        if len(stderr) > 0:
                            sys.stderr.write(stderr+"\n")
                        if len(stdout) > 0:
                            match, percent, e_val = [stdout.split()[i] for i in [1, 2, 10]]
                            e_val = float(e_val)
                            if e_val < bestFrameEVal:
                                bestFrameEVal = e_val
                                bestFrame = frame
                                bestPercent = percent
                                bestMatch = match
                                bestLength = len(peptide)
                                bestStrand = strand
                                bestStart = tmpStart
                                bestEnd = tmpStart + (bestLength*3)
                                bestAA = peptide
                start+=(1+len(peptideOri))*3
                
                
    if bestMatch == "":
        print("no match", transcript.id)
        continue
    
    # write DNA
    SeqIO.write(transcript, output_handleDNA, "fasta")
    
    # write Protein
    # Generate id and desciption
    if bestStrand == "-":
        #print(transcript.id, "reverse", bestStart, bestEnd, len(str(transcript.seq)), len(str(transcript.seq)) - bestEnd, len(str(transcript.seq)) - bestStart, bestAA)
        tmpStart = bestStart
        bestStart = len(str(transcript.seq)) - bestEnd - 1
        bestEnd = len(str(transcript.seq)) - tmpStart + 1
        
    accession = transcript.id
    description = bestMatch.split("|")[-1] + "|BLAST|" + str(len(str(bestAA))) + "_aa|" + bestStrand + "|" + str(bestStart) + "|" + str(bestEnd)
    
    protRec = SeqRecord(Seq(str(bestAA), generic_protein), id=accession, description=description)
    SeqIO.write(protRec, output_handlePROT, "fasta")

                
        
        