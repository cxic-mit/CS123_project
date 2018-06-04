import sys
import run_MRBFS


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


def main(node_start, node_end, range_start, range_end):
    """
    Iterate through every pair of nodes to find distances.
    Find the node with the minimum eccentricity.
    """
    input_file = './data/friends-000______small.txt'
    output_file = './results/paths.txt'

    good_nodes = get_good_nodes(input_file)
    start = good_nodes[node_start:node_end]
    end = good_nodes[range_start:range_end]

    for i in start:
        for j in end:
            if i != j:
                print('Searching for the shortest path from {} to {}...'.format(i, j))
                line = run_MRBFS.main(i, j)
                if line:
                    print('Found path! start|end|distance:', line)
                    with open(output_file, 'a') as f:
                        f.write(line)
                        f.write('\n')


if __name__ == "__main__":
    node_start = int(sys.argv[1])
    node_end = int(sys.argv[2])
    range_start = int(sys.argv[3])
    range_end = int(sys.argv[4])
    print('Node start:', node_start, 'Node end:', node_end)
    print('Range start:', range_start, 'Range end:', range_end)
    main(node_start, node_end, range_start, range_end)