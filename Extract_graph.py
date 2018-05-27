from mrjob.job import MRJob
import re

def read_line(line):
    user, friends_str = line.split(':')
    friends = friends_str.split(',')
    return user, friends


class Extract_graph(MRJob):
    
    def mapper_init(self):
        # with open("friends-000.txt", "r") as f:  
        # with open("data_0-10000.txt", "r") as f:
        with open("community2.txt", "r") as f:
            community = f.readlines() 
            self.community = community[0].split(",")


    def mapper(self, _, line):

        user, friends = read_line(line)

        if friends != ['private'] and \
           friends != ['notfound'] and \
           friends != ['']:
    
            for member in self.community:
                if member == user:
                    for friend in friends:
                        if friend in self.community:
                            yield member, friend
    

    def reducer(self, member, friend): 
        yield member, list(friend)


if __name__ == '__main__':
    Extract_graph.run()