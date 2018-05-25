from mrjob.job import MRJob
import itertools
from heapq import nlargest

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
        if 'private' in friends or 'notfound' in friends:
            return

        pairs = list(itertools.permutations(friends, 2))
        for pair in pairs:
            yield str(pair[0]) + ' ' + str(pair[1]), user

    def combiner(self, pair, friends):
        '''
        Count the number of mutual friends.
        Input: key-value pair representing two people and their friend in common
               e.g. (user1, user2), mutualFriend
        Output: key-value pair with unique key representing two people and all friends in common
                e.g. user1, (user2, [mutualFriend1, mutualFriend2, ...])
        '''
        user1, user2 = pair.split(' ')
        if friends:
            count = 0
            for f in friends:
                count += 1
            yield user1, user2 + ' ' + str(count)

    def reducer(self, user, friends):
        '''
        Get the TOP N recommendations for user.
        Input: key is user, values is potential friends - each tuple is a potential friend
               and the number of mutual friends they have
               e.g. user1, [(user2, numberOFMutualFriends, [mutualFriend1, mutualFriend2, ...]),
                            (user3, numberOFMutualFriends, [mutualFriend1, mutualFriend4, ...]), ...]
        Output: ranked list of TOP_N potential friends
        '''
        if friends:
            yield user, nlargest(TOP_N, friends, key = lambda e:int(e.split(' ')[1]))


if __name__ == '__main__':
    FriendsRecommender.run()
