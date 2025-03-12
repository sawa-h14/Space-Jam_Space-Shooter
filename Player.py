from CollideObjectBase import SphereCollideObject
from direct.gui.OnscreenImage import OnscreenImage
from direct.task import Task
from direct.task.Task import TaskManager
from SpaceJamClasses import Missile
from panda3d.core import Loader, NodePath, TransformState, Mat4, Vec3, TransparencyAttrib
from typing import Callable

class Spaceship(SphereCollideObject):
    def __init__(self, loader: Loader, taskMgr: TaskManager, accept: Callable[[str, Callable], None], modelPath: str, parentNode: NodePath, nodeName: str, texPath: str, posVec: Vec3, scaleVec: float):
        super(Spaceship, self).__init__(loader, modelPath, parentNode, nodeName, Vec3(0.25, 0, 0), 1.1)
        self.taskMgr = taskMgr
        self.loader = loader
        self.accept = accept
        self.render = parentNode
        self.modelNode.setPos(posVec)
        self.modelNode.setHpr(0, 0, 180)
        self.modelNode.setScale(scaleVec)
        self.modelNode.setName(nodeName)
        self.reloadTime = .25
        self.missileDistance = 4000 # Until the missile exploses.
        self.missileBay = 1 # Only one missile in the missile bay to be launched.

        # disable all textures at this node and below
        self.modelNode.setTextureOff(1)

        tex = loader.loadTexture(texPath)
        self.modelNode.setTexture(tex, 1)

        self.SetKeyBindings()
        self.taskMgr.add(self.CheckIntervals, 'checkMissiles', 34)
        self.EnableHUB()

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
        # self.accept('arrow_left', self.Left, [1])
        # self.accept('arrow_left-up', self.Left, [0])
        # self.accept('arrow_right', self.Right, [1])
        # self.accept('arrow_right-up', self.Right, [0])
        self.accept('q', self.LeftTilt, [1])
        self.accept('q-up', self.LeftTilt, [0])
        self.accept('e', self.RightTilt, [1])
        self.accept('e-up', self.RightTilt, [0])
        self.accept('f', self.Fire)
    
    def Thrust(self, keyDown):
        if keyDown:
            self.taskMgr.add(self.ApplyThrust, 'forward-thrust')
        else:
            self.taskMgr.remove('forward-thrust')

    def ApplyThrust(self, task):
        rate = 10
        trajectory = self.render.getRelativeVector(self.modelNode, Vec3.forward())
        trajectory.normalize()
        self.modelNode.setFluidPos(self.modelNode.getPos() + trajectory * rate )
        return Task.cont

    def Drag(self, keyDown):
        if keyDown:
            self.taskMgr.add(self.ApplyDrag, 'drag')
        else:
            self.taskMgr.remove('drag')

    def ApplyDrag(self, task):
        rate = 10
        trajectory = self.render.getRelativeVector(self.modelNode, Vec3.forward())
        trajectory.normalize()
        self.modelNode.setFluidPos(self.modelNode.getPos() - trajectory * rate )
        return Task.cont

    def LeftTurn(self, keyDown):
        if keyDown:
            self.taskMgr.add(self.ApplyLeftTurn, 'left-turn')
        else:
            self.taskMgr.remove('left-turn')

    def ApplyLeftTurn(self, task):
        # Half a degree every frame.
        rate = .5
        self.modelNode.setH(self.modelNode, rate)
        return Task.cont
    
    def RightTurn(self, keyDown):
        if keyDown:
            self.taskMgr.add(self.ApplyRightTurn, 'right-turn')
        else:
            self.taskMgr.remove('right-turn')

    def ApplyRightTurn(self, task):
        # Half a degree every frame.
        rate = .5
        self.modelNode.setH(self.modelNode, - rate)
        return Task.cont

    def UpTurn(self, keyDown):
        if keyDown:
            self.taskMgr.add(self.ApplyUpTurn, 'up-turn')
        else:
            self.taskMgr.remove('up-turn')

    def ApplyUpTurn(self, task):
        # Half a degree every frame.
        rate = .5
        self.modelNode.setP(self.modelNode, rate)
        return Task.cont

    def DownTurn(self, keyDown):
        if keyDown:
            self.taskMgr.add(self.ApplyDownTurn, 'down-turn')
        else:
            self.taskMgr.remove('down-turn')

    def ApplyDownTurn(self, task):
        # Half a degree every frame.
        rate = .5
        self.modelNode.setP(self.modelNode, - rate)
        return Task.cont

    def Left(self, keyDown):
        if keyDown:
            self.taskMgr.add(self.ApplyLeft, 'left')
        else:
            self.taskMgr.remove('left')

    def ApplyLeft(self, task):
        rate = 1
        self.modelNode.setX(self.modelNode, - rate)
        return Task.cont

    def Right(self, keyDown):
        if keyDown:
            self.taskMgr.add(self.ApplyRight, 'right')
        else:
            self.taskMgr.remove('right')

    def ApplyRight(self, task):
        rate = 1
        self.modelNode.setX(self.modelNode, rate)
        return Task.cont

    def LeftTilt(self, keyDown):
        if keyDown:
            self.taskMgr.add(self.ApplyLeftTilt, 'left-tilt')
        else:
            self.taskMgr.remove('left-tilt')

    def ApplyLeftTilt(self, task):
        # Half a degree every frame.
        rate = .5
        self.modelNode.setR(self.modelNode, rate)
        return Task.cont

    def RightTilt(self, keyDown):
        if keyDown:
            self.taskMgr.add(self.ApplyRightTilt, 'right-tilt')
        else:
            self.taskMgr.remove('right-tilt')

    def ApplyRightTilt(self, task):
        # Half a degree every frame.
        rate = .5
        self.modelNode.setR(self.modelNode, -rate)
        return Task.cont
    
    def Fire(self):
        if self.missileBay:
            travRate = self.missileDistance
            aim = self.render.getRelativeVector(self.modelNode, Vec3.forward()) # the direction the spaceship is facing.
            # Normalizing a vector makes it consistant all the time.
            aim.normalize()
            fireSolution = aim * travRate
            inFront = aim * 150
            travVec = fireSolution + self.modelNode.getPos()
            self.missileBay -= 1
            tag = 'Missile' + str(Missile.missileCount)

            posVec = self.modelNode.getPos() + inFront # Spawn the missile in front of the nose of the ship.

            # Create our missile.
            currentMissile = Missile(self.loader, './Assets/Phaser/phaser.egg', self.render, tag, posVec, 4.0)

            # "fluid = 1" makes collision be checked between the last interval and this interval to make sure there's nothing in-between both checks that wasn't hit.
            Missile.Intervals[tag] = currentMissile.modelNode.posInterval(2.0, travVec, startPos = posVec, fluid = 1)

            Missile.Intervals[tag].start()
        else:
            # If we aren't reloading, we want to start reloading.
            if not self.taskMgr.hasTaskNamed('reload'):
                print('Initializing reload...')
                # Call the reload method on no delay.
                self.taskMgr.doMethodLater(0, self.Reload, 'reload')
                return Task.cont
    
    def Reload(self, task):
        if task.time > self.reloadTime:
            self.missileBay += 1

            if self.missileBay > 1:
                self.missileBay = 1
            
            print("Reload complete.")
            return Task.done
        
        elif task.time <= self.reloadTime:
            print("Reload proceeding...")
            return Task.cont

    def CheckIntervals(self, task):
        for i in Missile.Intervals:
            #isPlaying returns true or false to see if the missile has gotten to the end of its path.
            if not Missile.Intervals[i].isPlaying():
                # If its path is done, we get rid of everything to do with that missile.
                Missile.cNodes[i].detachNode()
                Missile.fireModels[i].detachNode()
                del Missile.Intervals[i]
                del Missile.fireModels[i]
                del Missile.cNodes[i]
                del Missile.CollisionSolids[i]

                # debug
                print(i + ' has reached the end of its fire solution.')
                
                # We break because when things are deleted from a dictionary, we have to refactor the dictionary so we can reuse it, This is because when we delete things, there's a gap at that point.
                break

        return Task.cont
    
    def EnableHUB(self):
        self.Hud = OnscreenImage(image = "./Assets/Hud/Reticle3b.png", pos = Vec3(0,0,0), scale = 0.1)
        self.Hud.setTransparency(TransparencyAttrib.MAlpha)

