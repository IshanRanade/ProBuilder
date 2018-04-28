import numpy as np
import maya.cmds as cmds
import maya.mel as mel
import LinAlg
import math

class NodeType(object):
    translate = 0
    rotate = 1
    scale = 2
    init = 3
    split = 4
    mesh = 5
    splitSegment = 6
    repeat = 7

    @staticmethod
    def getString(nodeType):
        if nodeType == 0:
            return "Translate"
        if nodeType == 1:
            return "Rotate"
        if nodeType == 2:
            return "Scale"
        if nodeType == 3:
            return "Initial"
        if nodeType == 4:
            return "Split"
        if nodeType == 5:
            return "Mesh"
        if nodeType == 6:
            return "Split Segment"
        if nodeType == 7:
            return "Repeat"
          

class Node(object):
    
    def __init__(self, nodeType, nodz, nodzToNode, isPlug, isSocket):
        self.nodeType = nodeType
        self.children = []
        self.nodzNode = nodz.createNode(name=NodeType.getString(nodeType), preset='node_preset_1', position=None)
        self.nodz = nodz
        self.graph = None
        
        nodz.createAttribute(node=self.nodzNode, name='Node', index=-1, preset='attr_preset_1', plug=isPlug, socket=isSocket, dataType=str)

        nodzToNode[self.nodzNode] = self

class InitialNode(Node):

    def __init__(self, nodz, nodzToNode):
        super(InitialNode, self).__init__(NodeType.init, nodz, nodzToNode, True, False)

        self.lotX = 50
        self.lotY = 50
        self.lotZ = 50

class TranslateNode(Node):

    def __init__(self, nodz, nodzToNode):
        super(TranslateNode, self).__init__(NodeType.translate, nodz, nodzToNode, True, True)

        self.translateX = 0
        self.translateY = 0
        self.translateZ = 0

class RotateNode(Node):

    def __init__(self, nodz, nodzToNode):
        super(RotateNode, self).__init__(NodeType.rotate, nodz, nodzToNode, True, True)

        self.rotateX = 0
        self.rotateY = 0
        self.rotateZ = 0

class ScaleNode(Node):

    def __init__(self, nodz, nodzToNode):
        super(ScaleNode, self).__init__(NodeType.scale, nodz, nodzToNode, True, True)

        self.scaleX = 1
        self.scaleY = 1
        self.scaleZ = 1

class SplitNode(Node):

    def __init__(self, nodz, nodzToNode):
        super(SplitNode, self).__init__(NodeType.split, nodz, nodzToNode, False, True)

        self.segmentCount = 0
        #Directions => 0=X, 1=Y, 2=Z
        self.segmentDirection = 0

  
class SplitSegmentNode(Node):

    def __init__(self, nodz, nodzToNode):
        self.nodeType = NodeType.splitSegment
        self.children = []
        self.nodz = nodz
        self.graph = None

        self.proportion = 1
        
class MeshNode(Node):

    is_set=None
    name=None

    def __init__(self, nodz, nodzToNode):
        super(MeshNode, self).__init__(NodeType.mesh, nodz, nodzToNode, False, True)

        self.is_set = False

class RepeatNode(Node):

    def __init__(self, nodz, nodzToNode):
        super(RepeatNode, self).__init__(NodeType.repeat, nodz, nodzToNode, True, True)

        self.direction = 0

class Graph(object):

    def __init__(self, nodz):
        self.nodzToNode = {}
        self.nodes = set()
        self.nodz = nodz
        self.root = InitialNode(self.nodz, self.nodzToNode)
        self.nodes.add(self.root)

    def getNodeFromNodz(self, nodzNode):
        return self.nodzToNode[nodzNode]

    def addNode(self, nodeType):
        newNode = None
        if(nodeType == NodeType.translate):
            newNode = TranslateNode(self.nodz, self.nodzToNode)
        elif(nodeType == NodeType.rotate):
            newNode = RotateNode(self.nodz, self.nodzToNode)
        elif(nodeType == NodeType.scale):
            newNode = ScaleNode(self.nodz, self.nodzToNode)
        elif(nodeType == NodeType.split):
            newNode = SplitNode(self.nodz, self.nodzToNode)
        elif(nodeType == NodeType.splitSegment):
            newNode = SplitSegmentNode(self.nodz, self.nodzToNode)
        elif(nodeType == NodeType.mesh):
            newNode = MeshNode(self.nodz, self.nodzToNode)
        elif(nodeType == NodeType.repeat):
            newNode = RepeatNode(self.nodz, self.nodzToNode)

        self.nodes.add(newNode)

        return newNode

    def createEdge(self, srcNodzNode, srcPlugName, destNodzNode, dstSocketName):
        if self.nodzToNode[srcNodzNode].nodeType == NodeType.split and "Segment" in srcPlugName:
            self.nodzToNode[srcNodzNode].children[int(srcPlugName[len(srcPlugName)-1])].children.append(self.nodzToNode[destNodzNode])
        else:
            self.nodzToNode[srcNodzNode].children.append(self.nodzToNode[destNodzNode])

    def createManualEdge(self, srcNode, srcAttrib, destNode, destAttrib):
        #srcNode.children.append(destNode)
        self.nodz.createConnection(srcNode.nodzNode, srcAttrib, destNode.nodzNode, destAttrib)

    def printGraph(self):
        queue = [self.root]

        while len(queue) > 0:
            curr = queue.pop()

            if len(curr.children) == 0:
                print NodeType.getString(curr.nodeType)

                attrsParent = vars(curr)
                attrsChild = vars(child)

                print ', '.join("%s: %s" % item for item in attrsParent.items())
                print ', '.join("%s: %s" % item for item in attrsChild.items()) 

                print ""

            for child in curr.children:
                print NodeType.getString(curr.nodeType) + " -> " + NodeType.getString(child.nodeType)

                attrsParent = vars(curr)
                attrsChild = vars(child)

                print ', '.join("%s: %s" % item for item in attrsParent.items())
                print ', '.join("%s: %s" % item for item in attrsChild.items())

                queue.append(child)

                print ""

        print "----------------"

    def generateMesh(self):
        # First delete all the existing geometry in the scene
        transforms = cmds.ls(tr=True)
        polyMeshes = cmds.filterExpand(transforms, sm=12)
        cmds.select(polyMeshes, r=True)
        cmds.delete()

        self.generateMeshHelper(self.root, np.array([0,0,0]), np.array([1,0,0,0]), np.array([1,1,1]))

    def generateMeshHelper(self, node, translate, rotate, scale):

        is_gen=False 

        if node.nodeType == NodeType.translate:
            translate = np.add(translate, np.array([node.translateX, node.translateY, node.translateZ]))
        elif node.nodeType == NodeType.rotate:
            rotate = LinAlg.quaternion_multiply(rotate, LinAlg.quaternion_from_euler(node.rotateX, node.rotateY, node.rotateZ,'sxyz'))
        elif node.nodeType == NodeType.scale:
            scale = np.multiply(scale, np.array([node.scaleX, node.scaleY, node.scaleZ]))
        elif node.nodeType == NodeType.mesh:
            if(node.is_set):
                cmds.select( cmds.duplicate(node.name) )
                #Reset translate
                cmds.setAttr('%s.translateX'% node.name,0)
                cmds.setAttr('%s.translateY'% node.name,0)
                cmds.setAttr('%s.translateZ'% node.name,0)
                
                ax, ay, az = LinAlg.euler_from_quaternion(rotate)
                ax = ax* 180.0/math.pi
                ay = ay* 180.0/math.pi
                az = az* 180.0/math.pi
                
                #cmds.scale(scale[0], scale[1], scale[2])
                cmds.move(translate[0],translate[1],translate[2])
                cmds.rotate(ax,ay,az)
            else:
                cmds.polyCube()
                ax, ay, az = LinAlg.euler_from_quaternion(rotate)
                ax = ax* 180.0/math.pi
                ay = ay* 180.0/math.pi
                az = az* 180.0/math.pi
                cmds.scale(scale[0], scale[1], scale[2])
                cmds.move(translate[0],translate[1],translate[2])
                cmds.rotate(ax,ay,az)

            is_gen=True
            
        elif node.nodeType == NodeType.split:
                        
            total_weight = 0.0
            
            
            for child in node.children:
                total_weight = total_weight+child.proportion
                    
            #segment directions
            #X dir
            if node.segmentDirection%3 == 0:

                start=translate[0]-scale[0]/2.0
                
                for child in node.children:

                    new_scaleX=scale[0]*child.proportion / total_weight
                    new_scaleY=scale[1]
                    new_scaleZ = scale[2]

                    new_transX=start + new_scaleX/2.0
                    new_transY=translate[1]
                    new_transZ=translate[2]

                    start=start+ abs(new_scaleX)
            
                    self.generateMeshHelper(child, np.array([new_transX,new_transY,new_transZ]), np.array(rotate), np.array([new_scaleX,new_scaleY,new_scaleZ]))

            #Y dir          
            elif node.segmentDirection%3 == 1:

                start=translate[1]-scale[1]/2.0
                
                for child in node.children:

                    new_scaleX=scale[0]
                    new_scaleY=scale[1]*child.proportion / total_weight
                    new_scaleZ = scale[2]

                    new_transY=start + new_scaleY/2.0
                    new_transX=translate[0]
                    new_transZ=translate[2]

                    start=start+ abs(new_scaleY)
            
                    self.generateMeshHelper(child, np.array([new_transX,new_transY,new_transZ]), np.array(rotate), np.array([new_scaleX,new_scaleY,new_scaleZ]))

            #Z dir            
            elif node.segmentDirection%3 == 2:
                    
                start=translate[2]-scale[2]/2.0
                
                for child in node.children:

                    new_scaleX=scale[0]
                    new_scaleY=scale[1]
                    new_scaleZ = scale[2]*child.proportion / total_weight
            
                    new_transZ=start + new_scaleZ/2.0
                    new_transX=translate[0]
                    new_transY=translate[1]

                    start=start+ abs(new_scaleZ)
            
                    self.generateMeshHelper(child, np.array([new_transX,new_transY,new_transZ]), np.array(rotate), np.array([new_scaleX,new_scaleY,new_scaleZ]))
                            
            #jump out of function at here.
            return 0

        for child in node.children:
            self.generateMeshHelper(child, np.array(translate), np.array(rotate), np.array(scale))

        if not node.children:
            #
            if not is_gen:
                ax, ay, az = LinAlg.euler_from_quaternion(rotate,'sxyz')
                ax = ax* 180.0/math.pi
                ay = ay* 180.0/math.pi
                az = az* 180.0/math.pi
                cmds.polyCube()
                cmds.scale(scale[0], scale[1], scale[2])
                cmds.move(translate[0],translate[1],translate[2])
                cmds.rotate(ax,ay,az)
