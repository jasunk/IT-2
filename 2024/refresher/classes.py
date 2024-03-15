import pygame as py
from pygame.locals import *
import random

class GameLogic:
    def __init__(self, score, gravity, startSpeed, speedFactor, jumpForce, alive):
        self.score=score
        self.gravity = gravity/5
        self.startSpeed = startSpeed
        self.speedFactor = speedFactor
        self.jumpForce = -jumpForce/5
        self.alive=True

class Fugl:
    def __init__(self, gameLogic):
        self.gameLogic = gameLogic
        self.width, self.height = 24, 24
        self.x, self.y = 250-self.width/2, 250-self.height/2,
        self.sprite = py.rect.Rect(self.x, self.y, self.width, self.height)
        self.velocity = [0,0]

    def physics_process(self, gravity, jumpForce):
        keystrokes = py.key.get_pressed()
        if keystrokes[K_SPACE] and self.velocity[1]>=0 and self.gameLogic.alive:
            self.velocity[1]=jumpForce


        self.velocity[1]+=gravity

        self.y += self.velocity[1]

    def draw(self, plane):
        self.sprite.y = self.y
        py.draw.rect(plane, "red", self.sprite)


    def update(self, plane, gravity, jumpForce):
        self.physics_process(gravity, jumpForce)
        self.draw(plane)


class Pipe:
    def __init__(self,gameLogic, pos, speed, id, main=False):
        self.pos = pos
        self.main = main
        self.id = id
        self.speed = speed
        self.velocity = [self.speed,0]
        self.sprite = py.rect.Rect(pos[0], pos[1], 40, 300)
        self.gameLogic = gameLogic
        self.hasGivenScore=False

    def physics_process(self, fugl):


        if (self.pos[0] < fugl.x < self.pos[0]+40) and (self.pos[1] < fugl.y < self.pos[1]+175):
            print(self.id, "tap")
            self.gameLogic.alive=False

        elif (self.pos[0] < fugl.x <self.pos[0]+40) and not self.hasGivenScore and self.main:
            self.gameLogic.score+=1
            self.hasGivenScore=True
            print("score:",self.gameLogic.score)

        self.pos[0] += self.velocity[0]

    def draw(self, plane):
        self.sprite.x = self.pos[0]
        py.draw.rect(plane, "green", self.sprite)

    def update(self, plane, fugl):
        if self.gameLogic.alive: self.physics_process(fugl)
        self.draw(plane)