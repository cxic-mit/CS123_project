import sys
import os
from MRBFS import MRBFS

N = 10 #max 10 iterations
START_NODE = str(sys.argv[1])
END_NODE = str(sys.argv[2])
output_file_0 = 'preprocess_data.txt'
input_file = "./data/friends-000______small.txt"
args = '--start_node {0} --end_node {1} {2} --output=results'.format(START_NODE, END_NODE, output_file_0)
flag = False

def preprocess_data(output_file):

	with open(output_file_0, 'w') as out:
	
		with open(input_file) as f:
	
			for line in f:
				line = line.strip('\n')
				fields = line.split(':')
				if '' not in fields and 'private' not in fields and 'notfound'\
				not in fields:
					userID = fields[0]
					connections = fields[1].split(',')
					path = ''
					color = 'white'
					distance = 9999
					edges = ','.join(connections)
					outStr = '|'.join([userID, edges, str(distance), \
						path, color])
					out.write(outStr)
					out.write("\n")
	
		f.close()
	
	out.close()


mr_job = MRBFS(args=args.split())
preprocess_data(output_file_0)

for i in range(N):
	with mr_job.make_runner() as runner:
		print('running mrjob:', i)
		runner.run()

	os.system('cat results/* > {0}'.format(output_file_0))

with open(output_file_0) as f:
	for line in f:
		line = line.strip('\n')
		fields = line.split('|')
		if str(fields[0]) == END_NODE and int(fields[-3]) < 9999:
			flag = True
			print('The path from {0} to {1} is {2}, the distance is {3}'.format(START_NODE, END_NODE, \
				'->'.join(fields[-2].split()) + '->' + str(END_NODE), fields[-3]))

if not flag:
	print('Cannot find the path from {0} to {1} within {2} degree'.format(START_NODE, END_NODE,N))

os.system('rm {0}'.format(output_file_0))
os.system('rm -r ./__pycache__'.format(output_file_0))
os.system('rm -r results')


