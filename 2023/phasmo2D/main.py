import pygame as py
from pygame.locals import *
import time, random, sys
import settings, player, ghostV1, level, camera, levelCollection

mixer = py.mixer
mixer.init()
py.mixer.set_num_channels(10)
mixer.Channel(0).play(py.mixer.Sound("sounds/ambient/Rain_Medium_2.wav"))

py.init()

clock=py.time.Clock()

winWidth, winHeigth = settings.get_window()

gameSurf = py.display.set_mode((winWidth,winHeigth))

#currentGhost = ghostV1.Ghost(
#    10,
#    [1,2,3],
#    50,
#    level.Level(),
#    "heii",
#    [400,300]
#)
cam = camera.Camera([0,0])
#currentGhost.newRoamPos()
p1 = player.Player(cam,gameSurf, 3,1,[])
world = level.RoomCollection(levelCollection.level1, gameSurf, cam)
world.collisionFind()
while True:
    gameSurf.fill("black")
    for e in py.event.get():
        if e.type == QUIT:
            py.quit()
            sys.exit()


    world.draw()
    p1.update()
    py.display.update()
    clock.tick(60)

#currentGhost.room.draw(gameSurf,cam)
#currentGhost.goToNewPos()
#currentGhost.draw(gameSurf,cam)