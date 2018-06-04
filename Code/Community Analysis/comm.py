# The output of this community is user1, [(user_1, dist1),...(user_50, dist50)]
# This file takes in the output file from Get_pairs_distance.py and returns
# the 50 users within the community along with their distances to the user1
from mrjob.job import MRJob
import math


def read_line(line):
# This function reads in each line of the input file from Get_pairs_distance.py
# and returns each userN, and a list of other users and their distances
# to userN
    cnt=0
    line = re.findall(r"[-+]?\d*\.\d+|\d+", line)
    user_1 = line[0]
    lst = []
    
    for i in range(1,len(line)-1):
        cnt+=1
        if cnt%2==1:
            user_2 = line[i]
            distance = line[i+1]
            lst.append((user_2, distance))
    for i in range(len(lst)):
        lst[i]=(int(lst[i][0]),float(lst[i][1]))        
    
    return user_1, lst


class find_comm(MRJob):
# This mapreduce function returns each user and his corresponding friends community
# of size 50
    def mapper(self, _, line):
        ppl = []                   
        user, lst = read_line(line)       
        comm = sorted(lst,key=itemgetter(1))[:50]       
        yield user, comm
    
    def reducer(self, user, ppl):
        yield user, comm

if __name__ == '__main__':
    find_comm.run()