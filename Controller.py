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

		self.gui = GUI(NodeType.init, self)
		self.gui.show()

		self.nodz = self.gui.nodzWidget

		self.graph = Graph(self.nodz)

		self.nodz.signal_NodeSelected.connect(self.nodeSelected)
		self.nodz.signal_SocketConnected.connect(self.socketConnected)
		self.nodz.signal_NodeSelected.connect(self.populateGUIEditor)

	def nodeSelected(self, nodzNode):
		if nodzNode is not None:
			self.currentSelectedNode = self.graph.getNodeFromNodz(nodzNode)
			self.gui.changeEditorWidgetLayout(self.graph.getNodeFromNodz(nodzNode).nodeType)
			self.gui.update()
		else:
			self.currentSelectedNode = None

	def socketConnected(self, srcNode, srcPlugName, destNode, dstSocketName):
		self.graph.createEdge(srcNode, destNode)

	def addNode(self, nodeType):
		self.graph.addNode(nodeType)

	def generateMesh(self):
		self.graph.generateMesh()

	def populateGUIEditor(self, nodzNode):
		if nodzNode is not None:
			node = self.graph.getNodeFromNodz(nodzNode)

			if node.nodeType == NodeType.init:
				self.gui.editorWidget.currentWidget().lotXLineEdit.setText(str(node.lotX))
				self.gui.editorWidget.currentWidget().lotYLineEdit.setText(str(node.lotY))
				self.gui.editorWidget.currentWidget().lotZLineEdit.setText(str(node.lotZ))
			if node.nodeType == NodeType.translate:
				self.gui.editorWidget.currentWidget().translateXLineEdit.setText(str(node.translateX))
				self.gui.editorWidget.currentWidget().translateYLineEdit.setText(str(node.translateY))
				self.gui.editorWidget.currentWidget().translateZLineEdit.setText(str(node.translateZ))
			if node.nodeType == NodeType.rotate:
				self.gui.editorWidget.currentWidget().rotateXLineEdit.setText(str(node.rotateX))
				self.gui.editorWidget.currentWidget().rotateYLineEdit.setText(str(node.rotateY))
				self.gui.editorWidget.currentWidget().rotateZLineEdit.setText(str(node.rotateZ))
			if node.nodeType == NodeType.scale:
				self.gui.editorWidget.currentWidget().scaleXLineEdit.setText(str(node.scaleX))
				self.gui.editorWidget.currentWidget().scaleYLineEdit.setText(str(node.scaleY))
				self.gui.editorWidget.currentWidget().scaleZLineEdit.setText(str(node.scaleZ))		

			self.gui.update()

