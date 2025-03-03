from .behaviour import *
from random import random, randint
from math import floor

AIR_FRICTION = 0.9
EDGE_FRICTION = 0.8

class Move(Behaviour):
    def __init__(self,xv=0,yv=0,xa=0,ya=-1,mxv=60,myv=60,passable={EMPTY},replacable={},settle_depth=-1,disperse=-1,max_boost=5,div_y=10):
        super().__init__(B_MOVE)
        self.xv = xv
        self.yv = yv
        self.xa = xa
        self.ya = ya
        self.mxv = mxv
        self.myv = myv
        self.passable = passable
        self.replaceable = replacable
    
        self.settle_depth = settle_depth
        self.disperse = disperse
        self.max_boost = max_boost
        self.div_y = div_y
        self.sx = 0
        self.sy = 0

        self.active = True

    def settle(self,x,y,scene):
        if self.settle_depth == -1: 
            return 0
        
        movedir = 1 if self.yv >= 0 else -1
        settle = self.settle_depth * movedir

        fallwithin = 0 <= y + movedir < scene.h
        if fallwithin:
            state = scene.grid[y+movedir][x].state

            if state in self.replaceable:
                scene.replace(x,y,x,y+movedir)
                self.sx = x
                self.sy = y+movedir
                return 1
            
            if state in self.passable:
                scene.swap(x,y,x,y+movedir)
                self.sx = x
                self.sy = y+movedir
                return 1
            
        if y + settle < 0 or y + settle >= scene.h: 
            return 0
        
        if x:
            leftstate = scene.grid[y+settle][x-1].state
            left = 2 if leftstate in self.replaceable else 1 if leftstate in self.passable else 0
        else:
            left = 0

        if x != scene.w-1:
            rightstate = scene.grid[y+settle][x+1].state
            right = 2 if rightstate in self.replaceable else 1 if rightstate in self.passable else 0
        else:
            right = 0

        if left:
            if right: 
                if randint(0,1):
                    flag = left
                    direction = -1
                else:
                    flag = right
                    direction = 1
            else:
                flag = left
                direction = -1
        else:
            if right: 
                flag = right
                direction = 1
            else: 
                return 0

        if self.disperse != -1: 
            self.xv = (self.disperse + min(self.max_boost,abs(self.yv)/self.div_y)) * direction

        scene.swap(x,y,x+direction,y+settle) if flag == 1 else scene.replace(x,y,x+direction,y+settle)
        self.sx = x+direction
        self.sy = y+settle

        return 1

    def update(self,x,y,scene):
        self.xv += self.xa
        self.yv += self.ya

        self.xv *= AIR_FRICTION

        if self.active:
            scene.flag(x,y)

        signx = 1 if self.xv >= 0 else -1
        signy = 1 if self.yv >= 0 else -1
        absx = self.xv if self.xv >= 0 else -self.xv
        absy = self.yv if self.yv >= 0 else -self.yv

        if absx > self.mxv:
            self.xv = self.mxv * signx
            absx = self.mxv

        if absy > self.myv:
            self.yv = self.myv * signy
            absy = self.myv

        scene.grid[y][x].update_direction = signy

        cx = px = x
        cy = py = y

        if self.xv == 0 and self.yv == 0: 
            return 0

        if absx >= absy:
            speed = absx
            dx = signx
            dy = self.yv / speed
        else:
            speed = absy
            dx = self.xv / speed
            dy = signy

        floored = floor(speed)
        decimal = speed - floored
        steps = floored + (random() <= decimal)

        for _ in range(steps):
            cx += dx
            cy += dy

            nx = round(cx)
            ny = round(cy)

            withinx = 0 <= nx < scene.w
            withiny = 0 <= ny < scene.h

            if px == nx and py == ny: continue

            if withinx and withiny:
                nex = scene.grid[ny][nx]
                state = nex.state 

                if state in self.replaceable:
                    scene.replace(px,py,nx,ny)
                    px = nx
                    py = ny
                    continue

                if state in self.passable:
                    scene.swap(px,py,nx,ny,strictflag=True)
                    px = nx
                    py = ny
                    continue

                self.xv *= nex.friction / AIR_FRICTION
            else:
                self.xv *= EDGE_FRICTION / AIR_FRICTION

            if withinx and px != nx:
                statex = scene.grid[py][nx].state
                slidex = 2 if statex in self.replaceable else 1 if statex in self.passable else 0
            else:
                slidex = 0

            if withiny and py != ny:
                statey = scene.grid[ny][px].state
                slidey = 2 if statey in self.replaceable else 1 if statey in self.passable else 0
            else:
                slidey = 0

            if slidex:
                if slidey:
                    if randint(0,1):
                        self.xv = 0
                        dx = 0
                        scene.swap(px,py,px,ny,strictflag=True) if slidey == 1 else scene.replace(px,py,px,ny)
                        py = ny
                    else:
                        self.yv = 0
                        dy = 0
                        scene.swap(px,py,nx,py,strictflag=True) if slidex == 1 else scene.replace(px,py,nx,py)
                        px = nx
                else:
                    self.yv = 0
                    dy = 0
                    scene.swap(px,py,nx,py,strictflag=True) if slidex == 1 else scene.replace(px,py,nx,py)
                    px = nx
            else:
                if slidey:
                    self.xv = 0
                    dx = 0
                    scene.swap(px,py,px,ny,strictflag=True) if slidey == 1 else scene.replace(px,py,px,ny)
                    py = ny
                else:
                    if self.settle(px,py,scene):
                        cx = px = self.sx
                        cy = py = self.sy 
                        continue

                    self.xv = 0
                    self.yv = 0
                    self.active = False
                    break

        if x != px or y != py:
            scene.flag(x,y)
            scene.flag(px,py)
            self.active = True
            return 1
        
        return 0