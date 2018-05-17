from mrjob.job import MRJob

def calculate_distance(user_1, user_2):
    union = len(set(user_1) | set(user_2))
    intersect = len(set(user_1) & set(user_2))
    return (union-intersect)


def read_lines(line):
    user, friends_str = line.split(':')
    friends = friends_str.split(',')
        
    if friends != ['private'] and \
        friends != ['notfound'] and \
        friends != ['']:

        return user, friends


class get_pairs_distance(MRJob):

    #def configure_options(self):
    #    super(get_pairs_distance, self).configure_options()
    #    self.add_file_option('--txt', help='small_data')
    
    def mapper(self, _, line):
        #fname = self.options.upload_files[0]
        user, friends_str = line.split(':')
        friends = friends_str.split(',')
        
        if friends != ['private'] and \
            friends != ['notfound'] and \
            friends != ['']:

            #data = open(fname, "r")
            data = open("small_data.txt", "r")
            for line in data:
                another_user, another_friends = read_lines(line)
                distance = calculate_distance(friends, another_friends)
                yield user, (another_user, distance)

    
    def reducer(self, user, distance): 
        yield user, list(distance)


if __name__ == '__main__':
    get_pairs_distance.run()