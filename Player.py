from CollideObjectBase import SphereCollideObject
from direct.gui.DirectGui import *
from direct.gui.OnscreenImage import OnscreenImage
from direct.interval.LerpInterval import LerpFunc
from direct.interval.IntervalGlobal import Sequence, Func, Wait
from direct.particles.ParticleEffect import ParticleEffect
from direct.task import Task
from direct.task.Task import TaskManager
from panda3d.core import Loader, NodePath, Vec3, TransparencyAttrib, CollisionHandlerEvent, CollisionTraverser, TextNode, CollisionHandlerPusher
from SpaceJamClasses import Missile
from typing import Callable
# Regex module import for string editing.
import re

class Spaceship(SphereCollideObject):
    def __init__(self, loader: Loader, traverser: CollisionTraverser, taskMgr: TaskManager, pusher: CollisionHandlerPusher,
                accept: Callable[[str, Callable], None], modelPath: str, parentNode: NodePath, nodeName: str,
                texPath: str, posVec: Vec3, scaleVec: float, screen: NodePath):
        super(Spaceship, self).__init__(loader, modelPath, parentNode, nodeName, Vec3(0.25, 0, 0), 1.2, True)
        self.taskMgr = taskMgr
        self.loader = loader
        self.pusher = pusher
        self.accept = accept
        self.render = parentNode
        self.render2d = screen
        self.modelNode.setPos(posVec)
        self.modelNode.setHpr(0, 0, 180)
        self.modelNode.setScale(scaleVec)
        self.modelNode.setName(nodeName)
        self.reloadTime = .25
        self.missileDistance = 4000 # Until the missile exploses.
        self.missileBay = 1 # Only one missile in the missile bay to be launched.
        self.score = 0
        self.font = self.loader.loadFont('./Assets/Fonts/DS-DIGIB.TTF')     
        self.gameOver = False

        self.SetSE()
        self.SetKeyBindings()
        self.taskMgr.add(self.CheckIntervals, 'checkMissiles', 34)
        self.EnableHUD()

        self.cntExplode = 0
        self.explodeIntervals = {}
        self.traverser = traverser
        self.handler = CollisionHandlerEvent()

        # Specifies what to do when a collision event is detected
        self.traverser.addCollider(self.collisionPushNode, self.pusher)
        self.pusher.addCollider(self.collisionPushNode, self.modelNode)
        self.traverser.addCollider(self.collisionNode, self.handler)

        # Display the collisions for debugging purposes
        # self.traverser.showCollisions(self.render)
        # self.collisionNode.show()

        # detect when collisions happen
        self.handler.addInPattern('into')
        self.accept('into', self.HandleInto)

        self.SetParticles()
        self.SetScore()
        self.taskMgr.add(self.UpdateScore, "update-score")
        self.SetDamageScreen()

    def SetDamageScreen(self):      
        # Create a fullscreen white overlay
        self.flash_overlay = OnscreenImage(image="./Assets/Spaceships/white.png", parent=self.render2d)
        self.flash_overlay.setTransparency(TransparencyAttrib.MAlpha)
        self.flash_overlay.setScale(2)  # Cover entire screen
        self.flash_overlay.setColor(1, 1, 1, 0)  # Start fully transparent

    def SetSE(self):
        # Set the sound effects
        self.shootSound = base.loader.loadMusic('./Assets/Spaceships/shooting.mp3')
        self.shootSound.setVolume(0.1)
        self.loadSound = base.loader.loadMusic('./Assets/Spaceships/loading.mp3')
        self.loadSound.setVolume(0.1)
        self.explodeSound = base.loader.loadMusic('./Assets/Spaceships/explosion.mp3')
        self.explodeSound.setVolume(0.1)
        self.damageSound = base.loader.loadMusic('./Assets/Spaceships/damage.mp3')
        self.damageSound.setVolume(0.1)

    def SetKeyBindings(self):
        # All of our key bindings for our spaceship's movement.
        self.accept('w', self.Thrust, [1])
        self.accept('w-up', self.Thrust, [0])
        self.accept('s', self.Drag, [1])
        self.accept('s-up', self.Drag, [0])
        self.accept('arrow_left', self.LeftTurn, [1])
        self.accept('arrow_left-up', self.LeftTurn, [0])
        self.accept('arrow_right', self.RightTurn, [1])
        self.accept('arrow_right-up', self.RightTurn, [0])
        self.accept('arrow_up', self.UpTurn, [1])
        self.accept('arrow_up-up', self.UpTurn, [0])
        self.accept('arrow_down', self.DownTurn, [1])
        self.accept('arrow_down-up', self.DownTurn, [0])
        self.accept('q', self.LeftTilt, [1])
        self.accept('q-up', self.LeftTilt, [0])
        self.accept('e', self.RightTilt, [1])
        self.accept('e-up', self.RightTilt, [0])
        self.accept('f', self.Fire)
        self.accept('m', self.Sound)

    def DisableControls(self):
        self.taskMgr.remove('forward-thrust')
        self.taskMgr.remove('drag')
        self.taskMgr.remove('left-turn')
        self.taskMgr.remove('right-turn')
        self.taskMgr.remove('up-turn')
        self.taskMgr.remove('down-turn')
        self.taskMgr.remove('left')
        self.taskMgr.remove('right')
        self.taskMgr.remove('left-tilt')
        self.taskMgr.remove('right-tilt')
        self.taskMgr.remove('update-score')
        self.taskMgr.remove('checkMissiles')
        base.ignoreAll()

    def Thrust(self, keyDown):
        if keyDown:
            self.taskMgr.add(self.ApplyThrust, 'forward-thrust')
        else:
            self.taskMgr.remove('forward-thrust')

    def ApplyThrust(self, task):
        rate = 20
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
        rate = 20
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
            self.shootSound.play()

            self.traverser.addCollider(currentMissile.collisionNode, self.handler)
        else:
            # If we aren't reloading, we want to start reloading.
            if not self.taskMgr.hasTaskNamed('reload'):
                # print('Initializing reload...')
                # Call the reload method on no delay.
                self.taskMgr.doMethodLater(0, self.Reload, 'reload')
                return Task.cont
    
    def Reload(self, task):
        if task.time > self.reloadTime:
            self.missileBay += 1

            if self.missileBay > 1:
                self.missileBay = 1
            
            self.loadSound.play()
            # print("Reload complete.")
            return Task.done
        
        elif task.time <= self.reloadTime:
            # print("Reload proceeding...")
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
                # print(i + ' has reached the end of its fire solution.')
                
                # We break because when things are deleted from a dictionary, we have to refactor the dictionary so we can reuse it, This is because when we delete things, there's a gap at that point.
                break

        return Task.cont
    
    def EnableHUD(self):
        self.Hud = OnscreenImage(image = "./Assets/Hud/Reticle3b.png", pos = Vec3(0,0,0), scale = 0.1)
        self.Hud.setTransparency(TransparencyAttrib.MAlpha)

    def HandleInto(self, entry):
        fromNode = entry.getFromNodePath().getName()
        # print("fromNode: " + fromNode)
        intoNode = entry.getIntoNodePath().getName()
        # print("intoNode: " + intoNode)
        # print("full intoNode: " + str(base.render.find("**/" + intoNode)))

        intoPosition = Vec3(entry.getSurfacePoint(self.render))

        tempVar = fromNode.split('_')
        # print("tempVar: " + str(tempVar))
        shooter = tempVar[0] # missile-#
        # print("Shooter: " + str(shooter))
        tempVar = intoNode.split('-')
        # print("TempVar1: " + str(tempVar))
        tempVar = intoNode.split('_')
        # print("TempVar2: " + str(tempVar))
        victim = tempVar[0] # ex. drone#
        # print("Victim: " + str(victim))

        pattern = r'[0-9]'

        TargetStrippedString = re.sub(pattern, '', victim)
        ShooterStrippedString = re.sub(pattern, '', shooter)
        allowedStrings = ["Drone", "Drone-BB", "Drone-CD", "Drone-CX", "Drone-CY", "Drone-CZ", "Drone-A", "Drone-B", "Planet", "Space Station"]

        if ShooterStrippedString == "Missile" and TargetStrippedString in allowedStrings:
            # print(victim, ' hit at ', intoPosition)
            self.DestroyObject(victim, intoPosition)
            
            if shooter in Missile.Intervals:
                Missile.Intervals[shooter].finish()
        elif ShooterStrippedString == "Hero" and TargetStrippedString in allowedStrings:
            # print(shooter, ' bumps ', victim)
            self.GetDamage()
            if hasattr(self, "SoundTextObject"):
                self.SoundTextObject.destroy()
            self.textObject.destroy()
            self.DisableControls()
            self.gameOver = True

        # print(shooter + ' is DONE.')

    def DestroyObject(self, hitID, hitPosition):
        # Unity also has a find method, yet it is very inefficient if used anywhere but at the beginning of the program.
        nodeID = self.render.find(hitID)
        self.AddPoints(hitID)
        nodeID.detachNode()

        # Start the explosion.
        self.explodeNode.setPos(hitPosition)
        self.Explode()

    def Explode(self):
        self.cntExplode += 1
        tag = 'particles-' + str(self.cntExplode)

        self.explodeIntervals[tag] = LerpFunc(self.ExplodeLight, duration = 4.0)
        self.explodeIntervals[tag].start()
        self.explodeSound.play()

    def ExplodeLight(self, t):
        if t == 1.0 and self.explodeEffect.isEnabled():
            self.explodeEffect.disable()
        elif t == 0:
            self.explodeEffect.start(self.explodeNode)
    
    def SetParticles(self):
        base.enableParticles()
        self.explodeEffect = ParticleEffect()
        self.explodeEffect.loadConfig('./Assets/Part-Efx/default_efx.ptf')
        self.explodeEffect.setScale(40)
        self.explodeNode = self.render.attachNewNode('ExplosionEffects')

    def AddPoints(self, hitID):
        found_node = self.render.find(hitID)
        self.score += int(found_node.get_python_tag("points"))
        # print("score: " + str(self.score))

    def SetScore(self):
        self.textObject = OnscreenText(
            text='Score: ' +  str(self.score),
            pos=(-0.1, -0.2),
            scale=0.15, 
            fg=(0.31,0.78,0.47,1), 
            bg=(0,0,0,0.9), 
            font=self.font,
            align=TextNode.ARight,
            parent=base.a2dTopRight
        )
    
    def UpdateScore(self, task):
        self.textObject.destroy()
        self.textObject = OnscreenText(
            text='Score: ' +  str(self.score),
            pos=(-0.1, -0.2), 
            scale=0.15, 
            fg=(0.31,0.78,0.47,1), 
            bg=(0,0,0,0.9), 
            font=self.font,
            align=TextNode.ARight,
            parent=base.a2dTopRight
        )
        return task.cont
    
    def Sound(self):
        if self.shootSound.getVolume() > 0:
            self.shootSound.setVolume(0)
            self.loadSound.setVolume(0)
            self.explodeSound.setVolume(0)
            self.SoundTextObject = OnscreenText(
                text='Sound Off',
                pos=(-0.1, 0.1), 
                scale=0.15, 
                fg=(0.22,0.78,0.47,1), 
                bg=(0,0,0,0.9), 
                font=self.font, 
                align=TextNode.ARight,
                parent=base.a2dBottomRight
            )
        else:
            self.shootSound.setVolume(0.1)
            self.loadSound.setVolume(0.1)
            self.explodeSound.setVolume(0.1)
            self.SoundTextObject.destroy()
        return Task.cont

    def GetDamage(self):
        self.DamageEffects()
        if self.shootSound.getVolume() > 0:
            self.damageSound.play()

    def DamageEffects(self):
        self.blink_seq = Sequence(
            *(Func(self.flash_overlay.setColor, 1, 1, 1, 0.8), Wait(0.05),  # Show
              Func(self.flash_overlay.setColor, 1, 1, 1, 0), Wait(0.05)) * 3  # Repeat 3 times
        )

        # Start blinking
        self.blink_seq.start()
        
    def cleanup(self):
        self.modelNode.removeNode()
        Missile.cleanup()