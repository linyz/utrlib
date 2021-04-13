#!/usr/bin/env python3

### generate_metrics.py
### Takes a list of UTR sequences and output from RNAfold (see below for example data format) and generates A/U/G/C/GC content, finds uORFs (AUG) and generates their position and outputs to stdout (or piped to tsv)


### Example run:
### python3 generate_metrics.py -i seelig_5utr_sequences.csv -r RNAfold_output_cleaned.txt > final_output.tsv

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


import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-i", nargs = 1, help="input csv file")
parser.add_argument("-r", nargs = 1, help="input cleaned RNAfold output file")
args = parser.parse_args()
input_csv = args.i[0]

RNAfold_cleaned = args.r[0]

#returns a, u, g, c, and gc content
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


# start codons to use
start_codon = "AUG"

# stop codons
stop_codons = ["UAA", "UGA", "UAG"]

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

# returns all positions of uORFs
def find_uORF(input_seq):
	return list(find_all(input_seq, start_codon))

#
def find_uORF_length_frame(input_seq):
	uORF_positions = (list(find_all(input_seq, start_codon)))
	# if no uORFs, return empty list
	if len(uORF_positions) < 1:
		return []

	uORF_all = []

	#calculate uORF positions for each uORF. do this by generating a substring starting with AUG 
	for uORF_pos in uORF_positions:

		new_substring = input_seq[uORF_pos:]

		stop_codon_positions = []
		for codon in stop_codons:
			stop_codon_positions.append(new_substring.find(codon))

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


		# uORF_all.append([new_substring, stop_codon_positions, in_frame_stop_codon_positions, uORF_length])
		# uORF_all.append([new_substring, uORF_pos, uORF_length, len(new_substring), uORF_in_frame])
		#return ['AUGCUGUGAGAGCCAUUGGAAGACUGCCCUCU', 9] (uORF position****, length)
		uORF_all.append([uORF_pos, uORF_length, uORF_in_frame])
	return uORF_all

import csv
print('sequence', '\t', 'A-content', '\t', 'U-content', '\t', 'C-content', '\t', 'G-content', '\t', 'GC_content', '\t', 'uORF_positions', '\t', 'uORF_position_length_frame', '\t', 'MFE_structure', '\t', 'MFE_kcal/mol')
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
		print(sequence, '\t', augc_gc[0], '\t', augc_gc[1], '\t', augc_gc[2], '\t', augc_gc[3], '\t', augc_gc[4], '\t', find_uORF(sequence), '\t', find_uORF_length_frame(sequence), '\t', MFElinesplit[0], '\t', MFElinesplit[1])



