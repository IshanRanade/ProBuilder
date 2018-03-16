import nodz_main
from Graph import NodeType
from Graph import Node
from Graph import Graph
from GUI import GUI

class Controller(object):

	currentSelectedNode = None
	nodz = None
	gui = None
	graph = None

	def __init__(self):
		self.nodz = nodz_main.Nodz(None)
		self.nodz.initialize()
		self.nodz.show()

		self.graph = Graph(self.nodz)

		self.gui = GUI(NodeType.init, self.nodz, self)
		self.gui.show()

		self.nodz.signal_NodeSelected.connect(self.nodeSelected)
		self.nodz.signal_SocketConnected.connect(self.socketConnected)

	def nodeSelected(self, nodzNode):
		if nodzNode is not None:
			self.currentSelectedNode = self.graph.getNodeFromNodz(nodzNode)
			self.gui.changeEditorWidgetLayout(self.graph.getNodeFromNodz(nodzNode).nodeType)
			self.gui.update()
		else:
			self.currentSelectedNode = None

	def socketConnected(self, srcNode, srcPlugName, destNode, dstSocketName):
		self.graph.createEdge(srcNode, destNode)
		print 'connected src: "{0}" at "{1}" to dst: "{2}" at "{3}"'.format(srcNode, srcPlugName, destNode, dstSocketName)

	def addNode(self, nodeType):
		self.graph.addNode(nodeType)

	def generateMesh(self):
		self.graph.generateMesh()
