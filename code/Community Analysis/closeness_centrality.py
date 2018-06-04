### Using MapReduce to approximate Closeness Centrality
### Input: the communities (the center and the members) returned from 
###        “find_comm_50.py" and the distance for each pair of user returned
###        from "Get_pairs_distance.py"    
### Output: "202"   ["202", 0.2774]
###         "203"   ["203", 0.5774]
###         "205"   ["304", 0.7071]
###         "208"   ["208", 0.3792]
###         "209"   ["210", 0.1906]
### The outputs' meaning: for the community whose original center is "202",
### the person with the highest closeness centrality is "202" and its 
### closeness centrality is 0.2774; for the community with the center of 
### "203", the person with the highest degree centrality is "203" and its 
### closeness centrality is 0.5774.

import numpy as np
from mrjob.job import MRJob
import re

# Store the outputs from "Get_pairs_distance.py" in format of a dictionary
def construct_distance_dict(data):
    user_dict = {}

    for line in data:
        cnt = 0
        line = re.findall(r"[-+]?\d*\.\d+|\d+", line)
        user_1 = line[0]
        distance_dict = {}
        
        for i in range(1, len(line)-1):
            cnt += 1
            if cnt%2 == 1:
                user_2 = line[i]
                distance = line[i+1]
            
            distance_dict[user_2] = distance

        user_dict[user_1] = distance_dict

    return user_dict


class Closeness_centrality(MRJob):

    def mapper_init(self):
        
        # with open("output_distance_200-500.txt", "r") as f:  
        # with open("output_distance_1000-2000.txt", "r") as f: 
        with open("output_distance_10000-20000.txt", "r") as f: 
            data = f.readlines()

        self.distance_dict = construct_distance_dict(data)


    def mapper(self, _, line):

        center, community = line.split('\t')
        center = center.strip('""')

        community = community.strip('[]').split(',')
        n = len(community)
        
        # For each member in the community, compute its total distance to 
        # other members
        for member in community:

            if member in self.distance_dict:

                member_dict = self.distance_dict[member]
                closeness = 0.0

                for member_copy in community:

                    if member_copy in member_dict:

                        closeness += float(member_dict[member_copy])
            
                # Normalize the value of closeness centrality
                closeness_centrality = (n-1) / closeness

                yield center, (member, round(closeness_centrality, 4)) 

   
    def reducer(self, center, closeness_tuple): 
        
        closeness_dict = {}
        
        # Store the input into a dictionary for the following selection
        for i in closeness_tuple:
            member = i[0]
            centrality = i[1]
            closeness_dict[member] = centrality
        
        # The member with the shortest distance to other members in the 
        # community is the most "central"/"closest" person
        most_important = min(closeness_dict, key = closeness_dict.get)

        yield center, (most_important, closeness_dict[most_important])


if __name__ == '__main__':
    Closeness_centrality.run()