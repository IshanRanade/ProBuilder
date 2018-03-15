import numpy

class NodeType(object):
	translate = 0
	rotate = 1
	scale = 2
	init = 3
	split = 4

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
		if nodeType == 4:
			return "Split"

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
                     plug=True, socket=True, dataType=str)

	def addChild(self, nodeType, nodz):
		newChild = nodz.createNode(name=NodeType.getString(nodeType), preset='node_preset_1', position=None)
		nodz.createAttribute(node=newChild, name='Aattr1', index=-1, preset='attr_preset_1',
                     plug=True, socket=True, dataType=str)


		nodz.createConnection(newChild, 'Aattr1', self.nodzNode, 'Aattr1')

		self.children.append(newChild)


class DerivationTree(object):

	root = None
	nodz = None

	def __init__(self, nodz):
		self.root = Node(NodeType.init, nodz)
