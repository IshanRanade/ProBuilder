import maya.OpenMayaMPx as OpenMayaMPx
import sys
from Qt import QtCore, QtWidgets

import nodz_main
import Graph
import Controller
import GUI
import LinAlg

reload(nodz_main)
reload(Graph)
reload(GUI)
reload(Controller)
reload(LinAlg)


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

# Create an instance of a controller, which stores the application
controller = Controller.Controller()

if app:
    # command line stand alone test... run our own event loop
    app.exec_()
