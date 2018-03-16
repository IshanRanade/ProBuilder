from Qt import QtCore, QtWidgets
import nodz_main
from DerivationTree import NodeType
from DerivationTree import Node
from GUI import GUI
from Controller import Controller

try:
    app = QtWidgets.QApplication([])
except:
    # I guess we're running somewhere that already has a QApp created
    app = None

controller = Controller()

if app:
    # command line stand alone test... run our own event loop
    app.exec_()
