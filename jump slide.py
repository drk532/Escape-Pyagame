import pygame
from pygame.locals import *
import sys
import math

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
def redrawWindow():
    win.blit(bg,(bgx,0))
    win.blit(bg,(bgx2,0))
    runner.draw(win)
    pygame.display.update()

run=True
pygame.time.set_timer(USEREVENT+1, 500)
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
    clock.tick(speed)
