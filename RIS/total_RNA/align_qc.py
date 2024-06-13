#!/usr/bin/env python
import sys
import os

def line_count(file_path):
    if os.path.exists(file_path):
        return int(os.popen(f'wc -l {file_path}').read().split()[0])
    else:
        return 0

def write_stats(name, path, file_handle):
    # Combined. Call it on each file
    num_corrected = line_count(path + "_all_corrected.bed")
    num_inconsistent = line_count(path + "_all_inconsistent.bed")
    num_cannot_verify = line_count(path + "_cannot_verify.bed")
    total = num_corrected + num_inconsistent + num_cannot_verify
    # Compute sum. Compute percentage
    # Write to file
    file_handle.write(name + "\n")
    file_handle.write("---------------------------------\n")
    file_handle.write(f"{total:,}".rjust(10, ' ') + " Aligned Reads\n")
    file_handle.write(f"{num_corrected:,}".rjust(10, ' ') +  " Correct (" + f"{num_corrected/total:.2%}" + ")\n")
    file_handle.write(f"{num_inconsistent:,}".rjust(10, ' ') + " Inconsistent (" + f"{num_inconsistent/total:.2%}" + ")\n")
    file_handle.write(f"{num_cannot_verify:,}".rjust(10, ' ') + " Cannot Verify (" + f"{num_cannot_verify/total:.2%}" + ")\n")
    file_handle.write("\n")


combined_path = sys.argv[1]
data_path = sys.argv[2]
individual_path = sys.argv[3]
out_path = sys.argv[4]

with open(out_path, 'w') as file_handle:
    write_stats("Combined", combined_path, file_handle)

    # Loop through directories
    for f in os.listdir(data_path):
        if os.path.isdir(os.path.join(data_path, f)):
            for f2 in sorted(os.listdir(os.path.join(data_path, f))):
                write_stats(f2, os.path.join(individual_path, f2), file_handle)
       
