#!/usr/bin/env python
import sys
import re as re
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
from Bio.Seq import Seq
from Bio.Alphabet import generic_protein
from Bio.Blast.Applications import NcbiblastpCommandline

# input files
proteome_path = sys.argv[1]
transcriptome_path = sys.argv[2]
min_length = int(sys.argv[3])
out_path = sys.argv[4]
tmp_path = sys.argv[5]
num_threads = int(sys.argv[6])


# read transcriptome
transcripts = SeqIO.parse(transcriptome_path, 'fasta')
  
cline = NcbiblastpCommandline(query=tmp_path, db=proteome_path, evalue=0.001, remote=False, outfmt=6, max_target_seqs=1, max_hsps=1, num_threads=num_threads)

with open(out_path, "w") as output_fasta_handle:
    for transcript in transcripts:
        bestFrame = -1
        bestFrameEVal = 1e9
        bestPercent = 0
        bestMatch = ""
        for frame in range(0,3):
            translated = transcript.seq[frame:].translate(table="Standard", to_stop=True)
            print(frame, translated)
            if len(translated) >= min_length:
                with open(tmp_path, "w") as output_handle:
                    protRec = SeqRecord(Seq(str(translated), generic_protein), id=transcript.id, description=transcript.description)
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
        if bestFrame != -1:
            print(bestFrame, bestFrameEVal, bestPercent, bestMatch, transcript.id)
            
            translated = transcript.seq[bestFrame:].translate(table="Standard", to_stop=True)
            protRec = SeqRecord(Seq(str(translated), generic_protein), id=transcript.id, description=transcript.description)
            SeqIO.write(protRec, output_fasta_handle, "fasta")
        else:
            print("No match", transcript.id)    
        
                
        
        