### Using MapReduce to approximate Eigenvector Centrality
### Input: the friendster data, whose format is "202: 203, 205, 208" and 
###        the communities (the center and the members) returned from 
###        “find_comm_50.py"
### Output: "202"   ["395", 0.0204] 
###         "208"   ["208", 0.0612]
###         "209"   ["209", 0.5176]
###         "210"   ["209", 0.3858]
###         "211"   ["211", 0.5842]
### The outputs' meaning: for the community whose original center is "202",
### the person with the highest eigenvector centrality is "395" and its 
### eigenvector centrality is 0.0204; for the community with the center of 
### "208", the person with the highest eigenvector centrality is "208" and 
### its eigenvector centrality is 0.0612. 

import numpy as np
from mrjob.job import MRJob
import re
from numpy import linalg as LA


# Read and preprocess data's format
def read_line(line):
    user, friends_str = line.split(':')
    friends = friends_str.split(',')
    return user, friends


class Eigenvector_centrality(MRJob):

    def mapper_init(self):
        # Input a copy of the data 
        # (can be changed to other larger or smaller data files)
        # with open("data_200-500.txt", "r") as f:
        with open("data_1000-2000.txt", "r") as f:
        # with open("data_10000-20000.txt", "r") as f:
            self.data = f.readlines()


    def mapper(self, _, line):

        center, community = line.split('\t')
        center = center.strip('""')

        community = community.strip('[]').split(',')
        n = len(community)
        
        # Construct the adjacency matrix for each community
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
        
        # Compute the eigenvalue and eigenvector
        w, v = LA.eig(a_matrix)
        w = list(w)
        max_index = w.index(max(w))

        for i in range(n):
            eigenvector = round(v[max_index][i], 4)
            eigenvector_centrality = eigenvector.real

            yield center, (community[i], eigenvector_centrality)
                

    def reducer(self, center, eigenvector_tuple): 
        eigenvector_dict = {}
        
        # Store the inputs into a dictionary for the following selection
        for i in eigenvector_tuple:
            member = i[0]
            centrality = i[1]
            eigenvector_dict[member] = centrality
        
        # Select the largest eigenvalue and the corresponding eigenvector
        most_important = max(eigenvector_dict, key = eigenvector_dict.get)

        yield center, (most_important, eigenvector_dict[most_important])
        
        
if __name__ == '__main__':
    Eigenvector_centrality.run()