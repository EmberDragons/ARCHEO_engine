#imports
import pygame as pg
import tkinter as tk
import moderngl as mgl
import ctypes
import copy
import math
import os

from model import *
from camera import *
from lights import *
from scene_renderer import *
from mesh import Mesh
from tkinter import ttk, filedialog 
from tkinter.filedialog import askopenfile 


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
        self.fps = 0 

        #mesh, vbo and vao set up
        self.mesh = Mesh(self) #contains the textures



        #scene and lights
        self.lights = []
        self.light_set_up()

        #scene rendering program
        self.scene_renderer = SceneRenderer(self)

        self.scene = []
        self.scene_set_up()
        self.ui = []
        self.ui_set_up()
        self.letter = []
        self.letter_set_up()
        self.button = []
        self.button_set_up()


        #ui
        self.type_params = 0 #0 => obj nparams 1 => light params

    def scene_set_up(self):
        self.scene.append(Cube(self, (0,0,0), (0,0,0), (20,20,0.1), tex_id=1))
        self.scene.append(Cube(self, (-11,10,0), (0,0,0), (1,1,1),  tex_id=0))
    
    def add_cube(self, pos):
        self.scene.append(Cube(self, pos, tex_id=0))
        
    def ui_set_up(self):
        #color palette for uis: 
        # light self,green 132, 169, 140
        # middle green 82, 121, 111
        # dark blue 53, 79, 82
        # dark 47, 62, 70
        # white 242, 247, 242
        # gray 202, 210, 197
        # dark blue 20, 35, 43
        
        self.ui.append(UI(self, pos=(2.73,0,0), scale=(0.28,1.0,1.0), col=(53/255, 79/255, 82/255))) #background1 right window
        self.ui.append(UI(self, pos=(2.97,0,0), scale=(0.25,1.0,1.0), col=(47/255, 62/255, 70/255))) #background2 right window
        self.ui.append(UI(self, pos=(2.97,1.5,0), scale=(0.25,0.38,1.0), col=(82/255, 121/255, 111/255))) #background right window params
        self.ui.append(UI(self, pos=(2.97,23.2,0), scale=(0.25,0.04,1.0), col=(20/255, 35/255, 43/255))) #background right window name
        self.ui.append(UI(self, pos=(3.32, 2.83,0), scale=(0.22,0.21,1.0), col=(82/255,121/255,111/255))) #background right under params
        self.ui.append(UI(self, pos=(0,20,0), scale=(1.0,0.05,1.0), col=(47/255, 62/255, 70/255))) #background high

        #importations/params
        self.ui.append(UI(self, pos=(-17.13,42.3,0), scale=(0.055,0.023,0), tex_id=2)) #quit
        self.ui.append(UI(self, pos=(-14.75,42.3,0), scale=(0.055,0.023,0), tex_id=2)) #save
        self.ui.append(UI(self, pos=(-12.3,42.3,0), scale=(0.055,0.023,0), tex_id=2)) #texture imports
        self.ui.append(UI(self, pos=(-9.83,42.3,0), scale=(0.055,0.023,0), tex_id=2)) #model imports
        self.ui.append(UI(self, pos=(0,0,0), scale=(0.003,0.003,0.003), col=(1,1,1))) #crosshair

        self.ui.append(UI(self, pos=(45,34,0), scale=(0.02,0.027,0), tex_id=3)) #name modifier
        self.ui.append(UI(self, pos=(45,28.4,0), scale=(0.02,0.027,0), tex_id=3)) #pos modifier

        #1
        self.ui.append(UI(self, pos=(45,25.2,0), scale=(0.02,0.027,0), tex_id=3)) #rot modifier
        self.ui.append(UI(self, pos=(45,22,0), scale=(0.02,0.027,0), tex_id=3)) #scale modifier
        self.ui.append(UI(self, pos=(45,18.8,0), scale=(0.02,0.027,0), tex_id=3)) #tex modifier
        self.ui.append(UI(self, pos=(45,15.6,0), scale=(0.02,0.027,0), tex_id=3)) #tex modifier

        #2
        self.ui.append(UI(self, pos=(45,25.2,0), scale=(0.02,0.027,0), tex_id=3)) #col modifier
        self.ui.append(UI(self, pos=(45,22,0), scale=(0.02,0.027,0), tex_id=3)) #intensity modifier
        #self.ui.append(UI(self, pos=(1,1,0), scale=(0.5,0.5,0), tex_id="depth_texture")) #depth texture (debugging)
        

    def letter_set_up(self):
        #importations/params
        self.letter.append(Letter(self, pos=(-18.87,48.7,0), bg_col=(1,1,1), col=(0,0,0), scale=(0.05,0.02,0), tex_id="QUIT")) #quit
        self.letter.append(Letter(self, pos=(-16.2,48.7,0), bg_col=(1,1,1), col=(0,0,0), scale=(0.05,0.02,0), tex_id="SAVE")) #save
        self.letter.append(Letter(self, pos=(-13.5,48.7,0), bg_col=(1,1,1), col=(0,0,0), scale=(0.05,0.02,0), tex_id="MODEL")) #texture imports
        self.letter.append(Letter(self, pos=(-10.8,48.7,0), bg_col=(1,1,1), col=(0,0,0), scale=(0.05,0.02,0), tex_id="TEXT")) #model imports

        self.letter.append(Letter(self, pos=(4.7,41.7,0), bg_col=(20/255, 35/255, 43/255), scale=(0.150,0.022,0), tex_id="NAME:                    ", number=0))
        self.letter.append(Letter(self, pos=(4.7,35,0), bg_col=(47/255, 62/255, 70/255), scale=(0.150,0.022,0), tex_id="POSITION:                      ", number=1)) 

        #1
        self.letter.append(Letter(self, pos=(4.7,31,0), bg_col=(47/255, 62/255, 70/255), scale=(0.150,0.022,0), tex_id="ROTATION:                      ", number=2)) 
        self.letter.append(Letter(self, pos=(4.7,27,0), bg_col=(47/255, 62/255, 70/255), scale=(0.150,0.022,0), tex_id="SCALE:                             ", number=3)) 
        self.letter.append(Letter(self, pos=(4.7,23,0), bg_col=(47/255, 62/255, 70/255), scale=(0.150,0.022,0), tex_id="TEXTURE:                         ", number=4)) 
        self.letter.append(Letter(self, pos=(4.7,19,0), bg_col=(47/255, 62/255, 70/255), scale=(0.150,0.022,0), tex_id="V.A.O:                         ", number=5)) 

        #2
        self.letter.append(Letter(self, pos=(4.7,31,0), bg_col=(47/255, 62/255, 70/255), scale=(0.150,0.022,0), tex_id="COLOR:                        ", number=6)) 
        self.letter.append(Letter(self, pos=(4.7,27,0), bg_col=(47/255, 62/255, 70/255), scale=(0.150,0.022,0), tex_id="STRENGTH:                             ", number=7)) 
        self.letter.append(Letter(self, pos=(-5.6,-44,0), bg_col=(47/255, 62/255, 70/255), scale=(0.150,0.022,0), tex_id="FPS:                             ", number=8)) 


    def button_set_up(self):
        self.button.append(((-51,36,0),(0.110,0.07,0), "QUIT")) #quit
        self.button.append(((-44,36,0),(0.122,0.07,0), "SAVE")) #save
        self.button.append(((-37.3,36,0),(0.15,0.07,0), "MODEL")) #texture imports
        self.button.append(((-30.5,36,0),(0.19,0.07,0), "TEXTURE")) #model imports


        self.button.append(((45,34,0), (0.06,0.084,0), "name")) #button to change name => noice
        self.button.append(((45,28.4,0), (0.06,0.084,0), "position")) #button to change pos => noice

        #1
        self.button.append(((45,25.2,0), (0.06,0.084,0), "rotation")) #button to change rot => noice
        self.button.append(((45,22,0), (0.06,0.084,0), "scale")) #button to change scale => noice
        self.button.append(((45,18.8,0), (0.06,0.084,0), "texture")) #button to change tex => noice
        self.button.append(((45,15.6,0), (0.06,0.084,0), "vao")) #button to change vao => noice
        
        #2
        self.button.append(((45,25.2,0), (0.06,0.084,0), "color")) #button to change col => noice
        self.button.append(((45,22,0), (0.06,0.084,0), "intensity")) #button to change intensity => noice
        

    def light_set_up(self):
        #self.lights.append(Light(self, (10,40,2), (230,220,200), 12, name = "sun")) #main light
        self.lights.append(Light(self, (0,20,2), (230,220,200), 5, param = "point")) #main light
        
    def add_light(self, pos):
        if len(self.lights)<10:
            self.lights.append(Light(self,pos,(110,120,80),0.5, param = "point"))
        else:
            self.lights.pop(0)
            self.lights.append(Light(self,pos,(110,120,80),0.5, param = "point"))

    
    def render(self):
        #busy with rendering everything on screen
        #clear framebuffer
        self.ctx.clear(color=(0.12,0.11,0.1)) #background color

        #render letters/text first
        for id in range(len(self.letter)-1,-1,-1): #we must render them from last to first
            if self.type_params==0 and id <10 or self.type_params==0 and id >=12:
                self.letter[id].render()
            if self.type_params==1 and id <6 or self.type_params==1 and id >=10:
                self.letter[id].render()
        
        #render ui then
        for id in range(len(self.ui)-1,-1,-1): #we must render them from last to first
            if self.type_params==0 and id <17 or self.type_params==0 and id >=19:
                self.ui[id].render()
            if self.type_params==1 and id <13 or self.type_params==1 and id >=17:
                self.ui[id].render()
        
        for light in self.lights:
            light.light_ui.render()
            light.update_light_attributes()

        #render every objs
        self.scene_renderer.all_renders()

        
        #swap buffers
        pg.display.flip()
    

    def get_time(self):
        self.time = pg.time.get_ticks()

    def run(self):
        #runs every frame and control the whole thinggy : => manager
        while True:
            #update the camera matrices and code
            self.camera.update()
            self.get_time()
            self.render()
            self.delta_time = self.clock.tick(120)
            self.fps = self.clock.get_fps()

    #others funcs


    def openNewInputWindow(self, name):
        def open_file():
            file = filedialog.askopenfile(mode='r', filetypes=[('OBJ', '*.obj')])    
            if file:
                input_str.append(f"{os.path.abspath(file.name)}")
        def open_tex():
            file = filedialog.askopenfile(mode='r', filetypes=[('PNJ, JPG', '*.png *.jpg')])    
            if file:
                input_str.append(f"{os.path.abspath(file.name)}")

        def import_entry(name, id):
            if name == "TEXTURE":
                if id == 0:
                    input_str.append(tk.Entry(newWindow))
                    input_str[-1].insert(tk.END, "TEXTURE ACCESS NAME")
                    input_str[-1].grid(row=1+id, column=0) #the actual input place
                else:
                    tk.Button(newWindow, padx=10, text="Browse TEX", command=open_tex).grid(row=row_enter) #button enter
            if name == "MODEL":
                if id == 0:
                    input_str.append(tk.Entry(newWindow))
                    input_str[-1].insert(tk.END, "OBJ ACCESS NAME")
                    input_str[-1].grid(row=1+id, column=0) #the actual input place
                else:
                    tk.Button(newWindow, padx=10, text="Browse OBJ", command=open_file).grid(row=row_enter) #button enter
            
        def one_entry(column):
            input_str.append(tk.Entry(newWindow))
            if self.camera.selected_obj != None:
                if name == "name":
                    input_str[-1].insert(tk.END, str(self.camera.selected_obj.name))
                if name == "texture":
                    input_str[-1].insert(tk.END, str(self.camera.selected_obj.tex_id))
                if name == "vao":
                    input_str[-1].insert(tk.END, str(self.camera.selected_obj.vao_name))
                if name == "intensity":
                    input_str[-1].insert(tk.END, str(self.camera.selected_obj.intensity))
            input_str[-1].grid(row=1, column=column) #the actual input place
        def multiple_entry(column):
            input_str.append(tk.Entry(newWindow))
            if self.camera.selected_obj != None:
                if name == "position":
                    input_str[-1].insert(tk.END, str(self.camera.selected_obj.position[len(input_str)-1]))
                if name == "rotation":
                    input_str[-1].insert(tk.END, str(self.camera.selected_obj.rotation[len(input_str)-1]))
                if name == "scale":
                    input_str[-1].insert(tk.END, str(self.camera.selected_obj.scale[len(input_str)-1]))
                if name == "color":
                    input_str[-1].insert(tk.END, str(self.camera.selected_obj.color[len(input_str)-1]))
            else:
                input_str[-1].insert(tk.END, '0')
            input_str[-1].grid(row=1, column=column) #the actual input place
        def func():
            #button was pressed
            if self.camera.selected_obj != None:
                if name == "name":
                    self.camera.selected_obj.name = input_str[0].get()
                if name == "vao":
                    self.camera.selected_obj.on_init_vao(input_str[0].get())
                if name == "position":
                    self.camera.selected_obj.position = glm.vec3(float(input_str[0].get()), float(input_str[1].get()), float(input_str[2].get()))
                if name == "rotation":
                    self.camera.selected_obj.rotation = glm.vec3(float(input_str[0].get()), float(input_str[1].get()), float(input_str[2].get()))
                if name == "scale":
                    self.camera.selected_obj.scale = glm.vec3(float(input_str[0].get()), float(input_str[1].get()), float(input_str[2].get()))
                if name == "texture":
                    self.camera.selected_obj.tex_id = input_str[0].get()
                    to_int = True
                    for caracters in self.camera.selected_obj.tex_id:
                        if caracters not in [str(i) for i in range(10)]:
                            to_int=False
                    if to_int: #we check if the entered caracters are nbrs, if so we transform the tex_id type to int
                        self.camera.selected_obj.tex_id = int(self.camera.selected_obj.tex_id)
                if name == "intensity":
                    self.camera.selected_obj.intensity = input_str[0].get()
                if name == "color":
                    self.camera.selected_obj.color = glm.vec3(float(input_str[0].get()), float(input_str[1].get()), float(input_str[2].get()))

                self.camera.selected_obj.m_model = self.camera.selected_obj.get_model_matrix(self)
                self.camera.selected_obj.on_init()

            #imports
            if name == "TEXTURE":
                self.mesh.texture.load_texture_obj(f"{input_str[0].get()}", f"{input_str[1]}")
            if name == "MODEL":
                self.mesh.load_texture_obj(f"{input_str[0].get()}",link_tex=None, link=f"{input_str[1]}")
                
            reset_button()

        def reset_button():
            newWindow.destroy()
        # Toplevel object which will 
        # be treated as a new window
        newWindow = tk.Tk()
        row_enter = 2
        # sets the title of the
        # Toplevel widget
        newWindow.title("Input")
        newWindow.wm_attributes("-topmost",True) #keep it on top

        input_str = []
        if name == "name" or name == "texture" or name == "vao" or name == "intensity":
            newWindow.geometry("125x70")
            tk.Label(newWindow, text=f"{name}").grid(row=0) #white part
            one_entry(0)

#for the higher params
        elif name == "QUIT":
            self.mesh.destroy()
            self.scene_renderer.destroy()
            pg.quit()
            sys.exit()
        elif name == "TEXTURE":
            newWindow.geometry("125x90")
            tk.Label(newWindow, text=f"{name}").grid(row=0) 
            import_entry(name,0) #texture name
            import_entry(name,1) #texture link
            row_enter+=1
        elif name == "MODEL":
            newWindow.geometry("125x90")
            tk.Label(newWindow, text=f"{name}").grid(row=0) 
            import_entry(name,0) #obj name
            import_entry(name,1) #obj link
            row_enter+=1
        else:
            newWindow.geometry("375x70")
            tk.Label(newWindow, text=f"{name}").grid(row=0) #white part
            for i in range(3):
                multiple_entry(i)

        tk.Button(newWindow, 
                        text="Enter",
                        padx = 10, 
                        command = func).grid(row=row_enter) #button enter
        newWindow.mainloop()   
            


if __name__ == "__main__":
    #window size
    user32 = ctypes.windll.user32
    screensize = (user32.GetSystemMetrics(0), user32.GetSystemMetrics(1))


    #run game
    game = GraphicEngine(screensize)
    game.run()