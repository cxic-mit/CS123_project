from mrjob.job import MRJob
import itertools
from heapq import nlargest
import time

TOP_N = 5 #to reduce the file size

class FriendsRecommender(MRJob):
    def mapper(self, _, line):
        '''
    Create potential friend pair permutations.
        Input: each line is a person followed by list of the person's friends
               e.g. '104:101,1143,628701,2438054'
        Output: yield (user1, user2), mutualFriend

        '''
        user, friends_str = line.split(':')
        friends = friends_str.split(',')
        if friends == 'private' or friends == 'notfound':
            return

        pairs = list(itertools.permutations(friends, 2))
        for pair in pairs:
            yield pair, user

    def combiner(self, pair, friends):
        '''
        Count the number of mutual friends.
        Input: key-value pair representing two people and their friend in common
               e.g. (user1, user2), mutualFriend
        Output: key-value pair with unique key representing two people and all friends in common
                e.g. user1, (user2, [mutualFriend1, mutualFriend2, ...])
        '''
        if friends:
            count = 0
            for f in friends:
                count += 1
            yield pair[0], (pair[1], count)

    def reducer_init(self):
        self.dict = {}

    def reducer(self, user, friends):
        '''
        Get the TOP N recommendations for user.
        Input: key is user, values is potential friends - each tuple is a potential friend,
               the number of mutual friends they have, and the list of mutual friends that they have
               e.g. user1, [(user2, numberOFMutualFriends, [mutualFriend1, mutualFriend2, ...]),
                            (user3, numberOFMutualFriends, [mutualFriend1, mutualFriend4, ...]), ...]
        Output: ranked list of TOP_N potential friends
        '''
        if friends:
            self.dict[user] = nlargest(TOP_N, friends, key = lambda e:e[1])

    def reducer_final(self):
        for user, friend_list in self.dict.items():
            friend_list.sort(reverse = True)
            yield str(user), list(friend_list)

if __name__ == '__main__':
    FriendsRecommender.run()
