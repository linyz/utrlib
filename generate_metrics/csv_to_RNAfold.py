#!/usr/bin/env python3

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-i", nargs = 1, help="input csv file")

args = parser.parse_args()
input_csv = args.i[0]



import csv
with open(input_csv) as inputfile:
	csv_reader = csv.reader(inputfile, delimiter=',')
	for row in csv_reader:
		
		#convert all bases to uppercase
		sequence = row[1].upper()
		#convert T to U
		sequence = sequence.replace("T", "U")
		print(row[1])