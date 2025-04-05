from direct.interval.IntervalGlobal import Sequence
from direct.showbase.Loader import *
from direct.showbase.ShowBase import ShowBase
from direct.task.Task import TaskManager
from CollideObjectBase import *
from panda3d.core import *
import DefensePaths as defensePaths

class Universe(InverseSphereCollideObject):
    def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath, nodeName: str, texPath: str, posVec: Vec3,
                  scaleVec: float):
        super(Universe, self).__init__(loader, modelPath, parentNode, nodeName, Vec3(0, 0, 0), 0.9)
        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)

        # disable all textures at this node and below
        self.modelNode.setTextureOff(1)

        tex = loader.loadTexture(texPath)
        self.modelNode.setTexture(tex, 1)
    def cleanup(self):
        self.modelNode.removeNode()

class Planet(SphereCollideObject):
    def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath, nodeName: str, texPath: str, posVec: Vec3,
                  scaleVec: float, points: int = 100):
        super(Planet, self).__init__(loader, modelPath, parentNode, nodeName, Vec3(0, 0, 0), 1.2)
        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)

        # disable all textures at this node and below
        self.modelNode.setTextureOff(1)

        tex = loader.loadTexture(texPath)
        self.modelNode.setTexture(tex, 1)
        self.modelNode.set_python_tag("points", points)
    
    def cleanup(self):
        self.modelNode.removeNode()

class SpaceStation(CapsuleCollidableObject):
    def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath, nodeName: str, texPath: str, posVec: Vec3,
                  scaleVec: float, points: int = 100):
        super(SpaceStation, self).__init__(loader, modelPath, parentNode, nodeName, 1, -2, 0, 1, -2, -10, 12)
        self.collisionNode.setHpr(0, 0, 45)
        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)

        # disable all textures at this node and below
        self.modelNode.setTextureOff(1)

        tex = loader.loadTexture(texPath)
        self.modelNode.setTexture(tex, 1)
        self.modelNode.set_python_tag("points", points)

    def cleanup(self):
        self.modelNode.removeNode()

class Drone(SphereCollideObject):
    # How many drones have been spawned.
    droneCount = 0
    def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath, nodeName: str, texPath: str, posVec: Vec3,
                  scaleVec: float, color: Vec4 = (0,0,0,0), points: int = 200):
        super(Drone, self).__init__(loader, modelPath, parentNode, nodeName, Vec3(0, 0, 0), 4.5)
        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)

        # disable all textures at this node and below
        self.modelNode.setTextureOff(1)

        tex = loader.loadTexture(texPath)
        self.modelNode.setTexture(tex, 1)

        if color != (0,0,0,0): 
            self.modelNode.setColor(color)
        self.modelNode.set_python_tag("points", points)
    
    def cleanup(fullCycle):
        Drone.droneCount = 0
        for j in range(fullCycle):
            j += 1
            Drone.delNode("**/Drone"+ str(j) + "-BB")
            Drone.delNode("**/Drone"+ str(j) + "-CD")
            Drone.delNode("**/Drone"+ str(j) + "-CX")
            Drone.delNode("**/Drone"+ str(j) + "-CY")
            Drone.delNode("**/Drone"+ str(j) + "-CZ")

    def delNode(nodeName):
        node = base.render.find(nodeName)
        if not node.isEmpty():
            node.removeNode() 

class Missile(SphereCollideObject):
    fireModels = {}
    cNodes = {}
    CollisionSolids = {}
    Intervals = {}
    missileCount = 0

    def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath, nodeName: str, texPath: str, posVec: Vec3,
                  scaleVec: float = 1.0):
        super(Missile, self).__init__(loader, modelPath, parentNode, nodeName, Vec3(0, 0, 0), 3.0, isMissile=True)
        self.modelNode.setScale(scaleVec)
        self.modelNode.setPos(posVec)

        Missile.missileCount += 1
        Missile.fireModels[nodeName] = self.modelNode
        Missile.cNodes[nodeName] = self.collisionNode

        # We retrive the solid for our collisionNode.
        Missile.CollisionSolids[nodeName] = self.collisionNode.node().getSolid(0)
        # For debugging purposes, we show our missiles’ colliders and messages.
        Missile.cNodes[nodeName].show() 
        # print("Fire torpedo #" + str(Missile.missileCount))

    def cleanup():
        Missile.fireModels = {}
        Missile.cNodes = {}
        Missile.CollisionSolids = {}
        Missile.Intervals = {}
        Missile.missileCount = 0

class Orbiter(SphereCollideObject):
    numOrbits = 0
    cloudTimer = 240
    def __init__(self, loader: Loader, taskMgr: TaskManager, modelPath: str, parentNode: NodePath, nodeName: str,
                  scaleVec: Vec3, texPath:str, centralObject: PlacedObject, orbitRadius: float, orbitType: str, starinAt: Vec3, color: Vec4 = (0,0,0,0), velocity: float= 0.005, points: int = 200):
        super(Orbiter, self,).__init__(loader, modelPath, parentNode, nodeName, Vec3(0, 0, 0), 3.2)
        self.taskMgr = taskMgr
        self.velocity = velocity
        self.orbitType = orbitType
        self.modelNode.setScale(scaleVec)

        # disable all textures at this node and below
        self.modelNode.setTextureOff(1)

        tex = loader.loadTexture(texPath)
        self.modelNode.setTexture(tex, 1)

        if color != (0,0,0,0): 
            self.modelNode.setColor(color)
        self.modelNode.set_python_tag("points", points)

        self.orbitObject = centralObject
        self.orbitRadius = orbitRadius
        self.starinAt = starinAt
        Orbiter.numOrbits += 1

        self.cloudClock = 0

        self.taskFlag = "Traveler-" + str(Orbiter.numOrbits)
        taskMgr.add(self.Orbit, self.taskFlag)

    def Orbit(self, task):
        if self.orbitType == "MLB":
            positionVec = defensePaths.BaseballSeams(task.time * self.velocity, self.numOrbits, 2.0)
            self.modelNode.setPos(positionVec * self.orbitRadius + self.orbitObject.modelNode.getPos())

        elif self.orbitType == "Cloud":
            if self.cloudClock < Orbiter.cloudTimer:
                self.cloudClock += 1
            else:
                self.cloudClock = 0
                positionVec = defensePaths.Cloud()
                self.modelNode.setPos(positionVec * self.orbitRadius + self.orbitObject.modelNode.getPos())

        self.modelNode.lookAt(self.starinAt.modelNode)
        return task.cont
    
    def cleanup(self):
        Orbiter.numOrbits = 0
        self.taskMgr.remove(self.taskFlag)
        self.modelNode.removeNode()

class Wanderer(SphereCollideObject):
    numWanderers = 0
    def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath, nodeName: str,
                  scaleVec: Vec3, texPath:str, staringAt: Vec3, pathway:list, color: Vec4 = (0,0,0,0), points: int = 200):
        super(Wanderer, self,).__init__(loader, modelPath, parentNode, nodeName, Vec3(0, 0, 0), 3.2)
        self.modelNode.setScale(scaleVec)

        # disable all textures at this node and below
        self.modelNode.setTextureOff(1)

        tex = loader.loadTexture(texPath)
        self.modelNode.setTexture(tex, 1)

        if color != (0,0,0,0): 
            self.modelNode.setColor(color)
        self.modelNode.set_python_tag("points", points)

        posInterval0 = self.modelNode.posInterval(20, pathway[1], startPos = pathway[0])
        posInterval1 = self.modelNode.posInterval(20, pathway[2], startPos = pathway[1])
        posInterval2 = self.modelNode.posInterval(20, pathway[3], startPos = pathway[2])
        self.travelRoute = Sequence(posInterval0, posInterval1, posInterval2, name = "Traveler-" +  str(Wanderer.numWanderers))
        self.travelRoute.loop()

        self.starinAt = staringAt
        Wanderer.numWanderers += 1

    def cleanup(self):
        Wanderer.numWanderers = 0
        self.modelNode.removeNode()

class ApproachingDrone(SphereCollideObject):
    numDrones = 0
    def __init__(self, loader: Loader, taskMgr: TaskManager,
                modelPath: str, parentNode: NodePath, nodeName: str,
                scaleVec: Vec3, texPath:str, targetObject: PlacedObject, posVec: Vec3 = Vec3(0, 0, 0),  color: Vec4 = (0,0,0,0), points: int = 200):
        super(ApproachingDrone, self,).__init__(loader, modelPath, parentNode, nodeName, Vec3(0, 0, 0), 3.2)
        self.modelNode.setScale(scaleVec)
        self.targetObject = targetObject
        self.lastUpdateTime = 0
        self.updateInterval = 10  # seconds
        self.velocity = 5
        self.taskMgr = taskMgr
        self.playerPos = self.targetObject.modelNode.getPos()
        self.modelNode.setPos(posVec)
        self.droneCurrentPos = self.modelNode.getPos()
        self.direction = self.playerPos - self.droneCurrentPos
        self.direction.normalize()

        # disable all textures at this node and below
        self.modelNode.setTextureOff(1)

        tex = loader.loadTexture(texPath)
        self.modelNode.setTexture(tex, 1)

        if color != (0,0,0,0): 
            self.modelNode.setColor(color)
        self.modelNode.set_python_tag("points", points)

        ApproachingDrone.numDrones += 1

        self.taskFlag = "TravelerTowardPlayer-" + str(ApproachingDrone.numDrones)
        self.taskMgr.add(self.headToObject, self.taskFlag)

    def headToObject(self, task):
        current_time = task.time
        self.droneCurrentPos = self.modelNode.getPos()
        if current_time - self.lastUpdateTime >= self.updateInterval:
            self.playerPos = self.targetObject.modelNode.getPos()
            self.direction = self.playerPos - self.droneCurrentPos
            self.direction.normalize()

        self.modelNode.setPos(self.droneCurrentPos + Vec3(
            self.velocity * self.direction.getX(),
            self.velocity * self.direction.getY(),
            self.velocity * self.direction.getZ()))
        return task.cont
    
    def cleanup(self):
        ApproachingDrone.numDrones = 0
        self.taskMgr.remove(self.taskFlag)
        self.modelNode.removeNode()
