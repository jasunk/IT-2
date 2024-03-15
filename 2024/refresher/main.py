import pygame as py
from pygame.locals import *
import random
from classes import *
py.init()

surf = py.display.set_mode((800,500))

gameLogic = GameLogic(0,3,5,6,50, True)
fuggel = Fugl(gameLogic)

pipes = []
activePipePos = None
activeSpeed = -gameLogic.startSpeed

def newPipeSet():
    global activePipePos, activeSpeed

    pipe1 = Pipe(gameLogic, [850, random.randint(230, 450)],activeSpeed, len(pipes)+1, True)
    pipe2 = Pipe(gameLogic, [850, random.randint(-250,-120)],activeSpeed, len(pipes)+1)
    if pipe1.pos[1]+400 > pipe2.pos[1]:
        pipe2.pos[1]+=150
    activePipePos = pipe1
    pipes.append(pipe1)
    pipes.append(pipe2)
    activeSpeed *= 1.005

newPipeSet()


while 1:

    surf.fill("gray")
    for e in py.event.get():
        if e.type == QUIT:
            py.quit()
            exit()

    for pipe in pipes:
        pipe.update(surf, fuggel)

    fuggel.update(surf,gameLogic.gravity, gameLogic.jumpForce)



    fuggel.draw(surf)


    if activePipePos.pos[0]<500:
        newPipeSet()

    py.display.update()

    py.time.Clock().tick(60)