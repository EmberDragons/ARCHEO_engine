#imports
import pygame as pg
import moderngl as mgl
import ctypes
import copy

from model import *
from camera import *
from lights import *
from mesh import Mesh


#classes
class GraphicEngine:
    def __init__(self, win_size=(1000,1000)):
        #init pygame modules and set up
        pg.init()
        self.font = pg.font.SysFont('merriweather', 100)
        #window size manager
        self.WIN_SIZE = win_size
        #opengl attribute with pygame
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)
        #opengl context creation
        
        self.display_surface = pg.display.set_mode(self.WIN_SIZE, flags=pg.OPENGL | pg.DOUBLEBUF)
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
        self.mesh = Mesh(self) #contains the textures

        #scene and lights
        self.lights = []
        self.light_set_up()
        self.scene = []
        self.scene_set_up()
        self.ui = []
        self.ui_set_up()
        self.letter = []
        self.letter_set_up()

    def scene_set_up(self):
        self.scene.append(Object(self, (0,0,10), (-90,0,0), scale=(2,1,2), vao_name = "20430_Cat_v1_NEW", tex_id="model/20430_cat_diff_v1.jpg"))
        self.scene.append(Cube(self, (-6,0,0), (90,90,0), (2,2,2), tex_id=1))
        self.scene.append(Cube(self, (6,0,0), tex_id=0))
    
    def add_cube(self):
        pos = copy.deepcopy(self.camera.position)
        self.scene.append(Cube(self, pos, tex_id=0))

    def ui_set_up(self):
        #color palette for uis: 
        # blue 0.12,0.2,0.3
        # green deep 29, 120, 116
        # dark 4, 21, 31
        # white 242, 247, 242
        # gray 112, 102, 119
        self.ui.append(UI(self, pos=(0,0,0), scale=(0.003,0.003,0.003), col=(1,1,1))) #crosshair
        self.ui.append(UI(self, pos=(2.73,0,0), scale=(0.28,1.0,1.0), col=(4/255, 21/255, 31/255))) #background1 right window
        self.ui.append(UI(self, pos=(2.97,0,0), scale=(0.25,1.0,1.0), col=(112/255, 102/255, 119/255))) #background2 right window
        self.ui.append(UI(self, pos=(2.97,1.5,0), scale=(0.25,0.38,1.0), col=(0.12,0.2,0.3))) #background right window params
        self.ui.append(UI(self, pos=(2.97,23.2,0), scale=(0.25,0.04,1.0), col=(29/255, 120/255, 116/255))) #background right window name
        self.ui.append(UI(self, pos=(3.32, 2.83,0), scale=(0.22,0.21,1.0), col=(0.1,0.13,0.2))) #background right under params
        self.ui.append(UI(self, pos=(0,20,0), scale=(1.0,0.05,1.0), col=(4/255, 21/255, 31/255))) #background high

    def letter_set_up(self):
        self.letter.append(Letter(self, pos=(5.4,41.7,0), bg_col=(29/255, 120/255, 116/255), scale=(0.120,0.022,0), tex_id="NAME:                      ", number=0))
        self.letter.append(Letter(self, pos=(4.7,35,0), bg_col=(0.1,0.13,0.2), scale=(0.150,0.022,0), tex_id="POSITION:                      ", number=1)) 
        self.letter.append(Letter(self, pos=(4.7,31,0), bg_col=(0.1,0.13,0.2), scale=(0.150,0.022,0), tex_id="ROTATION:                      ", number=2)) 
        self.letter.append(Letter(self, pos=(4.7,27,0), bg_col=(0.1,0.13,0.2), scale=(0.150,0.022,0), tex_id="SCALE:                             ", number=3)) 
        self.letter.append(Letter(self, pos=(4.7,23,0), bg_col=(0.1,0.13,0.2), scale=(0.150,0.022,0), tex_id="TEXTURE:                         ", number=4)) 

    def light_set_up(self):
        self.lights.append(Light((4.5,-2,0),(10,190,110),0.7))
        self.lights.append(Light((20,10,10),(110,120,80),10))

    def add_light(self):
        pos = copy.deepcopy(self.camera.position)
        self.lights.append(Light(pos,(110,120,80),0.5))

    
    def render(self):
        #busy with rendering everything on screen
        #clear framebuffer
        self.ctx.clear(color=(0.12,0.11,0.1)) #background color

        #render letter first
        for id in range(len(self.letter)-1,-1,-1): #we must render them from last to first
            self.letter[id].render()
        
        #render ui then
        for id in range(len(self.ui)-1,-1,-1): #we must render them from last to first
            self.ui[id].render()
        #render scene
        for obj in self.scene:
            obj.render()

        #text rendering
        
        
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
            self.render()
            self.delta_time = self.clock.tick(120)


if __name__ == "__main__":
    #window size
    user32 = ctypes.windll.user32
    screensize = (user32.GetSystemMetrics(0), user32.GetSystemMetrics(1))

    #run game
    game = GraphicEngine(screensize)
    game.run()
