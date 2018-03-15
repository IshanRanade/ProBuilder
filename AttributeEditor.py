import os
import re
import json

from Qt import QtGui, QtCore, QtWidgets

from DerivationTree import NodeType

class AttributeEditor(QtWidgets.QMainWindow):

	def __init__(self, type):
		"""
		Initialize the graphics view.

		"""
		super(AttributeEditor, self).__init__()
		self.form_widget = WidgetSplit(self)
		self.setCentralWidget(self.form_widget)

		self.setWindowTitle(NodeType.getString(type))

	def changeWidget(self, nodeType):
		self.setWindowTitle(NodeType.getString(nodeType))

		if nodeType == NodeType.init:
			self.form_widget = WidgetSplit(self)
		elif nodeType == NodeType.translate:
			self.form_widget = WidgetTranslate(self)
		elif nodeType == NodeType.rotate:
			self.form_widget = WidgetSplit(self)
		elif nodeType == NodeType.scale:
			self.form_widget = WidgetSplit(self)
		elif nodeType == NodeType.split:
			self.form_widget = WidgetSplit(self)

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

