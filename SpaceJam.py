import random
from direct.showbase.ShowBase import ShowBase
from panda3d.core import *
from direct.showbase.Loader import *
import DefensePaths as defensePaths
import SpaceJamClasses

class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.SetupScene()

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

app = MyApp()
app.run()
