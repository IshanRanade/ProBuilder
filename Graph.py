import numpy as np
import maya.cmds as cmds
import maya.mel as mel
import LinAlg

class NodeType(object):
	translate = 0
	rotate = 1
	scale = 2
	init = 3
	split = 4
	mesh = 5
	#NEW! 
	Split_Helper = 7

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
                #NEW!
		if nodeType == 7:
			return "Split_Helper"

class Node(object):

	nodeType = None
	children = None

	nodzNode = None
	nodz = None

	graph = None
	

	def __init__(self, nodeType, nodz, nodzToNode):
		self.nodeType = nodeType
		self.children = []
		self.nodz = nodz

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


        segment = None
        graphFather = None
        
        segmentsArray = []

	def __init__(self, nodz, nodzToNode):
		super(SplitNode, self).__init__(NodeType.split, nodz, nodzToNode)
		
		self.segment = 0
		self.segmentArray = []

	def add_split_attr(self, segmentNum):

                #Clear segment array
                self.segmentArray = []
                
                for x in range(0,segmentNum):
                    #self.segmentArray.append( self.nodz.createAttribute(node=self.nodzNode, name='Seg'+str(x), index=-1, preset='attr_preset_1', plug=True, socket=True, dataType=str) )
                    self.nodz.createAttribute(node=self.nodzNode, name='Seg'+str(x), index=-1, preset='attr_preset_1', plug=True, socket=False, dataType=str)

                    #new_nodz = None
                    #new_nodz = self.nodz.createNode(name='helper'+str(x), preset='node_preset_1', position=None)
                    
                    #self.nodz.createAttribute(node=new_nodz, name='proportion', index=-1, preset='attr_preset_1', plug=True, socket=True, dataType=str)

                    
                    
                    


class MeshNode(Node):

	def __init__(self, nodz, nodzToNode):
		super(MeshNode, self).__init__(NodeType.mesh, nodz, nodzToNode)

#New
class Split_Helper(Node):

        proportion = None

	def __init__(self, nodz, nodzToNode):
		super(Split_Helper, self).__init__(NodeType.Split_Helper, nodz, nodzToNode)

		self.proportion = 1


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
		newNode = None
		if(nodeType == NodeType.translate):
			newNode = TranslateNode(self.nodz, self.nodzToNode)
		elif(nodeType == NodeType.rotate):
			newNode = RotateNode(self.nodz, self.nodzToNode)
		elif(nodeType == NodeType.scale):
			newNode = ScaleNode(self.nodz, self.nodzToNode)
		#NEW
		elif(nodeType == NodeType.split):
			newNode = SplitNode(self.nodz, self.nodzToNode)
		#NEW	
		elif(nodeType == NodeType.Split_Helper):
			newNode = Split_Helper(self.nodz, self.nodzToNode)
			
		elif(nodeType == NodeType.mesh):
			newNode = MeshNode(self.nodz, self.nodzToNode)

		self.nodes.add(newNode)

		return newNode

	def createEdge(self, srcNodzNode, destNodzNode):
		self.nodzToNode[srcNodzNode].children.append(self.nodzToNode[destNodzNode])

	def createManualEdge(self, srcNode, destNode):
		srcNode.children.append(destNode)
		self.nodz.createConnection(srcNode.nodzNode, 'Aattr1', destNode.nodzNode, 'Aattr1')

	def printGraph(self):
		queue = [self.root]

		while len(queue) > 0:
			curr = queue.pop()

			for child in curr.children:
				print curr.nodzNode.name + " -> " + child.nodzNode.name

				attrsParent = vars(curr)
				attrsChild = vars(child)

				print ', '.join("%s: %s" % item for item in attrsParent.items())
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
		# cmds.polyCube()
		# cmds.move(10,10,10)
		# cmds.rotate(19,10,10)

		self.generateMeshHelper(self.root, np.array([0,0,0]), np.array([1,0,0,0]), np.array([1,1,1]))

	def generateMeshHelper(self, node, translate, rotate, scale):
		if node.nodeType == NodeType.translate:
			translate = np.add(translate, np.array([node.translateX, node.translateY, node.translateZ]))
		elif node.nodeType == NodeType.rotate:
			rotate = LinAlg.quaternion_multiply(rotate, LinAlg.quaternion_from_euler(node.rotateX, node.rotateY, node.rotateZ))
		elif node.nodeType == NodeType.scale:
			scale = np.multiply(scale, np.array([node.scaleX, node.scaleY, node.scaleZ]))
		elif node.nodeType == NodeType.mesh:

			ax, ay, az = LinAlg.euler_from_quaternion(rotate)

			cmds.polyCube()
			cmds.scale(scale[0], scale[1], scale[2])
			cmds.move(translate[0],translate[1],translate[2])
			cmds.rotate(ax,ay,az)

		elif node.nodeType == NodeType.init:
			pass
		elif node.nodeType == NodeType.split:
			pass

		for child in node.children:
			self.generateMeshHelper(child, np.array(translate), np.array(rotate), np.array(scale))




