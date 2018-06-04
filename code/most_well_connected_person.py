# We define most well connected person as the node with the minimum eccentricity,
# a.k.a. the graph radius.

import run_MRBFS
from MRMinEccentricity import MRMinEccentricity

def get_good_nodes(input_file):
	"""
	Return a list of nodes that aren't private or notfound or ''
	"""
	nodes = []

	with open(input_file) as f:
		for line in f:
			line = line.strip('\n')
			fields = line.split(':')
			if '' not in fields and 'private' not in fields \
					and 'notfound' not in fields:
				nodes.append(fields[0])

	return nodes


def run_mrjob(mr_job, output_file, min_file):
	"""
	Run MRMinEccentricity
	"""
	for i in range(N):
		with mr_job.make_runner() as runner:
			runner.run()
		os.system('cat results/* > {0}'.format(min_file))


def main():
    """
    Iterate through every pair of nodes to find distances.
    Find the node with the minimum eccentricity.
    """
    input_file = './data/friends-000______small.txt'
    output_file = './results/paths.txt'
    min_file = './results/min.txt'

    nodes = get_good_nodes(input_file)[:100]
    for i in nodes:
        for j in nodes:
            if i != j:
				print(i, j)
				line = run_MRBFS.main(i, j)
				if line:
					with open(output_file, 'a') as f:
						f.write(line)
						f.write('\n')

# args = '--jobconf mapreduce.job.reduces=1  ----{} --{}'.format(output_file. min_file)
# mr_job = MRBFS(args=args.split())
# run_mrjob(mrjob, output_file, min_file)

if __name__ == "__main__":
	main()