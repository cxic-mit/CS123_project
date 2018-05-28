import numpy as np
from mrjob.job import MRJob
import re
from numpy import linalg as LA


def read_line(line):
    user, friends_str = line.split(':')
    friends = friends_str.split(',')
    return user, friends


class Eigenvector_centrality(MRJob):

    def mapper_init(self):

        with open("data_200-500.txt", "r") as f:
            self.data = f.readlines()


    def mapper(self, _, line):

        center, community = line.split('\t')
        center = center.strip('""')

        community = community.strip('[]').split(',')
        n = len(community)

        a_matrix = np.zeros(shape = (n,n))   

        for member in community:

            for line in self.data:
                user, friends = read_line(line)
                
                if friends != ['private\n'] and \
                   friends != ['notfound\n'] and \
                   friends != ['\n']:

                   for i in range(n):
                    if community[i] == user:
                        for j in range(n):
                            if community[j] in friends:
                                a_matrix[i, j] = 1

        w, v = LA.eig(a_matrix)
        w = list(w)
        max_index = w.index(max(w))
                     
        for i in range(n):
            eigenvector = round(v[max_index][i], 4)
            # eigenvector_centrality = v[max_index][i].real
            eigenvector_centrality = eigenvector.real

            yield center, (community[i], eigenvector_centrality)
                

    def reducer(self, center, eigenvector_tuple): 
        yield center, list(eigenvector_tuple)


if __name__ == '__main__':
    Eigenvector_centrality.run()