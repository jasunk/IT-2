import pygame as py
import random

class Ghost(py.sprite.Sprite):
    def __init__(self, name, speed, level, evidences, ability, huntTresh, activity):
        self.name = name
        self.speed = speed
        self.rooms = level
        self.currentRoom = self.rooms[random.randint(0,len(self.rooms)-1)]
        self.evidences = evidences
        self.ability = ability
        self.huntTreshold = huntTresh
        self.lineOfSight = False
        self.activity = activity
        self.image = py.image.load("sprites/test.png")

    def animate(self):
        pass

    def interract(self):
        pass


    def wander(self):
        pass

    def decideAction(self):
        pass

    def draw(self):
        pass
