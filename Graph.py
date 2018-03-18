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

	lotX = None
	lotY = None
	lotZ = None

	def __init__(self, nodz, nodzToNode):
		super(InitialNode, self).__init__(NodeType.init, nodz, nodzToNode)

		self.lotX = 0
		self.lotY = 0
		self.lotZ = 0

class TranslateNode(Node):

	translateX = None
	translateY = None
	translateZ = None

	def __init__(self, nodz, nodzToNode):
		super(TranslateNode, self).__init__(NodeType.translate, nodz, nodzToNode)

		self.translateX = 0
		self.translateY = 0
		self.translateZ = 0

class RotateNode(Node):

	rotateX = None
	rotateY = None
	rotateZ = None

	def __init__(self, nodz, nodzToNode):
		super(RotateNode, self).__init__(NodeType.rotate, nodz, nodzToNode)

		self.rotateX = 0
		self.rotateY = 0
		self.rotateZ = 0

class ScaleNode(Node):

	scaleX = None
	scaleY = None
	scaleZ = None

	def __init__(self, nodz, nodzToNode):
		super(ScaleNode, self).__init__(NodeType.scale, nodz, nodzToNode)

		self.scaleX = 0
		self.scaleY = 0
		self.scaleZ = 0

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

	def printGraph(self):
		queue = [self.root]

		while len(queue) > 0:
			curr = queue.pop()

			for child in curr.children:
				print curr.nodzNode.name + " -> " + child.nodzNode.name

				attrsParent = vars(curr)
				attrsChild = vars(child)

				print ', '.join("%s: %s" % item for item in attrsParent.items()), "\n"
				print ', '.join("%s: %s" % item for item in attrsChild.items())

				queue.append(child)

				print ""


	def generateMesh(self):
		# First delete all the existing geometry in the scene
		transforms = cmds.ls(tr=True)
		polyMeshes = cmds.filterExpand(transforms, sm=12)
		cmds.select(polyMeshes, r=True)
		cmds.delete()

		self.printGraph()

		# Now generate the mesh from the tree
		cmds.polyCube( sx=10, sy=15, sz=5, h=20 )



