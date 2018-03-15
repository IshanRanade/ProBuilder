import os
import re
import json

from Qt import QtGui, QtCore, QtWidgets

class AttributeEditor(QtWidgets.QMainWindow):

	def __init__(self, parent):
		"""
		Initialize the graphics view.

		"""
		super(AttributeEditor, self).__init__(parent)
		self.form_widget = FormWidget(self)
		self.setCentralWidget(self.form_widget) 

	

class FormWidget(QtWidgets.QWidget):

	def __init__(self, parent):
		super(FormWidget, self).__init__(parent)

		self.layout = QtWidgets.QVBoxLayout(self)

		self.button1 = QtWidgets.QPushButton("Button 1")
		self.layout.addWidget(self.button1)

		self.button2 = QtWidgets.QPushButton("Button 2")
		self.layout.addWidget(self.button2)

		self.setLayout(self.layout)

