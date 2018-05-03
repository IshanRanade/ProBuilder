from Qt import QtGui, QtCore, QtWidgets
import nodz_main
import math

from Graph import NodeType

class GUI(QtWidgets.QMainWindow):

    controller = None

    def __init__(self, type, controller):
        """
        Initialize the graphics view.

        """
        super(GUI, self).__init__()

        self.controller = controller

        self.layout = QtWidgets.QHBoxLayout(self)

        self.leftSide = QtWidgets.QVBoxLayout(self)

        self.generateWidget = Generate(self, self.controller)
        self.leftSide.addWidget(self.generateWidget)

        self.nodePickerWidget = NodePickerWidget(self, self.controller)
        self.leftSide.addWidget(self.nodePickerWidget)

        self.editor = Editor(self, self.controller)
        self.editorTranslate = EditorTranslate(self, self.controller)
        self.editorRotate = EditorRotate(self, self.controller)
        self.editorScale = EditorScale(self, self.controller)
        self.editorInitial = EditorInitial(self, self.controller)
        self.editorMesh = EditorMesh(self, self.controller)
        self.editorSplit = EditorSplit(self, self.controller)
        self.editorSplitSegment = EditorSplitSegment(self, self.controller)
        self.editorRepeat = EditorRepeat(self, self.controller)

        self.editorWidget = QtWidgets.QStackedWidget(self)
        self.editorWidget.addWidget(self.editorTranslate)     #0
        self.editorWidget.addWidget(self.editorRotate)        #1
        self.editorWidget.addWidget(self.editorScale)         #2
        self.editorWidget.addWidget(self.editorInitial)       #3
        self.editorWidget.addWidget(self.editorMesh)          #4
        self.editorWidget.addWidget(self.editorSplit)         #5        
        self.editorWidget.addWidget(self.editor)              #6
        self.editorWidget.addWidget(self.editorSplitSegment)  #7
        self.editorWidget.addWidget(self.editorRepeat)        #8
        
        self.leftSide.addWidget(self.editorWidget)

        self.editorWidget.setCurrentIndex(6)

        self.nodzWidget = nodz_main.Nodz(self, self.controller)
        self.nodzWidget.initialize()
        self.nodzWidget.setMinimumSize(1000, 800)

        # Put the left side layout into a widget so we can restrict
        # the size of the widget because we can't restrict layouts
        self.leftSideWidget = QtWidgets.QWidget()
        self.leftSideWidget.setMaximumWidth(200)
        self.leftSideWidget.setLayout(self.leftSide)
        self.layout.addWidget(self.leftSideWidget)
        self.layout.addWidget(self.nodzWidget)

        self.window = QtWidgets.QWidget(self)
        self.window.setLayout(self.layout)

        self.setCentralWidget(self.window)

        self.setWindowTitle("ProBuilder")

    def changeEditorWidgetLayout(self, nodeType):
        if nodeType == "Default":
            self.editorWidget.setCurrentIndex(6)
        elif nodeType == "SplitSegment":
            self.editorWidget.setCurrentIndex(7)
        elif nodeType == NodeType.init:
            self.editorWidget.setCurrentIndex(3)
        elif nodeType == NodeType.translate:
            self.editorWidget.setCurrentIndex(0)
        elif nodeType == NodeType.rotate:
            self.editorWidget.setCurrentIndex(1)
        elif nodeType == NodeType.scale:
            self.editorWidget.setCurrentIndex(2)
        elif nodeType == NodeType.split:
            self.editorWidget.setCurrentIndex(5)
        elif nodeType == NodeType.mesh:
            self.editorWidget.setCurrentIndex(4)
        elif nodeType == NodeType.repeat:
            self.editorWidget.setCurrentIndex(8)

    def setNextNodePosition(self, node, selectedNode, selectedAttribute):
        if selectedNode is not None and selectedAttribute is not None:
            deltaX = selectedNode.nodzNode.baseWidth + 50
            deltaY = (selectedNode.nodzNode.attrCount - 1) * selectedNode.nodzNode.attrHeight
            deltaY -= (selectedNode.nodzNode.baseHeight + 70) * (selectedNode.nodzNode.attrCount - selectedAttribute - 1)
            newPos = QtCore.QPoint(selectedNode.nodzNode.x() + deltaX, selectedNode.nodzNode.y() + deltaY)
            node.nodzNode.setPos(newPos)
        elif selectedNode is not None:
            deltaX = selectedNode.nodzNode.baseWidth + 50
            deltaY = (selectedNode.nodzNode.attrCount - 1) * selectedNode.nodzNode.attrHeight
            newPos = QtCore.QPoint(selectedNode.nodzNode.x() + deltaX, selectedNode.nodzNode.y() + deltaY)
            node.nodzNode.setPos(newPos)
        else:
            node.nodzNode.setPos(self.nodzWidget.mapToScene(self.nodzWidget.viewport().rect().center()))

class NodePickerWidget(QtWidgets.QWidget):

    def __init__(self, parent, controller):
        super(NodePickerWidget, self).__init__(parent)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setAlignment(QtCore.Qt.AlignTop)

        self.label = QtWidgets.QLabel("Create Node:")
        self.label.setAlignment(QtCore.Qt.AlignHCenter)
        self.layout.addWidget(self.label)

        self.button1 = QtWidgets.QPushButton("Translate")
        self.button1.clicked.connect(lambda: controller.addNode(NodeType.translate))
        self.layout.addWidget(self.button1)

        self.button2 = QtWidgets.QPushButton("Rotate")
        self.button2.clicked.connect(lambda: controller.addNode(NodeType.rotate))
        self.layout.addWidget(self.button2)

        self.button3 = QtWidgets.QPushButton("Scale")
        self.button3.clicked.connect(lambda: controller.addNode(NodeType.scale))
        self.layout.addWidget(self.button3)

        self.button4 = QtWidgets.QPushButton("Split")
        self.button4.clicked.connect(lambda: controller.addNode(NodeType.split))
        self.layout.addWidget(self.button4)

        self.button5 = QtWidgets.QPushButton("Repeat")
        self.button5.clicked.connect(lambda: controller.addNode(NodeType.repeat))
        self.layout.addWidget(self.button5)

        self.button6 = QtWidgets.QPushButton("Mesh")
        self.button6.clicked.connect(lambda: controller.addNode(NodeType.mesh))
        self.layout.addWidget(self.button6)

        self.setLayout(self.layout)

class Generate(QtWidgets.QWidget):

    def __init__(self, parent, controller):
        super(Generate, self).__init__(parent)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setAlignment(QtCore.Qt.AlignTop)

        self.label = QtWidgets.QLabel("Options:")
        self.label.setAlignment(QtCore.Qt.AlignHCenter)
        self.layout.addWidget(self.label)

        self.buttonLoad = QtWidgets.QPushButton("Load")
        self.buttonLoad.clicked.connect(controller.loadGraph)
        self.layout.addWidget(self.buttonLoad)

        self.buttonSave = QtWidgets.QPushButton("Save")
        self.buttonSave.clicked.connect(controller.saveGraph)
        self.layout.addWidget(self.buttonSave)

        self.button = QtWidgets.QPushButton("Generate")
        self.button.clicked.connect(controller.generateMesh)
        self.layout.addWidget(self.button)

        self.button2 = QtWidgets.QPushButton("Print Graph")
        self.button2.clicked.connect(controller.printGraph)
        self.layout.addWidget(self.button2)

        self.button3 = QtWidgets.QPushButton("Sample 1")
        self.button3.clicked.connect(controller.testGraph1)
        self.layout.addWidget(self.button3)

        self.button4 = QtWidgets.QPushButton("Sample 2")
        self.button4.clicked.connect(controller.testGraph2)
        self.layout.addWidget(self.button4)

        self.setLayout(self.layout)

class Editor(QtWidgets.QWidget):

    def __init__(self, parent, controller):
        super(Editor, self).__init__(parent)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setAlignment(QtCore.Qt.AlignTop)

        self.label = QtWidgets.QLabel("Attribute Editor:")
        self.label.setAlignment(QtCore.Qt.AlignHCenter)
        self.layout.addWidget(self.label)

        self.setLayout(self.layout)

class EditorTranslate(Editor):

    def __init__(self, parent, controller):
        super(EditorTranslate, self).__init__(parent, controller)

        self.controller = controller

        self.translateX = QtWidgets.QHBoxLayout(self)
        self.translateXLabel = QtWidgets.QLabel("Translate X: ")
        self.translateXLineEdit = QtWidgets.QLineEdit()
        self.translateXLineEdit.setValidator(QtGui.QDoubleValidator(-1000,1000, 5,self))
        self.translateXLineEdit.textEdited.connect(self.setValues)
        self.translateX.addWidget(self.translateXLabel)
        self.translateX.addWidget(self.translateXLineEdit)
        self.layout.addLayout(self.translateX)

        self.translateY = QtWidgets.QHBoxLayout(self)
        self.translateYLabel = QtWidgets.QLabel("Translate Y: ")
        self.translateYLineEdit = QtWidgets.QLineEdit()
        self.translateYLineEdit.setValidator(QtGui.QDoubleValidator(-1000,1000, 5,self))
        self.translateYLineEdit.textEdited.connect(self.setValues)
        self.translateY.addWidget(self.translateYLabel)
        self.translateY.addWidget(self.translateYLineEdit)
        self.layout.addLayout(self.translateY)

        self.translateZ = QtWidgets.QHBoxLayout(self)
        self.translateZLabel = QtWidgets.QLabel("Translate Z: ")
        self.translateZLineEdit = QtWidgets.QLineEdit()
        self.translateZLineEdit.setValidator(QtGui.QDoubleValidator(-1000,1000, 5,self))
        self.translateZLineEdit.textEdited.connect(self.setValues)
        self.translateZ.addWidget(self.translateZLabel)
        self.translateZ.addWidget(self.translateZLineEdit)
        self.layout.addLayout(self.translateZ)

        self.setLayout(self.layout) 

    def setValues(self):
        if self.translateXLineEdit.text() not in ["-", ""] and self.translateYLineEdit.text() not in ["-", ""] and self.translateZLineEdit.text() not in ["-", ""]  :
            self.controller.setTranslateValues(float(self.translateXLineEdit.text()), float(self.translateYLineEdit.text()), float(self.translateZLineEdit.text()))

class EditorRotate(Editor):

    def __init__(self, parent, controller):
        super(EditorRotate, self).__init__(parent, controller)

        self.controller = controller

        self.rotateX = QtWidgets.QHBoxLayout(self)
        self.rotateXLabel = QtWidgets.QLabel("Rotate X: ")
        self.rotateXLineEdit = QtWidgets.QLineEdit()
        self.rotateXLineEdit.setValidator(QtGui.QDoubleValidator(-1000,1000, 5,self))
        self.rotateXLineEdit.textEdited.connect(self.setValues)
        self.rotateX.addWidget(self.rotateXLabel)
        self.rotateX.addWidget(self.rotateXLineEdit)
        self.layout.addLayout(self.rotateX)

        self.rotateY = QtWidgets.QHBoxLayout(self)
        self.rotateYLabel = QtWidgets.QLabel("Rotate Y: ")
        self.rotateYLineEdit = QtWidgets.QLineEdit()
        self.rotateYLineEdit.setValidator(QtGui.QDoubleValidator(-1000,1000, 5,self))
        self.rotateYLineEdit.textEdited.connect(self.setValues)
        self.rotateY.addWidget(self.rotateYLabel)
        self.rotateY.addWidget(self.rotateYLineEdit)
        self.layout.addLayout(self.rotateY)

        self.rotateZ = QtWidgets.QHBoxLayout(self)
        self.rotateZLabel = QtWidgets.QLabel("Rotate Z: ")
        self.rotateZLineEdit = QtWidgets.QLineEdit()
        self.rotateZLineEdit.setValidator(QtGui.QDoubleValidator(-1000,1000, 5,self))
        self.rotateZLineEdit.textEdited.connect(self.setValues)
        self.rotateZ.addWidget(self.rotateZLabel)
        self.rotateZ.addWidget(self.rotateZLineEdit)
        self.layout.addLayout(self.rotateZ)

        self.setLayout(self.layout)

    def setValues(self):
        if self.rotateXLineEdit.text() not in ["-", ""] and self.rotateYLineEdit.text() not in ["-", ""] and self.rotateZLineEdit.text() not in ["-", ""]:
            self.controller.setRotateValues(float(self.rotateXLineEdit.text())*math.pi/180.0,
                                            float(self.rotateYLineEdit.text())*math.pi/180.0,
                                            float(self.rotateZLineEdit.text())*math.pi/180.0)

class EditorScale(Editor):

    def __init__(self, parent, controller):
        super(EditorScale, self).__init__(parent, controller)

        self.controller = controller

        self.scaleX = QtWidgets.QHBoxLayout(self)
        self.scaleXLabel = QtWidgets.QLabel("Scale X: ")
        self.scaleXLineEdit = QtWidgets.QLineEdit()
        self.scaleXLineEdit.setValidator(QtGui.QDoubleValidator(-1000,1000, 5,self))
        self.scaleXLineEdit.textEdited.connect(self.setValues)
        self.scaleX.addWidget(self.scaleXLabel)
        self.scaleX.addWidget(self.scaleXLineEdit)
        self.layout.addLayout(self.scaleX)

        self.scaleY = QtWidgets.QHBoxLayout(self)
        self.scaleYLabel = QtWidgets.QLabel("Scale Y: ")
        self.scaleYLineEdit = QtWidgets.QLineEdit()
        self.scaleYLineEdit.setValidator(QtGui.QDoubleValidator(-1000,1000, 5,self))
        self.scaleYLineEdit.textEdited.connect(self.setValues)
        self.scaleY.addWidget(self.scaleYLabel)
        self.scaleY.addWidget(self.scaleYLineEdit)
        self.layout.addLayout(self.scaleY)

        self.scaleZ = QtWidgets.QHBoxLayout(self)
        self.scaleZLabel = QtWidgets.QLabel("Scale Z: ")
        self.scaleZLineEdit = QtWidgets.QLineEdit()
        self.scaleZLineEdit.setValidator(QtGui.QDoubleValidator(-1000,1000, 5,self))
        self.scaleZLineEdit.textEdited.connect(self.setValues)
        self.scaleZ.addWidget(self.scaleZLabel)
        self.scaleZ.addWidget(self.scaleZLineEdit)
        self.layout.addLayout(self.scaleZ)

        self.setLayout(self.layout)

    def setValues(self):
        if self.scaleXLineEdit.text() not in ["-", ""] and self.scaleYLineEdit.text() not in ["-", ""] and self.scaleZLineEdit.text() not in ["-", ""]:
            self.controller.setScaleValues(float(self.scaleXLineEdit.text()), float(self.scaleYLineEdit.text()), float(self.scaleZLineEdit.text()))

class EditorInitial(Editor):

    def __init__(self, parent, controller):
        super(EditorInitial, self).__init__(parent, controller)

        self.controller = controller

        self.lotX = QtWidgets.QHBoxLayout(self)
        self.lotXLabel = QtWidgets.QLabel("Lot X: ")
        self.lotXLineEdit = QtWidgets.QLineEdit()
        self.lotXLineEdit.setValidator(QtGui.QDoubleValidator(-1000,1000, 5,self))
        self.lotXLineEdit.textEdited.connect(self.setValues)
        self.lotX.addWidget(self.lotXLabel)
        self.lotX.addWidget(self.lotXLineEdit)
        self.layout.addLayout(self.lotX)

        self.lotY = QtWidgets.QHBoxLayout(self)
        self.lotYLabel = QtWidgets.QLabel("Lot Y: ")
        self.lotYLineEdit = QtWidgets.QLineEdit()
        self.lotYLineEdit.setValidator(QtGui.QDoubleValidator(-1000,1000, 5,self))
        self.lotYLineEdit.textEdited.connect(self.setValues)
        self.lotY.addWidget(self.lotYLabel)
        self.lotY.addWidget(self.lotYLineEdit)
        self.layout.addLayout(self.lotY)

        self.lotZ = QtWidgets.QHBoxLayout(self)
        self.lotZLabel = QtWidgets.QLabel("Lot Z: ")
        self.lotZLineEdit = QtWidgets.QLineEdit()
        self.lotZLineEdit.setValidator(QtGui.QDoubleValidator(-1000,1000, 5,self))
        self.lotZLineEdit.textEdited.connect(self.setValues)
        self.lotZ.addWidget(self.lotZLabel)
        self.lotZ.addWidget(self.lotZLineEdit)
        self.layout.addLayout(self.lotZ)

        self.setLayout(self.layout)

    def setValues(self):
        if self.lotXLineEdit.text() not in ["-", ""] and self.lotYLineEdit.text() not in ["-", ""] and self.lotZLineEdit.text() not in ["-", ""]:
            self.controller.setInitialValues(float(self.lotXLineEdit.text()), float(self.lotYLineEdit.text()), float(self.lotZLineEdit.text()))

class EditorMesh(Editor):

    def __init__(self, parent, controller):
        super(EditorMesh, self).__init__(parent, controller)

        self.controller = controller

        self.meshFile = QtWidgets.QHBoxLayout(self)
        self.meshFileLabel = QtWidgets.QLabel("File: ")
        self.meshFileLineEdit = QtWidgets.QLineEdit()
        self.meshFileLineEdit.textEdited.connect(self.setName)
        self.meshFile.addWidget(self.meshFileLabel)
        self.meshFile.addWidget(self.meshFileLineEdit)
        self.layout.addLayout(self.meshFile)

        self.setLayout(self.layout)

    def setName(self):
        self.controller.setMeshName(self.meshFileLineEdit.text())

class EditorSplit(Editor):

    def __init__(self, parent, controller):
        super(EditorSplit, self).__init__(parent, controller)

        self.controller = controller

        self.segmentCount = QtWidgets.QHBoxLayout(self)
        self.segmentCountLabel = QtWidgets.QLabel("Segment Count: ")
        self.segmentCountSpinBox = QtWidgets.QSpinBox()
        self.segmentCountSpinBox.setSingleStep(1)
        self.segmentCountSpinBox.setRange(0, 10)
        self.segmentCountSpinBox.valueChanged.connect(self.setValues1)
        self.segmentCount.addWidget(self.segmentCountLabel)
        self.segmentCount.addWidget(self.segmentCountSpinBox)
        self.layout.addLayout(self.segmentCount)

        self.segmentDirection = QtWidgets.QHBoxLayout(self)
        self.segmentDirectionLabel = QtWidgets.QLabel("Segment Direction: ")
        self.segmentDirectionSpinBox = QtWidgets.QSpinBox()
        self.segmentDirectionSpinBox.setSingleStep(1)
        self.segmentDirectionSpinBox.setRange(0, 2)
        self.segmentDirectionSpinBox.valueChanged.connect(self.setValues2)
        self.segmentDirection.addWidget(self.segmentDirectionLabel)
        self.segmentDirection.addWidget(self.segmentDirectionSpinBox)
        self.layout.addLayout(self.segmentDirection)

        self.setLayout(self.layout)
#NEW
    def setValues1(self):
        self.controller.setSplitValues(self.segmentCountSpinBox.value())
    def setValues2(self):
        self.controller.setSplitDir(self.segmentDirectionSpinBox.value())

class EditorSplitSegment(Editor):
    def __init__(self, parent, controller):
        super(EditorSplitSegment, self).__init__(parent, controller)

        self.controller = controller

        self.proportion = QtWidgets.QHBoxLayout(self)
        self.proportionLabel = QtWidgets.QLabel("Proportion: ")
        self.proportionLineEdit = QtWidgets.QLineEdit()
        self.proportionLineEdit.setValidator(QtGui.QDoubleValidator(0,1000,5,self))
        self.proportionLineEdit.textEdited.connect(self.setValues)
        self.proportion.addWidget(self.proportionLabel)
        self.proportion.addWidget(self.proportionLineEdit)
        self.layout.addLayout(self.proportion)

        self.setLayout(self.layout)

    def setValues(self):
        self.controller.setSplitSegmentValues(float(self.proportionLineEdit.text()))

class EditorRepeat(Editor):
    def __init__(self, parent, controller):
        super(EditorRepeat, self).__init__(parent, controller)

        self.controller = controller

        self.repeatDirection = QtWidgets.QHBoxLayout(self)
        self.directionLabel = QtWidgets.QLabel("Direction: ")
        self.directionSpinBox = QtWidgets.QSpinBox()
        self.directionSpinBox.setSingleStep(1)
        self.directionSpinBox.setRange(0, 2)
        self.directionSpinBox.valueChanged.connect(self.setValues1)
        self.repeatDirection.addWidget(self.directionLabel)
        self.repeatDirection.addWidget(self.directionSpinBox)
        self.layout.addLayout(self.repeatDirection)

        self.repeatCount = QtWidgets.QHBoxLayout(self)
        self.repeatCountLabel = QtWidgets.QLabel("Max: ")
        self.repeatCountLineEdit = QtWidgets.QLineEdit()
        self.repeatCountLineEdit.setValidator(QtGui.QIntValidator(0,1000,self))
        self.repeatCountLineEdit.textEdited.connect(self.setValues2)
        self.repeatCount.addWidget(self.repeatCountLabel)
        self.repeatCount.addWidget(self.repeatCountLineEdit)
        self.layout.addLayout(self.repeatCount)

        self.repeatPercentage = QtWidgets.QHBoxLayout(self)
        self.repeatPercentageLabel = QtWidgets.QLabel("Size %")
        self.repeatPercentageSpinBox = QtWidgets.QSpinBox()
        self.repeatPercentageSpinBox.setSingleStep(1)
        self.repeatPercentageSpinBox.setRange(0, 100)
        self.repeatPercentageSpinBox.valueChanged.connect(self.setValues3)
        self.repeatPercentage.addWidget(self.repeatPercentageLabel)
        self.repeatPercentage.addWidget(self.repeatPercentageSpinBox)
        self.layout.addLayout(self.repeatPercentage)

        self.setLayout(self.layout)
    
    def setValues1(self):
        if self.repeatCountLineEdit.text() not in ["-", ""]:
            self.controller.setRepeatDir(self.directionSpinBox.value())
    def setValues2(self):
        if self.repeatCountLineEdit.text() not in ["-", ""]:
            self.controller.setRepeatMax(int(self.repeatCountLineEdit.text()))
    def setValues3(self):
        if self.repeatCountLineEdit.text() not in ["-", ""]:
            self.controller.setRepeatSize(self.repeatPercentageSpinBox.value())
