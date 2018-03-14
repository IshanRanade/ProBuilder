import numpy

class NodeType(object):
	translateNode = 0
	rotateNode = 1
	scaleNode = 2
	initNode = 3

class Node(object):

	translate = None
	scale = None
	rotate = None

	nodeType = None

	def __init__(self, nodeType):
		self.nodeType = nodeType
		self.translate = numpy.array([0,0,0])
		self.scale = numpy.array([0,0,0])
		self.rotate = numpy.array([0,0,0])


class DerivationTree(object):

	root = None

	def __init__(self):
		self.root = Node(NodeType.initNode)
