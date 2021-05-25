# run_metrics.py
#
# example run command: python3 run_metrics.py -i seelig_5utr_sequences.csv
# 
# will generate the following files: 
# 
# RNAfold_input.txt (trimmed original CSV file so that you just have a list of sequences)
# RNAfold_output.txt (output from running ViennaRNA-2.4.17 RNAfold on RNAfold_input.txt)
# RNAfold_output_cleaned.txt (extracts MFE structure and MFE from RNAfold_output.txt)
# final_output.tsv contains metric calculations (G/C content, uORF location, MFE, etc.)

# you might have to modify CSV to RNAfold depending on input CSV format (see below for example)
# 
# head seelig_5utr_sequences.csv 
# 0,CCCACCCCGGGCTCTCTCCTGGCCTCCCACCCCCGCGCCCGGCTTCCACC
# 1,CCCACCCCGGGCTCTCTCCTGGCTTCCCACCCCCGCGCCCGGCTTCCACC
# you will have to change RNAfold_path to your path of installation of ViennaRNA RNAFold
# see installing_ViennaRNA.sh for installation instructions - it may take several tries/failures. 


import subprocess
import sys
import time
import csv
import argparse
from argparse import RawTextHelpFormatter
RNAfold_path = '/Users/albert/Dropbox/Floor_Lab/Analysis/UTR_library/ViennaRNA-2.4.17/src/bin/RNAfold'

# start codons to use
start_codons = ["AUG", "CUG"]

# stop codons
stop_codons = ["UAA", "UGA", "UAG"]


######################
### CSV to RNAfold ###
######################


# get csv file ready for RNAfold

# head seelig_5utr_sequences.csv 
# 0,CCCACCCCGGGCTCTCTCCTGGCCTCCCACCCCCGCGCCCGGCTTCCACC
# 1,CCCACCCCGGGCTCTCTCCTGGCTTCCCACCCCCGCGCCCGGCTTCCACC

# head RNAfold_input.txt 
# CCCACCCCGGGCTCTCTCCTGGCCTCCCACCCCCGCGCCCGGCTTCCACC
# CCCACCCCGGGCTCTCTCCTGGCTTCCCACCCCCGCGCCCGGCTTCCACC

#!/usr/bin/env python3


parser = argparse.ArgumentParser(description="run_metrics.py runs RNAfold on sequences and outputs a file with A/U/GC content, uORF location/frame/length, MFE structure, and MFE. \n\nExample run command: python3 run_metrics.py -i seelig_5utr_sequences.csv\n\nThis will generate the following files: \nRNAfold_input.txt (trimmed original CSV file so that you just have a list of sequences)\nRNAfold_output.txt (output from running ViennaRNA-2.4.17 RNAfold on RNAfold_input.txt)\nRNAfold_output_cleaned.txt (extracts MFE structure and MFE from RNAfold_output.txt)\nfinal_output.tsv contains metric calculations (G/C content, uORF location, MFE, etc.)\n \nYou might have to modify CSV to RNAfold depending on input CSV format (see below for example)\nhead seelig_5utr_sequences.csv \n0,CCCACCCCGGGCTCTCTCCTGGCCTCCCACCCCCGCGCCCGGCTTCCACC\n1,CCCACCCCGGGCTCTCTCCTGGCTTCCCACCCCCGCGCCCGGCTTCCACC\nYou will have to change RNAfold_path to your path of installation of ViennaRNA RNAFold\nsee installing_ViennaRNA.sh for installation instructions - it may take several tries/failures.", 
	formatter_class=RawTextHelpFormatter)
parser.add_argument("-i", nargs = 1, help="input csv file")

args = parser.parse_args()

arg_var=vars(parser.parse_args())
if arg_var.get('i'):
	print(arg_var.get('i'))
else:
	parser.error('Invalid options provided')

input_csv = args.i[0]


print("Trimming original CSV file for RNAfold input")
f = open("RNAfold_input.txt", "a")


with open(input_csv) as inputfile:
	csv_reader = csv.reader(inputfile, delimiter=',')
	for row in csv_reader:
		#convert all bases to uppercase
		sequence = row[1].upper()
		#convert T to U
		sequence = sequence.replace("T", "U")
		print(row[1],file=f)
f.close()
print("RNAfold_input.txt has been generated from", input_csv)

######################
######################
######################




#######################
### Running RNAfold ###
#######################

# run RNAfold on all sequences

# head RNAfold_output.txt
# CCCACCCCGGGCUCUCUCCUGGCCUCCCACCCCCGCGCCCGGCUUCCACC
# ......((((((.(.....(((....))).....).))))))........ (-13.70)
# CCCACCCCGGGCUCUCUCCUGGCUUCCCACCCCCGCGCCCGGCUUCCACC
# ......((((((.(.....(((....))).....).))))))........ (-13.70)

print("running RNAfold on RNAfold_input.txt")
start = time.time()

process = subprocess.run([RNAfold_path, '-i', 'RNAfold_input.txt'], shell=False, check=True, stdout=subprocess.PIPE, universal_newlines=True)
output = process.stdout

f = open("RNAfold_output.txt", "a")
print(output, file=f)
f.close()
print("RNAfold_output.txt has been generated from RNAfold_input.txt")
print ('RNAfold took', int(time.time()-start), "seconds to run")


######################
######################
######################




###############################
### Running extract_RNAfold ###
###############################

# cleans RNAfold output files to integrate into metrics tsv
#
# head RNAfold_output_cleaned.txt
# ......((((((.(.....(((....))).....).))))))........ -13.70
# ......((((((.(.....(((....))).....).))))))........ -13.70


input_RNAfold = "RNAfold_output.txt"
f = open("RNAfold_output_cleaned.txt", "a")

with open(input_RNAfold) as inputfile:
	flag = True
	seq_length = 0
	for line in inputfile:
		#get rid of newlines
		cleaned_line = line.strip()

		if flag:
			seq_length = len(cleaned_line)
			flag = False
		else:
			mfe = cleaned_line[seq_length:][2:-1].strip()
			print(cleaned_line[:seq_length], mfe, file=f)
			flag = True
f.close()
print(input_RNAfold, "has been cleaned and RNAfold_output_cleaned.txt has been generated")

######################
######################
######################



###################################
### running generate_metrics.py ###
###################################

#!/usr/bin/env python3

### generate_metrics.py
### Takes a list of UTR sequences and output from RNAfold (see below for example data format) and generates A/U/G/C/GC content, finds uORFs (AUG) and generates their position and outputs to stdout (or piped to tsv)


# head seelig_5utr_sequences.csv 
# 0,CCCACCCCGGGCTCTCTCCTGGCCTCCCACCCCCGCGCCCGGCTTCCACC
# 1,CCCACCCCGGGCTCTCTCCTGGCTTCCCACCCCCGCGCCCGGCTTCCACC

# head RNAfold_output_cleaned.txt
# ......((((((.(.....(((....))).....).))))))........ -13.70
# ......((((((.(.....(((....))).....).))))))........ -13.70

# head final_output.tsv
# sequence 	 A-content 	 U-content 	 C-content 	 G-content 	 GC_content 	 uORF_positions 	 uORF_position_length_frame 	 MFE_structure 	 MFE_kcal/mol
# CCCACCCCGGGCUCUCUCCUGGCCUCCCACCCCCGCGCCCGGCUUCCACC 	 0.06 	 0.14 	 0.18 	 0.62 	 0.8 	 [] 	 [] 	 ......((((((.(.....(((....))).....).))))))........ 	 -13.70
# CCCACCCCGGGCUCUCUCCUGGCUUCCCACCCCCGCGCCCGGCUUCCACC 	 0.06 	 0.16 	 0.18 	 0.6 	 0.78 	 [] 	 [] 	 ......((((((.(.....(((....))).....).))))))........ 	 -13.70


print("Generating metrics")
input_csv = args.i[0]

RNAfold_cleaned = "RNAfold_output_cleaned.txt"

# returns a, u, g, c, and gc content
def calculate_augc_gc_content(input_seq):
	seq = input_seq.upper()
	seq 
	length = len(seq)
	
	a = seq.count("A")
	u = seq.count("U")
	g = seq.count("G")
	c = seq.count("C")
	def float_division(base,total):
		return base/float(total)
	return float_division(a,length), float_division(u,length), float_division(g,length), float_division(c,length), float_division(g+c, length)

# finds all positions including overlapping matches
# https://stackoverflow.com/questions/4664850/how-to-find-all-occurrences-of-a-substring
def find_all(a_str, sub):
    start = 0
    while True:
        start = a_str.find(sub, start)
        if start == -1: return
        yield start
        start += 1
        # start += len(sub) # use start += 1 to find overlapping matches

# function to flatten lists 
# ex:
# print(flatten([[1, 2, 3, 4], [5, 6, 7], [8, 9], 10]))
# [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
# https://stackabuse.com/python-how-to-flatten-list-of-lists/
def flatten(list_of_lists):
    if len(list_of_lists) == 0:
        return list_of_lists
    if isinstance(list_of_lists[0], list):
        return flatten(list_of_lists[0]) + flatten(list_of_lists[1:])
    return list_of_lists[:1] + flatten(list_of_lists[1:])

# returns all positions of uORFs (index position 0 = first nucleotide)
# ex:
# GGAAGUGCCUGAGCUAGUGAGCUGGCCAACGAGCUCCGCGGGCUGGGACC [8, 21, 42]
def find_uORF(input_seq):
	positions = []
	for codon in start_codons:
		if len(list(find_all(input_seq, codon))) > 0:
			positions.append(list(find_all(input_seq, codon)))
	# print(positions)
	return flatten(positions)

# for each uORF starting position, calculates length and if each uORF is in frame or not (-1 if no stop codon) (index position 0 = first nucleotide)
# ex:
# GGAAGUGCCUGAGCUAGUGAGCUGGCCAACGAGCUCCGCGGGCUGGGACC [[8, 9, True], [21, -1, False], [42, -1, False]]
def find_uORF_length_frame(input_seq):
	uORF_positions = find_uORF(input_seq)
	# print("uORF", uORF_positions)
	# if no uORFs, return empty list
	if len(uORF_positions) < 1:
		return []

	uORF_all = []

	#calculate uORF positions for each uORF. do this by generating a substring starting with AUG 
	for uORF_pos in uORF_positions:

		new_substring = input_seq[uORF_pos:]

		stop_codon_positions = []
		for codon in stop_codons:
			# stop_codon_positions.append(new_substring.find(codon)) # switch from .find (finds first occurrence) to find_all to find all occurrences
			stop_codon_positions.append(list(find_all(new_substring, codon)))
		stop_codon_positions = flatten(stop_codon_positions) # have to flatten list because of find_all output is [[], []]
		
		#only use in frame stop codons
		in_frame_stop_codon_positions = []
		for stop_codon_pos in stop_codon_positions:
			if stop_codon_pos % 3 == 0:
				in_frame_stop_codon_positions.append(stop_codon_pos)

		#return uORF length (+3 includes stop codon) or return -1 if none present
		if len(in_frame_stop_codon_positions) > 0:
			uORF_length = min(in_frame_stop_codon_positions) + 3
		else:
			uORF_length = -1

		#calculate if uORF is in frame or not with CDS
		uORF_in_frame = False
		if len(new_substring) % 3 == 0:
			uORF_in_frame = True

		uORF_all.append([uORF_pos, uORF_length, uORF_in_frame])
	return uORF_all

f = open("final_output.tsv", "a")

print('sequence', '\t', 'A-content', '\t', 'U-content', '\t', 'C-content', '\t', 'G-content', '\t', 'GC_content', '\t', 'uORF_positions', '\t', 'uORF_position_length_frame', '\t', 'MFE_structure', '\t', 'MFE_kcal/mol', file=f)
with open(input_csv) as inputfile, open(RNAfold_cleaned, 'r') as MFE:
	csv_reader = csv.reader(inputfile, delimiter=',')
	for row, MFEline in zip(csv_reader, MFE):
		
		#convert all bases to uppercase
		sequence = row[1].upper()
		#convert T to U
		sequence = sequence.replace("T", "U")
		augc_gc = calculate_augc_gc_content(sequence)
		# augc_gc[0], augc_gc[1], augc_gc[2], augc_gc[3], augc_gc[4])
		
		MFElinesplit = MFEline.strip().split()
		print(sequence, '\t', augc_gc[0], '\t', augc_gc[1], '\t', augc_gc[2], '\t', augc_gc[3], '\t', augc_gc[4], '\t', find_uORF(sequence), '\t', find_uORF_length_frame(sequence), '\t', MFElinesplit[0], '\t', MFElinesplit[1], file=f)
f.close()

print("final_output.tsv metrics have been generated from", input_csv,"and", RNAfold_cleaned)
