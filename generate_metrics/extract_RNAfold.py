#!/usr/bin/env python3

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-i", nargs = 1, help="input RNAfold file")

args = parser.parse_args()
input_RNAfold = args.i[0]



import csv
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
			print(cleaned_line[:seq_length], mfe)
			flag = True



	# csv_reader = csv.reader(inputfile, delimiter=',')
	# for row in csv_reader:
		
	# 	#convert all bases to uppercase
	# 	sequence = row[1].upper()
	# 	#convert T to U
	# 	sequence = sequence.replace("T", "U")
	# 	print(row[1])