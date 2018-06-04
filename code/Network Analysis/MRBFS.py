from mrjob.job import MRJob
from mrjob.protocol import RawValueProtocol
import sys

class Node:
	'''
	A node class for BFS in mapreduce
	'''

	def __init__(self):
		self.nodeID = ''
		self.children = []
		self.path = []
		self.distance = sys.maxsize
		self.color = 'white'

	def read_input(self, line):
		'''
		Read a graph file and store the values to a node
		'''
		record = line.split('|')
		if (len(record) == 5):
			self.nodeID = record[0]
			self.children = record[1].split(',')
			self.distance = int(record[2])
			if record[3]:
				self.path = record[3].split(' ')
			else:
				self.path = []
			self.color = record[4]

	def get_val(self):
		'''
		Get the information in a node
		'''
		children = ','.join(self.children)
		if self.path:
			path = ' '.join(self.path)
		else:
			path = ''

		return '|'.join([self.nodeID, children, str(self.distance), \
						path, self.color])


class MRBFS(MRJob):

	INPUT_PROTOCOL = RawValueProtocol
	OUTPUT_PROTOCOL = RawValueProtocol

	def configure_options(self):
		'''
		Configuration options
		'''
		super(MRBFS, self).configure_options()
		self.add_passthrough_option('--start_node', default='902', type=str, \
			help='starting node for finding shortest path')
		self.add_passthrough_option('--end_node', default='222', type=str, \
			help='end node for finding shortest path')
		self.add_passthrough_option('--max_edge', default=500, type=int, \
			help='max number of connections one can have')

	def mapper(self, _, line):
		'''
		Do the BFS algorithm in mapper
			yield: NodeID, NodeID | Children (null if we just expanded it) 
			| Distance | Path | Color
		'''
		node = Node()
		node.read_input(line)

		#initialize start node
		if str(self.options.start_node) == node.nodeID and node.color == 'white':
			node.color = 'gray'
			node.distance = 0
		#expand the node
		if node.color == 'gray':
			for child in node.children:
				child_node = Node()
				child_node.nodeID = child
				child_node.distance = node.distance + 1
				if node.path:
					child_node.path = []
					child_node.path.extend(node.path)
					child_node.path.append(node.nodeID)
				else:
					child_node.path = [node.nodeID]
				child_node.color = 'gray'
				yield child, child_node.get_val()
			node.color = 'black'
		yield node.nodeID, node.get_val()

	def reducer(self, key, value):
		'''
		Yield the shortest path and store the full list of children
			yield: NodeID, NodeID | Children (full list)| Distance (shortest)
			| Path (shortest) | Color (darkest)
		'''
		max_distance = sys.maxsize
		path = []
		node = Node()
		children = []
		color = 'white'

		for v in value:
			temp = Node()
			temp.read_input(v)

			# obtain a full list of children
			if len(temp.children) > 1:
				children = temp.children

			# save the minimum distance and corresponding path
			if temp.distance < max_distance:
				max_distance = temp.distance
				path = temp.path

			#save the darkest color

			if temp.color == 'black':
				color = 'black'

			if temp.color == 'gray' and color != 'black':
				color = 'gray'


		node.nodeID = key
		node.path = path
		node.distance = max_distance
		node.color = color
		node.children = children
		yield key, node.get_val()


if __name__ == '__main__':
	MRBFS.run()

