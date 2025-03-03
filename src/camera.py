class Camera:
    def __init__(self,x=0,y=0,z=5,hwidth=1280//2,hheight=650//2):
        self.x = x
        self.y = y
        self.z = z

        self.xv = 0
        self.yv = 0
        self.zv = 0

        self.pan_speed = 50
        self.pan_friction = 0.95
        self.zoom_speed = 1
        self.zoom_friction = 0.95

        self.min_zoom = 3
        self.max_zoom = 50

        self.offx = hwidth
        self.offy = hheight

    def update(self,mx,my,px,py,x,y,shift,scroll,dt):
        speed = self.pan_speed / self.z * (1 + shift)
        self.xv += x * speed
        self.yv += y * speed

        if scroll:
            self.offx = mx
            self.offy = my
            self.x = px
            self.y = py
            self.zv += scroll * self.zoom_speed * self.z

        self.xv *= self.pan_friction
        self.yv *= self.pan_friction
        self.zv *= self.zoom_friction

        self.x += self.xv * dt
        self.y += self.yv * dt
        self.z += self.zv * dt
        
        if self.z < self.min_zoom:
            self.zv = 0
            self.z = self.min_zoom
        elif self.z > self.max_zoom:
            self.zv = 0
            self.z = self.max_zoom

    def to_camera_space(self,x,y):
        return (x - self.x) * self.z + self.offx, (y - self.y) * self.z + self.offy

    def to_world_space(self,x,y):
        return (x - self.offx) / self.z + self.x, (y - self.offy) / self.z + self.y
