from mrjob.job import MRJob

class MRMinEccentricity(MRJob):

	def mapper(self, _, line):
	    fields = ','.split(line)
	    yield None, int(field[2])
  
	def combiner_find_words(self, _, lens):
		yield None, min(lens)
  
	def reducer(self, _, lens):
		yield None, min(lens)

if __name__ == '__main__':
	MRMinEccentricity.run()