import random
from direct.showbase.ShowBase import ShowBase
from panda3d.core import *
from direct.showbase.Loader import *
import DefensePaths as defensePaths
import SpaceJamClasses
from direct.task import Task

class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        
        # Mouse control.
        base.disableMouse()
        
        self.SetupScene()
        self.SetCamera()
        self.SetKeyBindings()
        
        fullCycle = 60
        for j in range(fullCycle):
            SpaceJamClasses.Drone.droneCount += 1
            nickName = "Drone" + str(SpaceJamClasses.Drone.droneCount)

            self.DrawCloudDefense(self.Planet1, nickName)
            self.DrawBaseballSeams(self.SpaceStation1, nickName, j, fullCycle, 2)
            self.DrawCircleX(self.Hero, nickName, j, fullCycle, 2)
            self.DrawCircleY(self.Hero, nickName, j, fullCycle, 2)
            self.DrawCircleZ(self.Hero, nickName, j, fullCycle, 2)

    def SetupScene(self):
        self.Universe = SpaceJamClasses.Universe(self.loader, "./Assets/Universe/Universe.x", self.render, 'Universe', "./Assets/Universe/starfield-in-blue.jpg", (0, 0, 0), 10000)
        self.Planet1 = SpaceJamClasses.Planet(self.loader, "./Assets/Planets/protoPlanet.x", self.render, 'Planet1', "./Assets/Planets/2k_jupiter.jpg", (-6000, -3000, -800), 250)
        self.Planet2 = SpaceJamClasses.Planet(self.loader, "./Assets/Planets/protoPlanet.x", self.render, 'Planet2', "./Assets/Planets/2k_mars.jpg", (0, 6000, 0), 300)
        self.Planet3 = SpaceJamClasses.Planet(self.loader, "./Assets/Planets/protoPlanet.x", self.render, 'Planet3', "./Assets/Planets/2k_mercury.jpg", (500, -5000, 200), 500)
        self.Planet4 = SpaceJamClasses.Planet(self.loader, "./Assets/Planets/protoPlanet.x", self.render, 'Planet4', "./Assets/Planets/2k_neptune.jpg", (300, 6000, 500), 150)
        self.Planet5 = SpaceJamClasses.Planet(self.loader, "./Assets/Planets/protoPlanet.x", self.render, 'Planet5', "./Assets/Planets/2k_uranus.jpg", (700, -2000, 100), 500)
        self.Planet6 = SpaceJamClasses.Planet(self.loader, "./Assets/Planets/protoPlanet.x", self.render, 'Planet6', "./Assets/Planets/2k_venus_atmosphere.jpg", (0, -900, -1400), 700)
        self.SpaceStation1 = SpaceJamClasses.SpaceStation(self.loader, "./Assets/Space Station/spaceStation.x", self.render, 'Space Station', "./Assets/Space Station/SpaceStation1_Dif2.png", (1500, 1000, -100), 40)
        self.Hero = SpaceJamClasses.Spaceship(self.loader, "./Assets/Spaceships/Dumbledore.x", self.render, 'Hero', "./Assets/Spaceships/spacejet_C.png", Vec3(800, 1800, -50), 50)

    def DrawBaseballSeams(self, centralObject, droneName, step, numSeams, radius = 1):
        unitVec = defensePaths.BaseballSeams(step, numSeams, B = 0.4)
        unitVec.normalize()
        position = unitVec * radius * 250 + centralObject.modelNode.getPos()
        SpaceJamClasses.Drone(self.loader, "./Assets/Drone Defender/DroneDefender.obj", self.render, droneName, "./Assets/Drone Defender/octotoad1_auv.png", position, 5)

    def DrawCloudDefense(self, centralObject, droneName):
        unitVec = defensePaths.Cloud()
        unitVec.normalize()
        position = unitVec * 500 + centralObject.modelNode.getPos()
        SpaceJamClasses.Drone(self.loader, "./Assets/Drone Defender/DroneDefender.obj", self.render, droneName, "./Assets/Drone Defender/octotoad1_auv.png", position, 10)
    
    def DrawCircleX(self, centralObject, droneName, step, numSeams, radius = 1):
        unitVec = defensePaths.CircleX(step, numSeams)
        unitVec.normalize()
        position = unitVec * radius * 250 + centralObject.modelNode.getPos()
        color = 255, 0, 0, 1 # red
        SpaceJamClasses.Drone(self.loader, "./Assets/Drone Defender/DroneDefender.obj", self.render, droneName, "./Assets/Drone Defender/octotoad1_auv.png", position, 5, color)

    def DrawCircleY(self, centralObject, droneName, step, numSeams, radius = 1):
        unitVec = defensePaths.CircleY(step, numSeams)
        unitVec.normalize()
        position = unitVec * radius * 250 + centralObject.modelNode.getPos()
        color = 0, 255, 0, 1 # green
        SpaceJamClasses.Drone(self.loader, "./Assets/Drone Defender/DroneDefender.obj", self.render, droneName, "./Assets/Drone Defender/octotoad1_auv.png", position, 5, color)

    def DrawCircleZ(self, centralObject, droneName, step, numSeams, radius = 1):
        unitVec = defensePaths.CircleZ(step, numSeams)
        unitVec.normalize()
        position = unitVec * radius * 250 + centralObject.modelNode.getPos()
        color = 0, 0, 255, 1 # blue
        SpaceJamClasses.Drone(self.loader, "./Assets/Drone Defender/DroneDefender.obj", self.render, droneName, "./Assets/Drone Defender/octotoad1_auv.png", position, 5, color)
    
    def SetKeyBindings(self):
        # All of our key bindings for our spaceship's movement.
        self.accept('w', self.Thrust, [1])
        self.accept('w-up', self.Thrust, [0])
        self.accept('s', self.Drag, [1])
        self.accept('s-up', self.Drag, [0])
        self.accept('a', self.LeftTurn, [1])
        self.accept('a-up', self.LeftTurn, [0])
        self.accept('d', self.RightTurn, [1])
        self.accept('d-up', self.RightTurn, [0])
        self.accept('arrow_up', self.UpTurn, [1])
        self.accept('arrow_up-up', self.UpTurn, [0])
        self.accept('arrow_down', self.DownTurn, [1])
        self.accept('arrow_down-up', self.DownTurn, [0])
        self.accept('q', self.LeftTilt, [1])
        self.accept('q-up', self.LeftTilt, [0])
        self.accept('e', self.RightTilt, [1])
        self.accept('e-up', self.RightTilt, [0])
    
    def Thrust(self, keyDown):
        if keyDown:
            self.taskMgr.add(self.ApplyThrust, 'forward-thrust')
        else:
            self.taskMgr.remove('forward-thrust')

    def ApplyThrust(self, task):
        rate = 5
        trajectory = self.render.getRelativeVector(self.Hero.modelNode, Vec3.forward())
        trajectory.normalize()
        self.Hero.modelNode.setFluidPos(self.Hero.modelNode.getPos() + trajectory * rate )
        return Task.cont

    def Drag(self, keyDown):
        if keyDown:
            self.taskMgr.add(self.ApplyDrag, 'drag')
        else:
            self.taskMgr.remove('drag')

    def ApplyDrag(self, task):
        rate = 5
        trajectory = self.render.getRelativeVector(self.Hero.modelNode, Vec3.forward())
        trajectory.normalize()
        self.Hero.modelNode.setFluidPos(self.Hero.modelNode.getPos() - trajectory * rate )
        return Task.cont

    def LeftTurn(self, keyDown):
        if keyDown:
            self.taskMgr.add(self.ApplyLeftTurn, 'left-turn')
        else:
            self.taskMgr.remove('left-turn')

    def ApplyLeftTurn(self, task):
        # Half a degree every frame.
        rate = .5
        self.Hero.modelNode.setH(self.Hero.modelNode.getH() + rate)
        return Task.cont
    
    def RightTurn(self, keyDown):
        if keyDown:
            self.taskMgr.add(self.ApplyRightTurn, 'right-turn')
        else:
            self.taskMgr.remove('right-turn')

    def ApplyRightTurn(self, task):
        # Half a degree every frame.
        rate = .5
        self.Hero.modelNode.setH(self.Hero.modelNode.getH() - rate)
        return Task.cont

    def UpTurn(self, keyDown):
        if keyDown:
            self.taskMgr.add(self.ApplyUpTurn, 'up-turn')
        else:
            self.taskMgr.remove('up-turn')

    def ApplyUpTurn(self, task):
        # Half a degree every frame.
        rate = .5
        self.Hero.modelNode.setP(self.Hero.modelNode.getP() + rate)
        return Task.cont

    def DownTurn(self, keyDown):
        if keyDown:
            self.taskMgr.add(self.ApplyDownTurn, 'down-turn')
        else:
            self.taskMgr.remove('down-turn')

    def ApplyDownTurn(self, task):
        # Half a degree every frame.
        rate = .5
        self.Hero.modelNode.setP(self.Hero.modelNode.getP() - rate)
        return Task.cont

    def LeftTilt(self, keyDown):
        if keyDown:
            self.taskMgr.add(self.ApplyLeftTilt, 'left-tilt')
        else:
            self.taskMgr.remove('left-tilt')

    def ApplyLeftTilt(self, task):
        # Half a degree every frame.
        rate = .5
        self.Hero.modelNode.setR(self.Hero.modelNode.getR() + rate)
        return Task.cont

    def RightTilt(self, keyDown):
        if keyDown:
            self.taskMgr.add(self.ApplyRightTilt, 'right-tilt')
        else:
            self.taskMgr.remove('right-tilt')

    def ApplyRightTilt(self, task):
        # Half a degree every frame.
        rate = .5
        self.Hero.modelNode.setR(self.Hero.modelNode.getR() - rate)
        return Task.cont
    
    def SetCamera(self):
        self.disableMouse()
        self.camera.reparentTo(self.Hero.modelNode)
        self.camera.setFluidPos(0, 1, 0)

app = MyApp()
app.run()
