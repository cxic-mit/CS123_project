# We define most well connected person as the node with the minimum eccentricity,
# a.k.a. the radius of the largest connected component of the network.
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


def write_results(preprocessed_file, paths_file, START_NODE, END_NODE, N):
    """
    Find paths and write viable path distance to an output file.
    Inputs:
        preprocessed_file: input file
        paths_file: output file
        START_NODE
        END_NODE
        N: degrees limitation
    Returns: no explicit return; writes to paths_file.
    """
    flag = False
    with open(preprocessed_file) as f, open(paths_file, 'w+') as out:
        for line in f:
            line = line.strip('\n')
            fields = line.split('|')
            if str(fields[0]) == END_NODE and int(fields[-3]) < 9999:
                flag = True
                print("The path from '{0}' to '{1}' is {2}, the distance is {3}.".format(START_NODE, END_NODE, \
                    '->'.join(fields[-2].split()) + '->' + str(END_NODE), fields[-3]))
                out.write(',' .join(START_NODE, END_NODE, fields[-3]))

    if not flag:
        print("Cannot find the path from '{0}' to '{1}' within {2} degrees.".format(START_NODE, END_NODE, N))


def main():
    """
    Iterate through every pair of nodes to find distances.
    Find the "most well connected" person, a.k.a. the graph radius.
    """
    input_file = './data/friends-000______small.txt'
    preprocessed_file = './results/preprocessed.txt'
    paths_file = './results/paths.txt'
    min_file = './results/min.txt'

    preprocess_data(input_file, preprocessed_file)

    N = 10
    START_NODE = 146 # currently trying to use just 1 start node and 10 end nodes
    nodes = 10
    end_nodes = range(START_NODE+1, START_NODE+nodes+1)

    for END_NODE in end_nodes:
        args = "--start_node '{0}' --end_node '{1}' {2} --output = ./results".format(START_NODE, END_NODE, preprocessed_file)
        print('Args:', args)
        print('Output file:', preprocessed_file)
        mr_job = MRBFS(args=args.split())

        for i in range(N):
            with mr_job.make_runner() as runner:
                runner.run()
        
        write_results(preprocessed_file, paths_file, str(START_NODE), str(END_NODE), N)

    # mr_job = MRMinEccentricity(args=[paths_file, min_file])
    # with mr_job.make_runner() as runner:
    #     runner.run()


if __name__== "__main__":
    main()
