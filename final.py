import pygame
from pygame.locals import *
import sys
import math
import random

pygame.init()

w,h=512,288


win=pygame.display.set_mode((w,h))
pygame.display.set_caption('robo jump')

bg=pygame.image.load('bg.jpg').convert()


bgx=0
bgx2=bg.get_width()

clock=pygame.time.Clock()

class player(object):
    run=[pygame.image.load(str(x)+'.png')for x in range(8,16)]
    jump=[pygame.image.load(str(x)+'.png')for x in range(1,8)]
    jumplist=[1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,3,3,3,3,3,4,4,4,4,4,4,4,4,4,4,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,-1,-1,-1,-1,-1,-1,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4]
    slide=[pygame.image.load('s1.png'),pygame.image.load('s2.png'),pygame.image.load('s2.png'),pygame.image.load('s2.png'),pygame.image.load('s2.png'),pygame.image.load('s2.png'),pygame.image.load('s2.png'),pygame.image.load('s2.png'),pygame.image.load('s3.png'),pygame.image.load('s4.png'),pygame.image.load('s5.png')]
    fall = pygame.image.load('0.png')
    def __init__(self,x,y,width,height):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.runCount=0
        self.jumping=False
        self.jumpCount=0
        self.sliding=False
        self.falling=False
        self.slideCount=0
        self.slideup=False
    def draw(self,win):

        if self.falling:
            win.blit(self.fall,(self.x,self.y+30))

            
        elif self.jumping:
            self.y-=self.jumplist[self.jumpCount]*1.2
            win.blit(self.jump[self.jumpCount//18],(self.x,self.y))
            self.jumpCount+=1
            if self.jumpCount>108:
                self.jumpCount=0
                self.jumping=False
                self.runCount=0
                
            self.hitbox=(self.x+4,self.y,self.width-24,self.height-10)
                
        elif self.sliding or self.slideup:
            if self.slideCount<20:
                self.y+=1

                self.hitbox=(self.x+4,self.y,self.width-24,self.height-10)
                
            elif self.slideCount==80:
                self.y-=19
                self.sliding=False
                self.slideup=True

            elif self.slideCount>20 and self.slideCount<80:
                self.hitbox=(self.x,self.y+3,self.width-8,self.height-35)

                
            if self.slideCount>=110:
                self.slideCount=0
                self.slideup=False
                self.runCount=0

                self.hitbox=(self.x+4,self.y,self.width-24,self.height-10)

                
            win.blit(self.slide[self.slideCount//10],(self.x,self.y))
            self.slideCount+=1
        else:
             if self.runCount>42:
                self.runCount=0
             win.blit(self.run[self.runCount//6],(self.x,self.y))
             self.runCount+=1

             
             self.hitbox=(self.x+4,self.y,self.width-24,self.height-10)


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
        if self.rotateCount>=8:
            self.rotateCount=0
        win.blit(pygame.transform.scale(self.rotate[self.rotateCount//2],(64,64)),(self.x,self.y))
        self.rotateCount+=1

    def collide(self,rect):
        if rect[0]+rect[2]>self.hitbox[0] and rect[0]<self.hitbox[0]+self.hitbox[2]:
            if rect[1]+rect[3]>self.hitbox[1]:
                return True
            return False
            

class spike(saw):  
    img = pygame.image.load('spike.png')
    def draw(self,win):
        self.hitbox = (self.x + 10, self.y, 10,192)
        pygame.draw.rect(win, (255,0,0), self.hitbox, 2)
        win.blit(self.img, (self.x,self.y))


    def collide(self,rect):
        if rect[0]+rect[2]>self.hitbox[0] and rect[0]<self.hitbox[0]+self.hitbox[2]:
            if rect[1]<self.hitbox[3]:
                return True
            return False


def updateFile():
    f = open('scores.txt','r')
    file = f.readlines()
    last = int(file[0])

    if last < int(score):
        f.close()
        file = open('scores.txt', 'w')
        file.write(str(score))
        file.close()

        return score

    return last





def endScreen():
    global pause, score, speed, obstacles
    pause = 0
    speed = 30
    obstacles = []

    run = True
    while run:
        pygame.time.delay(100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False
                runner.falling = False
                runner.sliding = False
                runner.jumpin = False

        win.blit(bg, (0,0))
        largeFont = pygame.font.SysFont('comicsans', 80)
        lastScore = largeFont.render('Best Score: ' + str(updateFile()),1,(255,255,255))
        currentScore = largeFont.render('Score: '+ str(score),1,(255,255,255))
        win.blit(lastScore, (w/2 - lastScore.get_width()/2,150))
        win.blit(currentScore, (w/2 - currentScore.get_width()/2, 240))
        pygame.display.update()
    score = 0









def redrawWindow():
    largeFont = pygame.font.SysFont('comicsans', 30)
    win.blit(bg,(bgx,0))
    win.blit(bg,(bgx2,0))
    text = largeFont.render('Score: ' + str(score), 1, (255,255,255))
    runner.draw(win)
    for obstacle in obstacles:
        obstacle.draw(win)
            

    win.blit(text, (400, 10))
    
    pygame.display.update()


run=True
obstacles=[]
pygame.time.set_timer(USEREVENT+1, 500)
pygame.time.set_timer(USEREVENT+2,random.randrange(3000,5000))
runner = player(32,186 ,64, 64)
speed=30
score = 0
pause = 0
fallSpeed = 0

while run:

    if pause > 0:
        pause += 1
        if pause > fallSpeed * 2:
            endScreen()

    score = speed//10 - 3
    for obstacle in obstacles: 
        obstacle.x -= 1.4
        if obstacle.collide(runner.hitbox):
            runner.falling=True



            if pause == 0:
                pause = 1
                fallSpeed = speed
            
        if obstacle.x < obstacle.width * -1:
            obstacles.pop(obstacles.index(obstacle))


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
                obstacles.append(spike(450,-122,64,310))
    redrawWindow()
    clock.tick(speed)
