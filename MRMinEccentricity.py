from mrjob.job import MRJob
from mrjob.step import MRStep

class MRMinEccentricity(MRJob):

	def mapper(self, _, line):
	    fields = line.split('|')
	    node = int(fields[0])
	    distance = int(fields[2])
	    yield node, distance

	def combiner(self, node, distances):
		max_distance = 0

		for i in distances:
			if i > max_distance:
				max_distance = i

		yield node, max_distance

	def reducer_max_distances(self, node, distances):
		max_distance = 0

		for i in distances:
			if i > max_distance:
				max_distance = i

		yield node, max_distance

	def reducer_init(self):
	    self.min_eccentricity = 10000
	    self.min_eccentricity_node = None
	  
	def reducer(self, node, max_distance):
		max_dist = list(max_distance)
		if self.min_eccentricity > max_dist[0]:
			self.min_eccentricity = max_dist[0]
			self.min_eccentricity_node = node

	def reducer_min_eccentricity(self):
		yield self.min_eccentricity_node, self.min_eccentricity

	def steps(self):
		return [
	      MRStep(mapper=self.mapper,
	             combiner=self.combiner,
	             reducer=self.reducer_max_distances),
	      MRStep(reducer_init=self.reducer_init,
	      		 reducer=self.reducer,
	      		 reducer_final=self.reducer_min_eccentricity)
	    ]

if __name__ == '__main__':
	MRMinEccentricity.run()