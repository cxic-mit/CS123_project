### Using MapReduce to approximate Degree Centrality
### Input: the friendster data, whose format is"202: 203, 205, 208" and 
###        the communities constructed by “find_comm_50.py"
### Output: "202"   ["395", 0.0204] 
###         "203"   ["395", 0.0204]
###         "205"   ["395", 0.0204]
###         "208"   ["208", 0.0612]
### The outputs' meaning: for the community whose original center is "202",
### the person with the highest degree centrality is "395" and its degree 
### centrality is 0.0204; for the community whose original center is "203",
### the person with the highest degree centrality is "395" and its degree 
### centrality is 0.0204. 

from mrjob.job import MRJob
import re

# Read and preprocess data's format
def read_line(line):
    user, friends_str = line.split(':')
    friends = friends_str.split(',')
    return user, friends


class Degree_centrality(MRJob):
    
    def mapper_init(self):
        # Input the communities 
        # with open("user_200-500_community.txt", "r") as f:
        with open("user_10000-20000_community.txt", "r") as f:
            self.communities = f.readlines()


    def mapper(self, _, line):

        user, friends = read_line(line)

        if friends != ['private'] and \
           friends != ['notfound'] and \
           friends != ['']:
            
            # Loop over each community
            for comm in self.communities:

                center, community = comm.split('\t')
                center = center.strip('""')
                community = community.strip('[]\n').split(',')
                n = len(community)
                
                # Loop over each member in the community
                for member in community:
                    if member == user:

                        friend_ls = []
                        for friend in friends:
                            
                            if friend in community:
                                friend_ls.append(friend)
                        
                        # Count each member's number of friends, and normalize
                        degree_centrality = len(friend_ls) / (n-1)
 
                        yield center, (member, round(degree_centrality, 4))
    

    def reducer(self, center, degree_tuple): 
        degree_dict = {}
        
        # Store the input into a dictionary for the following selection
        for i in degree_tuple:
            member = i[0]
            centrality = i[1]
            degree_dict[member] = centrality
        
        # The member with the largest number of friends is the most central
        most_important = max(degree_dict, key = degree_dict.get)

        yield center, (most_important, degree_dict[most_important])


if __name__ == '__main__':
    Degree_centrality.run()