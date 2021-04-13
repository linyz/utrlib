# get csv file ready for RNAfold
#
# head RNAfold_input.txt 
# CCCACCCCGGGCTCTCTCCTGGCCTCCCACCCCCGCGCCCGGCTTCCACC
# CCCACCCCGGGCTCTCTCCTGGCTTCCCACCCCCGCGCCCGGCTTCCACC

python3 csv_to_RNAfold.py -i seelig_5utr_sequences.csv > RNAfold_input.txt   

# run RNAfold on all sequences
#
# head RNAfold_output.txt
# CCCACCCCGGGCUCUCUCCUGGCCUCCCACCCCCGCGCCCGGCUUCCACC
# ......((((((.(.....(((....))).....).))))))........ (-13.70)
# CCCACCCCGGGCUCUCUCCUGGCUUCCCACCCCCGCGCCCGGCUUCCACC
# ......((((((.(.....(((....))).....).))))))........ (-13.70)
/Users/albert/Dropbox/Floor\ Lab/Analysis/UTR_library/ViennaRNA-2.4.17/src/bin/RNAfold -i RNAfold_input.txt > RNAfold_output.txt

# cleans RNAfold output files to integrate into metrics tsv
#
# head RNAfold_output_cleaned.txt
# ......((((((.(.....(((....))).....).))))))........ -13.70
# ......((((((.(.....(((....))).....).))))))........ -13.70
python3 extract_RNAfold.py -i RNAfold_output.txt > RNAfold_output_cleaned.txt

# generates metrics (A/U/G/C/GC content, finds uORFs (AUG), and parses RNAfold output and generates a TSV)
# head final_output.tsv
#
# sequence 	 A-content 	 U-content 	 C-content 	 G-content 	 GC_content 	 uORF_positions 	 uORF_position_length_frame 	 MFE_structure 	 MFE_kcal/mol
# CCCACCCCGGGCUCUCUCCUGGCCUCCCACCCCCGCGCCCGGCUUCCACC 	 0.06 	 0.14 	 0.18 	 0.62 	 0.8 	 [] 	 [] 	 ......((((((.(.....(((....))).....).))))))........ 	 -13.70
# CCCACCCCGGGCUCUCUCCUGGCUUCCCACCCCCGCGCCCGGCUUCCACC 	 0.06 	 0.16 	 0.18 	 0.6 	 0.78 	 [] 	 [] 	 ......((((((.(.....(((....))).....).))))))........ 	 -13.70
python3 generate_metrics.py -i seelig_5utr_sequences.csv -r RNAfold_output_cleaned.txt > final_output.tsv