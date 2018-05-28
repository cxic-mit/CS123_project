#read community file in mapreduce

from mrjob.job import MRJob
from collections import defaultdict


def read_line(line):
    cnt=0
    line = re.findall(r"[-+]?\d*\.\d+|\d+", line)
    user_1 = line[0]
    lst = []
    
    for i in range(1,len(line)-1):
        cnt+=1
        if cnt%2==1:
            user_2 = line[i]
            lst.append(user_2, distance)        
    return user_1, lst


class betweeness_centrality(MRJob):
    
    def mapper_init(self):
        with open("shortest_path.txt", "r") as f:
            self.data = f.readlines()


    def mapper(self, _, line):
        lst = []
        user_1, comm = read_line(line)
        len_comm = len(comm)
        pairs = list(itertools.permutations(comm, 2))
        for pr in pairs:
            for pair, path in data:
                if pr == pair:
                    shortest_path = path
                    lst.append((pr, shortest_path))

        yield comm, lst


    # the format of lst is [(pr1, path1)...,(prN, pathN)]
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
    betweeness_centrality.run()

