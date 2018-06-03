# We define most well connected person as the node with the minimum eccentricity,
# a.k.a. the graph radius.

import sys
import os
import run_MRBFS
from MRMinEccentricity import MRMinEccentricity


def write_results(output_file, paths_file, start_node):
	"""
	Find paths and write viable path distance to an output file.
	Inputs:
		preprocessed_file: input file
		paths_file: output file
		start-node: start node
		end_nodes: list of end nodes
		N: degrees limitation
	Returns: no explicit return; writes to paths_file.
	"""
	print('writing...')
	with open(output_file) as f, open(paths_file, 'a') as p:
		for line in f:
			line = line.strip('\n')
			fields = line.split('|')
			distance = int(fields[-3])
			end_node = str(fields[1])
			if distance < 9999:
				print('Found path!', start_node, end_node, distance)
				outStr = '|'.join([start_node, end_node, str(distance)])
				p.write(outStr)
				p.write('\n')


def main():
	"""
	Iterate through every pair of nodes to find distances.
	Find the node with the minimum eccentricity.
	"""
	output_file = './results/paths.txt'
	min_file = './results/min.txt'

	nodes = range(102, 1000)

	for i in nodes:
		for j in nodes:
			if i != j:
				start_node = str(i)
				end_node = str(j)
				print(start_node, end_node)
				line = run_MRBFS.main(start_node, end_node)
				if line:
					with open(output_file, 'a') as f:
						f.write(line)
						f.write('\n')


if __name__ == "__main__":
	main()