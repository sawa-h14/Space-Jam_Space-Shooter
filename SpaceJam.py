import random
from direct.showbase.ShowBase import ShowBase

class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.SetupScene()

    def SetupScene(self):
        self.Universe = self.loader.loadModel("./Assets/Universe/Universe.x")
        self.Universe.reparentTo(self.render)
        # set the environment scale so that it looks like infinity
        self.Universe.setScale(15000)
        # disable all textures at this node and below
        self.Universe.setTextureOff(1)
        # replace the texture
        tex = self.loader.loadTexture("./Assets/Universe/starfield-in-blue.jpg")
        self.Universe.setTexture(tex, 1)

        # add planets
        self.planetsImg = ("2k_jupiter.jpg", "2k_mars.jpg", "2k_mercury.jpg", "2k_neptune.jpg", "2k_uranus.jpg", "2k_venus_atmosphere.jpg")
        for index, imgFile in enumerate(self.planetsImg):
            setattr(self, f"Planet{index}", self.loader.loadModel("./Assets/Planets/protoPlanet.x"))
            planet = getattr(self, f"Planet{index}")
            planet.reparentTo(self.render)
            # create the scale and the position randomly
            pos_x = index * 400 - 1000
            pos_y = random.randrange(3000, 4000, 50)
            pos_z = random.randrange(-1000, 1000, 50)
            scale = random.randrange(50, 200)
            planet.setPos(pos_x, pos_y, pos_z)
            planet.setScale(scale)
            # replace the texture
            tex2 = self.loader.loadTexture(f"./Assets/Planets/{imgFile}")
            planet.setTexture(tex2, 1)        

        # add a spaceship
        self.Ship = self.loader.loadModel("./Assets/Spaceships/Dumbledore.x")
        self.Ship.reparentTo(self.render)
        self.Ship.setPos(0, 1500, 0)
        self.Ship.setHpr(-90, 90, 90)
        self.Ship.setScale(50)

        # add a space station
        self.Station = self.loader.loadModel("./Assets/Space Station/spaceStation.x")
        self.Station.reparentTo(self.render)
        self.Station.setScale(10)
        self.Station.setPos(0, 1000, -200)
        self.Station.setHpr(-90, 90, 45)

app = MyApp()
app.run()
