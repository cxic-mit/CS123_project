from mrjob.job import MRJob
import itertools
import heapq

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
        friends_list = list(friends)
        yield pair[0], (pair[1], len(friends_list), friends)

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
                e.g. user1, [(user2, largestNumberOFMutualFriends, [mutualFriend1, mutualFriend2, ...]),
                            (user3, secondLargestNumberOFMutualFriends, [mutualFriend1, ...]), ...]
        '''
        if friends:
            h = [(0, "") for i in range(TOP_N)]
            heapq.heapify(h)
            for f in friends:
                min_num, min_name = h[0]
                name, num_mu_friend, _ = f
                if num_mu_friend > min_num:
                    heapq.heapreplace(h, (num_mu_friend, name))
            self.dict[user] = h

    def reducer_final(self):
        for user, friend_list in self.dict.items():
            friend_list.sort(reverse = True)
            yield user, list(friend_list)

if __name__ == '__main__':
    FriendsRecommender.run()
