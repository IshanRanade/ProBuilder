from Qt import QtCore, QtWidgets
import nodz_main
from DerivationTree import NodeType
from DerivationTree import Node
from GUI import GUI
from Controller import Controller


######################################################################
# Test signals
######################################################################

# Nodes
@QtCore.Slot(str)
def on_nodeCreated(nodeName):
    print 'node created : ', nodeName

@QtCore.Slot(str)
def on_nodeDeleted(nodeName):
    print 'node deleted : ', nodeName

@QtCore.Slot(str, str)
def on_nodeEdited(nodeName, newName):
    print 'node edited : {0}, new name : {1}'.format(nodeName, newName)

#@QtCore.Slot(str)
def on_nodeSelected(node):

    currentSelectedNode = node

    if node is not None:
        gui.changeEditorWidgetLayout(nodzToNode[node].nodeType)
        gui.update()

        print 'node selected : ', node

# Graph
@QtCore.Slot()
def on_graphSaved():
    print 'graph saved !'

@QtCore.Slot()
def on_graphLoaded():
    print 'graph loaded !'

@QtCore.Slot()
def on_graphCleared():
    print 'graph cleared !'

@QtCore.Slot()
def on_graphEvaluated():
    print 'graph evaluated !'

# Other
@QtCore.Slot(object)
def on_keyPressed(key):
    print 'key pressed : ', key

try:
    app = QtWidgets.QApplication([])
except:
    # I guess we're running somewhere that already has a QApp created
    app = None

controller = Controller()

nodzToNode = {}
currentSelectedNode = None

nodz = nodz_main.Nodz(None)
nodz.initialize()
nodz.show()

nodz.signal_NodeSelected.connect(on_nodeSelected)
nodz.signal_KeyPressed.connect(on_keyPressed)


root = Node(NodeType.init, nodz, nodzToNode)
root.addChild(NodeType.translate, nodz, nodzToNode)

gui = GUI(NodeType.init, nodz)
gui.show()


if app:
    # command line stand alone test... run our own event loop
    app.exec_()
