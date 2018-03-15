import numpy

class NodeType(object):
	translateNode = 0
	rotateNode = 1
	scaleNode = 2
	initNode = 3

	@staticmethod
	def getString(nodeType):
		if nodeType == 0:
			return "Translate"
		if nodeType == 1:
			return "Rotate"
		if nodeType == 2:
			return "Scale"
		if nodeType == 3:
			return "Initial"

class Node(object):

	translate = None
	scale = None
	rotate = None

	nodeType = None
	children = None

	nodzNode = None

	def __init__(self, nodeType, nodz):
		self.translate = numpy.array([0,0,0])
		self.scale = numpy.array([0,0,0])
		self.rotate = numpy.array([0,0,0])
		self.nodeType = nodeType
		self.children = []

		self.nodzNode = nodz.createNode(name=NodeType.getString(nodeType), preset='node_preset_1', position=None)
		nodz.createAttribute(node=self.nodzNode, name='Aattr1', index=-1, preset='attr_preset_1',
                     plug=True, socket=False, dataType=str)


class DerivationTree(object):

	root = None
	nodz = None

	def __init__(self, nodz):
		self.root = Node(NodeType.initNode, nodz)
