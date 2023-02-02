from Bio.SeqUtils import GC
from Bio import SeqIO

from difflib import SequenceMatcher

import re
import sys

FILE = sys.argv[1]

# Max tolerance for common nucleotides in subsequences between two sequences (the subsequences must be at the same position)
# If the common subsequence has more nucleotides than the tolerance value, the second sequence will be discarded
MAX_SIMILARITY = 5
GC_PERC = (35, 65)  # Percentage range of GC
file_name = FILE.split('.')[0].replace('Input/', '')
RESULTS_FILE = f'Saved Results/{file_name}_filtered'
SAVE_AS = 'txt'
MAX_BASERUN_REPETITION = 2


def read_barcodes(file, extension):
	if extension == "txt":
		# Read barcodes
		with open(file, 'r') as f:
			content = f.read()
			content = content.split('\n')

		return content
	elif extension in ['fa', 'fna', 'fasta', 'fas']:
		content = []		

		for record in SeqIO.parse(file, "fasta"):
		    content.append(str(record.seq))

		return content

def match_found(seq, seq2):
	# Search a match between current sequence and the sequences already selected
	match = SequenceMatcher(None, seq, seq2).find_longest_match(0, len(seq), 0, len(seq2))
	repeated_nuc = len(seq[match.a:match.a + match.size])

	# If the common subsequence has more than 6 nucleotides and it starts at the same position in both sequences the current sequence won't be added to the list
	if repeated_nuc > MAX_SIMILARITY and match.a == match.b:
		return True

	return False


def filter_by_common_subsequence(barcodes):
	filtered_barcodes = []

	# # Iterate over the sequences
	# for pos, seq in enumerate(barcodes):
	# 	add_seq = True

	# 	# Iterate over the already selected sequences
	# 	for seq2 in filtered_barcodes:
	# 		if match_found(seq, seq2):
	# 			add_seq = False
	# 			break
			

	# 	# Add sequence to the filtered sequences list
	# 	if add_seq is True:
	# 		filtered_barcodes.append(seq)

	# 	if pos % 1000 == 0:
	# 		print(pos)

	for pos, seq in enumerate(barcodes):
		if seq not in filtered_barcodes:
			filtered_barcodes.append(seq)
	return filtered_barcodes


def filter_by_baseruns(barcodes, MAX_REPETITION):
	filtered_barcodes = []
	for barcode in barcodes:
		pattern = re.compile(r'(.)\1{' + str(MAX_REPETITION) + r',}')
		bases_repeated = re.search(pattern, barcode)  # Get a character and check if it repeats more times
		if bases_repeated is None:
			filtered_barcodes.append(barcode)

	return filtered_barcodes


def write_results_file(barcodes):
		# Empty results file
		with open(f"{RESULTS_FILE}.{SAVE_AS}", 'w') as f:
			f.write('')

		# Write sequences
		with open(f"{RESULTS_FILE}.{SAVE_AS}", 'w') as result_file:
			for pos, seq in enumerate(barcodes):
				if SAVE_AS == 'txt':
					result_file.write(f"{seq}\n")
				elif SAVE_AS in ['fa', 'fna', 'fasta', 'ffn', 'faa', 'frn']:
					result_file.write(f">ID: {pos}\n{seq}\n")
			



if __name__ == '__main__':
	barcodes = read_barcodes(FILE, FILE.split('.')[-1])
	barcodes = filter_by_baseruns(barcodes, MAX_BASERUN_REPETITION)
	barcodes = filter_by_common_subsequence(barcodes)
	write_results_file(barcodes)
