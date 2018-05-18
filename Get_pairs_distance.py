from mrjob.job import MRJob
import math

def calculate_distance(user_1, user_2):
    union = len(set(user_1) | set(user_2))
    intersect = len(set(user_1) & set(user_2))
    distance = math.sqrt(union - intersect)
    return distance


def read_line(line):
    user, friends_str = line.split(':')
    friends = friends_str.split(',')
    return user, friends


class Get_pairs_distance(MRJob):
    
    def mapper(self, _, line):
        user, friends = read_line(line)
        
        if friends != ['private'] and \
            friends != ['notfound'] and \
            friends != ['']:

            data = open("small_data.txt", "r")
            for line in data:
                another_user, another_friends = read_line(line)
                another_friends[-1] = another_friends[-1].strip('\n')
                distance = calculate_distance(friends, another_friends)
                yield user, (another_user, distance)

    
    def reducer(self, user, distance): 
        yield user, list(distance)


if __name__ == '__main__':
    Get_pairs_distance.run()
