import numpy as np
from mrjob.job import MRJob
import re

def construct_distance_dict(data):
    user_dict = {}

    for line in data:
        cnt=0
        line = re.findall(r"[-+]?\d*\.\d+|\d+", line)
        user_1 = line[0]
        distance_dict = {}
        
        for i in range(1,len(line)-1):
            cnt+=1
            if cnt%2==1:
                user_2 = line[i]
                distance = line[i+1]
            
            distance_dict[user_2] = distance

        user_dict[user_1] = distance_dict

    return user_dict


class Closeness_centrality(MRJob):

    def mapper_init(self):

        # with open("output_distance_0-10000.txt", "r") as f: 
        with open("output_distance_200-500.txt", "r") as f:   
            data = f.readlines()

        self.distance_dict = construct_distance_dict(data)


    def mapper(self, _, line):

        center, community = line.split('\t')
        center = center.strip('""')

        community = community.strip('[]').split(',')
        n = len(community)

        for member in community:
            member_dict = self.distance_dict[member]
            closeness = 0.0

            for member_copy in community:

                closeness += float(member_dict[member_copy])
            
            closeness_centrality = (n-1) / closeness

            yield center, (member, round(closeness_centrality, 4)) 

   
    def reducer(self, center, closeness_tuple): 
        
        closeness_dict = {}

        for i in closeness_tuple:
            member = i[0]
            centrality = i[1]
            closeness_dict[member] = centrality

        most_important = min(closeness_dict, key = closeness_dict.get)

        yield center, (most_important, closeness_dict[most_important])


if __name__ == '__main__':
    Closeness_centrality.run()
