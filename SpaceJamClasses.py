from direct.showbase.Loader import *
from direct.showbase.ShowBase import ShowBase
from CollideObjectBase import *
from panda3d.core import *

class Universe(InverseSphereCollideObject):
    def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath, nodeName: str, texPath: str, posVec: Vec3, scaleVec: float):
        super(Universe, self).__init__(loader, modelPath, parentNode, nodeName, Vec3(0, 0, 0), 0.9)
        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)

        # disable all textures at this node and below
        self.modelNode.setTextureOff(1)

        tex = loader.loadTexture(texPath)
        self.modelNode.setTexture(tex, 1)

class Planet(SphereCollideObject):
    def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath, nodeName: str, texPath: str, posVec: Vec3, scaleVec: float):
        super(Planet, self).__init__(loader, modelPath, parentNode, nodeName, Vec3(0, 0, 0), 1.1)
        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)

        # disable all textures at this node and below
        self.modelNode.setTextureOff(1)

        tex = loader.loadTexture(texPath)
        self.modelNode.setTexture(tex, 1)

class SpaceStation(CapsuleCollidableObject):
    def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath, nodeName: str, texPath: str, posVec: Vec3, scaleVec: float):
        super(SpaceStation, self).__init__(loader, modelPath, parentNode, nodeName, 1, -2, 0, 1, -2, -10, 12)
        self.collisionNode.setHpr(0, 0, 45)
        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)

        # disable all textures at this node and below
        self.modelNode.setTextureOff(1)

        tex = loader.loadTexture(texPath)
        self.modelNode.setTexture(tex, 1)

class Drone(SphereCollideObject):
    # How many drones have been spawned.
    droneCount = 0
    def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath, nodeName: str, texPath: str, posVec: Vec3, scaleVec: float, color: Vec4 = (0,0,0,0)):
        super(Drone, self).__init__(loader, modelPath, parentNode, nodeName, Vec3(0, 0, 0), 1.8)
        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)

        # disable all textures at this node and below
        self.modelNode.setTextureOff(1)

        tex = loader.loadTexture(texPath)
        self.modelNode.setTexture(tex, 1)
        if color != (0,0,0,0): 
            self.modelNode.setColor(color)
