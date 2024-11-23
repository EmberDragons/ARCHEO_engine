import numpy as np
import pygame as pg
import glm

import time
from function import *

class BaseModel:
    def __init__(self, app, pos=(0,0,0), rot = (0,0,0), scale = (1,1,1), tex_id=0, vao_name='cube'):
        self.app = app
        self.position = glm.vec3(pos)
        self.rotation = glm.vec3(glm.radians(rot))
        self.scale = glm.vec3(scale)
        self.m_model = self.get_model_matrix()
        self.tex_id = tex_id
        self.vao = app.mesh.vao.vaos[vao_name]
        self.shader_program = self.vao.program
        self.camera = self.app.camera

    def update(self): ...

    def get_model_matrix(self):
        m_model = glm.mat4()
        m_model = glm.translate(m_model, self.position)

        m_model = glm.rotate(m_model, self.rotation.x, glm.vec3(1,0,0))
        m_model = glm.rotate(m_model, self.rotation.y, glm.vec3(0,1,0))
        m_model = glm.rotate(m_model, self.rotation.z, glm.vec3(0,0,1))
        
        m_model = glm.scale(m_model, self.scale)
        return m_model

    def buffer_lights(self):
        LIGHT_POS = []
        LIGHT_COL = []
        LIGHT_INT = []
        for light in self.app.lights:
            light_pos = light.position
            light_col = light.color
            light_int = light.intensity
            LIGHT_POS.append(light_pos)
            LIGHT_COL.append(light_col)
            LIGHT_INT.append(light_int)
        while len(LIGHT_POS) < 20: #we have 20 lights max
            light_pos = (0,0,0)
            light_col = (0,0,0)
            light_int = 0
            LIGHT_POS.append(light_pos)
            LIGHT_COL.append(light_col)
            LIGHT_INT.append(light_int)

        LIGHT_POS = np.array(LIGHT_POS, dtype = 'f4')
        LIGHT_COL = np.array(LIGHT_COL, dtype = 'f4')
        LIGHT_INT = np.array(LIGHT_INT, dtype = 'f4')
        
        self.shader_program['light_pos'].write(LIGHT_POS)
        self.shader_program['light_color'].write(LIGHT_COL)
        self.shader_program['light_intensity'].write(LIGHT_INT)

    def render(self):
        self.update()
        self.vao.render()

class Cube(BaseModel):
    def __init__(self, app, pos=(0,0,0), rot=(0,0,0), scale=(1,1,1), tex_id=0, vao_name='cube'):
        super().__init__(app, pos, rot, scale, tex_id, vao_name)
        self.on_init()

    def update(self):
        self.texture.use()
        #matrices
        self.shader_program['m_proj'].write(self.camera.m_proj)
        self.shader_program['m_view'].write(self.camera.m_view)
        self.shader_program['cam_pos'].write(self.camera.position)
        self.shader_program['m_model'].write(self.m_model)
        #light
        self.buffer_lights()

    def on_init(self):
        #texture part
        self.texture = self.app.mesh.texture.textures[self.tex_id]
        self.shader_program['u_texture_0'] = 0
        self.update()

class Pyramid(BaseModel):
    def __init__(self, app, pos=(0,0,0), rot=(0,0,0), scale=(1,1,1), tex_id=0, vao_name='pyramid'):
        super().__init__(app, pos, rot, scale, tex_id, vao_name)
        self.on_init()

    def update(self):
        self.texture.use()
        #matrices
        self.shader_program['m_proj'].write(self.camera.m_proj)
        self.shader_program['m_view'].write(self.camera.m_view)
        self.shader_program['cam_pos'].write(self.camera.position)
        self.shader_program['m_model'].write(self.m_model)
        #light
        self.buffer_lights()

    def on_init(self):
        #texture part
        self.texture = self.app.mesh.texture.textures[self.tex_id]
        self.shader_program['u_texture_0'] = 0
        self.update()

class Object(BaseModel):
    def __init__(self, app, pos=(0,0,0), rot=(0,0,0), scale=(1,1,1), tex_id=0, vao_name='cube'):
        self.tex_id = vao_name
        if type(tex_id) == int:
            app.mesh.load_texture_obj(vao_name) #only load vao, no tex
            self.tex_id=tex_id
        else:
            app.mesh.load_texture_obj(vao_name, tex_id) #load both vao and tex
        super().__init__(app, pos, rot, scale, self.tex_id, vao_name)
        self.on_init(tex_id)

    def update(self):
        self.texture.use()
        #matrices
        self.shader_program['m_proj'].write(self.camera.m_proj)
        self.shader_program['m_view'].write(self.camera.m_view)
        self.shader_program['cam_pos'].write(self.camera.position)
        self.shader_program['m_model'].write(self.m_model)
        #light
        self.buffer_lights()

    def on_init(self, tex_id):
        #texture part
        self.texture = self.app.mesh.texture.textures[self.tex_id]
        self.shader_program['u_texture_0'] = 0
        self.texture.use()
        self.update()