import os
import re
import json

from Qt import QtGui, QtCore, QtWidgets
import nodz_main

from DerivationTree import NodeType

class GUI(QtWidgets.QMainWindow):

	def __init__(self, type, nodz):
		"""
		Initialize the graphics view.

		"""
		super(GUI, self).__init__()

		self.layout = QtWidgets.QVBoxLayout(self)
		self.layout.addWidget(WidgetSplit(self))
		self.layout.addWidget(WidgetSplit(self))

		#self.nodz = nodz_main.Nodz(self)
		self.layout.addWidget(nodz)

		self.window = QtWidgets.QWidget(self)
		self.window.setLayout(self.layout)

		self.setCentralWidget(self.window)

		self.setWindowTitle("ProBuilder")


	def changeWidget(self, nodeType):
		self.setWindowTitle(NodeType.getString(nodeType))

		if nodeType == NodeType.init:
			self.form_widget = WidgetInitial(self)
		elif nodeType == NodeType.translate:
			self.form_widget = WidgetTranslate(self)
		elif nodeType == NodeType.rotate:
			self.form_widget = WidgetRotate(self)
		elif nodeType == NodeType.scale:
			self.form_widget = WidgetScale(self)
		elif nodeType == NodeType.split:
			self.form_widget = WidgetSplit(self)
		elif nodeType == NodeType.mesh:
			self.form_widget = WidgetMesh(self)

		self.setCentralWidget(self.form_widget)

class WidgetSplit(QtWidgets.QWidget):

	def __init__(self, parent):
		super(WidgetSplit, self).__init__(parent)

		self.layout = QtWidgets.QVBoxLayout(self)

		self.button1 = QtWidgets.QPushButton("Button 1")
		self.layout.addWidget(self.button1)

		self.button2 = QtWidgets.QPushButton("Button 2")
		self.layout.addWidget(self.button2)

		self.setLayout(self.layout)

class WidgetTranslate(QtWidgets.QWidget):

	def __init__(self, parent):
		super(WidgetTranslate, self).__init__(parent)

		self.layout = QtWidgets.QVBoxLayout(self)

		self.button1 = QtWidgets.QPushButton("Button 1")
		self.layout.addWidget(self.button1)

		self.button2 = QtWidgets.QPushButton("Button 2")
		self.layout.addWidget(self.button2)

		self.setLayout(self.layout)

class WidgetRotate(QtWidgets.QWidget):

	def __init__(self, parent):
		super(WidgetRotate, self).__init__(parent)

		self.layout = QtWidgets.QVBoxLayout(self)

		self.button1 = QtWidgets.QPushButton("Button 1")
		self.layout.addWidget(self.button1)

		self.button2 = QtWidgets.QPushButton("Button 2")
		self.layout.addWidget(self.button2)

		self.setLayout(self.layout)

class WidgetScale(QtWidgets.QWidget):

	def __init__(self, parent):
		super(WidgetScale, self).__init__(parent)

		self.layout = QtWidgets.QVBoxLayout(self)

		self.button1 = QtWidgets.QPushButton("Button 1")
		self.layout.addWidget(self.button1)

		self.button2 = QtWidgets.QPushButton("Button 2")
		self.layout.addWidget(self.button2)

		self.setLayout(self.layout)

class WidgetInitial(QtWidgets.QWidget):

	def __init__(self, parent):
		super(WidgetInitial, self).__init__(parent)

		self.layout = QtWidgets.QVBoxLayout(self)

		self.button1 = QtWidgets.QPushButton("Button 1")
		self.layout.addWidget(self.button1)

		self.button2 = QtWidgets.QPushButton("Button 2")
		self.layout.addWidget(self.button2)

		self.setLayout(self.layout)

class WidgetMesh(QtWidgets.QWidget):

	def __init__(self, parent):
		super(WidgetMesh, self).__init__(parent)

		self.layout = QtWidgets.QVBoxLayout(self)

		self.button1 = QtWidgets.QPushButton("Button 1")
		self.layout.addWidget(self.button1)

		self.button2 = QtWidgets.QPushButton("Button 2")
		self.layout.addWidget(self.button2)

		self.setLayout(self.layout)

