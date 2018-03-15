import numpy

class NodeType(object):
	translate = 0
	rotate = 1
	scale = 2
	init = 3
	split = 4
	mesh = 5

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
		if nodeType == 5:
			return "Mesh"

class Node(object):

	translate = None
	scale = None
	rotate = None

	nodeType = None
	children = None

	nodzNode = None

	def __init__(self, nodeType, nodz, nodzToNode):
		self.translate = numpy.array([0,0,0])
		self.scale = numpy.array([0,0,0])
		self.rotate = numpy.array([0,0,0])
		self.nodeType = nodeType
		self.children = []

		self.nodzNode = nodz.createNode(name=NodeType.getString(nodeType), preset='node_preset_1', position=None)
		nodz.createAttribute(node=self.nodzNode, name='Aattr1', index=-1, preset='attr_preset_1',
                     plug=True, socket=True, dataType=str)

		nodzToNode[self.nodzNode] = self

	def addChild(self, nodeType, nodz, nodzToNode):
		newChild = Node(nodeType, nodz, nodzToNode)
		nodz.createConnection(self.nodzNode, 'Aattr1', newChild.nodzNode, 'Aattr1')
		self.children.append(newChild)


class DerivationTree(object):

	root = None
	nodz = None

	def __init__(self, nodz, nodzToNode):
		self.root = Node(NodeType.init, nodz, nodzToNode)
