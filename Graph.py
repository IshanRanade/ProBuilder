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
        self.parent = None
        
        nodz.createAttribute(node=self.nodzNode, name='Node', index=-1, preset='attr_preset_1', plug=isPlug, socket=isSocket, dataType=str)

        nodzToNode[self.nodzNode] = self

class InitialNode(Node):

    def __init__(self, nodz, nodzToNode):
        super(InitialNode, self).__init__(NodeType.init, nodz, nodzToNode, True, False)

        self.lotX = 10
        self.lotY = 10
        self.lotZ = 10

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
        self.nodzNode = None
        self.children = []
        self.nodz = nodz
        self.graph = None
        self.parent = None

        self.idx = None
        self.proportion = 1
        
class MeshNode(Node):

    def __init__(self, nodz, nodzToNode):
        super(MeshNode, self).__init__(NodeType.mesh, nodz, nodzToNode, False, True)

        self.isSet = False
        self.filePath = None

class RepeatNode(Node):

    count = None
    percentage = None

    def __init__(self, nodz, nodzToNode):
        super(RepeatNode, self).__init__(NodeType.repeat, nodz, nodzToNode, True, True)

        self.direction = 0
        self.count = 5
        self.percentage = 20.0

class Graph(object):

    mesh_ID = 0

    def __init__(self, nodz):
        self.nodzToNode = {}
        self.nodes = set()
        self.nodz = nodz
        self.root = InitialNode(self.nodz, self.nodzToNode)
        self.nodes.add(self.root)
        file_ID = 0

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
        elif(nodeType == NodeType.init):
            newNode = InitialNode(self.nodz, self.nodzToNode)

        self.nodes.add(newNode)

        return newNode

    def createEdge(self, srcNodzNode, srcPlugName, destNodzNode, dstSocketName):
        if self.nodzToNode[srcNodzNode].nodeType == NodeType.split and "Segment" in srcPlugName:
            self.nodzToNode[srcNodzNode].children[int(srcPlugName[len(srcPlugName)-1])].children.append(self.nodzToNode[destNodzNode])
            self.nodzToNode[destNodzNode].parent = self.nodzToNode[srcNodzNode].children[int(srcPlugName[len(srcPlugName)-1])]
        else:
            self.nodzToNode[srcNodzNode].children.append(self.nodzToNode[destNodzNode])
            self.nodzToNode[destNodzNode].parent = self.nodzToNode[srcNodzNode]

    def createManualEdge(self, srcNode, srcAttrib, destNode, destAttrib):
        self.nodz.createConnection(srcNode.nodzNode, srcAttrib, destNode.nodzNode, destAttrib)
        destNode.parent = srcNode

    def printGraph(self):
        queue = [self.root]

        while len(queue) > 0:
            curr = queue.pop()

            if len(curr.children) == 0:
                print NodeType.getString(curr.nodeType)

                attrsParent = vars(curr)

                print ', '.join("%s: %s" % item for item in attrsParent.items())

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
        self.file_ID = 0

        self.generateMeshHelper(self.root, np.array([0.0,0.0,0.0]), np.array([1.0,0.0,0.0,0.0]), 
            np.array([1.0*self.root.lotX, 1.0*self.root.lotY, 1.0*self.root.lotZ]))

    def generateMeshHelper(self, node, translate, rotate, scale):

        # Translate Node
        if node.nodeType == NodeType.translate:
            translate = np.add(translate, np.array([node.translateX, node.translateY, node.translateZ]))
        # Rotate Node
        elif node.nodeType == NodeType.rotate:
            rotate = LinAlg.quaternion_multiply(rotate, LinAlg.quaternion_from_euler(node.rotateX, node.rotateY, node.rotateZ,'sxyz'))
        # Scale Node
        elif node.nodeType == NodeType.scale:
            scale = np.multiply(scale, np.array([node.scaleX, node.scaleY, node.scaleZ]))
        # Mesh Node
        elif node.nodeType == NodeType.mesh:

            cmds.select( clear=True )
                        
            if node.isSet:

                cmds.select( clear=True )
                
                #NEW
                path = "C:\\Users\\Administrator\\Desktop\\Models\\" + node.filePath + ".ma"
                
                cmds.file(path, i=True, namespace=node.filePath + str(self.mesh_ID), mergeNamespacesOnClash=True)
                selection = cmds.ls(node.filePath+ str(self.mesh_ID)+":*", type="mesh")

                for item in selection:
                
                    cmds.select(item)
                    ax, ay, az = LinAlg.euler_from_quaternion(rotate)
                    
                    ax = ax * 180.0 / math.pi
                    ay = ay * 180.0 / math.pi
                    az = az * 180.0 / math.pi

                    cmds.scale(scale[0], scale[1], scale[2])
                    cmds.move(translate[0] + 0.5 * scale[0],translate[1] + 0.5 * scale[1],translate[2] + 0.5 * scale[2])
                    cmds.rotate(ax,ay,az)
                    
                cmds.select( clear=True )
                self.mesh_ID +=1;
            else:
                cmds.polyCube()
                ax, ay, az = LinAlg.euler_from_quaternion(rotate)

                ax = ax * 180.0 / math.pi
                ay = ay * 180.0 / math.pi
                az = az * 180.0 / math.pi

                cmds.scale(scale[0], scale[1], scale[2])
                cmds.move(translate[0] + 0.5 * scale[0],translate[1] + 0.5 * scale[1],translate[2] + 0.5 * scale[2])
                cmds.rotate(ax,ay,az)

        # Repeat Node

        #NEW!
        elif node.nodeType == NodeType.repeat:
            if len(node.children) > 0:
                #maxRange = min(int(node.count), int(100.0 / (1.0 * node.percentage)))
                maxRange = int(node.count)
                
                for i in range(0, maxRange):

                    percentage = 100.0 / float(node.count)

                    rot_dir = np.array([0,0,0,1])
                    rot_dir[node.direction] = scale[node.direction]

                    # In fact we need to translate rotate to eular angles....FxxK!
                    ax, ay, az = LinAlg.euler_from_quaternion(rotate)
                    # Compute Rotate Matrix
                    R = LinAlg.euler_matrix(ax,ay,az,'sxyz')
                    # Rotate the scaled direction
                    rot_dir = np.dot(R , rot_dir)

                    tempTranslate = np.array(translate)
                    tempTranslate[0] += rot_dir[0] * i * (1.0 * percentage / 100.0)
                    tempTranslate[1] += rot_dir[1] * i * (1.0 * percentage / 100.0)
                    tempTranslate[2] += rot_dir[2] * i * (1.0 * percentage / 100.0)

                    tempScale = np.array(scale)
                    tempScale[node.direction] = scale[node.direction] * (1.0 * percentage / 100.0)


                    for child in node.children:
                        self.generateMeshHelper(child, np.array(tempTranslate), np.array(rotate), np.array(tempScale))

            return
        # Split Segment Node
        elif node.nodeType == NodeType.splitSegment:
            totalWeight = 0.0
            prevWeight = 0.0

            for i in range(0, len(node.parent.children)):
                child = node.parent.children[i]

                totalWeight += 1.0 * child.proportion
                
                if i < node.idx:
                    prevWeight += 1.0 * child.proportion

            # Supports any rotation
            rot_dir = np.array([0,0,0,1])
            rot_dir[node.parent.segmentDirection] = scale[node.parent.segmentDirection]
            # In fact we need to translate rotate to eular angles....FxxK!
            ax, ay, az = LinAlg.euler_from_quaternion(rotate)
            # Compute Rotate Matrix
            R = LinAlg.euler_matrix(ax,ay,az,'sxyz')
            # Rotate the scaled direction
            rot_dir = np.dot(R , rot_dir)

            translate[0] += (1.0 * rot_dir[0] * prevWeight) / (1.0 * totalWeight)
            translate[1] += (1.0 * rot_dir[1] * prevWeight) / (1.0 * totalWeight)
            translate[2] += (1.0 * rot_dir[2] * prevWeight) / (1.0 * totalWeight)
            
            #translate[node.parent.segmentDirection] += (1.0 * scale[node.parent.segmentDirection] * prevWeight) / (1.0 * totalWeight)
            scale[node.parent.segmentDirection] *= (1.0 * node.proportion / totalWeight)
        # Split Node
        elif node.nodeType == NodeType.split:
            pass

        for child in node.children:
            self.generateMeshHelper(child, np.array(translate), np.array(rotate), np.array(scale))
