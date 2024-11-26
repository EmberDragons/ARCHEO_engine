import glm
import pygame as pg
import math

FOV = 50
NEAR = 0.1
FAR = 100
SPEED = 0.01
SENSITIVITY = 0.1

class Camera():
    def __init__(self, app, position = (0,0,0), yaw=90, pitch=0):
        self.app = app
        self.aspect_ratio = app.WIN_SIZE[0]/app.WIN_SIZE[1]
        self.position = glm.vec3(position)
        self.up = glm.vec3(0,1,0)
        self.right = glm.vec3(1,0,0)
        self.forward = glm.vec3(0,0,-1)
        #view matrix
        self.m_view = self.get_view_matrix()
        #projection matrix
        self.m_proj = self.get_projection_matrix()

        # movement
        self.yaw = yaw
        self.pitch = pitch
    
    def rotate(self):
        rel_x, rel_y=pg.mouse.get_rel()
        self.yaw+=rel_x*SENSITIVITY
        self.pitch-=rel_y*SENSITIVITY
        self.pitch = max(-89,min(89,self.pitch))

    def update_camera_vectors(self):
        yaw, pitch = glm.radians(self.yaw), glm.radians(self.pitch)

        self.forward.x = glm.cos(yaw) * glm.cos(pitch)
        self.forward.y = glm.sin(pitch)
        self.forward.z = glm.sin(yaw) * glm.cos(pitch)

        self.forward = glm.normalize(self.forward)
        self.right = glm.normalize(glm.cross(self.forward, glm.vec3(0,1,0)))
        self.up = glm.normalize(glm.cross(self.right, self.forward))

    def update(self):
        self.move()
        self.rotate()
        self.update_camera_vectors()
        self.reload_matrices()
    
    def move(self):
        velocity = SPEED*self.app.delta_time
        keys = pg.key.get_pressed()
        if keys[pg.K_z]:
            self.position += velocity*self.forward
        if keys[pg.K_s]:
            self.position -= velocity*self.forward
        if keys[pg.K_d]:
            self.position += velocity*self.right
        if keys[pg.K_q]:
            self.position -= velocity*self.right
        if keys[pg.K_SPACE]:
            self.position += velocity*self.up
        if keys[pg.K_LCTRL]:
            self.position -= velocity*self.up
        if keys[pg.K_a]:
            hit_obj = self.ray_dist(self.position)
            print(hit_obj)

    
    def ray_dist(self, point):
        #we need to use the raymarching approach to find the object we are looking at
        # we know the safe dist is three :  _ _ _ we check new safe dist : _ if too small, we hit an object
        min_return = 0.2
        max_return = 100

        smallest_dist = 100
        new_point = point #the new point
        for obj in self.app.scene:
            dist = self.sdBox(obj.position, obj.scale, point)
            if dist <= min_return:
                #hit
                return obj
            if dist > max_return:
                #no hit we missed it =C
                return None
            if smallest_dist>dist:
                #we raymarch again
                smallest_dist=dist
        new_point = point+self.forward*smallest_dist
        return self.ray_dist(new_point)
    
    def sdBox(self, center, scale, point):
        dist_x = abs(point.x-center.x)
        dist_y = abs(point.y-center.y)
        dist_z = abs(point.z-center.z)
        return (math.sqrt((max(dist_x-scale.x,0))**2 + (max(dist_y-scale.y,0))**2 + (max(dist_z-scale.z,0))**2))
    

    def reload_matrices(self):
        #view matrix
        self.m_view = self.get_view_matrix()

    def get_projection_matrix(self):
        return glm.perspective(glm.radians(FOV), self.aspect_ratio, NEAR, FAR)
    
    def get_view_matrix(self):
        return glm.lookAt(self.position,self.position+self.forward,self.up)