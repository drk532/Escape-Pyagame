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

    def __init__(self,x,y,width,height):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.runCount=0
    def draw(self,win):
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
    if bgx<bg.get_width()*-1:
        bgx=bg.get_width()
    if bgx2<bg.get_width()*-1:
        bgx2=bg.get_width()
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False
            pygame.quit()
            quit()
        if event.type == USEREVENT+1:
            speed += 1
    clock.tick(speed)
