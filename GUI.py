from Qt import QtGui, QtCore, QtWidgets
import nodz_main

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

        self.generateWidget = Generate(self, self.controller)
        self.layout.addWidget(self.generateWidget)

        self.nodePickerWidget = NodePickerWidget(self, self.controller)
        self.layout.addWidget(self.nodePickerWidget)

        self.editor = Editor(self, self.controller)
        self.editorTranslate = EditorTranslate(self, self.controller)
        self.editorRotate = EditorRotate(self, self.controller)
        self.editorScale = EditorScale(self, self.controller)
        self.editorInitial = EditorInitial(self, self.controller)
        self.editorMesh = EditorMesh(self, self.controller)
        self.editorSplit = EditorSplit(self, self.controller)
        #new
        self.editorSplit_Helper =  EditorSplit_Helper(self, self.controller)

        self.editorWidget = QtWidgets.QStackedWidget(self)
        self.editorWidget.addWidget(self.editorTranslate)     #0
        self.editorWidget.addWidget(self.editorRotate)        #1
        self.editorWidget.addWidget(self.editorScale)         #2
        self.editorWidget.addWidget(self.editorInitial)       #3
        self.editorWidget.addWidget(self.editorMesh)          #4
        self.editorWidget.addWidget(self.editorSplit)         #5        
        self.editorWidget.addWidget(self.editor)              #6

        #NEW
        self.editorWidget.addWidget(self.editorSplit_Helper)  #7

        
        
        
        self.layout.addWidget(self.editorWidget)

        self.editorWidget.setCurrentIndex(6)

        self.nodzWidget = nodz_main.Nodz(self)
        self.nodzWidget.initialize()
        self.layout.addWidget(self.nodzWidget)

        self.window = QtWidgets.QWidget(self)
        self.window.setLayout(self.layout)

        self.setCentralWidget(self.window)

        self.setWindowTitle("ProBuilder")

    def changeEditorWidgetLayout(self, nodeType):
        if nodeType == "Default":
            self.editorWidget.setCurrentIndex(6)
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
        #NEW!
        elif nodeType == NodeType.splitSegment:
            self.editorWidget.setCurrentIndex(7)

class NodePickerWidget(QtWidgets.QWidget):

    def __init__(self, parent, controller):
        super(NodePickerWidget, self).__init__(parent)

        #self.setStyleSheet("background-color: black;")

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setAlignment(QtCore.Qt.AlignTop)

        self.label = QtWidgets.QLabel("Create Node:")
        self.label.setMinimumWidth(150)
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

        self.button5 = QtWidgets.QPushButton("Mesh")
        self.button5.clicked.connect(lambda: controller.addNode(NodeType.mesh))
        self.layout.addWidget(self.button5)

        self.setLayout(self.layout)

class Generate(QtWidgets.QWidget):

    def __init__(self, parent, controller):
        super(Generate, self).__init__(parent)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setAlignment(QtCore.Qt.AlignTop)

        self.label = QtWidgets.QLabel("Create Mesh:")
        self.label.setAlignment(QtCore.Qt.AlignHCenter)
        self.layout.addWidget(self.label)

        self.button = QtWidgets.QPushButton("Generate")
        self.button.clicked.connect(controller.generateMesh)
        self.layout.addWidget(self.button)

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

        #print "hello"

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
            self.controller.setRotateValues(float(self.rotateXLineEdit.text()), float(self.rotateYLineEdit.text()), float(self.rotateZLineEdit.text()))

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
        self.lotXLineEdit.setValidator(QtGui.QIntValidator(0,1000,self))
        self.lotXLineEdit.textEdited.connect(self.setValues)
        self.lotX.addWidget(self.lotXLabel)
        self.lotX.addWidget(self.lotXLineEdit)
        self.layout.addLayout(self.lotX)

        self.lotY = QtWidgets.QHBoxLayout(self)
        self.lotYLabel = QtWidgets.QLabel("Lot Y: ")
        self.lotYLineEdit = QtWidgets.QLineEdit()
        self.lotYLineEdit.setValidator(QtGui.QIntValidator(0,1000,self))
        self.lotYLineEdit.textEdited.connect(self.setValues)
        self.lotY.addWidget(self.lotYLabel)
        self.lotY.addWidget(self.lotYLineEdit)
        self.layout.addLayout(self.lotY)

        self.lotZ = QtWidgets.QHBoxLayout(self)
        self.lotZLabel = QtWidgets.QLabel("Lot Z: ")
        self.lotZLineEdit = QtWidgets.QLineEdit()
        self.lotZLineEdit.setValidator(QtGui.QIntValidator(0,1000,self))
        self.lotZLineEdit.textEdited.connect(self.setValues)
        self.lotZ.addWidget(self.lotZLabel)
        self.lotZ.addWidget(self.lotZLineEdit)
        self.layout.addLayout(self.lotZ)

        self.setLayout(self.layout)

    def setValues(self):
        if self.lotXLineEdit.text() not in ["-", ""] and self.lotYLineEdit.text() not in ["-", ""] and self.lotZLineEdit.text() not in ["-", ""]:
            self.controller.setInitialValues(int(self.lotXLineEdit.text()), int(self.lotYLineEdit.text()), int(self.lotZLineEdit.text()))

#New2
class EditorMesh(Editor):

    def __init__(self, parent, controller):
        super(EditorMesh, self).__init__(parent, controller)

        self.controller = controller

        self.scaleX = QtWidgets.QHBoxLayout(self)
        self.scaleXLabel = QtWidgets.QLabel("Name: ")
        self.scaleXLineEdit = QtWidgets.QLineEdit()
        #self.scaleXLineEdit.setValidator(QtGui.QStringValidator(0,1000,self))
        self.scaleXLineEdit.textEdited.connect(self.setName)
        self.scaleX.addWidget(self.scaleXLabel)
        self.scaleX.addWidget(self.scaleXLineEdit)
        self.layout.addLayout(self.scaleX)

        self.setLayout(self.layout)

    def setName(self):
        self.controller.setMeshName(self.scaleXLineEdit.text())

class EditorSplit(Editor):

    def __init__(self, parent, controller):
        super(EditorSplit, self).__init__(parent, controller)

        self.controller = controller

        self.segmentCount = QtWidgets.QHBoxLayout(self)
        self.segmentCountLabel = QtWidgets.QLabel("Segment Count: ")
        self.segmentCountSpinBox = QtWidgets.QSpinBox()
        self.segmentCountSpinBox.setSingleStep(1)
        self.segmentCountSpinBox.setRange(0, 10)
        self.segmentCountSpinBox.valueChanged.connect(self.setCountValue)
        self.segmentCount.addWidget(self.segmentCountLabel)
        self.segmentCount.addWidget(self.segmentCountSpinBox)
        self.layout.addLayout(self.segmentCount)

        self.segmentDirection = QtWidgets.QHBoxLayout(self)
        self.segmentDirectionLabel = QtWidgets.QLabel("Segment Direction: ")
        self.segmentDirectionSpinBox = QtWidgets.QSpinBox()
        self.segmentDirectionSpinBox.setSingleStep(1)
        self.segmentDirectionSpinBox.setRange(0, 2)
        self.segmentDirectionSpinBox.valueChanged.connect(self.setDirection)
        self.segmentDirection.addWidget(self.segmentDirectionLabel)
        self.segmentDirection.addWidget(self.segmentDirectionSpinBox)
        self.layout.addLayout(self.segmentDirection)

        self.setLayout(self.layout)

    def setCountValue(self):
        self.controller.setSegmentValues(self.segmentCountSpinBox.value())
    def setDirection(self):
        self.controller.setDirValues(self.segmentDirectionSpinBox.value())

class EditorSegment(Editor):
    def __init__(self, parent, controller):
        super(EditorSegment, self).__init__(parent, controller)

        self.controller = controller

        self.proportion = QtWidgets.QHBoxLayout(self)
        self.proportionLabel = QtWidgets.QLabel("Proportion: ")
        self.proportionLineEdit = QtWidgets.QLineEdit()
        self.proportionLineEdit.setValidator(QtGui.QDoubleValidator(-1000,1000, 5,self))
        self.proportionLineEdit.textEdited.connect(self.setValues)
        self.proportion.addWidget(self.proportionLabel)
        self.proportion.addWidget(self.proportionLineEdit)
        self.layout.addLayout(self.proportion)

        self.setLayout(self.layout)

    def setValues(self):
        self.controller.setProportionValues(float(self.proportionLineEdit.text()))

#tmp class
class EditorSplit_Helper(Editor):

    def __init__(self, parent, controller):
        super(EditorSplit_Helper, self).__init__(parent, controller)

        self.controller = controller

        self.scaleX = QtWidgets.QHBoxLayout(self)
        self.scaleXLabel = QtWidgets.QLabel("Proportion: ")
        self.scaleXLineEdit = QtWidgets.QLineEdit()
        self.scaleXLineEdit.setValidator(QtGui.QDoubleValidator(-1000,1000, 5,self))
        self.scaleXLineEdit.textEdited.connect(self.setValues)
        self.scaleX.addWidget(self.scaleXLabel)
        self.scaleX.addWidget(self.scaleXLineEdit)
        self.layout.addLayout(self.scaleX)

        self.setLayout(self.layout)

    def setValues(self):
        self.controller.setProportionValues(float(self.scaleXLineEdit.text()))
