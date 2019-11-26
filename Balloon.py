class Balloon(object):
    def __init__(self, speed=5, hp=1, color="red"):
        self.speed = speed
        self.hp = hp
        self.color = color
        self.position = (-1, -1) #in pixels, aka starts off-screen
        self.distanceTraveled = 0
        self.radius = 10
        self.coins = 1