from mrjob.job import MRJob
import itertools
TOP_N = 10

class FriendsRecommender(MRJob):
    def mapper(self, _, line):
        '''
        Compute the reversed index for each connection
        between the source.
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
        print(pair)
        yield pair[0], (pair[1], sum(friends), friends)

    def reducer(self, user, friends):
        '''
        Get the TOP N recommendations for user.
        Input: key is user, values is potential friends - each tuple is a potential friend,
               the number of mutual friends they have, and the list of mutual friends that they have
               e.g. user1, [(user2, numberOFMutualFriends, [mutualFriend1, mutualFriend2, ...]),
                            (user3, numberOFMutualFriends, [mutualFriend1, mutualFriend4, ...]), ...]
        Output: ranked list of TOP_N potential friends
                e.g. user1, [(user2, largestNumberOFMutualFriends, [mutualFriend1, mutualFriend2, ...]),
                            (user3, secondLargestNumberOFMutualFriends, [mutualFriend1, ...]), ...]
        '''
        yield user, friends.sort(key=lambda x: x[1])[:TOP_N]

if __name__ == '__main__':
    FriendsRecommender.run()
