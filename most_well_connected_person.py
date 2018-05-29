# We define most well connected person as the node with the minimum eccentricity,
# a.k.a. the radius of the largest connected component of the network.
import sys
import os
from MRBFS import MRBFS
from MRMinEccentricity import MRMinEccentricity

def preprocess_data(input_file, preprocess_file):
    with open(preprocess_file, 'w+') as p, open(input_file) as i:
        for line in i:
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
                outStr = '|'.join([userID, edges, str(distance), path, color])
                p.write(outStr)
                p.write('\n')
    i.close()
    p.close()

def write_results(preprocess_file, output_file, START_NODE, END_NODE, N):
    flag = False
    with open(preprocess_file) as f, open(output_file, 'w+') as out:
        for line in f:
            line = line.strip('\n')
            fields = line.split('|')
            if str(fields[0]) == END_NODE and int(fields[-3]) < 9999:
                flag = True
                print('The path from {0} to {1} is {2}, the distance is {3}'.format(START_NODE, END_NODE, \
                    '->'.join(fields[-2].split()) + '->' + str(END_NODE), fields[-3]))
                out.write(',' .join(START_NODE, END_NODE, fields[-3]))
    if not flag:
        print('Cannot find the path from {0} to {1} within {2} degrees.'.format(START_NODE, END_NODE, N))

def main():
    input_file = './data/friends-000______small.txt'
    preprocess_file = './results/preprocessed_data.txt'
    output_file = './results/output.txt'
    min_file = './results/min.txt'

    preprocess_data(input_file, preprocess_file)

    N = 10
    START_NODE = 146
    nodes = 10
    end_nodes = range(START_NODE+1, START_NODE+nodes+1)

    for END_NODE in end_nodes:
        args = '--start_node {0} --end_node {1} {2} --output = ./results'.format(START_NODE, END_NODE, preprocess_file)
        mr_job = MRBFS(args=args.split())

        for i in range(N):
            with mr_job.make_runner() as runner:
                runner.run()

        write_results(preprocess_file, output_file, START_NODE, END_NODE, N)

    mr_job = MRMinEccentricity(args=[output_file, min_file])

if __name__== "__main__":
    main()
