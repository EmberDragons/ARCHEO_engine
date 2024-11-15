import glm
import pygame as pg

FOV = 50
NEAR = 0.1
FAR = 100
SPEED = 0.01
SENSITIVITY = 0.1

class Camera():
    def __init__(self, app, position = (0,0,-4), yaw=90, pitch=0):
        self.app = app
        self.aspect_ratio = app.WIN_SIZE[0]/app.WIN_SIZE[1]
        self.position = position
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

    def reload_matrices(self):
        #view matrix
        self.m_view = self.get_view_matrix()

    def get_projection_matrix(self):
        return glm.perspective(glm.radians(FOV), self.aspect_ratio, NEAR, FAR)
    
    def get_view_matrix(self):
        return glm.lookAt(self.position,self.position+self.forward,self.up)