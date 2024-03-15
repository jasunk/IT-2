import pygame as py
from pygame.locals import *
import random,camera


class Ghost(py.sprite.Sprite):
    def __init__(self, speed, evidence, activity, room, ability, position):
        super().__init__()
        self.speed = speed
        self.activity = activity
        self.evidence = evidence
        self.room = room
        self.ability = ability
        self.pos = position
        self.sprite = py.image.load("sprites/test.png")
        self.newX, self.newY = [0,0]



    def interract(self):
        randomChance = random.randint(0,100)
        if randomChance<self.activity:
            self.room.things[random.randint(0,len(self.room.things)-1)].interract()

    def move(self,x,y):
        self.pos[0] += x
        self.pos[1] += y

    def draw(self,surf,camera):
        surf.blit(self.sprite,(self.pos[0]+camera.getPos()[0],self.pos[1]+camera.getPos()[1]))

    def newRoamPos(self):
        room_x_range = [200,600]
        room_y_range = [200,400]

        self.newX = random.randint(room_x_range[0],room_x_range[1])
        self.newY = random.randint(room_y_range[0],room_y_range[1])


    def goToNewPos(self):
        toMove = [0,0]
        if self.pos[0]<self.newX:
            toMove[0]=self.speed/3
        if self.pos[0]>self.newX:
            toMove[0]=-self.speed/3
        if self.pos[1]<self.newY:
            toMove[1]=self.speed/3
        if self.pos[1]>self.newY:
            toMove[1]=-self.speed/3
        self.move(toMove[0],toMove[1])
        if (self.newX-self.speed<self.pos[0] < self.newX+self.speed) and (self.newY-self.speed<self.pos[1]<self.newY+self.speed):

            self.interract()
            self.newRoamPos()


    def changeRoom(self):
        pass

    def hunt(self, period, view, room, behaviour):
        pass













