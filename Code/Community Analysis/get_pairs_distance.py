### Using MapReduce to get the distance between each pair of users
### Input: the friendster data, whose format is like "202: 203, 205, 208"
### Output: "202"   [["202", 0.0], ["203", 3.7416573867739413], 
###                  ["205", 3.605551275463989], ["208", 4.242640687119285]]

from mrjob.job import MRJob
import math

# Read and preprocess data's format
def read_line(line):
    user, friends_str = line.split(':')
    friends = friends_str.split(',')
    return user, friends

# Approximate the distance of each pair of by calculating the Euclidean 
# distance of the adjacency vector for each user
def calculate_distance(user_1, user_2):
    union = len(set(user_1) | set(user_2))
    intersect = len(set(user_1) & set(user_2))
    distance = math.sqrt(union - intersect)
    return distance


class Get_pairs_distance(MRJob):

    def mapper_init(self):
        # Input a copy of the data 
        # (can be accordingly changed to other larger or smaller data files)
        # with open("data_200-500.txt", "r") as f:
        # with open("data_1000-2000.txt", "r") as f:
        with open("data_10000-20000.txt", "r") as f:
            self.data = f.readlines()


    def mapper(self, _, line):
        user, friends = read_line(line)
        
        # Skip the users who have no information about their friends
        if friends != ['private'] and \
           friends != ['notfound'] and \
           friends != ['']:

            for line in self.data:
                another_user, another_friends = read_line(line)
                
                if another_friends != ['private\n'] and \
                   another_friends != ['notfound\n'] and \
                   another_friends != ['\n']:
                
                    another_friends[-1] = another_friends[-1].strip('\n')
                    distance = calculate_distance(friends, another_friends)
                    yield user, (another_user, distance)

    
    def reducer(self, user, distance): 
        yield user, list(distance)


if __name__ == '__main__':
    Get_pairs_distance.run()