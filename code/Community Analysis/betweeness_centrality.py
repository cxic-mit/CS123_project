#read community file in 
#return the community and the person that has the highest betweenness
#score within the community

from mrjob.job import MRJob
from collections import defaultdict
import itertools

def read_line(line):
# This function reads in each line of the input file from the community file
# and returns each userN, and a list of other users that are within his community
    cnt=0
    line = re.findall(r"[-+]?\d*\.\d+|\d+", line)
    user_1 = line[0]
    lst = []
    
    for i in range(1,len(line)-1):       
        user_2 = line[i]
        lst.append(user_2)        
    return user_1, lst


class betweenness_centrality(MRJob):
# The mapreduce implementation maps each user and his community
# to the shortest paths of each users and returns the central 
# user within the community based on calculated betweenness score
# the format of lst is [(pr1, path1)...,(prN, pathN)]

    def mapper_init(self):
        with open("shortest_path.txt", "r") as f:
            self.data = f.readlines()

    def mapper(self, _, line):
        lst = []
        user_1, comm = read_line(line)
        pairs = list(itertools.permutations(comm, 2))
        for pr in pairs:
            for pair, path in self.data:
                if pr == pair:
                    shortest_path = path
                    lst.append((pr, shortest_path))

        yield comm, lst


    
    def reducer(self, comm, pr_path_lst):
        dict_score = {}
        dict_score = defaultdict(lambda: 0, dict_score)
        for i in pr_path_lst:
            for j in comm:           
                if j is in i[1] and j != i[1][-1]:
                    dict_score[j] += 1
        scale = (len(dict_score)-1)*(len(dict_score)-2)/2
        final_dict = {k: v / (len(comm) * scale) for k, v in dict_score.iteritems()}

        for key, value in sorted(final_dict.iteritems(), key=lambda (k,v): (v,k)):
            important_person = (key, value)       
        
        yield comm, important_person



if __name__ == '__main__':
    betweenness_centrality.run()
