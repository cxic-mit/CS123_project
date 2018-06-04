import sys
import os
from MRBFS import MRBFS

def preprocess_data(input_file, output_file):
    """
    Preprocess data - strip \n and remove blank/private/notfound friend lists,
    add delimiters, and add default color and distance.

    Inputs: input_file
    Returns: no explicit return; writes to preprocessed_file.
    """
    print('preprocessing data!')
    with open(output_file, 'w') as out, open(input_file) as f:
        for line in f:
            line = line.strip('\n')
            fields = line.split(':')
            if '' not in fields and 'private' not in fields \
            and 'notfound' not in fields:
                userID = fields[0]
                connections = fields[1].split(',')
                path = ''
                color = 'white'
                distance = 9999
                edges = ','.join(connections)
                outStr = '|'.join([userID, edges, str(distance), path, color])
                out.write(outStr)
                out.write("\n")
    f.close()
    out.close()


def run_mrjob(mr_job, N, output_file):
    """
    Run MRBFS
    """
    for i in range(N):
        with mr_job.make_runner() as runner:
            print('running mrjob:', i)
            runner.run()
        os.system('cat results/* > {0}'.format(output_file))


def find_path(start_node, end_node, N, output_file):
    """
    Print path between start_node and end_node if there is one.
    Otherwise, print 'cannot find path' message.
    """
    with open(output_file) as f:
        for line in f:
            line = line.strip('\n')
            fields = line.split('|')
            if str(fields[0]) == end_node and int(fields[-3]) < 9999:
                distance = int(fields[-3])
                print('The path from {0} to {1} is {2}, the distance is {3}'.format(start_node, end_node, \
                    '->'.join(fields[-2].split()) + '->' + str(end_node), distance))
                path_string = ','.join([str(start_node), str(end_node), str(distance)])
                return path_string

    print('Cannot find the path from {0} to {1} within {2} degree'.format(start_node, end_node, N))


def main(start_node,
         end_node,
         N=10,
         input_file='./data/friends-000______small.txt',
         output_file='results/preprocess_data.txt'):
    """
    Main method; calls other methods.

    Inputs:
        start_node: starting user
        end_node: ending user
        N: number of BFS iterations
        input_file: all user data
        output_file: paths from the start_node to all nodes
    Returns:
        Returns path and also prints the path or cannot find path.
    """
    args = '--start_node {0} --end_node {1} {2} --output=results'.format(start_node, end_node, output_file)
    mr_job = MRBFS(args=args.split())
    preprocess_data(input_file, output_file)
    run_mrjob(mr_job, N, output_file)
    path_string = find_path(start_node, end_node, N, output_file)
    return path_string


if __name__== "__main__":
    start_node = str(sys.argv[1])
    end_node = str(sys.argv[2])

    main(start_node,
         end_node,
         N = 10,
         input_file = './data/friends-000______small.txt',
         output_file = 'results/preprocess_data.txt')

# os.system('rm {0}'.format(output_file_0))
# os.system('rm -r ./__pycache__'.format(output_file_0))
# os.system('rm -r results')