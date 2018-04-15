from Graph import NodeType
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
        self.nodz.signal_AttrSelected.connect(self.attributeSelected)

        self.gui.setWindowOpacity(0.8)
        

        # Create a test graph
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
            self.gui.changeEditorWidgetLayout(self.graph.getNodeFromNodz(nodzNode).nodeType)
            self.gui.update()
        else:
            self.currentSelectedNode = None
            self.gui.changeEditorWidgetLayout("Default")
            self.gui.update()

    def attributeSelected(self, nodzNode, attributeNum):
        print attributeNum

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
            #NEW
            if node.nodeType == NodeType.split:
                self.gui.editorWidget.currentWidget().segmentCountSpinBox.setValue(int(node.segment))
                self.gui.editorWidget.currentWidget().segmentDirectionSpinBox.setValue(int(node.seg_dir))
            if node.nodeType == NodeType.splitSegment:
                self.gui.editorWidget.currentWidget().scaleXLineEdit.setText(str(node.proportion))
            #New2
            if node.nodeType == NodeType.mesh:
                self.gui.editorWidget.currentWidget().scaleXLineEdit.setText(str(node.name))

            self.gui.update()

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

        #NEW2
    def setSegmentValues(self, segmentNum):
        self.currentSelectedNode.segment = segmentNum
        #self.currentSelectedNode.add_split_attr(int(segmentNum))

        for x in range (0,segmentNum):
            self.currentSelectedNode.nodz.createAttribute(node=self.currentSelectedNode.nodzNode, name='Segment '+str(x), index=x, preset='attr_preset_1', plug=True, socket=False, dataType=str)
            
            new_node = self.graph.addNode(NodeType.splitSegment)

            #No need to do this since it has already been added in addNode!
            #self.currentSelectedNode.children.append(new_node)
            
            self.currentSelectedNode.nodz.createConnection( self.currentSelectedNode.nodzNode, 'Segment '+str(x),new_node.nodzNode, 'Node')
                    
    def setDirValues(self, seg_dir):
        self.currentSelectedNode.seg_dir = seg_dir
    
    def setProportionValues(self, proportion):
        self.currentSelectedNode.proportion = proportion

    #New2
    def setMeshName(self, name):
        self.currentSelectedNode.name=name
        self.currentSelectedNode.is_set=True
