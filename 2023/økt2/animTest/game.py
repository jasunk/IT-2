import pygame as py
from pygame.locals import *
import random, time, sys

py.init()

SCREENWIDTH = 800
SCREENHEIGHT = 400
gameplane= py.display.set_mode((SCREENWIDTH, SCREENHEIGHT))

playerX=10
playerY=150

playerSprites = [
    ["tile000.png","tile001.png","tile002.png","tile003.png","tile004.png","tile005.png","tile006.png","tile007.png","tile008.png","tile009.png"],
    ["tile000.png","tile001.png","tile002.png","tile003.png","tile004.png","tile005.png","tile006.png","tile007.png"],
    ["tile000.png","tile001.png","tile002.png","tile003.png","tile004.png","tile005.png","tile006.png","tile007.png"],
    ["tile000.png","tile001.png","tile002.png","tile003.png","tile004.png","tile005.png","tile006.png","tile007.png","tile008.png","tile009.png"],
    ["tile000.png","tile001.png","tile002.png","tile003.png","tile004.png","tile005.png","tile006.png","tile007.png","tile008.png","tile009.png"],
    ["tile000.png","tile001.png","tile002.png","tile002.png","tile002.png","tile002.png","tile002.png","tile002.png","tile002.png","tile002.png","tile002.png","tile002.png","tile002.png","tile002.png","tile002.png","tile002.png","tile002.png","tile002.png","tile002.png","tile002.png","tile002.png","tile002.png","tile002.png","tile002.png","tile002.png","tile002.png","tile002.png","tile002.png","tile002.png","tile002.png","tile002.png","tile002.png","tile002.png","tile002.png","tile002.png","tile002.png","tile002.png","tile002.png","tile002.png","tile002.png","tile002.png","tile002.png","tile002.png","tile002.png","tile002.png","tile002.png","tile002.png","tile002.png","tile002.png","tile002.png","tile002.png","tile002.png","tile002.png","tile002.png","tile002.png","tile002.png","tile002.png","tile002.png","tile002.png","tile002.png","tile002.png","tile002.png","tile002.png","tile002.png","tile002.png","tile002.png","tile002.png"],
    ["tile000.png","tile001.png","tile002.png","tile003.png","tile004.png","tile005.png","tile006.png","tile007.png","tile008.png"]
]
playerState = "idle"
currentAnimIndex = 0
FPS = 16
FramePerSec = py.time.Clock()
spriteIndex=0
newState="idle"
setZero=False
direction=False
playerScale=100



class Player(py.sprite.Sprite):


    def __init__(self):

        super().__init__()

        #self.image = py.image.load("anims/"+playerState+"/"+playerSprites[currentAnimIndex][spriteIndex])
#        self.image =py.transform.flip(py.image.load("anims/"+playerState+"/"+playerSprites[currentAnimIndex][spriteIndex]), direction, False)

        # Load the original image
        original_image = py.image.load("anims/" + playerState + "/" + playerSprites[currentAnimIndex][spriteIndex])

        # Flip the image
        flipped_image = py.transform.flip(original_image, direction, False)

        # Scale up the flipped image
        scaled_image = py.transform.scale(flipped_image, (playerScale, playerScale))  # Replace new_width and new_height with desired dimensions

        self.image = scaled_image

        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)



jumping = False
jumpSpeed=20

def jump():
    global jumping, playerY, spriteIndex, jumpSpeed, playerState, currentAnimIndex, spriteIndex, playerX
    jumping=True
    pressed_keys = py.key.get_pressed()



    for i in range(10):

        time.sleep(0.02)
        playerState="jump"
        currentAnimIndex=5
        P1 = Player()
        playerY-=jumpSpeed

        if pressed_keys[K_LEFT]:
            playerX-=8*playerScale/60
        if pressed_keys[K_RIGHT]:
            playerX+=8*playerScale/60

        gameplane.blit(P1.image, (playerX,playerY))
        jumpSpeed-=2
        py.display.update()
        FramePerSec.tick(FPS)
        gameplane.fill((0, 0, 0))
        spriteIndex += 1


    for i in range(11):
        time.sleep(0.02)
        playerState="jump"
        currentAnimIndex=5
        P1 = Player()
        playerY+=jumpSpeed
        if pressed_keys[K_LEFT]:
            playerX-=8*playerScale/60
        if pressed_keys[K_RIGHT]:
            playerX+=8*playerScale/60

        gameplane.blit(P1.image, (playerX,playerY))
        jumpSpeed+=2
        py.display.update()
        FramePerSec.tick(FPS)
        gameplane.fill((0, 0, 0))
        spriteIndex += 1

    spriteIndex=0
    for i in range (9):
        time.sleep(0.02)
        playerState="land"
        currentAnimIndex=6
        P1 = Player()


        gameplane.blit(P1.image, (playerX,playerY))

        py.display.update()
        FramePerSec.tick(FPS)
        gameplane.fill((0, 0, 0))
        spriteIndex += 1




while True:

    pressed_keys = py.key.get_pressed()

    if pressed_keys[K_SPACE] or pressed_keys[K_UP]:

        jump()

    if pressed_keys[K_RIGHT] and not pressed_keys[K_LSHIFT] and not pressed_keys[K_DOWN]:
        direction=False

        playerX+=5*playerScale/60
        playerState="walk"
        setZero=False

    elif  pressed_keys[K_RIGHT] and  pressed_keys[K_DOWN]:
        direction=False
        playerX+=3*playerScale/60
        playerState="crouch_walk"
        setZero=False

    elif  pressed_keys[K_RIGHT] and  pressed_keys[K_LSHIFT]:
        direction=False
        playerX+=10*playerScale/60
        playerState="run"
        setZero=False
    elif pressed_keys[K_LEFT] and not pressed_keys[K_LSHIFT] and not pressed_keys[K_DOWN]:
        direction=True

        playerX-=5*playerScale/60
        playerState="walk"
        setZero=False
    elif  pressed_keys[K_LEFT] and  pressed_keys[K_DOWN]:
        direction=True
        playerX-=3*playerScale/60
        playerState="crouch_walk"
        setZero=False

    elif  pressed_keys[K_LEFT] and  pressed_keys[K_LSHIFT]:
        direction=True
        playerX-=10*playerScale/60
        playerState="run"
        setZero=False
    elif pressed_keys[K_DOWN]:

        playerState="crouch_idle"
        setZero=False

    else:
        if not setZero:
            currentAnimIndex=0
            setZero=True
        playerState="idle"

    match playerState:
        case "idle":
            currentAnimIndex = 0
        case "walk":
            currentAnimIndex = 1
        case "run":
            currentAnimIndex = 2
        case "crouch_walk":
            currentAnimIndex = 3
        case "crouch_idle":
            currentAnimIndex = 4
        case "jump":
            currentAnimIndex = 5
        case "land":
            currentAnimIndex = 6
        case _:
            print("playerState error")

    if spriteIndex >= len(playerSprites[currentAnimIndex]):
        spriteIndex = 0


    P1 = Player()

    for event in py.event.get():
        if event.type == QUIT:
            py.quit()
            sys.exit()
        if event.type == KEYUP or KEYDOWN:
            spriteIndex=0


    gameplane.blit(P1.image, (playerX,playerY))

    py.display.update()
    FramePerSec.tick(FPS)
    gameplane.fill((0, 0, 0))
    spriteIndex += 1
