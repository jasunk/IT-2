import random
import sys

import pygame as py
from pygame.locals import *
import math
from settings import *
from maps import rooms, nextRoom




#grunnmur for alle kinematicbodies
class AnimationSet():

    #deler opp et spritesheet til separate bilder, returnerer bildet ved index index
    def splitSheet(self, sheet, imgSize, split, index, flip = 0):
        xSize = imgSize[0]/split[0]
        ySize = imgSize[1]/split[1]
        img = py.Surface((xSize,ySize), py.SRCALPHA)

        sheet = py.image.load(sheet)
        img.blit(sheet, (0,0), (xSize*(index[0]), ySize*(index[1]),xSize*(index[0]+1), ySize*(index[1]+1)))

        img = py.transform.flip(img, flip, 0)
        return img

    #Returnerer enkeltbilder (ikke spritesheets)
    def returnSingleSprite(self, img, size=None):
        image = py.image.load(img)
        if size:
            image = py.transform.scale(image,[size])
        return image

    #List comprehention brukes til å fylle en array med bilder som en animasjon
    def returnArr(self, img, imgSize, split, flip = 0):
        return [self.splitSheet(img,imgSize, [split, 1], [i,0], flip) for i in range(0,split-1)]




#grunnmur for standard objekter som skal kunne animeres og beveges (spiller, fiender)
class KinematicBody(py.sprite.Sprite):
    def __init__(self, pos, speed, health, game, friction = 1, canBeHit=True, size=1.5):
        #initiater sprite for å kunne bruke spritecollide
        super().__init__()

        #placeholder for å unngå errors
        self.spriteList = [py.image.load("sprites/topdown_shooter_assets/sBullet.png")]

        #Counter som må nå et gitt tall før neste animasjons-frame spilles av, for å animere karakter i lavere FPS enn prosseseringen
        self.frameForFrameShift = 0
        self.frame = 0
        self.shouldDraw = True

        #pos er lowkey pensjonert, bruker eksklusivt rect. vel (velocity) brukes for "smooth" bevegelse
        self.pos = pos
        self.vel = [0,0]

        #skalerer bilder (deathImg brukes som standard for å generere en rect)
        self.size = size

        #For å gjøre karakter større ved hit, setter self.size til hitsize og går nedover mot targetsize igjen
        self.targetSize = size
        self.hitSize = size*1.5

        #definerer et bilde for død og en rect
        self.deathImg = py.image.load("sprites/topdown_shooter_assets/sEnemyDead.png")
        self.deathImg = py.transform.scale(self.deathImg, (self.deathImg.get_rect().width*self.size, self.deathImg.get_rect().height*self.size))
        self.rect = self.deathImg.get_rect()
        self.rect.center = (pos[0]+leftSidePadding, pos[1])

        #self explanatory lowkey
        self.speed = speed
        self.friction = friction
        self.inithp = health
        self.hp = health
        self.alive = True

        #Lister som håndterer tegning av egne partikler og skudd, for at ikke alle må karakterer må ha kontroll på dem
        self.particles = []
        self.bullets = []
        self.bulletSprites = py.sprite.Group()
        #gir tilgang til spillogikk
        self.game = game
        self.bulletsToCollideWith = self.game.bulletSprites if isinstance(self, Enemy) else self.game.enemyBullets

        #Felles lyder for kinematicbodies
        self.hitsound = py.mixer.Sound("sounds/hit.wav")
        self.dieSound = py.mixer.Sound("sounds/die.wav")



    #sjekker om karakter kolliderer med oppsatte vegger
    def check_collision(self, direction):
        if direction == "x":
            if self.rect.x<leftSidePadding:self.lifetime=-1
            #bruker egen spriteRect og sammenligner med aktive "collisionTiles" (definerte vegger)
            hits = py.sprite.spritecollide(self, self.game.collisionTiles, False)

            #Håndterer x og y separat, slik at du fortsatt kan gå opp imens du treffer en sidevegg og motsatt
            if hits:
                if self.vel[0]>0:
                    self.rect.x = hits[0].rect.left - self.rect.width
                if self.vel[0]<0:
                    self.rect.x = hits[0].rect.right

                #Om en er fiende flipper man retning slik at man ikke fortetter å gå inn i veggen
                if isinstance(self, Enemy):
                    self.vel[0]*=-1

        if direction == "y":
            hits = py.sprite.spritecollide(self, self.game.collisionTiles, False)
            if hits:
                if self.vel[1]>0:
                    self.rect.y = hits[0].rect.top - self.rect.height
                if self.vel[1]<0:
                    self.rect.y = hits[0].rect.bottom
                if isinstance(self, Enemy):

                    self.vel[1]*=-1




    #Legger til / trekker fra velocity
    def addVelocity(self,velArray):
        self.vel[0] += velArray[0]

        self.vel[1] += velArray[1]

    #Setter faste velocities for å ikke aksellerere inn i andre galakser
    def setVelocity(self,velArray):
        if abs(self.vel[0])<abs(velArray[0]):
            self.vel[0] = velArray[0]

        if abs(self.vel[1]) < abs(velArray[1]):
            self.vel[1] = velArray[1]

    #håndterer bevegelse med velocity, friksjon og kollisjon
    def move(self):
        self.rect.x += self.vel[0]

        self.check_collision("x")
        self.rect.y += self.vel[1]
        self.check_collision("y")


        self.vel[0] *= self.friction
        self.vel[1] *= self.friction

    #tegner partikler
    def particleHandling(self, surf):
        self.particles = [p for p in self.particles if p.lifetime >= 0]
        self.bullets = [p for p in self.bullets if p.lifetime >= 0]
        for p in self.particles:
            p.update(surf)
        #tegner egne skudd
        for b in self.bullets:
            b.update(surf)

    def isTouchingBullet(self):
        print(self.bulletsToCollideWith)
        hits = py.sprite.spritecollide(self, self.bulletsToCollideWith, False)

        for h in [h for h in hits if h.canHit]:

            self.hitsound.play()
            self.addVelocity([h.vel[0]/self.size, h.vel[1]/self.size])
            self.hp -= h.dmg
            if isinstance(self, Player):self.game.player_hp_bar_update()
            if h.dmg >=50:
                h.dmg *= 0.8
            else:
                h.canHit = False
                h.lifetime=-1
                h.dmg=0

            #legger til noen røde partikler som blod
            for i in range(int(20*self.game.partikkelfaktor)):
                size = random.randint(3,8)
                self.particles.append(Particle([size,size],[self.rect.x+30, self.rect.y+30], [random.randint(-6,6),random.randint(-6,6)],"red",random.randint(10,20) ))
            if isinstance(self,Enemy):self.game.hitlist_update(self)


    #tegner seg selv
    def draw(self, surf):
        if self.game.showHitbox: py.draw.rect(surf, "red", self.rect)

        if self.size > self.targetSize:
            self.size-=0.25

        self.particleHandling(surf)
        if self.frame>len(self.spriteList)-1:
            self.frame=0

        if self.shouldDraw:
            if not self.alive:
                surf.blit(self.deathImg, (self.rect.x, self.rect.y))
            else:

                scaledSprite = py.transform.scale(self.spriteList[self.frame],(self.spriteList[self.frame].get_size()[0]*self.size,self.spriteList[self.frame].get_size()[1]*self.size))
                if isinstance(self, Player):
                    surf.blit(scaledSprite, (self.rect.x-10, self.rect.y-10))
                else:
                    surf.blit(scaledSprite, (self.rect.x, self.rect.y))



        if self.alive:
            self.move()
            self.isTouchingBullet()
        if self.hp <=0 and self.alive:

            self.dieSound.play()
            self.alive = False
            self.game.hitlist_update()


            if random.randint(0,100)>85:self.game.pickups.append(HealthPickup([self.rect.x+self.rect.width/2, self.rect.y+self.rect.height/2], self.game))



        if self.frameForFrameShift>=int(self.size):
            self.frameForFrameShift=0
            if self.frame < len(self.spriteList)-1:
                self.frame+=1
            else:
                self.frame=0
        else:
            self.frameForFrameShift+=1





#Definerer fiendenes animasjoner på forhånd for å ikke måtte prossesere bilder som skal gjenbrukes
animSet = AnimationSet()
ENEMYANIMATIONS  = {

    "runRight":animSet.returnArr("sprites/topdown_shooter_assets/sEnemy_strip7.png",[280,40], 7),
    "runLeft":animSet.returnArr("sprites/topdown_shooter_assets/sEnemy_strip7.png",[280,40], 7, 1),
    "dead":animSet.returnArr("sprites/topdown_shooter_assets/sEnemyDead.png", [40,40], 1)
}

#Generell fiende definert av en kinematicBody
class Enemy(KinematicBody):

    def __init__(self, pos, speed, health, damage, seekArea, player,game, size=1.5 ):

        self.animations = ENEMYANIMATIONS
        super().__init__(pos,speed,health,game, 0.8,True,size)

        #definerer generelle egenskaper'
        self.scale = size
        self.dmg = damage
        self.dir = "Right"
        self.spriteList = self.animations["run"+self.dir]
        self.circle_radius = seekArea/1.25

        #Referanse til spiller
        self.player = player


        self.changeDir = 10
        self.despawnTimer = 150
        self.name = random.choice(TILFELDIGNAVN).upper()
        self.game.hitlist_update()


    #undersøker om spiller er innenfor en sirkel med definert radius gitt med seekArea
    def is_point_inside_circle(self):

        #bruker vektorregning for å finne avstand mellom spiller og fiende, returnerer True om distansen er mindre enn radiusen
        distance = math.sqrt((self.player.rect.x - (self.rect.x+30))**2 + (self.player.rect.y - (self.rect.y+30))**2)
        return distance < self.circle_radius


    #Om fiende IKKE ser spiller, gjør den dette
    def seekState(self):

        #velger tilfeldig retning med tilfeldig mellomrom
        if self.changeDir<0:
            self.changeDir=random.randint(5,15)
            self.vel[0] += random.randint(int(-self.speed*1.5), int(self.speed*1.5))
            self.vel[1] += random.randint(int(-self.speed*1.5), int(self.speed*1.5))
        else:
            self.changeDir-=1

        #om ingen bevegelse, ikke animer
        if (self.vel[0] and self.vel[1]) == 0:
            self.frame=0






    #generell logikk
    def update(self, surf):

        #om utenfor spillområdet -> dø
        if (self.rect.x<400 or self.rect.x>1400 or self.rect.y<0 or self.rect.y >1000) and self.alive:
            self.alive=False

            self.shouldDraw=False

        if self.alive:self.seekState()

        self.draw(surf)


        if self.vel[0]<0:
            self.dir = "Left"
        else:
            self.dir = "Right"

        if not self.alive:

            self.spriteList = self.animations["dead"]
            self.despawnTimer-=1
        self.spriteList = self.animations["run"+self.dir]


#type fiende som løper etter spiller om den er innenfor radius
class ChaseEnemy(Enemy):
    def __init__(self, pos, speed, health, damage, seekArea, player,game, size=1.5 ):
        super().__init__(pos, speed, health, damage, seekArea, player,game, size)
        self.type = "CHASER"
        if size >2:
            self.type = "BIG CHASER"

    def chaseState(self):
        vector = [self.player.rect.x-self.rect.x, self.player.rect.y-self.rect.y]
        lengdeDia = math.sqrt((vector[0]**2 + vector[1]**2)/2)
        if lengdeDia==0:lengdeDia=1
        self.vel[0] = vector[0]/(lengdeDia/5)
        self.vel[1] = vector[1]/(lengdeDia/5)

    def seekState(self):
        super().seekState()
        if self.is_point_inside_circle():
            self.chaseState()

#type fiende som rømmer fra spiller om den er innenfor radius
class RunEnemy(Enemy):
    def __init__(self, pos, speed, health, damage, seekArea, player,game, size=1.3 ):
        super().__init__(pos, int(speed*2), int(health/1.5), damage, int(seekArea/2), player,game, int(size))
        self.type = "EVADER"

    def runState(self):
        vector = [self.player.rect.x-self.rect.x, self.player.rect.y-self.rect.y]
        lengdeDia = math.sqrt((vector[0]**2 + vector[1]**2)/2)
        if lengdeDia==0:lengdeDia=1
        self.vel[0] = -vector[0]/(lengdeDia/5)
        self.vel[1] = -vector[1]/(lengdeDia/5)

    def seekState(self):
        super().seekState()
        if self.is_point_inside_circle():
            self.runState()

class ShootingEnemy(RunEnemy):
    def __init__(self,pos, speed, health, damage, seekArea, player,game, size=1.3 ):
        super().__init__(pos, speed, health, damage, seekArea, player,game, size)
        self.type = "SHOOTER"
        self.shootCooldown = 0
        self.shootCooldownSTD = 100
        self.shootSound = py.mixer.Sound("sounds/shoot_def.wav")
        self.shootSound.set_volume(0.3)
        self.gun = Gun(self,1,0,0,[self.size, self.size],self.game)

    def shoot(self):


        if self.shootCooldown<=0:
            self.shootCooldown=self.shootCooldownSTD
            self.shootSound.play()

            createvector = [self.player.rect.x-self.rect.x, self.player.rect.y-self.rect.y]
            vectorLength = math.sqrt((createvector[0]**2 + createvector[1]**2)/2)
            shotVel = 12
            _ = Bullet([self.rect.x+self.rect.width/2, self.rect.y+self.rect.height/2], [(createvector[0]/vectorLength)*shotVel, (createvector[1]/vectorLength)*shotVel], self.dmg,1.5, self.game, True)
            self.game.enemyBullets.add(_)
            self.bullets.append(_)

            #lager pewpew-ild
            for i in range(int(random.randint(5,14)*self.game.partikkelfaktor)):
                self.particles.append(Particle([5*self.size,5*self.size],[self.rect.x, self.rect.y],[(createvector[0]/(vectorLength/10)+random.randint(-7,7)), (createvector[1]/(vectorLength/5))+random.randint(-7,7)], "yellow", 7, 0.65))
                self.particles.append(Particle([4*self.size,4*self.size],[self.rect.x, self.rect.y],[(createvector[0]/(vectorLength/5)+random.randint(-3,3)), (createvector[1]/(vectorLength/5))+random.randint(-3,3)], "red", 5, 0.8))
                self.particles.append(Particle([5*self.size,5*self.size],[self.rect.x, self.rect.y],[(createvector[0]/(vectorLength/3)+random.randint(-3,3)), (createvector[1]/(vectorLength/3))+random.randint(-3,3)], "black", 5, 0.8))

        else:
            self.shootCooldown-=1
    def seekState(self):

        super().seekState()
        if not self.is_point_inside_circle():
            self.shoot()

    def update(self, surf):
        super().update(surf)
        self.gun.update(surf, [self.player.rect.x, self.player.rect.y])


#Spillerklasse
class Player(KinematicBody):

    def __init__(self, pos, speed, health, game):
        animSet = AnimationSet()

        self.animations = {
            "idleRight":animSet.returnArr("sprites/topdown_shooter_assets/sPlayerIdle_strip4.png",[160,40], 4),
            "idleLeft":animSet.returnArr("sprites/topdown_shooter_assets/sPlayerIdle_strip4.png",[160,40], 4, 1),
            "runRight":animSet.returnArr("sprites/topdown_shooter_assets/sPlayerRun_strip7.png",[280,40], 7),
            "runLeft":animSet.returnArr("sprites/topdown_shooter_assets/sPlayerRun_strip7.png",[280,40], 7, 1)
        }

        super().__init__(pos, speed, health, game, 0.7)


        self.dir = "Right"

        #definerer startverdier for costum-gun
        self.personalGun = {
            "dmg":3,
            "recoil": 10,
            "fireRate":10,
            "size":[1,1]
        }
        #basically skillpoints
        self.allocation_points = 0
        #gjør egen rect litt mindre og sentrerer den på bildet
        self.rect.width-=20
        self.rect.height-=20
        self.rect.centerx+=30


        #definerer startverdier
        self.spriteList = self.animations["run"+self.dir]
        self.dashCooldown = 20
        self.guns = [Gun(self, self.personalGun["dmg"], self.personalGun["recoil"], self.personalGun["fireRate"], self.personalGun["size"], self.game),Gun(self, 2, 1.2,0, [1, 0.5], self.game), Gun(self, 15, 15,5, [1.5,1.5], self.game), Gun(self, 50, 40,15, [3, 1.5], self.game), Gun(self, 100, 140,15, [6, 3], self.game)]
        self.activeGunIndex = 0
        self.game.player.add(self)
        self.game.playerRef = self
        self.dashSound = py.mixer.Sound("sounds/dash.wav")

        self.headerFont = returnFont(30)
        self.infoFont = returnFont(12)
        self.UI = py.Surface((400,1000),DOUBLEBUF| HWACCEL)
        self.tutorialSurf = py.Surface((400,300),DOUBLEBUF| HWACCEL)
        self.tutorialUI()
        self.playerUI([0,0])
        self.lastTouchedEnemyName = ""
        self.invincible = False
        self.invincibilityFrameAmount = 10
        self.invincibilityFrameNow = 0
        self.hitsound = py.mixer.Sound("sounds/playerHit.wav")
        self.game.display("both")

    #sjekker om treffer enemy
    def isTouchingEnemy(self):
        #bruker en mindre rect for å se om vi treffer fiende

        hits = py.sprite.spritecollide(self, self.game.enemySprites, False)
        if self.alive and self.invincibilityFrameNow<=0 and hits:
            for e in [h for h in hits if h.alive]:

                self.invincibilityFrameNow=self.invincibilityFrameAmount
                self.hp-=e.dmg
                self.game.player_hp_bar_update()
                #får fiende til å sprette motsatt retning
                e.vel[0] = (self.rect.x - e.rect.x)/10
                e.vel[1] = (self.rect.y - e.rect.y)/10
                self.lastTouchedEnemyName = e.name
                self.hitsound.play()
                #legger til noen røde partikler som blod
                for i in range(int(8*self.game.partikkelfaktor)):
                    size = random.randint(3,8)
                    self.particles.append(Particle([size,size],[self.rect.x+20, self.rect.y+20], [random.randint(-6,6),random.randint(-6,6)],"red",random.randint(10,20) ))
        self.invincibilityFrameNow -=1

    def checkIfExit(self):
        hits = py.sprite.spritecollide(self, self.game.exits, False)

        if hits and len(self.game.livingEnemies)==0:
            if self.hp+100<self.inithp:
                self.hp+=100
            elif self.hp+100 >= self.inithp:
                self.hp = self.inithp
            self.game.player_hp_bar_update()
            nextRoom(self.game.currentRoomIndex+1, self)
            self.allocation_points +=1
            self.game.currentRoomIndex+=1
            self.game.load_level()
            self.game.spawnEnemies(self, (2+self.game.currentRoomIndex),[3,7], [15,30], 20, 15 )
            self.playerUI([0,0])
    #sjekker for spillerInput
    def input(self, mousePos):
        keystrokes = py.key.get_pressed()
        usedSpeed = self.speed
        diagonalSpeed = math.sqrt((self.speed**2 + self.speed**2)/2)
        self.dashCooldown-=1
        if keystrokes[K_LSHIFT] and self.dashCooldown<0:
            for i in range(int(10*self.game.partikkelfaktor)):
                self.particles.append(Particle([5,5], [self.rect.x, self.rect.y],[random.randrange(-10,10), random.randrange(-10,10)], "gray", 15, 0.7))
            self.dashCooldown=20
            py.mixer.Sound.play(self.dashSound)
            diagonalSpeed *=5
            usedSpeed*=5

        if keystrokes[K_w]:
            super().setVelocity([0,-usedSpeed])
        if keystrokes[K_s]:
            super().setVelocity([0,usedSpeed])
        if keystrokes[K_a]:
            super().setVelocity([-usedSpeed,0])
        if keystrokes[K_d]:
            super().setVelocity([usedSpeed,0])

        if keystrokes[K_w] and keystrokes[K_d]:
            super().setVelocity([diagonalSpeed,-diagonalSpeed])
        if keystrokes[K_w] and keystrokes[K_a]:
            super().setVelocity([-diagonalSpeed,-diagonalSpeed])
        if keystrokes[K_s] and keystrokes[K_a]:
            super().setVelocity([-diagonalSpeed,diagonalSpeed])
        if keystrokes[K_s] and keystrokes[K_d]:
            super().setVelocity([diagonalSpeed,diagonalSpeed])

        if not (keystrokes[K_w] or keystrokes[K_s] or keystrokes[K_a] or keystrokes[K_d]):
            moving = False
        else:
            moving = True

        if mousePos[0]<self.rect.x:
            self.dir="Left"
        elif mousePos[0]>self.rect.x:
            self.dir="Right"
        self.checkIfExit()
        if moving:
            self.spriteList = self.animations["run"+self.dir]
        else:
            self.spriteList = self.animations["idle" + self.dir]


    #oppdaterer egen gunner
    def update_personal_gun(self):
        if self.personalGun["dmg"]<0: self.personalGun["dmg"]=0
        self.personalGun["size"][0] = self.personalGun["dmg"]/10 + 1
        self.personalGun["size"][1] = self.personalGun["dmg"]/12 + 1

        if self.personalGun["fireRate"]<0: self.personalGun["fireRate"]=0
        if self.personalGun["recoil"]==0: self.personalGun["recoil"]=0.

        self.guns[0] = Gun(self, self.personalGun["dmg"], self.personalGun["recoil"], self.personalGun["fireRate"], self.personalGun["size"], self.game)


    #håndterer knapper for input av egen gunner
    def gunStatHandler(self,  mousePos):
        y_shift = 300
        damageUp = Button([300, y_shift], [30, 30], "+", 1, True)
        dmg_label = Label([200, y_shift], 20, "DAMAGE", "black")
        damageDown = Button([100, y_shift], [30, 30], "-", -1, True)

        fireRateUp = Button([300, y_shift+50], [30, 30], "+", 1, True)
        fireRate_label = Label([200, y_shift+50], 20, "FIRERATE", "black")
        fireRateDown = Button([100, y_shift+50], [30, 30], "-", -1, True)

        recoilUp = Button([300, y_shift+100], [30, 30], "+", 1, True)
        recoildLabel = Label([200, y_shift+100], 20, "RECOIL", "black")
        recoilDown = Button([100, y_shift+100], [30, 30], "-", -1, True)

        dmg_stat = Label([200, y_shift+160],20, f"Damage: {self.personalGun['dmg']}", "black")
        fireRate_stat = Label([200, y_shift+180],20, f"Firerate: {self.personalGun['fireRate']}", "black")
        recoil_stat = Label([200, y_shift+200],20, f"Recoil: {self.personalGun['recoil']}", "black")

        availible_mods = Label([200, y_shift+140],20, f"Modifikasjonspoeng : {self.allocation_points}", "black")

        preset_section_height = 930
        preset_title = Label([200, preset_section_height], 30, "JUKSEVÅPEN", "black")
        smg_preset = Button([50, preset_section_height+40], [90, 30], "SMG",0, True)
        pistol_preset = Button([150, preset_section_height+40], [90, 30], "AK-69",0, True)
        AR_preset = Button([250, preset_section_height+40], [90, 30], "WAP",0, True)
        sniper_preset = Button([350, preset_section_height+40], [90, 30], "BOOM",0, True)


        if py.mouse.get_pressed()[0]:

            if self.allocation_points>0:
                if damageUp.is_pressed(mousePos):
                    self.personalGun["dmg"]+=1
                    self.allocation_points-=1
                if recoilUp.is_pressed(mousePos):
                    self.personalGun["recoil"]-=5
                    self.allocation_points-=1
                if fireRateUp.is_pressed(mousePos):
                    self.personalGun["fireRate"]-=0.5
                    self.allocation_points-=1


            if damageDown.is_pressed(mousePos):
                self.personalGun["dmg"]-=1
                self.allocation_points+=1
            if fireRateDown.is_pressed(mousePos):
                self.personalGun["fireRate"]+=2
                self.allocation_points+=1
            if recoilDown.is_pressed(mousePos):
                self.personalGun["recoil"]+=5
                self.allocation_points+=1

            if smg_preset.is_pressed(mousePos):self.activeGunIndex=1
            if pistol_preset.is_pressed(mousePos):self.activeGunIndex=2
            if AR_preset.is_pressed(mousePos):self.activeGunIndex=3
            if sniper_preset.is_pressed(mousePos):self.activeGunIndex=4


        buttons = [damageUp, damageDown, fireRateUp, fireRateDown, recoilUp, recoilDown, smg_preset, pistol_preset, AR_preset, sniper_preset]
        labels = [preset_title, recoildLabel, fireRate_label, dmg_label, dmg_stat, fireRate_stat, recoil_stat, availible_mods]

        for l in labels:
            l.draw(self.UI)

        for b in buttons:
            if b.is_pressed(mousePos):
                self.update_personal_gun()


            b.update(self.UI, mousePos)

    #Oppdaterer UI-surfen når nødvendig
    def tutorialUI(self):
        rect = py.rect.Rect(0,0,400,300)
        py.draw.rect(self.tutorialSurf, "pink", rect)
        t1 = self.infoFont.render("WASD for å bevege seg", True, "black")
        t2 = self.infoFont.render("Trykk LSHIFT for å dashe", True, "black")
        t3 = self.infoFont.render("DREP alle fiender og gå ut åpning ", True, "black")
        t4= self.infoFont.render("for å nå neste rom.", True, "black")
        t5= self.infoFont.render("Oppgrader gunneren din ", True, "black")
        t6= self.infoFont.render("med modifikasjonspoeng", True, "black")
        t7 = self.infoFont.render("ESCAPE for innstillinger", True, "black")
        self.tutorialSurf.blit(t1, (90, 0))
        self.tutorialSurf.blit(t2, (80, 50))
        self.tutorialSurf.blit(t3, (30, 100))
        self.tutorialSurf.blit(t4, (105, 130))
        self.tutorialSurf.blit(t5, (90, 180))
        self.tutorialSurf.blit(t6, (90, 210))
        self.tutorialSurf.blit(t7, (90, 260))
    def playerUI(self, mousePos):
        text = self.headerFont.render("GUNUPGRADES", True, "black")
        _ = py.rect.Rect(0,0,400,1000)
        py.draw.rect(self.UI,"pink", _)
        textRect = text.get_rect()
        textRect.center = (200, 100)
        self.UI.blit(text, textRect)
        gunDisplayImg = self.guns[self.activeGunIndex].img
        gunDisplayImg= py.transform.scale(gunDisplayImg, (gunDisplayImg.get_rect().width*2, gunDisplayImg.get_rect().height*2))
        self.UI.blit(gunDisplayImg, (200-gunDisplayImg.get_width()/2, 200-gunDisplayImg.get_height()/2))

        self.UI.blit(self.tutorialSurf, (0,550))
        self.gunStatHandler(mousePos)

    #tegner UI høyreside
    def drawPlayerUI(self, surf, mousePos):
        surf.blit(self.UI,(1400,0))
        if mousePos[0]>1400 and py.mouse.get_pressed()[0]:

            self.playerUI(mousePos)

    def update(self, surf, mousePos):
        self.isTouchingEnemy()
        if not self.alive:
            self.game.state = "gameOver"
        self.guns[self.activeGunIndex].update(surf, mousePos)
        self.input(mousePos)

        super().draw(surf)
        self.drawPlayerUI(surf, mousePos)
        if self.rect.x<-10 or self.rect.x>1010:
            self.vel[0]*=-1
        if self.rect.y<-10 or self.rect.y>1010:
            self.vel[1]*=-1


#Gun-klasse gjør at man i teorien kan ha flere gunnere i et inventory
class Gun:
    def __init__(self, parent, damage, recoil, cooldownSTD, size, game, knockBack=True):
        self.img = py.image.load("sprites/topdown_shooter_assets/sGun.png")
        self.imgRect = self.img.get_rect()
        self.sizeArr = [size[0], size[1]]
        self.img = py.transform.scale(self.img, (self.imgRect.width*size[0], self.imgRect.height*size[1]))
        self.knockBack = knockBack
        self.size=size[1]
        self.dmg = damage
        self.recoil = recoil
        self.parent = parent
        self.offset = [70, 25]
        self.smoothing_factor = [0.5,0.5]
        self.currentPos = [self.parent.rect.x, self.parent.rect.y]
        self.rotation = 0
        self.dy=10
        self.bullets = []
        self.cooldown = cooldownSTD
        self.cooldownSTD = cooldownSTD
        self.active= True
        self.game = game

        if cooldownSTD<3:
            self.shootSound = py.mixer.Sound("sounds/shoot_light.wav")
        elif cooldownSTD<8:
            self.shootSound = py.mixer.Sound("sounds/shoot_def.wav")
        else:
            self.shootSound = py.mixer.Sound("sounds/shoot_deep.wav")

    #plasserer seg self en gitt avstand fra spiller, og "lagger" litt bak i posisjon
    def positionSelf(self):
        target_pos = [0, 0]

        if self.parent.dir == "Left":
            target_pos[0] = self.parent.rect.x - self.offset[0]+40 +self.size*5
        elif self.parent.dir == "Right":
            target_pos[0] = self.parent.rect.x + self.offset[0]-10+self.size*5


        target_pos[1] = self.parent.rect.y + self.offset[1] + self.dy/10

        # Smoothly update the gun position
        self.currentPos[0] += (target_pos[0] - self.currentPos[0]) * self.smoothing_factor[0]
        self.currentPos[1] += (target_pos[1] - self.currentPos[1]) * self.smoothing_factor[1]

    #roterer basert på musen
    def update_rotation(self, mouse_pos):
        self.dx = mouse_pos[0] - self.currentPos[0]
        self.dy = mouse_pos[1] - self.currentPos[1]

        self.rotation = math.degrees(math.atan2(self.dy, self.dx))+180

    def draw(self, surf):
        rotated_img = py.transform.rotate(self.img, -self.rotation)
        rect = rotated_img.get_rect(center=(self.currentPos[0], self.currentPos[1]))

        surf.blit(rotated_img, rect.topleft)


    #skuddMetode
    def shoot(self, mouse_pos):

        #finner en vektor gitt fra Gun sin posisjon til musen
        vector = [mouse_pos[0]-self.currentPos[0], mouse_pos[1]-self.currentPos[1]]

        #OM SKYTER
        if self.cooldown<0 and leftSidePadding< mouse_pos[0]<1400:
            py.mixer.Sound.play(self.shootSound)
            self.cooldown=self.cooldownSTD

            #finner lengde av vektoren for å kunne dele den opp i en normalisert retning (slik at ikke musens avstand har noe å si)
            lengdeDia = math.sqrt((vector[0]**2 + vector[1]**2)/2)

            #lager et skuddobjekt
            bulletSpeedFactor = 16
            _ = Bullet(self.currentPos,[vector[0]/(lengdeDia/bulletSpeedFactor), vector[1]/(lengdeDia/bulletSpeedFactor)],self.dmg, self.size, self.game )

            self.parent.bullets.append(_)
            self.game.bulletSprites.add(_)

            #recoil
            self.currentPos[0] += vector[0]/(lengdeDia/self.recoil)
            self.currentPos[1] += vector[1]/(lengdeDia/self.recoil)

            #om skal forflytte spiller:
            if self.knockBack:
                self.parent.addVelocity([(vector[0]*self.recoil/5)/(-lengdeDia/5),(vector[1]*self.recoil/5)/(-lengdeDia/5)])

            #lager pewpew-ild
            for i in range(int(random.randint(5,14)*self.game.partikkelfaktor)):
                self.parent.particles.append(Particle([5*self.size,5*self.size],self.currentPos,[(vector[0]/(lengdeDia/10)+random.randint(-7,7)), (vector[1]/(lengdeDia/5))+random.randint(-7,7)], "yellow", 7, 0.65))
                self.parent.particles.append(Particle([4*self.size,4*self.size],self.currentPos,[(vector[0]/(lengdeDia/5)+random.randint(-3,3)), (vector[1]/(lengdeDia/5))+random.randint(-3,3)], "red", 5, 0.8))
                self.parent.particles.append(Particle([5*self.size,5*self.size],self.currentPos,[(vector[0]/(lengdeDia/3)+random.randint(-3,3)), (vector[1]/(lengdeDia/3))+random.randint(-3,3)], "black", 5, 0.8))




    def update(self, surf, mouse_pos):
        if self.active:
            if isinstance(self.parent, Player):
                if py.mouse.get_pressed()[0]: self.shoot(mouse_pos)
            self.positionSelf()
            self.update_rotation(mouse_pos)
            self.draw(surf)
            self.cooldown-=1



#klasse for et generelt partikkel
class Particle(py.sprite.Sprite):
    def __init__(self, size, pos, vel, color, lifetime, damping=0.8, img=False):
        super().__init__()
        self.size = [size[0], size[1]]
        self.pos = [pos[0], pos[1]]
        self.vel = [vel[0], vel[1]]
        self.damping = damping
        self.color = color
        self.lifetime = lifetime
        if not (not img):
            self.image = py.image.load(img).convert_alpha()

        else:
            self.image = False
            self.rect = py.rect.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])


    def move(self):
        self.rect.x += self.vel[0]
        self.rect.y += self.vel[1]
        self.vel[0] *= self.damping
        self.vel[1] *= self.damping

    def draw(self, surf):
        if self.image:
            surf.blit(self.image, self.rect)
        else:
            py.draw.rect(surf, self.color, self.rect)

    def update(self, surf):
        self.move()
        self.draw(surf)
        self.lifetime-=1

#versjon av partikkel med andre verdier
class Bullet(Particle):
    def __init__(self, pos, vel, dmg, size, game, enemy=False):
        if enemy:super().__init__([1,1], pos, vel, "black", 150, 0.99,"sprites/topdown_shooter_assets/eBullet.png")
        else:    super().__init__([1,1], pos, vel, "black", 150, 0.99,"sprites/topdown_shooter_assets/sBullet.png")

        self.dmg = dmg

        self.image = py.transform.scale(self.image, (self.image.get_size()[0]*size, self.image.get_size()[1]*size))
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.game = game
        self.canHit = True
        self.sound = py.mixer.Sound("sounds/hitwall.wav")

        self.bounceAmount = 3

    def wallhit(self, dir="none"):
        hits = py.sprite.spritecollide(self, self.game.collisionTiles, False)
        if hits:
            if self.bounceAmount>0:
                match dir:
                    case "x":
                        self.vel[0] *= -1
                        if self.vel[0]>0: self.rect.x+=15
                        if self.vel[0]<0: self.rect.x-=15

                    case "y":
                        self.vel[1] *= -1
                        if self.vel[1]>0: self.rect.y+=15
                        if self.vel[1]<0: self.rect.y-=15
                self.bounceAmount-=1
            else:
                self.lifetime=-1

            self.sound.play()
            for i in range(int(6*self.game.partikkelfaktor)):
                self.game.playerRef.particles.append(Particle([4,4],[self.rect.x, self.rect.y], [random.randint(-2,2),random.randint(-2,2)],"dark gray",random.randint(5,15) ))
                self.game.playerRef.particles.append(Particle([4,4],[self.rect.x, self.rect.y], [random.randint(-4,4),random.randint(-4,4)],"yellow",random.randint(5,12) ))


    def move(self):
        self.rect.x += self.vel[0]
        self.wallhit("x")
        self.rect.y += self.vel[1]
        self.wallhit("y")
        self.vel[0] *= self.damping
        self.vel[1] *= self.damping
        self.lifetime-=1


    def update(self, surf):

        super().update(surf)
        if self.game.showHitbox: py.draw.rect(surf, "red", self.rect)



#en generell "tile". Lager konstante referanser for å optimalisere
GRASSIMG = py.image.load("sprites/grass.png")
WALLIMG  = py.image.load("sprites/wall.png")
class Tiler(py.sprite.Sprite):
    def __init__(self, imgType, pos):
        super().__init__()
        if imgType == "grass": self.sprite = GRASSIMG.convert()
        elif imgType == "wall":self.sprite = WALLIMG.convert()
        else:
            print(f"IMAGE of type {imgType} not found, giving up on life")
            py.quit()
            exit()

        self.sprite = py.transform.scale(self.sprite, (WH/10, WH/10))
        self.pos = pos
        self.rect = py.rect.Rect(pos[0]*self.sprite.get_size()[0]-self.sprite.get_size()[0]+leftSidePadding, pos[1]*self.sprite.get_size()[0]-self.sprite.get_size()[0], self.sprite.get_size()[0], self.sprite.get_size()[1])


    def draw(self, surf):
        surf.blit(self.sprite, (self.rect.x, self.rect.y))



#spillogikk
class Game:
    def __init__(self):

        self.state = "intro"
        self.tiles, self.enemies, self.livingEnemies, self.pickups = [], [], [], []
        self.collisionTiles, self.exits, self.entrances, self.bulletSprites, self.enemyBullets, self.enemySprites = py.sprite.LayeredUpdates(),py.sprite.LayeredUpdates(),py.sprite.LayeredUpdates(), py.sprite.LayeredUpdates(), py.sprite.LayeredUpdates(), py.sprite.Group()

        self.currentRoomIndex = 1
        self.crosshair = Crosshair()




        self.enemyIcon = py.image.load("sprites/topdown_shooter_assets/enemyIcon.png").convert_alpha()

        self.volum = 1
        self.partikkelfaktor = 1

        self.map_surf = py.Surface((1400, 1000),DOUBLEBUF| HWACCEL)
        self.player_hp_surf = py.Surface((leftSidePadding,200),DOUBLEBUF| HWACCEL)
        self.hitlist_surf = py.Surface((leftSidePadding,800))
        self.leftDisplay = py.Surface((leftSidePadding,1000),DOUBLEBUF| HWACCEL)
        self.chosenDeathMessage = False


        self.player = py.sprite.LayeredUpdates()
        self.playerRef = Player([500,500], 10, 500, self)
        self.showHitbox = False

        self.load_level()
        py.mixer.music.load("sounds/music.wav")
        py.mixer.music.set_volume(0.5)
        py.mixer.music.play(-1)


    #leftSideDisplay (fiendeliste)
    def player_hp_bar_update(self):
        self.player_hp_surf.fill("pink")
        player_hp_label = Label([200,25],30,"PLAYERHEALTH:", "black")
        hp_bar_bg = py.rect.Rect(25, 50, 350, 30)
        hp_bar = py.rect.Rect(27, 52, 346*(self.playerRef.hp/self.playerRef.inithp), 26)
        hp = Label([100, 64],15, f"HP: {self.playerRef.hp} / {self.playerRef.inithp}", "white")
        py.draw.rect(self.player_hp_surf, "white", hp_bar_bg)
        py.draw.rect(self.player_hp_surf, "red", hp_bar)
        hp.draw(self.player_hp_surf)
        player_hp_label.draw(self.player_hp_surf)
        self.display("player")

    def place_hitlist_object(self, i):
        fromTop = 50
        current_enemy = self.livingEnemies[i]
        displayRect = py.rect.Rect(45,fromTop+102*i,310,100)
        img = self.enemyIcon
        img = py.transform.scale(img, [40*(self.enemies[i].scale-0.5),40*(self.enemies[i].scale-0.3)])
        img_rect = img.get_rect()
        img_rect.centerx, img_rect.centery= 85,fromTop+55+i*100
        py.draw.rect(self.hitlist_surf,"beige", displayRect)
        name = Label([200, 20+fromTop+102*i],15,f"{current_enemy.name}","black" )
        type = Label([200, fromTop+35+102*i],13,f"Type: {current_enemy.type}","black" )
        name.draw(self.hitlist_surf)
        type.draw(self.hitlist_surf)

        hp_bar = py.rect.Rect(120, fromTop+50+i*102,(current_enemy.hp/current_enemy.inithp)*200, 20)
        hp = Label([150, fromTop+60+i*102],15, f"{current_enemy.hp} / {current_enemy.inithp}", "white")
        py.draw.rect(self.hitlist_surf, "red", hp_bar)
        hp.draw(self.hitlist_surf)
        self.hitlist_surf.blit(img, img_rect)
        pass
    def hitlist_update(self, target=False):
        self.updateEnemyLists()
        if not target:
            self.hitlist_surf.fill("pink")
            enemy_list_label = Label([200, 10], 30, "HITLIST:", "black")
            enemy_list_label.draw(self.hitlist_surf)


            for i in range(len(self.livingEnemies)):
                self.place_hitlist_object(i)

        else:
            i=self.livingEnemies.index(target)
            self.place_hitlist_object(i)
        self.display("hitlist")
    def display(self, newSurf="None"):

        match newSurf:
            case "player": self.leftDisplay.blit(self.player_hp_surf.convert(), (0,0))
            case "hitlist":self.leftDisplay.blit(self.hitlist_surf.convert(), (0,200))
            case "None": print("no new info")
            case "both":
                self.hitlist_update()
                self.player_hp_bar_update()
                self.leftDisplay.blit(self.player_hp_surf.convert(), (0,0))
                self.leftDisplay.blit(self.hitlist_surf.convert(), (0,200))
            case _:      print("Invalid request")


        #tegner romnummer
        romNummer = Label([200, 110], 30, f"ROM {self.currentRoomIndex}", "blue")

        py.draw.rect(self.leftDisplay, "pink", py.rect.Rect(0,100,leftSidePadding,30))
        romNummer.draw(self.leftDisplay)

    def display_draw(self, surf):
        surf.blit(self.leftDisplay, (0,0))

    def load_level(self):
        self.tiles, self.enemies, self.livingEnemies, self.pickups = [], [], [], []
        self.collisionTiles, self.exits, self.entrances, self.bulletSprites, self.enemySprites = py.sprite.LayeredUpdates(),py.sprite.LayeredUpdates(), py.sprite.LayeredUpdates(), py.sprite.LayeredUpdates(), py.sprite.Group()
        self.playerRef.bullets = []

        for i in range(0, len(rooms[self.currentRoomIndex]["map"])):
            for j in range(0, len(rooms[self.currentRoomIndex]["map"])):
                if rooms[self.currentRoomIndex]["map"][i][j]==0:
                    self.tiles.append(Tiler("grass",[(j),i]))
                if rooms[self.currentRoomIndex]["map"][i][j]==1:
                    _ = Tiler("wall",[(j),i])
                    self.collisionTiles.add(_)
                    self.tiles.append(_)
                if rooms[self.currentRoomIndex]["map"][i][j]==2:
                    _ = Tiler("grass",[(j),i])
                    self.exits.add(_)
                    self.tiles.append(_)
                if rooms[self.currentRoomIndex]["map"][i][j]==3:
                    _ = Tiler("grass",[(j),i])
                    self.entrances.add(_)
                    self.tiles.append(_)
        self.update_map()

    def chooseRandomEnemy(self,p, speedRange, healthRange, damage):
        _ = random.randrange(0,100)

        if _<45:
            return ChaseEnemy(
                [random.randint(100,WH-150),random.randint(100,WH-150)],
                random.randrange(speedRange[0], speedRange[1]),
                random.randint(healthRange[0], healthRange[1])+self.currentRoomIndex,
                damage,500,p,self)

        elif _<70:
            return RunEnemy(
                [random.randint(100,WH-150),random.randint(100,WH-150)],
                random.randrange(speedRange[0], speedRange[1]),
                random.randint(healthRange[0], healthRange[1])+self.currentRoomIndex,
                damage,500,p,self)
        elif _<100:
            return ShootingEnemy([random.randint(100,WH-150),random.randint(100,WH-150)],random.randrange(speedRange[0], speedRange[1]),random.randint(healthRange[0], healthRange[1])+self.currentRoomIndex,damage,500,p,self,1.4)
        else: return

    def spawnEnemies(self, p, amount, speedRange, healthRange, damage, bigSpawnChance):
        for i in range(amount):
            if random.randrange(0,100) > bigSpawnChance:
                _ = self.chooseRandomEnemy(p,speedRange,healthRange,damage)

            else:
                _ = ChaseEnemy(
                    [random.randint(100,WH-150),random.randint(100,WH-150)],
                    random.randrange(speedRange[0], speedRange[1])/2,
                    random.randint(healthRange[0], healthRange[1])*2,
                    damage*3,500,p,self,3)
            self.enemies.append(_)
            self.livingEnemies.append(_)
            self.enemySprites.add(_)
        self.hitlist_update()

    def update_map(self):
        for t in self.tiles:
            t.draw(self.map_surf)

    def draw_level(self, surf):

        surf.blit(self.map_surf,(0,0))


    def updateEnemyLists(self):
        self.enemies = [e for e in self.enemies if e.despawnTimer>0]
        self.livingEnemies = [e for e in self.enemies if e.alive]
        self.enemySprites = py.sprite.Group(self.livingEnemies)


    #settings-skjerm med volumkontroll og mulighet til å lukke spillet samt begrense partikler
    def settingsScreen(self, surf, mousePos):
        bg = py.rect.Rect(0,0, WW, WH)
        py.draw.rect(surf, "pink", bg)
        title = Label([WW/2, WH/5], 80, "SETTINGS", "Black")
        title.draw(surf)

        #knapper
        resume = Button([WW/2, WH/2],[500,75], "FORTSETT SPILL", 0,False, "dark green", "white")
        if resume.is_pressed(mousePos): self.state = "game"


        quit = Button([WW/2, WH-100],[400,75], "LUKK SPILL", 0,False, "red", "white")
        if quit.is_pressed(mousePos):
            py.quit()
            exit()

        volume_label = Label([WW/2, WH/2+200], 30, f"VOLUM: {self.volum*100:.1f}", "black")

        volumeUp = Button([WW/2+200, WH/2+200], [30, 30], "+", 1, False)
        volumeDown = Button([WW/2-200, WH/2+200], [30, 30], "-", -1, False)
        if volumeUp.is_pressed(mousePos):
            self.volum+=0.1
            py.mixer.music.set_volume(self.volum)
        if volumeDown.is_pressed(mousePos):
            self.volum-=0.1
            py.mixer.music.set_volume(self.volum)

        partikkel_label = Label([WW/2, WH/2+250], 30, f"PARTIKKELFAKTOR: {self.partikkelfaktor:.1f}", "black")

        particleUp = Button([WW/2+200, WH/2+250], [30, 30], "+", 1, False)
        particleDown = Button([WW/2-200, WH/2+250], [30, 30], "-", -1, False)

        if particleUp.is_pressed(mousePos):
            self.partikkelfaktor+=0.1
        if particleDown.is_pressed(mousePos):
            self.partikkelfaktor-=0.1
        bs = [resume, quit, volumeUp, volumeDown, particleUp, particleDown]
        ls = [volume_label, partikkel_label]
        for b in bs: b.update(surf, mousePos)
        for l in ls: l.draw(surf)

    def chooseDeathMessage(self):
        return  Dialog(f"DINE SISTE ORD: '{random.choice(SISTEORD)}'", "black", [WW/2, WH/2+300])

    def gameOverScreen(self, surf, mousePos):
        if not self.chosenDeathMessage:
            self.chosenDeathMessage = self.chooseDeathMessage()
        bg = py.rect.Rect(0,0, WW, WH)
        py.draw.rect(surf, "pink", bg)
        title = Label([WW/2, WH/3], 40, "GAME OVER", "Black")
        title.draw(surf)

        romNummer = Label([WW/2, WH/2+200], 30, f"DU KOM TIL ROM {self.currentRoomIndex}", "blue")
        romNummer.draw(surf)
        #viser fiende som drepte deg
        sisteFiende = Label([WW/2, WH/2+250], 25, f"DREPT AV: {self.playerRef.lastTouchedEnemyName}", "red")
        sisteFiende.draw(surf)
        #viser tilfeldige siste ord
        self.chosenDeathMessage.draw(surf)



        play_b = Button([WW/2, WH/2],[300,75], "RESTART", 0,False, "black", "white")
        if play_b.is_pressed(mousePos):
            self.state = "game"
            self.playerRef = Player([500,500], 10, 500, self)
            self.currentRoomIndex = 1
            self.load_level()

        play_b.update(surf, mousePos)


    def gameLoop(self, surf, mousePos):
        if self.chosenDeathMessage: self.chosenDeathMessage=False
        keys = py.key.get_pressed()
        if keys[K_r]: self.showHitbox = False
        if keys[K_t]: self.showHitbox = True
        if keys[K_ESCAPE]: self.state="settings"
        self.draw_level(surf)
        self.updateEnemyLists()

        pups = [p for p in self.pickups if p.lifetime>0]

        for e in self.enemies:
            e.update(surf)

        for p in pups:
            p.update(surf)
        self.playerRef.update(surf, py.mouse.get_pos())
        self.display_draw(surf)



    def introScreen(self, surf, mousePos):
        bg = py.rect.Rect(0,0, WW, WH)
        py.draw.rect(surf, "pink", bg)
        title = Label([WW/2, WH/3], 40, "PANGPANGSKYTESPILL", "Black")
        title.draw(surf)
        play_b = Button([WW/2, WH/2],[200,75], "SPILL", 0,False, "black", "white")
        if play_b.is_pressed(mousePos): self.state = "game"
        play_b.update(surf, mousePos)


    def update(self, surf, mousePos, events):
        for e in events:
            if e.type == QUIT:
                py.quit()
                exit()

        match self.state:
            case "game":     self.gameLoop(      surf, mousePos)
            case "intro":    self.introScreen(   surf, mousePos)
            case "gameOver": self.gameOverScreen(surf, mousePos)
            case "settings": self.settingsScreen(surf, mousePos)
        self.crosshair.update(surf, mousePos, events)




class Dialog:
    def __init__(self, text, char, pos):
        self.targetText = text
        self.currentText = ""
        self.char = char
        self.pos = [pos[0], pos[1]]
        self.font = returnFont(20)

    def talk(self):
        if len(self.targetText)>0: self.currentText += self.targetText[0]
        self.targetText = self.targetText[1:]

    def draw(self, surf):
        self.talk()
        t = self.font.render(str(self.currentText),False,"black")
        textRect = t.get_rect()
        textRect.center = (self.pos[0], self.pos[1])
        surf.blit(t, textRect)

class Label:
    def __init__(self, pos, size, displayText, color):
        self.txtColor = color
        self.d_t = displayText
        self.font = returnFont(int(size/1.5))
        self.text = self.font.render(str(displayText),False,self.txtColor)
        self.textRect = self.text.get_rect()
        self.textRect.center = (pos[0], pos[1])

    def updateColor(self, color):
        self.text = self.font.render(str(self.d_t),False,color)
    def draw(self, surf):

        surf.blit(self.text, self.textRect)

class Button(Label):
    def __init__(self, pos, size, displayText, sound_vibe = 0,UI=False, inactiveColor="beige", hoverColor="gray"):
        self.inactiveColor = inactiveColor
        self.hoverColor = hoverColor
        self.currentColor = [self.inactiveColor, self.hoverColor]
        self.rect = py.rect.Rect(pos[0]-size[0]/2, pos[1]-size[1]/2, size[0], size[1])
        if UI: self.x_d = 1400
        else: self.x_d = 0

        self.clickable = True
        if sound_vibe   > 0: self.sound = py.mixer.Sound("sounds/button_up.wav")
        elif sound_vibe < 0: self.sound = py.mixer.Sound("sounds/button_down.wav")
        else: self.sound = False

        super().__init__(pos, size[1]/1.5, displayText, self.currentColor[1])

    def is_pressed(self, mousePos):
        if self.rect.left+self.x_d<mousePos[0]<self.rect.right+self.x_d and self.rect.top<mousePos[1]<self.rect.bottom:
            self.currentColor = [self.hoverColor, self.inactiveColor]
            if self.txtColor != self.currentColor[1]: self.updateColor(self.currentColor[1])
            if py.mouse.get_pressed()[0] :

                if self.clickable:
                    if not self.sound:
                        print("no sound file")
                    else:
                        self.sound.play()
                        self.sound.set_volume(0.2)
                    return True
                self.clickable = False
        else:
            self.currentColor = [self.inactiveColor, self.hoverColor]
        if not py.mouse.get_pressed()[0]:
            self.clickable=True

    def draw(self, surf):
        py.draw.rect(surf, self.currentColor[0],self.rect)
        if self.txtColor != self.currentColor[1]: self.updateColor(self.currentColor[1])
        super().draw(surf)
    def update(self, surf, mousepos):
        self.is_pressed(mousepos)
        self.draw(surf)


class Pickup(py.sprite.Sprite):
    def __init__(self, pos, sprite, lifetime, game):
        self.img = sprite.convert_alpha()
        self.game = game
        self.rect = self.img.get_rect()

        self.rect.x, self.rect.y = pos
        self.lifetime = lifetime
        game.pickups.append(self)

    def playerDetector(self):
        hits = py.sprite.spritecollide(self, self.game.player, False)
        if hits:
            self.lifetime=-1
            return [True, hits[0]]

        return [False]
    def update(self, surf):
        self.lifetime-=1
        surf.blit(self.img, self.rect)

class HealthPickup(Pickup):
    def __init__(self, pos, game):
        super().__init__(pos,py.transform.scale(py.image.load("sprites/hp_pu.png"),(40,40)),100, game)

    def update(self, surf):
        super().update(surf)
        if self.playerDetector()[0]:
            p = self.playerDetector()[1]
            if p.hp+100<p.inithp: p.hp+=100
            elif p.hp+100>p.inithp: p.hp=p.inithp

            self.game.player_hp_bar_update()


class Crosshair():
    def __init__(self):

        self.image = py.image.load("sprites/crosshair_.png").convert_alpha()
        self.image = py.transform.scale(self.image, (40,40))
        self.rect = self.image.get_rect()

    def moveMouse(self, mousePos):
        self.rect.center = mousePos
    def update(self, surf, mousepos, events):

        for e in events:
            if e.type== MOUSEMOTION: self.moveMouse(mousepos)
        #make the cursor rotate around its own center

        surf.blit(self.image, self.rect)

