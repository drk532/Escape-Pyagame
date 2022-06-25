import pygame
from pygame.locals import *
import sys
import math
import random

pygame.init()

w,h=512,288

win=pygame.display.set_mode((w,h))
pygame.display.set_caption('my game')

bg=pygame.image.load('bg.jpg').convert()


bgx=0
bgx2=bg.get_width()

clock=pygame.time.Clock()

class player(object):
    run=[pygame.image.load(str(x)+'.png')for x in range(8,16)]
    jump=[pygame.image.load(str(x)+'.png')for x in range(1,8)]
    jumplist=[1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,3,3,3,3,3,4,4,4,4,4,4,4,4,4,4,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,-1,-1,-1,-1,-1,-1,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4]
    slide=[pygame.image.load('s1.png'),pygame.image.load('s2.png'),pygame.image.load('s2.png'),pygame.image.load('s2.png'),pygame.image.load('s2.png'),pygame.image.load('s2.png'),pygame.image.load('s2.png'),pygame.image.load('s2.png'),pygame.image.load('s3.png'),pygame.image.load('s4.png'),pygame.image.load('s5.png')]
    def __init__(self,x,y,width,height):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.runCount=0
        self.jumping=False
        self.jumpCount=0
        self.sliding=False
        self.slideCount=0
        self.slideup=False
    def draw(self,win):
        if self.jumping:
            self.y-=self.jumplist[self.jumpCount]*0.8
            win.blit(self.jump[self.jumpCount//18],(self.x,self.y))
            self.jumpCount+=1
            if self.jumpCount>108:
                self.jumpCount=0
                self.jumping=False
                self.runCount=0
        elif self.sliding or self.slideup:
            if self.slideCount<20:
                self.y+=1
            elif self.slideCount==80:
                self.y-=19
                self.sliding=False
                self.slideup=True
            if self.slideCount>=110:
                self.slideCount=0
                self.slideup=False
                self.runCount=0
            win.blit(self.slide[self.slideCount//10],(self.x,self.y))
            self.slideCount+=1
        else:
             if self.runCount>42:
                self.runCount=0
             win.blit(self.run[self.runCount//6],(self.x,self.y))
             self.runCount+=1


class saw(object):
    rotate=[pygame.image.load('SAW0.PNG'),pygame.image.load('SAW1.PNG'),pygame.image.load('SAW2.PNG'),pygame.image.load('SAW3.PNG')]
    def __init__(self,x,y,width,height):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.rotateCount=0
        self.vel=1.4
    def draw(self,win):
        self.hitbox=(self.x+10,self.y+5,self.width-20,self.height-5)
        pygame.draw.rect(win,(255,0,0),self.hitbox,2)
        if self.rotateCount>=8:
            self.rotateCount=0
        win.blit(pygame.transform.scale(self.rotate[self.rotateCount//2],(64,64)),(self.x,self.y))
            

class spike(saw):  
    img = pygame.image.load('spike.png')
    def draw(self,win):
        self.hitbox = (self.x + 10, self.y, 28,315)
        pygame.draw.rect(win, (255,0,0), self.hitbox, 2)
        win.blit(self.img, (self.x,self.y))




def redrawWindow():
    win.blit(bg,(bgx,0))
    win.blit(bg,(bgx2,0))
    runner.draw(win)
    for obstacle in obstacles:
        obstacle.draw(win)
    pygame.display.update()


run=True
obstacles=[]
pygame.time.set_timer(USEREVENT+1, 500)
pygame.time.set_timer(USEREVENT+2,random.randrange(2000,4500))
runner = player(32,186 ,64, 64)
speed=30
while run:
    redrawWindow()
    bgx-=1.4
    bgx2-=1.4
    keys=pygame.key.get_pressed()
    if bgx<bg.get_width()*-1:
        bgx=bg.get_width()
    if bgx2<bg.get_width()*-1:
        bgx2=bg.get_width()
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False
            pygame.quit()
            quit()
        if keys[pygame.K_SPACE or pygame.K_UP]:
            if not(runner.jumping):
                runner.jumping=True
        if keys[pygame.K_DOWN]:
            if not(runner.sliding):
                runner.sliding=True
        if event.type == USEREVENT+1:
            speed += 1
        if event.type == USEREVENT+2:
            r=random.randrange(0,2)
            if r == 0:
                obstacles.append(saw(450, 186, 64, 64))
            elif r==1:
                obstacles.append(spike(450,-120,48,186))
    for obstacle in obstacles: 
        obstacle.x -= 1.4
        if obstacle.x < obstacle.width * -1:
            obstacles.pop(obstacles.index(obstacle))
    clock.tick(speed)
