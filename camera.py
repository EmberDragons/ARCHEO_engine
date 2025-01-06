import glm
import pygame as pg
import sys, os
import math

FOV = 70
NEAR = 0.1
FAR = 100
SPEED = 0.01
SENSITIVITY = 0.2

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

        self.lock = False
        self.selected_obj = None

        self.update_camera_vectors()

    def set_mouse_locked(self):
        #mouse settings and lock
        pg.event.set_grab(True)
        pg.mouse.set_visible(False)

    def set_mouse_unlocked(self):
        #mouse settings and lock
        pg.event.set_grab(False)
        pg.mouse.set_visible(True)

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
        self.check_keys()
        if self.lock:
            self.set_mouse_locked()
            self.rotate()
            self.update_camera_vectors()
        else:
            self.set_mouse_unlocked()
        self.reload_matrices()
    
    def check_keys(self):
        #movement
        velocity = SPEED*self.app.delta_time
        keys = pg.key.get_pressed()
        movement = 0
        if keys[pg.K_z]:
            movement += velocity*self.forward
        if keys[pg.K_s]:
            movement -= velocity*self.forward
        if keys[pg.K_d]:
            movement += velocity*self.right
        if keys[pg.K_q]:
            movement -= velocity*self.right
        if keys[pg.K_SPACE]:
            movement += velocity*self.up
        if keys[pg.K_LCTRL]:
            movement -= velocity*self.up

        self.position+=movement

        #props instantiation
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                self.app.mesh.destroy()
                self.app.scene_renderer.destroy()
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN and event.key == pg.K_1:
                vector = self.vector_world(pg.mouse.get_pos(), self.m_view, self.m_proj, self.app.WIN_SIZE[0], self.app.WIN_SIZE[1])
                new_pos = self.position+vector*3
                self.app.add_cube(new_pos)
            if event.type == pg.KEYDOWN and event.key == pg.K_2:
                vector = self.vector_world(pg.mouse.get_pos(), self.m_view, self.m_proj, self.app.WIN_SIZE[0], self.app.WIN_SIZE[1])
                new_pos = self.position+vector*3
                self.app.add_light(new_pos)

        #screen movementa nd locking
        if pg.mouse.get_pressed()[2]:
            if self.lock == False:
                rel_x, rel_y=pg.mouse.get_rel() #なんで！！！ああああ wtf AHHHHHHH ps (me of the next day after lots of reste and break) : soooo, this only works thanks to thius line of code because it allows us to ignore the first frame when the mouse is moved (if it wasn't at the center of the screen ) so you welcome, have a nice day
            self.lock = True
        else:
            self.lock = False

        #click on objects or uis
        if pg.mouse.get_pressed()[0]:
            #uis
            mouse_pos = (((pg.mouse.get_pos()[0]/self.app.WIN_SIZE[0])-0.5)*51*2, ((pg.mouse.get_pos()[1]/self.app.WIN_SIZE[1])-0.5)*-38.1*2) #this is arbitrairy value, i miss sleep to much to think why (just don't mess with it plz)
            button_used = False
            #the type_params is for when we select a light or an object (to not render all textes at once)
            for id in range(len(self.app.button)-1,-1,-1): #we must render them from last to first
                if self.app.type_params==0 and id <10 or self.app.type_params==0 and id >=12:
                    size_x = abs(self.app.button[id][0][0]*self.app.button[id][1][0])
                    size_y = abs(self.app.button[id][0][1]*self.app.button[id][1][1])
                    if mouse_pos[0]>self.app.button[id][0][0] and mouse_pos[0]<self.app.button[id][0][0]+size_x: #in x right
                        if mouse_pos[1]>self.app.button[id][0][1] and mouse_pos[1]<self.app.button[id][0][1]+size_y: #in y right
                            self.app.openNewInputWindow(f"{self.app.button[id][2]}")
                            button_used = True
                if self.app.type_params==1 and id <6 or self.app.type_params==1 and id >=10:
                    size_x = abs(self.app.button[id][0][0]*self.app.button[id][1][0])
                    size_y = abs(self.app.button[id][0][1]*self.app.button[id][1][1])
                    if mouse_pos[0]>self.app.button[id][0][0] and mouse_pos[0]<self.app.button[id][0][0]+size_x: #in x right
                        if mouse_pos[1]>self.app.button[id][0][1] and mouse_pos[1]<self.app.button[id][0][1]+size_y: #in y right
                            self.app.openNewInputWindow(f"{self.app.button[id][2]}")
                            button_used = True
            #objs
            if button_used == False:
                vector = self.vector_world(pg.mouse.get_pos(), self.m_view, self.m_proj, self.app.WIN_SIZE[0], self.app.WIN_SIZE[1])
                hit_obj = self.ray_dist(self.position, vector)
                self.selected_obj = hit_obj
                #change the params
                list_lights = []
                for light in self.app.lights:
                    list_lights.append(light.light_ui)
                if hit_obj in list_lights:
                    self.app.type_params = 1
                else:
                    self.app.type_params = 0
    
    def ray_dist(self, point, vector):
        #we need to use the raymarching approach to find the object we are looking at
        # we know the safe dist is three :  _ _ _ we check new safe dist : _ if too small, we hit an object (raymarching approch)
        min_return = 0.25
        max_return = 100

        smallest_dist = 100
        new_point = point #the new point

        #new list joining scene and lights
        list_objs = self.app.scene.copy()
        for light in self.app.lights:
            list_objs.append(light.light_ui)
        for obj in list_objs:
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

        new_point = point+vector*smallest_dist
        return self.ray_dist(new_point, vector)

    def sdBox(self, center, scale, point):
        dist_x = abs(point.x-center.x)
        dist_y = abs(point.y-center.y)
        dist_z = abs(point.z-center.z)
        return (math.sqrt((max(dist_x-scale.x,0))**2 + (max(dist_y-scale.z,0))**2 + (max(dist_z-scale.y,0))**2)) #we are using 2 diff system so y is z
    

    def vector_world(self, mouse_pos, mat_view, mat_projection, SCR_WIDTH, SCR_HEIGHT):
        x = (2 * mouse_pos[0]) / SCR_WIDTH - 1
        y = 1 - (2 * mouse_pos[1]) / SCR_HEIGHT
        z = 1
        ray_nds = glm.vec3(x, y, z)
        ray_clip = glm.vec4(ray_nds.x, ray_nds.y, -1, 1)
        ray_eye = glm.inverse(mat_projection) * ray_clip
        ray_eye = glm.vec4(ray_eye.x, ray_eye.y, -1, 0)
        inv_ray_wor = (glm.inverse(mat_view) * ray_eye)
        ray_wor = glm.vec3(inv_ray_wor.x, inv_ray_wor.y, inv_ray_wor.z)
        ray_wor = glm.normalize(ray_wor)
        return ray_wor

    def reload_matrices(self):
        #view matrix
        self.m_view = self.get_view_matrix()

    def get_projection_matrix(self):
        return glm.perspective(glm.radians(FOV), self.aspect_ratio, NEAR, FAR)
    
    def get_view_matrix(self):
        return glm.lookAt(self.position,self.position+self.forward,self.up)