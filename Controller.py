from Graph import NodeType
from Graph import Graph
from GUI import GUI


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

        mesh1 = self.graph.addNode(NodeType.mesh)
        self.gui.setNextNodePosition(mesh1, self.currentSelectedNode, 0)
        self.graph.createManualEdge(self.currentSelectedNode, "Segment 0", mesh1, "Node")

        mesh2 = self.graph.addNode(NodeType.mesh)
        self.gui.setNextNodePosition(mesh2, self.currentSelectedNode, 1)
        self.graph.createManualEdge(self.currentSelectedNode, "Segment 1", mesh2, "Node")
        
        mesh3 = self.graph.addNode(NodeType.mesh)
        self.gui.setNextNodePosition(mesh3, self.currentSelectedNode, 2)
        self.graph.createManualEdge(self.currentSelectedNode, "Segment 2", mesh3, "Node")


        """
        translate1 = self.graph.addNode(NodeType.translate)
        translate1.translateX, translate1.translateY, translate1.translateZ = 0, 0, 6

        translate2 = self.graph.addNode(NodeType.translate)
        translate2.translateX, translate2.translateY, translate2.translateZ = 6, 0, 0

        translate3 = self.graph.addNode(NodeType.translate)
        translate3.translateX, translate3.translateY, translate3.translateZ = 0, 0, 16

        scale1 = self.graph.addNode(NodeType.scale)
        scale1.scaleX, scale1.scaleY, scale1.scaleZ = 8, 10, 18
         
        scale2 = self.graph.addNode(NodeType.scale)
        scale2.scaleX, scale2.scaleY, scale2.scaleZ = 7, 13, 18
        
        scale3 = self.graph.addNode(NodeType.scale)
        scale3.scaleX, scale3.scaleY, scale3.scaleZ = 1, 1, 1

        mesh1 = self.graph.addNode(NodeType.mesh)
        mesh2 = self.graph.addNode(NodeType.mesh)
        mesh3 = self.graph.addNode(NodeType.mesh)

        self.graph.createManualEdge(self.graph.root, translate1)
        self.graph.createManualEdge(translate1, scale1)
        self.graph.createManualEdge(scale1, mesh1)
        self.graph.createManualEdge(self.graph.root, translate2)
        self.graph.createManualEdge(translate2, scale2)
        self.graph.createManualEdge(scale2, mesh2)
        self.graph.createManualEdge(mesh2, translate3)
        self.graph.createManualEdge(translate3, scale3)
        self.graph.createManualEdge(scale3, mesh3)
        """

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
            self.gui.editorWidget.currentWidget().rotateXLineEdit.setText(str(node.rotateX))
            self.gui.editorWidget.currentWidget().rotateYLineEdit.setText(str(node.rotateY))
            self.gui.editorWidget.currentWidget().rotateZLineEdit.setText(str(node.rotateZ))
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
            self.gui.editorWidget.currentWidget().scaleXLineEdit.setText(str(node.name))
        elif node.nodeType == NodeType.repeat:
            self.gui.editorWidget.currentWidget().directionSpinBox.setValue(node.direction)

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

    def setSplitValues(self, segmentCount, segmentDirection):
        for x in range(self.currentSelectedNode.segmentCount, segmentCount):
            newNode = self.graph.addNode(NodeType.splitSegment)
            self.currentSelectedNode.children.append(newNode)
            self.currentSelectedNode.nodz.createAttribute(node=self.currentSelectedNode.nodzNode, name='Segment '+str(x), index=x, preset='attr_preset_1', plug=True, socket=False, dataType=str)
        
        self.currentSelectedNode.segmentDirection = segmentDirection
        self.currentSelectedNode.segmentCount = segmentCount

    def setSplitSegmentValues(self, proportion):
        self.currentSelectedNode.children[self.currentSelectedAttribute].proportion = proportion

    def setRepeatValues(self, direction):
        self.currentSelectedNode.direction = direction

    def setMeshName(self, name):
        self.currentSelectedNode.name=name
        self.currentSelectedNode.is_set=True
