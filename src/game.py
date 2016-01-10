#Requirements
import sys
import os
import random
import pygame
from pygame.locals import *
import constants
#import player
import bricks
import player
pygame.init()

#Start Class Declaration
class PyBreakout:

    def __init__(self):
        self.initialize()
        self.mainLoop()

    #Declare variables and initialization classes here
    def initialize(self):
        pygame.init()

        self.width = 924
        self.height = 768
        self.screen = pygame.display.set_mode((self.width, self.height))

        self.caption = "pyBreakout"
        pygame.display.set_caption(self.caption)

        self.framerate = 60
        #self.backgroundColour = (255,255,255)
        #self.foregroundColour = (0,99,207)

        self.clock = pygame.time.Clock()

        self.fontScore = pygame.font.SysFont("Arial Black", 21, bold=False)

        self.gameScore = 0
        self.gameBatsLeft = 3
        self.gameBricksLeft = 120

        #self.brick = bricks.Brick(self.screen)

        self.ticks = 0

        #initialize the bricks that will be displayed
        self.bricksArr = []
        # xPos = 44
        # yPos = 160
        # for i in range(12):
        #     brickObj = bricks.Brick(self.screen)
        #     brickObj.setPosX(xPos)
        #     brickObj.setPosY(yPos)
        #     self.bricksArr.append(brickObj)
        #     xPos += 70

        self.initBricks()
        self.special = random.randint(1, 120)

        self.bat = player.Bat(self.screen)

        self.projectile = player.Projectile(self.screen)

        self.projectileFired = False

    def initBricks(self):
        yPos = 160
        for x in range(10):
            xPos = 44
            for i in range(12):
                brickObj = bricks.Brick(self.screen)
                brickObj.setPosX(xPos)
                brickObj.setPosY(yPos)
                self.bricksArr.append(brickObj)
                xPos += 70
            yPos += 22


    def fireProjectile(self):
        self.projectileFired = True
        self.projectile.setPosition(self.bat.getPosX() + 42, self.bat.getPosY())

    def mainLoop(self):
        while True:
            gameTime = self.clock.get_time()
            self.update(gameTime)
            self.draw(gameTime)
            self.clock.tick(self.framerate)

    #Projectile Collision Handler
    def projectileCollision(self):

        #Draw bounding box for Projectile
        rectProjectile = pygame.Rect(self.projectile.getPosX(), self.projectile.getPosY(),5,5)

        #Draw bounding box for Bricks
        for i in range(120):
            rectBrick = pygame.Rect(self.bricksArr[i].getPosX(),self.bricksArr[i].getPosY(), 66, 18)
            if rectProjectile.colliderect(rectBrick):
                if i == self.special:
                    self.gameBatsLeft += 1
                    self.gameScore += 20
                else:
                    self.bricksArr[i].setPosX(1000)
                    self.gameBricksLeft = self.gameBricksLeft - 1
                    self.gameScore += 10
                    self.projectile.reflect()
                    self.projectile.reflectGrad()

        #Draw bounding box for bat
        rectBat = []
        rectBat.append(pygame.Rect(self.bat.getPosX(), self.bat.getPosY(), 20, 15))
        rectBat.append(pygame.Rect(self.bat.getPosX()+20, self.bat.getPosY(), 20, 15))
        rectBat.append(pygame.Rect(self.bat.getPosX()+40, self.bat.getPosY(), 5, 15))
        rectBat.append(pygame.Rect(self.bat.getPosX()+45, self.bat.getPosY(), 20, 15))
        rectBat.append(pygame.Rect(self.bat.getPosX()+65, self.bat.getPosY(), 20, 15))

        for i in range(5):
            if rectProjectile.colliderect(rectBat[0]):
                self.projectile.setGrad(-1)
                self.projectile.reflect()
            elif rectProjectile.colliderect(rectBat[1]):
                self.projectile.setGrad(-0.3)
                self.projectile.reflect()
            elif rectProjectile.colliderect(rectBat[2]):
                self.projectile.setGrad(0)
                self.projectile.reflect()
            elif rectProjectile.colliderect(rectBat[3]):
                self.projectile.setGrad(0.3)
                self.projectile.reflect()
            elif rectProjectile.colliderect(rectBat[4]):
                self.projectile.setGrad(1)
                self.projectile.reflect()

        #Draw bounding box for walls
        rectWalls = []
        rectWalls.append(pygame.Rect(20,50,20,650))
        rectWalls.append(pygame.Rect(20,50,884,20))
        rectWalls.append(pygame.Rect(884,50,20,650))
        for i in range(3):
            if rectProjectile.colliderect(rectWalls[i]):
                self.projectile.reflectGrad()

        #Draw Bounding for entire level (lost projectile)
        rectOutofBounds = pygame.Rect(0,760,1000,10) # remember to do the thing
        if rectProjectile.colliderect(rectOutofBounds):
            self.projectileFired = False
            self.gameBatsLeft = self.gameBatsLeft - 1
            self.projectile.setGrad(0)
            self.projectile.reflect()

    def gameLost(self):
        print("balls")

    def gameWon(self):
        print("thing")

    def update(self, gameTime):

        if self.gameBatsLeft == -1:
            self.gameLost()
        if self.gameBricksLeft == 0:
            self.gameWon()

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game = MainMenu()

        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_a] or pressed[pygame.K_LEFT]:
            if self.bat.getPosX() >= 44:
                self.bat.setPosX(self.bat.getPosX() - 10)
        if pressed[pygame.K_d] or pressed[pygame.K_RIGHT]:
            if self.bat.getPosX() <= 799:
                self.bat.setPosX(self.bat.getPosX() + 10)
        if pressed[pygame.K_SPACE] and (self.projectileFired == False):
            self.fireProjectile() #could use some work

        self.ticks = self.ticks + gameTime

        if (self.projectileFired == True):
            self.projectile.move()
            self.projectileCollision()


    def draw(self, gameTime):
        self.screen.fill(constants.backgroundColour)

        #Display The Scoring Text
        labelBricksLeft = self.fontScore.render("Bricks Left: %d" % self.gameBricksLeft, 1, constants.foregroundColour)
        labelBatsLeft = self.fontScore.render("Bats Left: %d" % self.gameBatsLeft, 1, constants.foregroundColour)
        labelScore = self.fontScore.render("Score: %d" % self.gameScore, 1, constants.foregroundColour)

        #write text to screen
        self.screen.blit(labelBricksLeft, (20,20))
        self.screen.blit(labelBatsLeft, (370,20))
        self.screen.blit(labelScore, (710,20))

        #Draw bounding boxes
        pygame.draw.rect(self.screen, constants.foregroundColour, [20,50,20,650])
        pygame.draw.rect(self.screen, constants.foregroundColour, [20,50,884,20])
        pygame.draw.rect(self.screen, constants.foregroundColour, [884,50,20,650])


        # Colour the blocks
        c = 0
        for x in range(120):
            self.bricksArr[x].draw(c)
            if (x == 23 or x == 47 or x == 71 or x == 95):
                c = c + 1

        self.bricksArr[self.special].draw(5)

        #Draw Player
        self.bat.draw()

        if (self.projectileFired == True):
            self.projectile.draw()

        #Projectile Debug

        pygame.display.flip()

class MainMenu:

    def __init__(self):
        pygame.init()

        self.width = 924
        self.height = 768
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.framerate = 60
        self.fontWelcome = pygame.font.SysFont("Arial Black", 21, bold=False)
        self.logo = pygame.image.load(os.path.join('resources', 'logo.jpg'))
        self.state = 0

        self.mainLoop()

    def setState(self, state):
        #0: Main menu 1: Win 2: Loss
        self.state = state

    def mainLoop(self):
        while True:
            gameTime = self.clock.get_time()
            self.update(gameTime)
            self.draw(gameTime)
            self.clock.tick(self.framerate)

    def update(self, gameTime):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_SPACE:
                    game = PyBreakout()

    def draw(self, gameTime):
        self.screen.fill(constants.backgroundColour)

        labelWelcome = self.fontWelcome.render("Press <Space> To Start Game", 1, constants.foregroundColour)

        if self.state == 0:
            self.screen.blit(self.logo, (40,200))
            self.screen.blit(labelWelcome, (300, 400))


        pygame.display.flip()


if __name__ == "__main__":
    game = MainMenu()
