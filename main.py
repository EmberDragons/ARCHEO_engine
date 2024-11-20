#imports
import pygame as pg
import moderngl as mgl
import sys, os
import ctypes

from model import *
from camera import *
from lights import *
from mesh import Mesh


#classes
class GraphicEngine:
    def __init__(self, win_size=(1000,1000)):
        #init pygame modules
        pg.init()
        #window size manager
        self.WIN_SIZE = win_size
        #opengl attribute with pygame
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)
        #opengl context creation
        pg.display.set_mode(self.WIN_SIZE, flags=pg.OPENGL | pg.DOUBLEBUF)
        #mouse settings and lock
        pg.event.set_grab(True)
        pg.mouse.set_visible(False)
        #detect current opengl for usage
        self.ctx = mgl.create_context()
        self.ctx.enable(flags=mgl.DEPTH_TEST | mgl.CULL_FACE)
        #camera
        self.camera = Camera(self)
        #create an object to help track time
        self.clock = pg.time.Clock()
        self.time = 0
        self.delta_time = 0

        #mesh, vbo and vao set up
        self.mesh = Mesh(self)

        #scene and lights
        self.lights = []
        self.light_set_up()
        self.scene = []
        self.scene_set_up()

    def scene_set_up(self):
        self.scene.append(Cube(self, (-6,0,0), tex_id=1))
        self.scene.append(Cube(self, (6,0,0), tex_id=0))
        self.scene.append(Pyramid(self, (0,0,0), tex_id=0))

    def light_set_up(self):
        self.lights.append(Light((4.5,-2,0),(10,190,110),0.7))
        self.lights.append(Light((20,10,10),(110,120,80),10))

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                self.mesh.destroy()
                pg.quit()
                sys.exit()
    
    def render(self):
        #busy with rendering everything on screen
        #clear framebuffer
        self.ctx.clear(color=(0.12,0.11,0.1)) #background color
        #render scene
        for obj in self.scene:
            obj.render()
        #swap buffers
        pg.display.flip()
    
    def get_time(self):
        self.time = pg.time.get_ticks()*0.001

    def run(self):
        #runs every frame and control the whole thinggy : => manager
        while True:
            #update the camera matrices and code
            self.camera.update()

            self.get_time()
            self.check_events()
            self.render()
            self.delta_time = self.clock.tick(120)

if __name__ == "__main__":
    #window size
    user32 = ctypes.windll.user32
    screensize = (user32.GetSystemMetrics(0), user32.GetSystemMetrics(1))

    #run game
    game = GraphicEngine(screensize)
    game.run()