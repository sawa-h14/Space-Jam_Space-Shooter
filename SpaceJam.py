from direct.gui.DirectGui import *
from direct.showbase.Loader import *
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from panda3d.core import CollisionTraverser, TransparencyAttrib, CollisionHandlerPusher, WindowProperties
import DefensePaths as defensePaths
import SpaceJamClasses
import sys
import Player
from direct.interval.IntervalGlobal import Sequence, Func, Wait

class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        # Mouse control
        base.disableMouse()

        # Check collisions 
        self.cTrav = CollisionTraverser()
        self.cTrav.traverse(self.render)
        self.pusher = CollisionHandlerPusher()
        self.font = self.loader.loadFont('./Assets/Fonts/DS-DIGIB.TTF')

        self.SetStartMenu()

        # Enable window resizing
        props = WindowProperties()
        props.setFixedSize(False)  # Allow resizing
        base.win.requestProperties(props)

        # Listen for window resize events
        self.accept("window-event", self.WindowResize)

    def SetStartMenu(self):
        # Make a black backdrop that covers the whole window
        self.titleMenuBackdrop = DirectFrame(frameColor = (0, 0, 0, 1),
                                     frameSize = (-1, 1, -1, 1),
                                     parent = render2d)
        # The menu itself
        self.titleMenu = DirectFrame(frameColor = (1, 1, 1, 0))

        title = DirectLabel(text = "Space Jam",
                            scale = 0.4,
                            pos = (0, 0, 0.5),
                            parent = self.titleMenu,
                            relief = None,
                            text_font = self.font,
                            text_fg=(0.31,0.78,0.47,1))
        self.title2 = DirectLabel(text = "Press 'S' to start",
                            scale = 0.2,
                            pos = (0, 0, 0.1),
                            parent = self.titleMenu,
                            relief = None,
                            text_font = self.font,
                            text_fg=(0.31,0.78,0.47,1))
        
        self.title2.isVisible = True        
        self.taskMgr.doMethodLater(0.8, self.FlickerStartText, "FlickerStartText")
        self.accept('s', self.StartGame)

    def FlickerStartText(self, task):
        if self.title2.isVisible:
            self.title2.show()
        else:
            self.title2.hide()
        self.title2.isVisible = not self.title2.isVisible  # Toggle visibility
        return task.again  # Repeat task

    def StartGame(self):
        self.taskMgr.remove('FlickerStartText')
        startSound = base.loader.loadMusic('./Assets/Spaceships/start.mp3')
        startSound.setVolume(0.2)
        startSound.play()
        self.SetGameOverScreen()
        self.ignoreAll()

        # Start game, enable controls, remove menu text
        self.titleMenu.hide()
        self.titleMenuBackdrop.hide()
        self.SetupScene()
        self.SetCamera()
        
        self.fullCycle = 60
        for j in range(self.fullCycle):
            SpaceJamClasses.Drone.droneCount += 1
            nickName = "Drone" + str(SpaceJamClasses.Drone.droneCount)

            self.DrawCloudDefense(self.Planet1, nickName)
            self.DrawBaseballSeams(self.SpaceStation1, nickName, j, self.fullCycle, 2)
            self.DrawCircleX(self.Planet2, nickName, j, self.fullCycle, 2)
            self.DrawCircleY(self.Planet2, nickName, j, self.fullCycle, 2)
            self.DrawCircleZ(self.Planet2, nickName, j, self.fullCycle, 2)

        # wait until game over
        self.taskMgr.add(self.WaitGameOver, "WaitGameOver")
        self.accept("window-event", self.WindowResize)

    def SetupScene(self):
        self.Universe = SpaceJamClasses.Universe(self.loader, "./Assets/Universe/Universe.x", self.render, 'Universe', "./Assets/Universe/starfield-in-blue.jpg", (0, 0, 0), 10000)
        self.Planet1 = SpaceJamClasses.Planet(self.loader, "./Assets/Planets/protoPlanet.x", self.render, 'Planet1', "./Assets/Planets/2k_jupiter.jpg", (-6000, -3000, -800), 250, points=50)
        self.Planet2 = SpaceJamClasses.Planet(self.loader, "./Assets/Planets/protoPlanet.x", self.render, 'Planet2', "./Assets/Planets/2k_mars.jpg", (0, 6000, 0), 300, points=50)
        self.Planet3 = SpaceJamClasses.Planet(self.loader, "./Assets/Planets/protoPlanet.x", self.render, 'Planet3', "./Assets/Planets/2k_mercury.jpg", (500, -5000, 200), 500)
        self.Planet4 = SpaceJamClasses.Planet(self.loader, "./Assets/Planets/protoPlanet.x", self.render, 'Planet4', "./Assets/Planets/2k_neptune.jpg", (600, 6000, 500), 150, points=200)
        self.Planet5 = SpaceJamClasses.Planet(self.loader, "./Assets/Planets/protoPlanet.x", self.render, 'Planet5', "./Assets/Planets/2k_uranus.jpg", (700, -2000, 100), 500)
        self.Planet6 = SpaceJamClasses.Planet(self.loader, "./Assets/Planets/protoPlanet.x", self.render, 'Planet6', "./Assets/Planets/2k_venus_atmosphere.jpg", (0, -900, -1400), 700)
        self.SpaceStation1 = SpaceJamClasses.SpaceStation(self.loader, "./Assets/Space Station/spaceStation.x", self.render, 'Space Station', "./Assets/Space Station/SpaceStation1_Dif2.png", (1500, 1000, -100), 40, points=500)
        self.Hero = Player.Spaceship(
            self.loader, self.cTrav, self.taskMgr, self.pusher, self.accept, "./Assets/Spaceships/Dumbledore.x", self.render,
            'Hero', "./Assets/Spaceships/spacejet_C.png", (800, 1800, -50), 50, self.render2d)
        self.Sentinail1 = SpaceJamClasses.Orbiter(self.loader, self.taskMgr, "./Assets/Drone Defender/DroneDefender.obj", self.render, "Drone-A", 20.0, "./Assets/Drone Defender/octotoad1_auv.png", self.Planet5, 900, "MLB", self.Hero, color=(1, 1, 0.4, 1), velocity= 0.1, points=500)
        self.Sentinail2 = SpaceJamClasses.Orbiter(self.loader, self.taskMgr, "./Assets/Drone Defender/DroneDefender.obj", self.render, "Drone-B", 20.0, "./Assets/Drone Defender/octotoad1_auv.png", self.Planet2, 900, "Cloud", self.Hero, color=(1, 0.2, 0.8, 1), velocity= 0.5, points=500)
        self.Sentinail3 = SpaceJamClasses.Orbiter(self.loader, self.taskMgr, "./Assets/Drone Defender/DroneDefender.obj", self.render, "Drone-C", 10.0, "./Assets/Drone Defender/octotoad1_auv.png", self.Planet4, 900, "MLB", self.Hero, color=(0.6, 1, 0.2, 1), velocity= 0.2, points=500)
        self.Sentinail4 = SpaceJamClasses.Orbiter(self.loader, self.taskMgr, "./Assets/Drone Defender/DroneDefender.obj", self.render, "Drone-D", 10.0, "./Assets/Drone Defender/octotoad1_auv.png", self.Planet2, 900, "Cloud", self.Hero, color=(0.4, 1, 1, 1), points=500)

    def DrawBaseballSeams(self, centralObject, droneName, step, numSeams, radius = 1):
        unitVec = defensePaths.BaseballSeams(step, numSeams, B = 0.4)
        unitVec.normalize()
        position = unitVec * radius * 250 + centralObject.modelNode.getPos()
        SpaceJamClasses.Drone(self.loader, "./Assets/Drone Defender/DroneDefender.obj", self.render, droneName + "-BB", "./Assets/Drone Defender/octotoad1_auv.png", position, 5)

    def DrawCloudDefense(self, centralObject, droneName):
        unitVec = defensePaths.Cloud()
        unitVec.normalize()
        position = unitVec * 500 + centralObject.modelNode.getPos()
        SpaceJamClasses.Drone(self.loader, "./Assets/Drone Defender/DroneDefender.obj", self.render, droneName + "-CD", "./Assets/Drone Defender/octotoad1_auv.png", position, 10)
    
    def DrawCircleX(self, centralObject, droneName, step, numSeams, radius = 1):
        unitVec = defensePaths.CircleX(step, numSeams)
        unitVec.normalize()
        position = unitVec * radius * 250 + centralObject.modelNode.getPos()
        color = 1, 0, 0, 1 # red
        SpaceJamClasses.Drone(self.loader, "./Assets/Drone Defender/DroneDefender.obj", self.render, droneName + "-CX", "./Assets/Drone Defender/octotoad1_auv.png", position, 5, color)

    def DrawCircleY(self, centralObject, droneName, step, numSeams, radius = 1):
        unitVec = defensePaths.CircleY(step, numSeams)
        unitVec.normalize()
        position = unitVec * radius * 250 + centralObject.modelNode.getPos()
        color = 0, 1, 0, 1 # green
        SpaceJamClasses.Drone(self.loader, "./Assets/Drone Defender/DroneDefender.obj", self.render, droneName + "-CY", "./Assets/Drone Defender/octotoad1_auv.png", position, 5, color)

    def DrawCircleZ(self, centralObject, droneName, step, numSeams, radius = 1):
        unitVec = defensePaths.CircleZ(step, numSeams)
        unitVec.normalize()
        position = unitVec * radius * 250 + centralObject.modelNode.getPos()
        color = 0, 0, 1, 1 # blue
        SpaceJamClasses.Drone(self.loader, "./Assets/Drone Defender/DroneDefender.obj", self.render, droneName + "-CZ", "./Assets/Drone Defender/octotoad1_auv.png", position, 5, color)
    
    def SetCamera(self):
        self.disableMouse()
        self.camera.reparentTo(self.Hero.modelNode)
        self.camera.setFluidPos(0, 0.5, 0)

    def SetGameOverScreen(self):
        self.gameOverScreen = DirectDialog(
            frameSize = (-1.5, 1.5, -1, 1),
            fadeScreen = 0.8,
            relief = DGG.FLAT,
            frameTexture = "./Assets/Window/freepik__background__22475.png")
        self.gameOverScreen.setTransparency(TransparencyAttrib.MAlpha)
        # Hide the screen until the player loses
        self.gameOverScreen.hide()

        label = DirectLabel(text = "Game Over",
                    parent = self.gameOverScreen,
                    scale = 0.2,
                    pos = (0, 0, 0.3),
                    frameColor = (0.5, 0.5, 0.5, 1),
                    text_font = self.font,
                    relief = None,
                    text_fg=(0.31,0.78,0.47,1))
        
        self.finalScoreLabel = DirectLabel(text = "",
                                   parent = self.gameOverScreen,
                                   scale = 0.1,
                                   pos = (0, 0, 0.2),
                                   frameColor = (0.5, 0.5, 0.5, 1),
                                   text_font = self.font,
                                   relief = None,
                                   text_fg=(0.31,0.78,0.47,1))
        
    def WaitGameOver(self, task):
        if self.Hero.gameOver:
            if self.gameOverScreen.isHidden():
                # Show the game-over screen, and set the
                # text of the "finalScoreLabel" object to
                # reflect the player's score.
                self.gameOverScreen.show()
                self.finalScoreLabel["text"] = "Final score: " + str(self.Hero.score)
                self.finalScoreLabel["frameColor"] = (0.5, 0.5, 0.5, 1)
                self.finalScoreLabel.setText()

                self.restartText = DirectLabel(text = "Press  'R'  to restart",
                            scale = 0.12,
                            pos = (0, 0, -0.1),
                            parent = self.gameOverScreen,
                            text_font = self.font,
                            frameColor = (0.5, 0.5, 0.5, 1),
                            relief = None,
                            text_fg=(0.31,0.78,0.47,1))
                
                self.quitText = DirectLabel(text = "Press  'q'  to quit",
                            scale = 0.12,
                            pos = (0, 0, -0.25),
                            parent = self.gameOverScreen,
                            text_font = self.font,
                            frameColor = (0.5, 0.5, 0.5, 1),
                            relief = None,
                            text_fg=(0.31,0.78,0.47,1))
                self.restartText.isVisible = True

                self.taskMgr.doMethodLater(0.8, self.FlickerEndText, "FlickerEndText")
                self.accept('r', self.RestartGame)
                self.accept('q', self.QuitGqme)
                self.accept("window-event", self.WindowResize)
                
        return task.cont  # Keep waiting
    
    def FlickerEndText(self, task):
        if self.restartText.isVisible:
            self.restartText.show()
            self.quitText.show()
        else:
            self.restartText.hide()
            self.quitText.hide()
        self.restartText.isVisible = not self.restartText.isVisible  # Toggle visibility
        return task.again  # Repeat task

    def RestartGame(self):
        self.taskMgr.remove('FlickerEndText')
        self.gameOverScreen.destroy()
        self.taskMgr.remove('WaitGameOver')
        self.cleanup()
        self.StartGame()

    def cleanup(self):
        self.Sentinail1.cleanup()
        self.Sentinail2.cleanup()
        self.Sentinail3.cleanup()
        self.Sentinail4.cleanup()
        self.Hero.cleanup()
        self.SpaceStation1.cleanup()
        self.Planet1.cleanup()
        self.Planet2.cleanup()
        self.Planet3.cleanup()
        self.Planet4.cleanup()
        self.Planet5.cleanup()
        self.Planet6.cleanup()
        SpaceJamClasses.Drone.cleanup(self.fullCycle)

    def WindowResize(self, window):
        width = base.win.getXSize()  # Get new width
        height = base.win.getYSize()  # Get new height
        # print(f"Window resized: {width}x{height}")
        new_aspect_ratio = width / height
        base.camLens.setAspectRatio(new_aspect_ratio)
    
    def QuitGqme(self):
        sys.exit()

app = MyApp()
app.run()
