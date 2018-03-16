import numpy
import maya.cmds as cmds
import maya.mel as mel

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

	nodeType = None
	children = None

	nodzNode = None

	def __init__(self, nodeType, nodz, nodzToNode):
		self.nodeType = nodeType
		self.children = []

		self.nodzNode = nodz.createNode(name=NodeType.getString(nodeType), preset='node_preset_1', position=None)
		nodz.createAttribute(node=self.nodzNode, name='Aattr1', index=-1, preset='attr_preset_1', plug=True, socket=True, dataType=str)

		nodzToNode[self.nodzNode] = self

class InitialNode(Node):

	def __init__(self, nodz, nodzToNode):
		super(InitialNode, self).__init__(NodeType.init, nodz, nodzToNode)

class TranslateNode(Node):

	def __init__(self, nodz, nodzToNode):
		super(TranslateNode, self).__init__(NodeType.translate, nodz, nodzToNode)

class RotateNode(Node):

	def __init__(self, nodz, nodzToNode):
		super(RotateNode, self).__init__(NodeType.rotate, nodz, nodzToNode)

class ScaleNode(Node):

	def __init__(self, nodz, nodzToNode):
		super(ScaleNode, self).__init__(NodeType.scale, nodz, nodzToNode)

class SplitNode(Node):

	def __init__(self, nodz, nodzToNode):
		super(SplitNode, self).__init__(NodeType.split, nodz, nodzToNode)

class MeshNode(Node):

	def __init__(self, nodz, nodzToNode):
		super(MeshNode, self).__init__(NodeType.mesh, nodz, nodzToNode)


class Graph(object):

	root = None
	nodz = None
	nodes = None
	nodzToNode = None

	def __init__(self, nodz):
		self.nodzToNode = {}
		self.nodes = set()
		self.nodz = nodz
		self.root = InitialNode(self.nodz, self.nodzToNode)
		self.nodes.add(self.root)

	def getNodeFromNodz(self, nodzNode):
		return self.nodzToNode[nodzNode]

	def addNode(self, nodeType):
		if(nodeType == NodeType.translate):
			self.nodes.add(TranslateNode(self.nodz, self.nodzToNode))
		elif(nodeType == NodeType.rotate):
			self.nodes.add(RotateNode(self.nodz, self.nodzToNode))
		elif(nodeType == NodeType.scale):
			self.nodes.add(ScaleNode(self.nodz, self.nodzToNode))
		elif(nodeType == NodeType.split):
			self.nodes.add(SplitNode(self.nodz, self.nodzToNode))
		elif(nodeType == NodeType.mesh):
			self.nodes.add(MeshNode(self.nodz, self.nodzToNode))

	def createEdge(self, srcNode, destNode):
		self.nodzToNode[srcNode].children.append(self.nodzToNode[destNode])

	def generateMesh(self):
		cmds.polyCube( sx=10, sy=15, sz=5, h=20 )



