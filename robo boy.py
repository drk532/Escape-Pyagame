import pygame
from pygame.locals import *
import sys
import math
import random

pygame.init()

w,h=512,288


screen=pygame.display.set_mode((w,h))
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
        self.RUNC=0
        self.jumping=False
        self.JC=0
        self.sliding=False
        self.falling=False
        self.SC=0
        self.slideup=False
    def draw(self,screen):

        if self.falling:
            screen.blit(self.fall,(self.x,self.y+30))

            
        elif self.jumping:
            self.y-=self.jumplist[self.JC]*1.2
            screen.blit(self.jump[self.JC//18],(self.x,self.y))
            self.JC+=1
            if self.JC>108:
                self.JC=0
                self.jumping=False
                self.RUNC=0
                
            self.hit=(self.x+4,self.y,self.width-24,self.height-10)
                
        elif self.sliding or self.slideup:
            if self.SC<20:
                self.y+=1

                self.hit=(self.x+4,self.y,self.width-24,self.height-10)
                
            elif self.SC==80:
                self.y-=19
                self.sliding=False
                self.slideup=True

            elif self.SC>20 and self.SC<80:
                self.hit=(self.x,self.y+3,self.width-8,self.height-35)

                
            if self.SC>=110:
                self.SC=0
                self.slideup=False
                self.RUNC=0

                self.hit=(self.x+4,self.y,self.width-24,self.height-10)

                
            screen.blit(self.slide[self.SC//10],(self.x,self.y))
            self.SC+=1
        else:
             if self.RUNC>42:
                self.RUNC=0
             screen.blit(self.run[self.RUNC//6],(self.x,self.y))
             self.RUNC+=1

             
             self.hit=(self.x+4,self.y,self.width-24,self.height-10)


class saw(object):
    rotate=[pygame.image.load('SAW0.PNG'),pygame.image.load('SAW1.PNG'),pygame.image.load('SAW2.PNG'),pygame.image.load('SAW3.PNG')]
    def __init__(self,x,y,width,height):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.RC=0
        self.vel=1.4
    def draw(self,screen):
        self.hit=(self.x+10,self.y+5,self.width-20,self.height-5)
        if self.RC>=8:
            self.RC=0
        screen.blit(pygame.transform.scale(self.rotate[self.RC//2],(64,64)),(self.x,self.y))
        self.RC+=1

    def collison(self,rect):
        if rect[0]+rect[2]>self.hit[0] and rect[0]<self.hit[0]+self.hit[2]:
            if rect[1]+rect[3]>self.hit[1]:
                return True
            return False
            

class spike(saw):  
    img = pygame.image.load('spike.png')
    def draw(self,screen):
        self.hit = (self.x + 10, self.y, 10,192)
        pygame.draw.rect(screen, (255,0,0), self.hit, 2)
        screen.blit(self.img, (self.x,self.y))


    def collison(self,rect):
        if rect[0]+rect[2]>self.hit[0] and rect[0]<self.hit[0]+self.hit[2]:
            if rect[1]<self.hit[3]:
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
    global pause, score, speed, obss
    pause = 0
    speed = 30
    obss = []

    run = True
    while run:
        pygame.time.delay(100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False
                robo.falling = False
                robo.sliding = False
                robo.jumpin = False

        screen.blit(bg, (0,0))
        FONT= pygame.font.SysFont('comicsans', 80)
        lastScore = FONT.render('Best Score: ' + str(updateFile()),1,(255,255,255))
        currentScore = FONT.render('Score: '+ str(score),1,(255,255,255))
        screen.blit(lastScore, (w/2 - lastScore.get_width()/2,150))
        screen.blit(currentScore, (w/2 - currentScore.get_width()/2, 240))
        pygame.display.update()
    score = 0









def redrawScreen():
    FONT= pygame.font.SysFont('comicsans', 30)
    screen.blit(bg,(bgx,0))
    screen.blit(bg,(bgx2,0))
    text = FONT.render('Score: ' + str(score), 1, (255,255,255))
    robo.draw(screen)
    for obs in obss:
        obs.draw(screen)
            

    screen.blit(text, (400, 10))
    
    pygame.display.update()


run=True
obss=[]
pygame.time.set_timer(USEREVENT+1, 500)
pygame.time.set_timer(USEREVENT+2,random.randrange(3000,5000))
robo = player(32,186 ,64, 64)
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
    for obs in obss: 
        obs.x -= 1.4
        if obs.collison(robo.hit):
            robo.falling=True



            if pause == 0:
                pause = 1
                fallSpeed = speed
            
        if obs.x < obs.width * -1:
            obss.pop(obss.index(obs))


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
            if not(robo.jumping):
                robo.jumping=True
        if keys[pygame.K_DOWN]:
            if not(robo.sliding):
                robo.sliding=True
        if event.type == USEREVENT+1:
            speed += 1
        if event.type == USEREVENT+2:
            r=random.randrange(0,2)
            if r == 0:
                obss.append(saw(450, 186, 64, 64))
            elif r==1:
                obss.append(spike(450,-122,64,310))
    redrawScreen()
    clock.tick(speed)
