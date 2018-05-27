# The output of this community is userA, [(user_1, dist1),...(user_50, dist50)]

from mrjob.job import MRJob
import math
import re
from operator import itemgetter

def read_line(line):
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

    def mapper(self, _, line):
        ppl = []                   
        user, lst = read_line(line)
        comm = sorted(lst,key=itemgetter(1))[:50]

        for i in comm:
            ppl.append(i[0])        
        yield user, ppl
    
    def reducer(self, user, ppl):
        yield user, ppl

if __name__ == '__main__':
    find_comm.run()
