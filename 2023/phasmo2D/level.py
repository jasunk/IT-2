import pygame as py
import camera

class Thing(py.sprite.Sprite):
    def __init__(self, type, pos):
        super().__init__()
        self.type = type
        self.pos = pos

    def draw(self, surf,camera):
        self.image = py.image.load("sprites/blomst.png")
        surf.blit(self.image, (self.pos[0]+camera.getPos()[0], self.pos[1]+camera.getPos()[1]))
    def interract(self):
        mixer = py.mixer
        mixer.init()
        mixer.Channel(1).play(py.mixer.Sound("sounds/house/Can_clink_4.wav"))
        print("interracted with blomst")

class Level():
    def __init__(self):
        self.things = [Thing(1) for x in range(5)]
    def draw(self,plane, camera):
        for thing in self.things:
            thing.draw(plane, camera)

class Room():
    def __init__(self, name, pos, scale,  floorColor, furniture):
        self.name = name
        self.pos = pos
        self.scale = scale

        self.floorColor = floorColor
        self.furniture = furniture
    def collisions(self):
        return [self.pos, self.scale]
    def draw(self,plane, cam):
        py.draw.rect(plane, self.floorColor, py.Rect(self.pos[0]+cam.getPos()[0], self.pos[1]+cam.getPos()[1], self.scale[0], self.scale[1]))
        for thing in ((self.furniture)):
            thing.draw(plane,cam)

class RoomCollection():
    def __init__(self, levelList, plane, cam):
        self.levelList = levelList
        self.cam = cam
        self.plane = plane
    def collisionFind(self):
        collisionList = []
        for room in self.levelList:

            for collision in room.collisions():

                collisionList.append(collision)
        return collisionList
    def draw(self):
        for room in self.levelList:

            room.draw(self.plane, self.cam)
