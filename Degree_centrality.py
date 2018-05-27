from mrjob.job import MRJob
import re

def read_line(line):
    user, friends_str = line.split(':')
    friends = friends_str.split(',')
    return user, friends


class Degree_centrality(MRJob):
    
    def mapper_init(self):

        with open("comm_50.txt", "r") as f:
            self.communities = f.readlines()

    def mapper(self, _, line):

        user, friends = read_line(line)

        if friends != ['private'] and \
           friends != ['notfound'] and \
           friends != ['']:

            for comm in self.communities:
                center, community = comm.split('\t')
                center = center.strip('""')
                community = community.strip('[]\n').split(',')
                
                for member in community:
                    if member == user:

                        friend_ls = []
                        for friend in friends:
                            
                            if friend in community:
                                friend_ls.append(friend)
 
                        yield center, (member, len(friend_ls))
    

    def reducer(self, center, friend_tuple): 

        yield center, list(friend_tuple)


if __name__ == '__main__':
    Degree_centrality.run()