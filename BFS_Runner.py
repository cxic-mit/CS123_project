import argparse
from BFSIteration import MRBFSIteration
import os
from io import StringIO
import sys


# Short class to capture stdout
class Capturing(list):
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self
    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        sys.stdout = self._stdout

# Method to get ids from cmd line at runtime
def GetArgs():
	
	parser = argparse.ArgumentParser()
	parser.add_argument('--input_id', type=str, required=True)
	parser.add_argument('--target_id', type=str, required=True)
	args = parser.parse_args()
	input_id = args.input_id
	target_id = args.target_id
	
	return (input_id, target_id)


# Method for transforming original dataset into required format for breadth-first search
def Initialize_BFS_Data(input_id, output_file):

	with open(output_file, 'w') as out:
	
		with open("./data/friends-000______small.txt") as f:
	
			for line in f:
				line = line.strip('\n')
				fields = line.split(':')
				if '' not in fields and 'private' not in fields and 'notfound'\
				not in fields:
					userID = fields[0]
					connections = fields[1].split(',')
		
					color = 'WHITE'
					distance = 9999
		
					if (userID == input_id) :
						color = 'GRAY'
						distance = 0
		
					if (userID != ''):
						edges = ','.join(connections)
						outStr = '|'.join((userID, edges, str(distance), color))
						out.write(outStr)
						out.write("\n")
	
		f.close()
	
	out.close()



# Get input and target ids and specify a temporary data file to keep track of modifications made by BFS
input_id, target_id = GetArgs()
output_file = 'BFS-temp.txt'

# Initialize network data for BFS
Initialize_BFS_Data(input_id, output_file)

# Initialize instance of BFS class
arg_str = '--target {0} {1} --output=results'.format(target_id, output_file)
mr_job = MRBFSIteration(args=arg_str.split())


# Run map-reduce jobs in loop while capturing stdout 
with Capturing() as output:

	for i in range(20):

		# Run map-reduce
		with mr_job.make_runner() as runner:
			runner.run()

		# Replace social network dataset with map-reduce results and clean temporary files
		os.system('cat results/* > {0}'.format(output_file))
		os.system('rm -r results')

# Final clean-up
os.system('rm {0}'.format(output_file))

# Map-reduce prints degrees of separation for all possible paths. Print result for minimum path.
if output:
	degs = min([int(x) for x in output])
	input_name, target_name = int(input_id), int(target_id)
	print ('{0} is {1} degrees of separation away from {2}'.format(input_name, degs, target_name))
else:
	print ('{0} is more than {1} degrees of separation away from {2}'.format(input_id, 20, target_id))