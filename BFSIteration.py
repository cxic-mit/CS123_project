from mrjob.job import MRJob
from mrjob.protocol import RawValueProtocol


# Define a class to handle nodes in a social network
class Node:
	
	'''
	ID: A unique number identifying a particular individual in the network
	connections: A list of IDs indicating the list of people this individual is connected to
	distance: A number indicating the number of connections between the individual and the a chosen person in the network
	color: An attribute indicating the status of a given node. A node can be white, gray, or black. If white (gray) {black}
	then the node has yet to be explored (should now be explored) {has already been explored}.

		
	'''
	
	def __init__(self):
		self.ID = ''
		self.connections = []
		self.distance = 9999
		self.color = 'WHITE'


	def getinfo(self, line):
		'''
		Read in pipe-deliminated info about a node. 
		Format is ID|CONNECTIONS|DISTANCE|COLOR where connections are in csv format.
		'''
		fields = line.split('|')
		if (len(fields) == 4):
			self.ID = fields[0]
			self.connections = fields[1].split(',')
			self.distance = int(fields[2])
			self.color = fields[3]

	def giveinfo(self):
		'''
		Return info in the same format that getinfo reads it in.
		'''
		connections = ','.join(self.connections)
		return '|'.join( (self.ID, connections, str(self.distance), self.color) )
		

class MRBFSIteration(MRJob):

	# Normal output for MRJob is in json. Since we're running a breadth-first-search iteratively on a dataset we need to return 
	# data in the format it was entered in for the next iteration to run properly.
	INPUT_PROTOCOL = RawValueProtocol
	OUTPUT_PROTOCOL = RawValueProtocol
	
	
	def configure_options(self):
		'''
		Set any configuration options for the map reduce job(s). In this case, we use add_passthrough_option to 
					  pass along the target person in the network.
		'''
		super(MRBFSIteration, self).configure_options()
		self.add_passthrough_option('--target', help="ID of character we are searching for")


	def mapper(self, _, line):
		'''
		Perform the breadth-first-search.
		'''
		
		node = Node()
		node.getinfo(line)

		if (node.color == 'GRAY'):
			for connection in node.connections:
				
				temp_node = Node()
				temp_node.ID = connection
				temp_node.distance = int(node.distance) + 1
				temp_node.color = 'GRAY'
				if (self.options.target == connection):
					print (temp_node.distance)
				yield connection, temp_node.giveinfo()

			# visited node
			node.color = 'BLACK'

		yield node.ID, node.giveinfo()


	def reducer(self, key, values):
		'''
		reducer: If the connection between the two specified nodes in the network is made in multiple different ways then this 
		method chooses the shortest path between the two.
		'''
		edges = []
		distance = 9999
		color = 'WHITE'

		for value in values:
			node = Node()
			node.getinfo(value)

			if (len(node.connections) > 0):
				edges.extend(node.connections)

			if (node.distance < distance):
				distance = node.distance

			if ( node.color == 'BLACK' ):
				color = 'BLACK'

			if ( node.color == 'GRAY' and color == 'WHITE' ):
				color = 'GRAY'

		node = Node()
		node.ID = key
		node.distance = distance
		node.color = color
		
        #Limit the number of edges to 500 here. You can remove the [:500] on a Linux cluster.
		node.connections = edges[:500]

		yield key, node.giveinfo()
		
		

if __name__ == '__main__':
	MRBFSIteration.run()
