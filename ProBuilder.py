import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx
from Qt import QtCore, QtWidgets
import nodz_main
from Graph import NodeType
from Graph import Node
from GUI import GUI
from Controller import Controller
import sys

class MyCommandClass( OpenMayaMPx.MPxCommand ):
    
    def __init__(self):
        ''' Constructor. '''
        pass
    
    def doIt(self, args):
        ''' Command execution. '''
        pass

kPluginCmdName = "ProBuilder"
cmdCreator = MyCommandClass()

# Initialize the script plug-in
def initializePlugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin(mobject)
    try:
        mplugin.registerCommand( kPluginCmdName, cmdCreator )
    except:
        sys.stderr.write( "Failed to register command: %s\n" % kPluginCmdName )
        raise

# Uninitialize the script plug-in
def uninitializePlugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin(mobject)
    try:
        mplugin.deregisterCommand( kPluginCmdName )
    except:
        sys.stderr.write( "Failed to unregister command: %s\n" % kPluginCmdName )
        raise

try:
    app = QtWidgets.QApplication([])
except:
    # I guess we're running somewhere that already has a QApp created
    app = None

controller = Controller()

if app:
    # command line stand alone test... run our own event loop
    app.exec_()
