"""
TODO: 
- optimize
- perhaps change settling to velocity updates ==> faster dispersion for water, no teleporting, etc.
- add inertia????
"""

import pygame
import pygame.gfxdraw
from math import floor,ceil
import sys
from src.scene import Scene
from src.camera import Camera

pygame.font.init()
font = pygame.font.SysFont("Verdana",30)

def clamp(x,l,r):
    if x < l: return l
    if x > r: return r
    return x

class Display:
    def __init__(self,width=1280,height=650,bg=(0,0,0),border=(0,30,87),fps=120):
        self.width = width
        self.height = height
        self.hwidth = width//2
        self.hheight = height//2
        self.bg = bg
        self.border = border
        self.fps = fps
        
        self.screen = pygame.display.set_mode((width,height))
        self.clock = pygame.time.Clock()

        self.scene = Scene(256,256)
        self.camera = Camera(x=0, y=self.scene.h/2-30, z=5, hwidth=self.hwidth, hheight=self.hheight)

        self.lastinteraction = -9999
        #self.repeatrate = self.scene.brush_size // 5 + 1
        self.repeatrate = 1

        self.surface = pygame.surface.Surface((self.scene.w+2,self.scene.h+2))
        self.surface.fill((255,255,255))
        self.surface.fill(self.scene.grid[0][0].colour,(1,1,self.scene.w,self.scene.h))

        self.debug = False

    def update(self):
        self.screen.fill(self.bg)
        dt = self.clock.tick_busy_loop(self.fps) / 1000

        scroll = 0
        arrow_x = 0
        step = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEWHEEL:
                scroll = event.precise_y
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_BACKQUOTE:
                    self.scene.debug_next()
                    self.debug = self.scene.debug > 0
                elif event.key == pygame.K_SPACE:
                    self.scene.paused = not self.scene.paused
                elif event.key == pygame.K_LEFT:
                    arrow_x -= 1
                elif event.key == pygame.K_RIGHT:
                    arrow_x += 1
                elif event.key == pygame.K_RETURN:
                    self.scene.paused = False
                    self.scene.debug_list = []
                    step = True

        keys = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pressed()
        click = mouse[0]
        mx,my = pygame.mouse.get_pos()
        px,py = self.camera.to_world_space(mx,my)
        key_x = keys[pygame.K_d] - keys[pygame.K_a]
        key_y = keys[pygame.K_s] - keys[pygame.K_w]
        arrow_y = keys[pygame.K_UP] - keys[pygame.K_DOWN]
        shift = keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]

        self.camera.update(mx,my,px,py,key_x,key_y,shift,scroll,dt)

        interact = False
        if click:
            #self.repeatrate = self.scene.brush_size // 5 + 1
            if self.scene.paused or self.scene.frame > self.lastinteraction + self.repeatrate:
                self.lastinteraction = self.scene.frame
                interact = True
        else:
            self.lastinteraction = -69420
        
        self.scene.interact(interact,shift,arrow_x,arrow_y,px,py)
        self.scene.update()

        if step:
            self.scene.paused = True

        for x,y,colour in self.scene.draw():
            self.surface.set_at((x+1,y+1),colour)

        l,t = self.camera.to_world_space(0,0)
        l = clamp(floor(l + self.scene.offx),0,self.scene.w+1)
        t = clamp(floor(t + self.scene.offy),0,self.scene.h+1)

        r,b = self.camera.to_world_space(self.width-1,self.height-1)
        r = clamp(ceil(r + self.scene.offx),0,self.scene.w+1)
        b = clamp(ceil(b + self.scene.offy),0,self.scene.h+1)

        pos = self.camera.to_camera_space(l - self.scene.offx - 1, t - self.scene.offy - 1)
        rendered = pygame.transform.scale_by(self.surface.subsurface((l,t,r-l+1,b-t+1)),self.camera.z)
        self.screen.blit(rendered, pos)
        pygame.gfxdraw.aacircle(self.screen,mx,my,int(self.scene.brush_size * self.camera.z / 2), (0,255,0) if shift else (255,0,0))

        if self.debug:
            for l,r,t,b in self.scene.get_debug():
                pygame.draw.rect(self.screen,(255,0,0) if self.scene.debug == 1 else (0,255,0),(self.camera.to_camera_space(l - self.scene.offx, t-self.scene.offy),((r-l+1)*self.camera.z,(b-t+1)*self.camera.z)),width=max(1,round(self.camera.z/5)))

        fps = round(1/dt)
        text = font.render(str(fps),1,(255,255,255))
        self.screen.blit(text,(0,0))

        pygame.display.flip()
        
display = Display()

while 1:
    display.update()