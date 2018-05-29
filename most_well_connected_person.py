# We define most well connected person as the node with the minimum eccentricity,
# a.k.a. the radius of the largest connected component of the network.
import sys
import os
from MRBFS import MRBFS

def preprocess_data(input_file, preprocess_file):
    with open(preprocess_file, 'w+') as p, open(input_file) as f:
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
                outStr = '|'.join([userID, edges, str(distance), path, color])
                p.write(outStr)
                p.write('\n')
    f.close()
    p.close()


def write_results(preprocess_file, output_file, START_NODE, end_nodes):
    with open(preprocess_file) as f, open(output_file) as out:
        for line in f:
            line = line.strip('\n')
            fields = line.split('|')
            for end_node in end_nodes:
                if str(fields[0]) == end_node and int(fields[-3]) < 9999:
                    print('write line')
                    out.write('{} {} {}'.format(START_NODE, end_node, fields[-3]))

def main():
    input_file = './data/friends-000______small.txt'
    preprocess_file = './results/preprocess_data.txt'
    output_file = './results/output.txt'

    preprocess_data(input_file, preprocess_file)

    N_iterations = 10
    START_NODE = 102
    nodes = 10
    end_nodes = range(START_NODE, START_NODE+nodes)

    for end_node in end_nodes:
        args = '--start_node {0} --end_node {1} {2} --output=results'.format(START_NODE, end_node, preprocess_file)
        print(args)
        mr_job = MRBFS(args=args.split())

        for i in range(N_iterations):
            with mr_job.make_runner() as runner:
                runner.run()
            os.system('cat results/* > {0}'.format(preprocess_file))

    #write_results(preprocess_file, output_file, START_NODE, end_nodes)

if __name__== "__main__":
    main()
