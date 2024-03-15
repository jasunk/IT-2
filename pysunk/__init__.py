from pygame import *
from pygame.locals import *
import math

def rescale_factored(surf, factor):
    return transform.scale(surf, (surf.get_size()[0]*factor[0], surf.get_size()[1]*factor[1]))

def within_radius(radiusPos, radius, entitypos, surf, depth):
    multiCheck = False
    if isinstance(radiusPos, Rect):
        radiusPos = [radiusPos.center[0], radiusPos.center[1]]
    if isinstance(entitypos, Rect):
        multiCheck = True

    draw.circle(surf, (0,0,0), radiusPos, radius)
    if not multiCheck:
        vektor = [entitypos[0]-radiusPos[0], entitypos[1]-radiusPos[1]]
        return math.sqrt(vektor[0]**2 + vektor[1]**2) <= radius
    else:

        _x = [entitypos.left+(entitypos.width/(depth-1))*i - radiusPos[0] for i in range(depth)]
        _y = [entitypos.top+(entitypos.height/(depth-1))*i - radiusPos[1] for i in range(depth)]
        for i in range(len(_x)):
            for j in range(len(_y)):
                draw.circle(surf, "red", [_x[i]+radiusPos[0], _y[j]+radiusPos[1]], 2)
                if math.sqrt(_x[i]**2 + _y[j]**2) <= radius:return True



class CostumCursor:
    def __init__(self, cursorImg):
        self.cursorImg = cursorImg.convert_alpha()
        mouse.set_cursor((8,8),(0,0),(0,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,0))
    def draw(self, surf, mousePos):
        surf.blit(self.cursorImg, [mousePos[0] -self.cursorImg.get_size()[0]/2,mousePos[1]- self.cursorImg.get_size()[1]/2])

class GameLogic:
    def __init__(self, FPS,cursor = None):

        self.FPS = FPS
        if cursor: self.cursor = CostumCursor(cursor)
        else:      self.cursor = None
        self.mousePos = [0,0]
    def update(self, surf, events):

        for e in events:
            if e.type == QUIT:
                quit()
                exit()
            if e.type == MOUSEMOTION: self.mousePos = e.pos
        if self.cursor: self.cursor.draw(surf, self.mousePos)

class KinematicBody(sprite.Sprite):
    def __init__(self, pos, damping, img, mass, game):
        super().__init__()
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.mass = mass
        self.vel = [0,0]
        self.damping = damping
        self.game = game
        self.gravity = 9.81/game.FPS


    def move(self):
        self.rect.centerx += self.vel[0]
        self.rect.centery += self.vel[1]
        self.vel[0]*=self.damping
        self.vel[1]*=self.damping
        if -1<self.vel[0]<1:self.vel[0] = 0
        if -1<self.vel[1]<1:self.vel[1] = 0
    def add_velocity(self, vel, limit = [9000, 9000]):
        if vel[0] and vel[1] != 0:
            length = math.sqrt((vel[0]**2 + vel[1]**2)/2)
            vel[0] = length
            vel[1] = length

        if self.vel[0] < limit[0]: self.vel[0] += vel[0]
        if self.vel[1] < limit[1]: self.vel[1] += vel[1]
        print(self.vel)

    def set_velocity(self, vel):
        if vel[0] and vel[1] != None:
            length = math.sqrt(vel[0]**2 + vel[1]**2)

            vel[0] /= length
            vel[1] /= length
            self.vel = vel
        elif vel[0] != None: self.vel[0] = vel[0]
        elif vel[1] != None: self.vel[1] = vel[1]
        print(self.vel)

    def update(self, surf):

        self.move()
        surf.blit(self.image, self.rect.center)
