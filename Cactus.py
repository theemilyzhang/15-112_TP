class Cactus(object):
    price = 20
    def __init__(self, location):
        self.location = location #tuple
        self.radius = 30
        self.name = "cactus" #TODO: probably don't need this?
        self.damage = 1
        self.defaultCoolDown = 10
        self.currentCoolDown = self.defaultCoolDown - 1