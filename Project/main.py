import os
import re
import sys
import yaml

from Bio import SeqIO
from Bio.SeqUtils import GC

from itertools import product

from difflib import SequenceMatcher


def read_yaml(file_path):
    with open(file_path, "r") as f:
        return yaml.safe_load(f)


def generate_barcodes(config):
	conda_source = config['GENERATE_BARCODES']['CONDA_SOURCE']
	length = config['GENERATE_BARCODES']['LENGTH']
	number = config['GENERATE_BARCODES']['NUMBER']
	file_name = config['GENERATE_BARCODES']['FILE_NAME']

	if length <= 10:
		comb = product(['A', 'C', 'T', 'G'], repeat=length)
		with open(file_name, 'w') as f:
			content = ''
			for pos, item in enumerate(comb):
				barcode = ''.join(item)
				content += f'>{pos}\n{barcode}\n'
			f.write(content)
	else:
		if config['APP']['OS'] != 'linux' or config['APP']['SHELL'] != 'bash':
			raise Exception('The barcodes generation can only be done in linux machines with bash shell :(')

		else:
			os.system("chmod u+x generate_barcodes.sh")
			os.system(f"./generate_barcodes.sh {conda_source} {length} {number} {file_name}")


def read_barcodes(input_file):
	extension = input_file.split('.')[-1]

	if extension == "txt":
		# Read barcodes
		with open(input_file, 'r') as f:
			content = f.read()
			content = content.split('\n')

		return content

	elif extension in ['fa', 'fna', 'fasta', 'fas']:
		content = []		

		for record in SeqIO.parse(input_file, "fasta"):
		    content.append(str(record.seq))

		return content


def filter_by_baseruns(barcodes, MAX_REPETITION):
	filtered_barcodes = []
	for barcode in barcodes:
		pattern = re.compile(r'(.)\1{' + str(MAX_REPETITION) + r',}')
		bases_repeated = re.search(pattern, barcode)  # Get a character and check if it repeats more times
		if bases_repeated is None:
			filtered_barcodes.append(barcode)

	return filtered_barcodes


def match_found(seq, seq2, MAX_SIMILARITY):
	# Search a match between current sequence and the sequences already selected
	match = SequenceMatcher(None, seq, seq2).find_longest_match(0, len(seq), 0, len(seq2))
	repeated_nuc = len(seq[match.a:match.a + match.size])

	# If the common subsequence has more than 6 nucleotides and it starts at the same position in both sequences the current sequence won't be added to the list
	if repeated_nuc > MAX_SIMILARITY and match.a == match.b:
		return True

	return False


def filter_by_common_subsequence(barcodes, MAX_SIMILARITY):
	filtered_barcodes = []

	print('Filtering by common subsequence\n')
	# Iterate over the sequences
	for pos, seq in enumerate(barcodes):
		add_seq = True

		# Iterate over the already selected sequences
		for seq2 in filtered_barcodes:
			# Check if the two sequences have the same subsequence
			if match_found(seq, seq2, MAX_SIMILARITY):
				add_seq = False
				break
			

		# Add sequence to the filtered sequences list
		if add_seq is True:
			filtered_barcodes.append(seq)

		if pos % 1000 == 0:
			print(pos, 'barcodes done')

	print(len(barcodes), 'barcodes done')


	return filtered_barcodes


def write_results_file(barcodes, output_file):
	extension = output_file.split('.')[-1]

	# Write sequences
	with open(output_file, 'w') as result_file:
		for pos, seq in enumerate(barcodes):
			if extension == 'txt':
				result_file.write(f"{seq}\n")
			elif extension in ['fa', 'fna', 'fasta', 'ffn', 'faa', 'frn']:
				result_file.write(f">ID: {pos}\n{seq}\n")


if __name__ == '__main__':
	config = read_yaml('config.yaml')

	if config['APP']['GENERATE_BARCODES'] is True:
		generate_barcodes(config)
	
	barcodes = read_barcodes(config['VARIABLES']['INPUT_FILE'])
	barcodes = filter_by_baseruns(barcodes, config['VARIABLES']['MAX_BASERUN_REPETITION'])
	# barcodes = filter_by_common_subsequence(barcodes, config['VARIABLES']['MAX_SIMILARITY'])
	# Não está filtrando por porcentagem de GC

	write_results_file(barcodes, config['VARIABLES']['OUTPUT_FILE'])
