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

		root = Node(NodeType.init, self.nodz, self.nodzToNode)
		root.addChild(NodeType.translate, self.nodz, self.nodzToNode)

		gui = GUI(NodeType.init, self.nodz)
		gui.show()

	def nodeSelected(self, node):
		self.currentSelectedNode = node

		if self.node is not None:
			self.gui.changeEditorWidgetLayout(self.nodzToNode[node].nodeType)
			self.gui.update()

			print 'node selected : ', node
