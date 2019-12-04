class Balloon(object):
    def __init__(self, speed=5, hp=1, color="red"):
        self.speed = speed
        self.hp = hp
        self.color = color
        self.position = (-1, -1) #in pixels, aka starts off-screen
        self.distanceTraveled = 0
        self.radius = 10
        self.coins = 1
        self.angleIncrement = 1/16

class FastBalloon(Balloon):
    def __init__(self):
        super().__init__()
        self.color = "blue"


fast = FastBalloon()

print (fast.color)