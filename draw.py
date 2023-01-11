#!/bin/python3

# a python program for Kristine Joy by Peti

import pygame
import time
import math


def decimal_range_plus_one(start, stop, increment): # used in for loops
    while start < stop and not math.isclose(start, stop):
        yield start
        start += increment
    yield start


def func3D(functionID,u,v): # 3d functions   f(u,v) -> (x,y,z)
    if functionID==0: # this is the green function
        height=-v*7
        r=max(0.14,0.21-v)
        shiftx = v*v*2
        shifty = v*(1.0-v)*0
        return (math.sin(u*math.pi*2)*r+shiftx,math.cos(u*math.pi*2)*r+shifty,height)

    else: # red functions
        u-=0.501 # shift range to (-0.5,0.5)
        v-=0.501

        if v>0: # distort square into disk shape, but only the top half
            d=1/math.sqrt(u*u+v*v) # normalize the 2D vector
            u2=u*d
            v2=v*d
            factor=max(abs(u2),abs(v2)) 
            u*=factor
            v*=factor

        v+=0.501
        opening=functionID/8*0.7*phase+0.1+phase*0.2
        r=0.2+(v*(1.5+functionID/8*0.4)*math.sin(math.pi*v*(1-opening*0.65)))
        u=u*0.3+functionID/3.7

        f1 = opening*0.7+0.3
        height = math.sin(v*math.pi*0.9*f1)/f1*2.

    return (math.sin(u*math.pi*2)*r,math.cos(u*math.pi*2)*r,height)

def generateScene():
    global timeSeconds 
    timeSeconds = (time.clock_gettime_ns(0)-timeStart)/1000000000
    subdiv = 26
    functionID=0
    global tri
    tri=[]
    global phase
    phase=min((timeSeconds/6.)%2,1)  # transforming  during 6 seconds, then staying like that for another 6 seconds then start over

    for functionID in range(0,8):

        grid=[] # plot the function in 3D
        grid.clear()
        for cv in decimal_range_plus_one(0,1,1./(subdiv-1)):
            onerow=[]
            onerow.clear()
            for cu in decimal_range_plus_one(0,1,1/(subdiv-1)):
                onerow.append(func3D(functionID,cu,cv))
            grid.append(onerow)

        # putting triangles on the grid points
        # triangles are made of color tuple (red,green,blue) and a tuple of 3 vertices with 3 coordinates each
        for iv in range(0,subdiv-1):
            cv=iv/subdiv
            cu=0
            cud=1/subdiv
            for iu in range(0,subdiv-1):

                if functionID==0:
                    color=(30,120-cu*(1.0-cu)*200,10) # green with some variations
                else:
                    brightness = 0.4+cv*cv*0.6 # make it darker in the bottom, where light doesn't get
                    if iv==subdiv-2 or iu==0 or iu==subdiv-2:
                        brightness *= 0.5 # mark edge darker
                    color=(230*brightness,60*brightness,20*brightness) # red color with brightness adjusted

                #two triangles make one square. Comment out one of the triangles to see the missing triangles
                tri.append((color,(grid[iv][iu],grid[iv+1][iu],grid[iv][iu+1]))) 
                tri.append((color,(grid[iv+1][iu],grid[iv+1][iu+1],grid[iv][iu+1])))  

                cu+=cud


def rotate(x,y,sina,cosa):
    return x*cosa-y*sina,y*cosa+x*sina

def renderFrame(): # putting the triangles on the screen

    viewangle = 0.6+math.sin(timeSeconds*0.2)*0.4

    viewdistance = 10 # slowly moving point of view
    viewPoint=(0.6,math.cos(viewangle)*viewdistance,math.sin(viewangle)*viewdistance+2.)

    def zsortFunc(t):
        i=0 #sorting by first vertex
        x=t[1][i][0]-viewPoint[0]
        z=t[1][i][1]-viewPoint[1]
        y=t[1][i][2]-viewPoint[2]
        return x*x+y*y+z*z;

    tri.sort(key=zsortFunc,reverse=True) # draw triangles far to close, so they cover up. zsortFunc returns the square of the distance to viewPoint
    tri2d=[]
    sina=math.sin(viewangle)
    cosa=math.cos(viewangle)
    for t in tri:
        projectedPoints=[]
        for i in range(0,3): 
            x=t[1][i][0]-viewPoint[0] # offset vertex locations by the viewPoint
            z=t[1][i][1]-viewPoint[1]
            y=t[1][i][2]-viewPoint[2]

            y,z=rotate(y,z,sina,cosa)  # rotating around axis x so that you get a top down view angle

            sx=x/z*screenSizex+screenSizex/2; # perspective projection of the vertex of a triangle into screen space
            sy=y/z*screenSizex+screenSizey/2;

            projectedPoints.append((sx,sy));

        tri2d.append((t[0],projectedPoints))

    skycolor = (130,170,255)
    screen.fill(skycolor)
    for t in tri2d:
        pygame.draw.polygon(screen,t[0],t[1])
    pygame.display.flip() # drawing polygons on the invisible surface, which is now flipped to the screen when it's done


#start here!
pygame.init() # getting a graphical screen
global screenSizex,screenSizey,screen,timeStart
screenSizex,screenSizey = (pygame.display.Info().current_w, pygame.display.Info().current_h)
screen = pygame.display.set_mode((screenSizex,screenSizey))
timeStart = time.clock_gettime_ns(0)


while True: # the main loop runs until you close the window
    generateScene()
    renderFrame()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            pygame.quit()
            exit()

