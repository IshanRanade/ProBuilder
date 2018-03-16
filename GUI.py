import os
import re
import json

from Qt import QtGui, QtCore, QtWidgets
import nodz_main

from Graph import NodeType

class GUI(QtWidgets.QMainWindow):

	controller = None

	def __init__(self, type, nodz, controller):
		"""
		Initialize the graphics view.

		"""
		super(GUI, self).__init__()

		self.controller = controller

		self.layout = QtWidgets.QHBoxLayout(self)

		self.editorTranslate = EditorTranslate(self)
		self.editorRotate = EditorRotate(self)
		self.editorScale = EditorScale(self)
		self.editorInitial = EditorInitial(self)
		self.editorMesh = EditorMesh(self)
		self.editorSplit = EditorSplit(self)

		self.editorWidget = QtWidgets.QStackedWidget(self)
		self.editorWidget.addWidget(self.editorTranslate) #0
		self.editorWidget.addWidget(self.editorRotate)    #1
		self.editorWidget.addWidget(self.editorScale)     #2
		self.editorWidget.addWidget(self.editorInitial)   #3
		self.editorWidget.addWidget(self.editorMesh)      #4
		self.editorWidget.addWidget(self.editorSplit)     #5
		self.layout.addWidget(self.editorWidget)

		self.editorWidget.setCurrentIndex(3)

		self.nodePickerWidget = NodePickerWidget(self, self.controller)
		self.layout.addWidget(self.nodePickerWidget)

		self.nodzWidget = nodz
		self.layout.addWidget(nodz)

		self.window = QtWidgets.QWidget(self)
		self.window.setLayout(self.layout)

		self.setCentralWidget(self.window)

		self.setWindowTitle("ProBuilder")

	def changeEditorWidgetLayout(self, nodeType):
		if nodeType == NodeType.init:
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

class NodePickerWidget(QtWidgets.QWidget):

	def __init__(self, parent, controller):
		super(NodePickerWidget, self).__init__(parent)

		self.layout = QtWidgets.QVBoxLayout(self)

		self.label = QtWidgets.QLabel("Create Node:")
		self.layout.addWidget(self.label)

		self.button1 = QtWidgets.QPushButton("Translate")
		self.button1.clicked.connect(lambda: controller.addNode(NodeType.translate))
		self.layout.addWidget(self.button1)

		self.button2 = QtWidgets.QPushButton("Rotate")
		self.layout.addWidget(self.button2)

		self.button3 = QtWidgets.QPushButton("Scale")
		self.layout.addWidget(self.button3)

		self.button4 = QtWidgets.QPushButton("Split")
		self.layout.addWidget(self.button4)

		self.button5 = QtWidgets.QPushButton("Mesh")
		self.layout.addWidget(self.button5)

		self.setLayout(self.layout)

class EditorTranslate(QtWidgets.QWidget):

	def __init__(self, parent):
		super(EditorTranslate, self).__init__(parent)

		self.layout = QtWidgets.QVBoxLayout(self)

		self.label = QtWidgets.QLabel("Attribute Editor:")
		self.layout.addWidget(self.label)

		self.button1 = QtWidgets.QPushButton("Button 1")
		self.layout.addWidget(self.button1)

		self.button2 = QtWidgets.QPushButton("Button 2")
		self.layout.addWidget(self.button2)

		self.setLayout(self.layout)

class EditorRotate(QtWidgets.QWidget):

	def __init__(self, parent):
		super(EditorRotate, self).__init__(parent)

		self.layout = QtWidgets.QVBoxLayout(self)

		self.label = QtWidgets.QLabel("Attribute Editor:")
		self.layout.addWidget(self.label)

		self.button1 = QtWidgets.QPushButton("Button 1")
		self.layout.addWidget(self.button1)

		self.setLayout(self.layout)

class EditorScale(QtWidgets.QWidget):

	def __init__(self, parent):
		super(EditorScale, self).__init__(parent)

		self.layout = QtWidgets.QVBoxLayout(self)

		self.label = QtWidgets.QLabel("Attribute Editor:")
		self.layout.addWidget(self.label)

		self.button1 = QtWidgets.QPushButton("Button 1")
		self.layout.addWidget(self.button1)

		self.button2 = QtWidgets.QPushButton("Button 2")
		self.layout.addWidget(self.button2)

		self.setLayout(self.layout)

class EditorInitial(QtWidgets.QWidget):

	def __init__(self, parent):
		super(EditorInitial, self).__init__(parent)

		self.layout = QtWidgets.QVBoxLayout(self)

		self.lotX = QtWidgets.QHBoxLayout(self)
		self.lotX.addWidget(QtWidgets.QLabel("Lot X: "))
		self.lotX.addWidget(QtWidgets.QLineEdit())
		self.layout.addLayout(self.lotX)

		self.lotY = QtWidgets.QHBoxLayout(self)
		self.lotY.addWidget(QtWidgets.QLabel("Lot Y: "))
		self.lotY.addWidget(QtWidgets.QLineEdit())
		self.layout.addLayout(self.lotY)

		self.lotZ = QtWidgets.QHBoxLayout(self)
		self.lotZ.addWidget(QtWidgets.QLabel("Lot Z: "))
		self.lotZ.addWidget(QtWidgets.QLineEdit())
		self.layout.addLayout(self.lotZ)

		# self.button1 = QtWidgets.QPushButton("Button 1")
		# self.layout.addWidget(self.button1)

		# self.button2 = QtWidgets.QPushButton("Button 2")
		# self.layout.addWidget(self.button2)

		self.setLayout(self.layout)

class EditorMesh(QtWidgets.QWidget):

	def __init__(self, parent):
		super(EditorMesh, self).__init__(parent)

		self.layout = QtWidgets.QVBoxLayout(self)

		self.label = QtWidgets.QLabel("Attribute Editor:")
		self.layout.addWidget(self.label)

		self.button1 = QtWidgets.QPushButton("Button 1")
		self.layout.addWidget(self.button1)

		self.button2 = QtWidgets.QPushButton("Button 2")
		self.layout.addWidget(self.button2)

		self.setLayout(self.layout)

class EditorSplit(QtWidgets.QWidget):

	def __init__(self, parent):
		super(EditorSplit, self).__init__(parent)

		self.layout = QtWidgets.QVBoxLayout(self)

		self.label = QtWidgets.QLabel("Attribute Editor:")
		self.layout.addWidget(self.label)

		self.button1 = QtWidgets.QPushButton("Button 1")
		self.layout.addWidget(self.button1)

		self.button2 = QtWidgets.QPushButton("Button 2")
		self.layout.addWidget(self.button2)

		self.setLayout(self.layout)

