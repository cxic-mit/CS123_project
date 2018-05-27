# The output of this community is userA, [user_1,...user_50]
from mrjob.job import MRJob
import math



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


class find_comm(MRJob):

    def mapper_init(self):       
        with open("output_200-500_community.txt", "r") as f:  
    		data = f.readlines()

    def mapper(self, _, line):            
        for line in self.data:
            user_1, lst = read_line(line)
            comm = sorted(lst)[1:10]
            yield user, comm
    
    def reducer(self, user, comm):
        yield user, comm

if __name__ == '__main__':
    Get_pairs_distance.run()