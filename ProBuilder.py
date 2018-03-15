from Qt import QtCore, QtWidgets
import nodz_main
from DerivationTree import NodeType
from DerivationTree import Node
import AttributeEditor


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

@QtCore.Slot(str)
def on_nodeSelected(nodesName):

    global gui
    gui.changeWidget(NodeType.translate)

    print 'node selected : ', nodesName

@QtCore.Slot(str, object)
def on_nodeMoved(nodeName, nodePos):
    print 'node {0} moved to {1}'.format(nodeName, nodePos)

# Attrs
@QtCore.Slot(str, int)
def on_attrCreated(nodeName, attrId):
    print 'attr created : {0} at index : {1}'.format(nodeName, attrId)

@QtCore.Slot(str, int)
def on_attrDeleted(nodeName, attrId):
    print 'attr Deleted : {0} at old index : {1}'.format(nodeName, attrId)

@QtCore.Slot(str, int, int)
def on_attrEdited(nodeName, oldId, newId):
    print 'attr Edited : {0} at old index : {1}, new index : {2}'.format(nodeName, oldId, newId)

# Connections
@QtCore.Slot(str, str, str, str)
def on_connected(srcNodeName, srcPlugName, destNodeName, dstSocketName):
    print 'connected src: "{0}" at "{1}" to dst: "{2}" at "{3}"'.format(srcNodeName, srcPlugName, destNodeName, dstSocketName)

@QtCore.Slot(str, str, str, str)
def on_disconnected(srcNodeName, srcPlugName, destNodeName, dstSocketName):
    print 'disconnected src: "{0}" at "{1}" from dst: "{2}" at "{3}"'.format(srcNodeName, srcPlugName, destNodeName, dstSocketName)

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

nodz = nodz_main.Nodz(None)
# nodz.loadConfig(filePath='')
nodz.initialize()
nodz.show()


nodz.signal_NodeSelected.connect(on_nodeSelected)
nodz.signal_KeyPressed.connect(on_keyPressed)


root = Node(NodeType.init, nodz)
root.addChild(NodeType.translate, nodz)

gui = AttributeEditor.AttributeEditor(NodeType.init)
gui.show()


# Graph
print nodz.evaluateGraph()

if app:
    # command line stand alone test... run our own event loop
    app.exec_()
