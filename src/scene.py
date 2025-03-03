from random import uniform, randint
from math import isqrt,pi,sin,cos,ceil,log2
from .particle import *

MAXDEPTH = 20
NEIGHBOURHOOD = 2

"""
Node children:
|---|---|
| 0 | 1 |
|---|---|
| 2 | 3 |
|---|---|
"""

class Node:
    def __init__(self,l,r,t,b,dep=0):
        self.l = l
        self.r = r
        self.t = t
        self.b = b
        self.dep = dep
        self.min_active = -1
        self.max_active = -1
        self.lazy = -1

    def build(self):        
        if self.l == self.r:
            self.c0 = self.c1 = self.c2 = self.c3 = None
            return self
        
        self.xm = (self.l + self.r) >> 1
        self.ym = (self.t + self.b) >> 1
        self.c0 = Node(self.l,self.xm,self.t,self.ym,self.dep+1).build()
        self.c1 = Node(self.xm+1,self.r,self.t,self.ym,self.dep+1).build()
        self.c2 = Node(self.l,self.xm,self.ym+1,self.b,self.dep+1).build()
        self.c3 = Node(self.xm+1,self.r,self.ym+1,self.b,self.dep+1).build()

        return self
    
    def check(self):
        if self.lazy == -1: return

        self.max_active = self.min_active = self.lazy

        if not self.c0 is None:
            self.c0.lazy = self.c1.lazy = self.c2.lazy = self.c3.lazy = self.lazy
            self.lazy = -1
    
    def update(self,scene,l,r,t,b,frame):
        self.check()

        if self.min_active >= frame: 
            return

        if l <= self.l and self.r <= r and t <= self.t and self.b <= b:
            self.lazy = frame
            self.check()

            if scene.debug == 2: scene.debug_list.append((self.l,self.r,self.t,self.b))

            return
        
        if self.l > r or self.r < l or self.t > b or self.b < t:
            return

        if self.xm >= l: 
            if self.ym >= t: self.c0.update(scene,l,r,t,b,frame)
            if self.ym < b: self.c2.update(scene,l,r,t,b,frame)

        if self.xm < r: 
            if self.ym >= t: self.c1.update(scene,l,r,t,b,frame)
            if self.ym < b: self.c3.update(scene,l,r,t,b,frame)
        
        self.min_active = min(self.c0.min_active,self.c1.min_active,self.c2.min_active,self.c3.min_active)
        self.max_active = max(self.c0.max_active,self.c1.max_active,self.c2.max_active,self.c3.max_active)

    def query(self,scene,direction):
        self.check()
        
        if self.max_active < scene.frame or self.l >= scene.w or self.t >= scene.h: 
            return False

        if self.min_active >= scene.frame and self.r < scene.w and self.b < scene.h:
            res = False
            for y in range(self.t,self.b+1) if direction == -1 else range(self.b,self.t-1,-1):
                for x in range(self.l,self.r+1) if randint(0,1) else range(self.r,self.l-1,-1):
                    res = scene.grid[y][x].update(scene,direction) | res

            if scene.debug == 1: scene.debug_list.append((self.l,self.r,self.t,self.b))

            return res
        
        if direction == -1:
            if randint(0,1): res = self.c0.query(scene,direction)|self.c1.query(scene,direction)
            else: res = self.c1.query(scene,direction)|self.c0.query(scene,direction)
            if randint(0,1): return self.c2.query(scene,direction)|self.c3.query(scene,direction)|res
            else: return self.c3.query(scene,direction)|self.c2.query(scene,direction)|res
        else:
            if randint(0,1): res = self.c2.query(scene,direction)|self.c3.query(scene,direction)
            else: res = self.c3.query(scene,direction)|self.c2.query(scene,direction)
            if randint(0,1): return self.c0.query(scene,direction)|self.c1.query(scene,direction)|res
            else: return self.c1.query(scene,direction)|self.c0.query(scene,direction)|res

class Scene:
    def __init__(self,w=128,h=128,debug=0):
        self.w = w
        self.h = h

        self.grid = [[Empty(x,y) for x in range(self.w)] for y in range(self.h)]
        self.updates = set()
        self.frame = 0

        self.s = 1 << ceil(log2(w if w > h else h))
        self.root = Node(0,self.s-1,0,self.s-1).build()

        self.brush = SAND
        self.brush_size = 5

        self.paused = False

        self.debug = debug
        self.debug_list = []

        self.offx = self.w / 2
        self.offy = self.h / 2

    def debug_next(self):
        self.debug += 1
        if self.debug == 3: self.debug = 0

    def flag(self,x,y):
        identifier = x * self.h + y
        if identifier not in self.updates:
            self.updates.add(identifier)
            self.root.update(self,x-1,x+1,y-1,y+1,self.frame+1)

    def set_at(self,x,y,state):
        self.grid[y][x] = ID_TO_CLASS[state](x,y)
        self.flag(x,y)

    def swap(self,x1,y1,x2,y2,strictflag=False):
        self.grid[y1][x1],self.grid[y2][x2] = self.grid[y2][x2],self.grid[y1][x1]
        a = self.grid[y1][x1]
        b = self.grid[y2][x2]
        a.x = x1
        a.y = y1
        b.x = x2
        b.y = y2

        if strictflag:
            if a.state != EMPTY: 
                self.flag(x1,y1)
                self.flag(x2,y2)
        else:
            self.flag(x1,y1)
            self.flag(x2,y2)

    def replace(self,x1,y1,x2,y2):
        self.grid[y1][x1],self.grid[y2][x2] = Empty(x1,y1),self.grid[y1][x1]
        b = self.grid[y2][x2]
        b.x = x2
        b.y = y2

        self.flag(x1,y1)
        self.flag(x2,y2)

    def within(self,x,y):
        return 0 <= x < self.w and 0 <= y < self.h

    def interact(self,click,shift,x,y,px,py):
        self.brush += x
        if self.brush == -1: self.brush = N_TYPES - 1
        elif self.brush == N_TYPES: self.brush = 0

        self.brush_size += y
        if self.brush_size == 0: self.brush_size = 1
        
        if not click: return
        
        wx = round(px + self.offx)
        wy = round(py + self.offy)

        flag = False

        extentx = self.brush_size//2
        for dx in range(-extentx,extentx+1):
            extenty = isqrt(extentx**2 - dx**2)
            identifierx = (wx + dx) * self.h
            for dy in range(-extenty,extenty+1):
                if not self.within(wx+dx,wy+dy): continue

                if shift:
                    b = self.grid[wy+dy][wx+dx].get_behaviour(B_MOVE)
                    if not b is None:
                        speed = uniform(5,10)
                        angle = uniform(0,2*pi)
                        b.xv += speed * cos(angle)
                        b.yv -= speed * sin(angle)
                        flag = True
                else:
                    state = self.grid[wy+dy][wx+dx].state
                    if self.brush in MOVABLE:
                        if randint(0,1) or state != EMPTY:
                            continue
                    elif state == self.brush:
                        continue

                    self.grid[wy+dy][wx+dx] = ID_TO_CLASS[self.brush](wx+dx,wy+dy)
                    flag = True

                identifier = identifierx + wy+dy
                self.updates.add(identifier)

        if flag: self.root.update(self,wx-extentx-1,wx+extentx+1,wy-extentx-1,wy+extentx+1,self.frame+1)

    def update(self):
        if self.paused: return

        if self.root.query(self,1)|self.root.query(self,-1):
            pass

        self.frame += 1

    def draw(self):        
        for identifier in self.updates:
            x = identifier // self.h
            y = identifier % self.h
            yield x,y,self.grid[y][x].colour

        self.updates = set()
    
    def get_debug(self):
        for l,r,t,b in self.debug_list:
            yield l,r,t,b

        if self.paused: return

        self.debug_list = []

