import nodz_main
from DerivationTree import NodeType
from DerivationTree import Node
from GUI import GUI

class Controller(object):

	currentSelectedNode = None
	nodzToNode = None
	nodz = None
	root = None
	gui = None

	def __init__(self):
		self.nodz = nodz_main.Nodz(None)
		self.nodz.initialize()
		self.nodz.show()

		self.nodzToNode = {}

		self.root = Node(NodeType.init, self.nodz, self.nodzToNode)
		self.root.addChild(NodeType.translate, self.nodz, self.nodzToNode)

		self.gui = GUI(NodeType.init, self.nodz)
		self.gui.show()

		self.nodz.signal_NodeSelected.connect(self.nodeSelected)

	def nodeSelected(self, node):
		self.currentSelectedNode = node

		if node is not None:
			self.gui.changeEditorWidgetLayout(self.nodzToNode[node].nodeType)
			self.gui.update()
