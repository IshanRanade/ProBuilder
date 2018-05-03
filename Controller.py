from Graph import NodeType
from Graph import Graph
from GUI import GUI
from Qt import QtGui, QtCore, QtWidgets
import os
import json
import math


class Controller(object):

    currentSelectedNode = None
    currentSelectedAttribute = None
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
        self.nodz.signal_AttrSelected.connect(self.attributeSelected)

        self.gui.setWindowOpacity(0.8)
        
    def testGraph1(self):
        for key in self.graph.nodzToNode:
            key._remove()
            self.gui.nodzWidget.signal_NodeDeleted.emit([key])
            
        self.graph = None
        self.graph = Graph(self.nodz)

        self.currentSelectedNode = self.graph.root
        repeat = self.graph.addNode(NodeType.repeat)
        self.gui.setNextNodePosition(repeat, self.currentSelectedNode, None)
        self.graph.createManualEdge(self.currentSelectedNode, "Node", repeat, "Node")

        self.currentSelectedNode = repeat
        split1 = self.graph.addNode(NodeType.split)
        self.gui.setNextNodePosition(split1, self.currentSelectedNode, None)
        self.graph.createManualEdge(self.currentSelectedNode, "Node", split1, "Node")

        self.currentSelectedNode = split1
        self.setSplitValues(3, split1.segmentDirection)
        split1.segmentCount = 3

        split1.children[0].proportion = 1
        split1.children[1].proportion = 1
        split1.children[2].proportion = 1

        mesh1 = self.graph.addNode(NodeType.mesh)
        self.gui.setNextNodePosition(mesh1, self.currentSelectedNode, 0)
        self.graph.createManualEdge(self.currentSelectedNode, "Segment 0", mesh1, "Node")
        mesh1.parent = split1.children[0]

        mesh2 = self.graph.addNode(NodeType.mesh)
        self.gui.setNextNodePosition(mesh2, self.currentSelectedNode, 1)
        self.graph.createManualEdge(self.currentSelectedNode, "Segment 1", mesh2, "Node")
        mesh2.parent = split1.children[1]
        
        mesh3 = self.graph.addNode(NodeType.mesh)
        self.gui.setNextNodePosition(mesh3, self.currentSelectedNode, 2)
        self.graph.createManualEdge(self.currentSelectedNode, "Segment 2", mesh3, "Node")
        mesh3.parent = split1.children[2]

        self.currentSelectedNode = None

    def testGraph2(self):
        for key in self.graph.nodzToNode:
            key._remove()
            self.gui.nodzWidget.signal_NodeDeleted.emit([key])
            
        self.graph = None
        self.graph = Graph(self.nodz)
        # Create a test graph
        self.currentSelectedNode = self.graph.root
        translate1 = self.graph.addNode(NodeType.translate)
        self.gui.setNextNodePosition(translate1, self.currentSelectedNode, None)
        self.graph.createManualEdge(self.currentSelectedNode, "Node", translate1, "Node")

        self.currentSelectedNode = translate1
        split1 = self.graph.addNode(NodeType.split)
        self.gui.setNextNodePosition(split1, self.currentSelectedNode, None)
        self.graph.createManualEdge(self.currentSelectedNode, "Node", split1, "Node")

        self.currentSelectedNode = split1
        self.setSplitValues(3, split1.segmentDirection)
        split1.segmentCount = 3

        split1.children[0].proportion = 1
        split1.children[1].proportion = 4.0
        split1.children[2].proportion = 1

        mesh1 = self.graph.addNode(NodeType.mesh)
        self.gui.setNextNodePosition(mesh1, self.currentSelectedNode, 0)
        self.graph.createManualEdge(self.currentSelectedNode, "Segment 0", mesh1, "Node")
        mesh1.parent = split1.children[0]

        mesh2 = self.graph.addNode(NodeType.mesh)
        self.gui.setNextNodePosition(mesh2, self.currentSelectedNode, 1)
        self.graph.createManualEdge(self.currentSelectedNode, "Segment 1", mesh2, "Node")
        mesh2.parent = split1.children[1]
        
        mesh3 = self.graph.addNode(NodeType.mesh)
        self.gui.setNextNodePosition(mesh3, self.currentSelectedNode, 2)
        self.graph.createManualEdge(self.currentSelectedNode, "Segment 2", mesh3, "Node")
        mesh3.parent = split1.children[2]

        self.currentSelectedNode = None

    def deleteNode(self):
        currNode = self.currentSelectedNode

        if currNode is not None:

            self.gui.nodzWidget.signal_NodeDeleted.emit([currNode.nodzNode])
            currNode.nodzNode._remove()
            
            if currNode.parent is not None:
                currNode.parent.children.remove(currNode)
                self.graph.nodes.remove(currNode)
                self.graph.nodzToNode.pop(currNode.nodzNode)

    def deleteNodes(self):
        currNode = self.currentSelectedNode

        if currNode is not None:
            nodesToDelete = set()
            nodesToDelete.add(currNode)

            queue = [currNode]
            while len(queue) > 0:
                n = queue[0]
                del queue[0]

                for child in n.children:
                    nodesToDelete.add(child)
                    queue.append(child)

            for n in nodesToDelete:
                if n.nodzNode is not None:
                    self.gui.nodzWidget.signal_NodeDeleted.emit([n.nodzNode])
                    n.nodzNode._remove()
                    self.graph.nodzToNode.pop(n.nodzNode)

                if n.parent is not None:
                    n.parent.children.remove(n)
                
                self.graph.nodes.remove(n)
                    

    def nodeSelected(self, nodzNode):
        if nodzNode is not None:
            self.currentSelectedNode = self.graph.getNodeFromNodz(nodzNode)
            self.currentSelectedAttribute = None
            self.gui.changeEditorWidgetLayout(self.graph.getNodeFromNodz(nodzNode).nodeType)
            self.gui.update()
        else:
            self.currentSelectedNode = None
            self.currentSelectedAttribute = None
            self.gui.changeEditorWidgetLayout("Default")
            self.gui.update()
            return
            
        self.populateGUIEditor(self.graph.getNodeFromNodz(nodzNode))

    def attributeSelected(self, nodzNode, attributeNum):
        if self.graph.getNodeFromNodz(nodzNode).nodeType == NodeType.split:
            self.currentSelectedNode = self.graph.getNodeFromNodz(nodzNode)
            self.currentSelectedAttribute = attributeNum
            self.gui.changeEditorWidgetLayout("SplitSegment")
            self.gui.update()
            self.populateGUIEditor(self.graph.getNodeFromNodz(nodzNode).children[attributeNum])

    def socketConnected(self, srcNode, srcPlugName, destNode, dstSocketName):
        self.graph.createEdge(srcNode, srcPlugName, destNode, dstSocketName)

    def addNode(self, nodeType):
        newNode = self.graph.addNode(nodeType)
        self.gui.setNextNodePosition(newNode, self.currentSelectedNode, self.currentSelectedAttribute)

    def generateMesh(self):
        self.graph.generateMesh()

    def loadGraph(self, fileName=None):
        #fileName = QtWidgets.QFileDialog.getOpenFileName(None)
        fileName = 'D:\ProBuilder\ProBuilder\Graphs\graph1.json'

        JSON = json.load(open(fileName))

        nodeIndexToNode = {}

        queue = []
        queue.append((None, '0'))

        while len(queue) > 0:
            parentIdx, childIdx = queue[0]
            del queue[0]

            if parentIdx is not None:
                parentNode = nodeIndexToNode[parentIdx]
            childNode = None

            if childIdx not in nodeIndexToNode:
                if JSON[childIdx]["type"] != NodeType.init:
                    childNode = self.graph.addNode(JSON[childIdx]["type"])
                self.currentSelectedNode = childNode

                if JSON[childIdx]["type"] == NodeType.translate:
                    self.setTranslateValues(JSON[childIdx]["translateX"], JSON[childIdx]["translateY"], JSON[childIdx]["translateZ"])
                elif JSON[childIdx]["type"] == NodeType.rotate:
                    self.setRotateValues(JSON[childIdx]["rotateX"], JSON[childIdx]["rotateY"], JSON[childIdx]["rotateZ"])
                elif JSON[childIdx]["type"] == NodeType.scale:
                    self.setScaleValues(JSON[childIdx]["scaleX"], JSON[childIdx]["scaleY"], JSON[childIdx]["scaleZ"])
                elif JSON[childIdx]["type"] == NodeType.split:
                    self.setSplitValues(JSON[childIdx]["segmentCount"] )
                    self.setSplitDir(JSON[childIdx]["segmentDirection"])
                    for i in range(0, JSON[childIdx]["segmentCount"]):
                        childNode.children[i].proportion = JSON[str(JSON[childIdx]["children"][i])]["proportion"]
                elif JSON[childIdx]["type"] == NodeType.mesh:
                    childNode.filePath = JSON[childIdx]["meshFile"]

                    if(childNode.filePath != None):
                        childNode.isSet = True

                    
                elif JSON[childIdx]["type"] == NodeType.splitSegment:
                    childNode.idx = JSON[childIdx]["idx"]
                elif JSON[childIdx]["type"] == NodeType.repeat:
                    self.setRepeatDir(JSON[childIdx]["direction"])
                    self.setRepeatMax(JSON[childIdx]["count"])
                    self.setRepeatSize(JSON[childIdx]["percentage"])
                    
                elif JSON[childIdx]["type"] == NodeType.init:
                    self.currentSelectedNode = self.graph.root
                    self.deleteNodes()
                    self.graph = None
                    self.graph = Graph(self.nodz)
                    self.currentSelectedNode = self.graph.root
                    childNode = self.graph.root
                    self.setInitialValues(JSON[childIdx]["lotX"], JSON[childIdx]["lotY"], JSON[childIdx]["lotZ"])
            else:
                childNode = nodeIndexToNode[childIdx]
                self.currentSelectedNode = childNode

            if parentIdx is not None:
                if JSON[parentIdx]["type"] == NodeType.split:
                    childNode.parent = parentNode
                else:
                    childNode.nodzNode.setPos(QtCore.QPoint(JSON[childIdx]["nodzPosX"], JSON[childIdx]["nodzPosY"]))

                    if JSON[parentIdx]["type"] == NodeType.splitSegment:
                        self.graph.createManualEdge(parentNode.parent, "Segment " + str(parentNode.idx), childNode, "Node")
                    else:
                        self.graph.createManualEdge(parentNode, "Node", childNode, "Node")
            else:
                childNode.nodzNode.setPos(QtCore.QPoint(JSON[childIdx]["nodzPosX"], JSON[childIdx]["nodzPosY"]))

            nodeIndexToNode[childIdx] = childNode

            for nextIdx in JSON[childIdx]["children"]:
                queue.append((childIdx, str(nextIdx)))

    def saveGraph(self, fileName=None):
        #fileName = QtWidgets.QFileDialog.getOpenFileName(None)
        fileName = 'D:\ProBuilder\ProBuilder\Graphs\graph1.json'

        graphData = {}

        nodeIndex = 0
        nodeToIndex = {}

        # Set the values for each node based on their type
        queue = []

        startNode = None
        if self.currentSelectedNode is None:
            startNode = self.graph.root
        else:
            startNode = self.currentSelectedNode

        queue.append(startNode)

        while len(queue) > 0:
        
            node = queue[0]
            del queue[0]

            if node not in nodeToIndex:
                graphData[nodeIndex] = {}
                nodeToIndex[node] = nodeIndex
                
                graphData[nodeIndex]["type"] = node.nodeType

                if node.nodzNode is not None:
                    graphData[nodeIndex]["nodzPosX"] = node.nodzNode.x()
                    graphData[nodeIndex]["nodzPosY"] = node.nodzNode.y()

                if node.nodeType == NodeType.translate:
                    graphData[nodeIndex]["translateX"] = node.translateX
                    graphData[nodeIndex]["translateY"] = node.translateY
                    graphData[nodeIndex]["translateZ"] = node.translateZ
                elif node.nodeType == NodeType.rotate:
                    graphData[nodeIndex]["rotateX"] = node.rotateX
                    graphData[nodeIndex]["rotateY"] = node.rotateY
                    graphData[nodeIndex]["rotateZ"] = node.rotateZ
                elif node.nodeType == NodeType.scale:
                    graphData[nodeIndex]["scaleX"] = node.scaleX
                    graphData[nodeIndex]["scaleY"] = node.scaleY
                    graphData[nodeIndex]["scaleZ"] = node.scaleZ
                elif node.nodeType == NodeType.init:
                    graphData[nodeIndex]["lotX"] = node.lotX
                    graphData[nodeIndex]["lotY"] = node.lotY
                    graphData[nodeIndex]["lotZ"] = node.lotZ
                elif node.nodeType == NodeType.split:
                    graphData[nodeIndex]["segmentCount"] = node.segmentCount
                    graphData[nodeIndex]["segmentDirection"] = node.segmentDirection
                elif node.nodeType == NodeType.mesh:
                    graphData[nodeIndex]["meshFile"] = node.filePath
                elif node.nodeType == NodeType.splitSegment:
                    graphData[nodeIndex]["idx"] = node.idx
                    graphData[nodeIndex]["proportion"] = node.proportion
                elif node.nodeType == NodeType.repeat:
                    graphData[nodeIndex]["direction"] = node.direction
                    graphData[nodeIndex]["count"] = node.count
                    graphData[nodeIndex]["percentage"] = node.percentage

                nodeIndex += 1

                for child in node.children:
                    queue.append(child)

        # Now set the children arrays for every node
        queue = [startNode]
        seenNodes = set()
        while len(queue) > 0:
            node = queue[0]
            del queue[0]

            if 'children' not in graphData[nodeToIndex[node]]:
                graphData[nodeToIndex[node]]['children'] = []
                for child in node.children:
                    graphData[nodeToIndex[node]]['children'].append(nodeToIndex[child])
                    queue.append(child)

        jsonData = json.dumps(graphData)
        with open(fileName, 'w+') as file:
            file.write(jsonData)   

    def populateGUIEditor(self, node):
        if node.nodeType == NodeType.init:
            self.gui.editorWidget.currentWidget().lotXLineEdit.setText(str(node.lotX))
            self.gui.editorWidget.currentWidget().lotYLineEdit.setText(str(node.lotY))
            self.gui.editorWidget.currentWidget().lotZLineEdit.setText(str(node.lotZ))
        elif node.nodeType == NodeType.translate:
            self.gui.editorWidget.currentWidget().translateXLineEdit.setText(str(node.translateX))
            self.gui.editorWidget.currentWidget().translateYLineEdit.setText(str(node.translateY))
            self.gui.editorWidget.currentWidget().translateZLineEdit.setText(str(node.translateZ))
        elif node.nodeType == NodeType.rotate:
            self.gui.editorWidget.currentWidget().rotateXLineEdit.setText(str(node.rotateX*180.0/math.pi))
            self.gui.editorWidget.currentWidget().rotateYLineEdit.setText(str(node.rotateY*180.0/math.pi))
            self.gui.editorWidget.currentWidget().rotateZLineEdit.setText(str(node.rotateZ*180.0/math.pi))
        elif node.nodeType == NodeType.scale:
            self.gui.editorWidget.currentWidget().scaleXLineEdit.setText(str(node.scaleX))
            self.gui.editorWidget.currentWidget().scaleYLineEdit.setText(str(node.scaleY))
            self.gui.editorWidget.currentWidget().scaleZLineEdit.setText(str(node.scaleZ))
        elif node.nodeType == NodeType.split:
            self.gui.editorWidget.currentWidget().segmentCountSpinBox.setValue(int(node.segmentCount))
            self.gui.editorWidget.currentWidget().segmentDirectionSpinBox.setValue(int(node.segmentDirection))
        elif node.nodeType == NodeType.splitSegment:
            self.gui.editorWidget.currentWidget().proportionLineEdit.setText(str(node.proportion))
        elif node.nodeType == NodeType.mesh:
            self.gui.editorWidget.currentWidget().meshFileLineEdit.setText(str(node.filePath))
        elif node.nodeType == NodeType.repeat:
            self.gui.editorWidget.currentWidget().directionSpinBox.setValue(node.direction)
            self.gui.editorWidget.currentWidget().repeatCountLineEdit.setText(str(node.count))
            self.gui.editorWidget.currentWidget().repeatPercentageSpinBox.setValue(node.percentage)

        self.gui.update()

    def printGraph(self):
        self.graph.printGraph()

    def setInitialValues(self, lotXValue, lotYValue, lotZValue):
        self.currentSelectedNode.lotX = lotXValue
        self.currentSelectedNode.lotY = lotYValue
        self.currentSelectedNode.lotZ = lotZValue

    def setTranslateValues(self, translateXValue, translateYValue, translateZValue):
        self.currentSelectedNode.translateX = translateXValue
        self.currentSelectedNode.translateY = translateYValue
        self.currentSelectedNode.translateZ = translateZValue

    def setRotateValues(self, rotateXValue, rotateYValue, rotateZValue):
        self.currentSelectedNode.rotateX = rotateXValue
        self.currentSelectedNode.rotateY = rotateYValue
        self.currentSelectedNode.rotateZ = rotateZValue

    def setScaleValues(self, scaleXValue, scaleYValue, scaleZValue):
        self.currentSelectedNode.scaleX = scaleXValue
        self.currentSelectedNode.scaleY = scaleYValue
        self.currentSelectedNode.scaleZ = scaleZValue

#NEW
    def setSplitValues(self, segmentCount):
        for x in range(self.currentSelectedNode.segmentCount, segmentCount):
            newNode = self.graph.addNode(NodeType.splitSegment)
            self.currentSelectedNode.children.append(newNode)
            newNode.parent = self.currentSelectedNode
            newNode.idx = x
            self.graph.nodes.add(newNode)
            self.currentSelectedNode.nodz.createAttribute(node=self.currentSelectedNode.nodzNode, name='Segment '+str(x), index=x, preset='attr_preset_1', plug=True, socket=False, dataType=str)
        
        self.currentSelectedNode.segmentCount = segmentCount

    def setSplitDir(self, segmentDirection):
        
        self.currentSelectedNode.segmentDirection = segmentDirection

    def setSplitSegmentValues(self, proportion):
        self.currentSelectedNode.children[self.currentSelectedAttribute].proportion = proportion


#NEW
    def setRepeatDir(self, direction):
        self.currentSelectedNode.direction = direction

    def setRepeatMax(self, count):
        self.currentSelectedNode.count = count

    def setRepeatSize(self, percentage):
        self.currentSelectedNode.percentage = percentage
#

    def setMeshName(self, name):
        self.currentSelectedNode.filePath = name
        self.currentSelectedNode.isSet = True
