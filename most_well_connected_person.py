# We define most well connected person as the node with the minimum eccentricity,
# a.k.a. the graph radius.

import sys
import os
from MRBFS import MRBFS
from MRMinEccentricity import MRMinEccentricity

def preprocess_data(input_file, preprocessed_file):
    """
    Preprocess data - strip \n and remove blank/private/notfound friend lists,
    add delimiters, and add default color and distance.

    Inputs: input_file
    Returns: no explicit return; writes to preprocessed_file.
    """
    with open(input_file) as i, open(preprocessed_file, 'w+') as p:
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


def write_results(preprocessed_file, paths_file, start_node):
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
    print('in write_results')
    flag = False
    with open(preprocessed_file) as f, open(paths_file, 'a') as p:
        for line in f:
            line = line.strip('\n')
            fields = line.split('|')
            degrees = int(fields[-3])
            end_node = str(fields[0])
            print(start_node, end_node, degrees)
            if degrees < 9999:
                print('Start:', start_node)
                print('End:', end_node)
                print("The path from '{0}' to '{1}' is {2}, the distance is {3}.".format(start_node, end_node, \
                    '->'.join(fields[-2].split()) + '->' + end_node, fields[-3]))
                outStr = '|'.join([start_node, end_node, str(degrees)])
                p.write(outStr)
                p.write('\n')


def main():
    """
    Iterate through every pair of nodes to find distances.
    Find the node with the minimum eccentricity.
    """
    input_file = './data/friends-000______small.txt'
    preprocessed_file = './results/preprocessed.txt'
    paths_file = './results/paths.txt'
    min_file = './results/min.txt'

    preprocess_data(input_file, preprocessed_file)

    N = 10
    nodes = 900
    start_nodes = map(str, range(100, 100+nodes))

    for start_node in start_nodes:
        print(start_node)
        # use '0' as an end node because an end node is required to run MRBFS
        args = "--start_node '{0}' --end_node '{1}' {2} --output = ./results".format(start_node, '0', preprocessed_file)
        mr_job = MRBFS(args=args.split())

        for i in range(N):
            with mr_job.make_runner() as runner:
                runner.run()
            os.system('cat results/* > {0}'.format(preprocessed_file))
        
        write_results(preprocessed_file, paths_file, start_node)

    # mr_job = MRMinEccentricity(args=[paths_file, min_file])
    # with mr_job.make_runner() as runner:
    #     runner.run()

if __name__== "__main__":
    main()
