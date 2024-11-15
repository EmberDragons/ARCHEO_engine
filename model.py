import numpy as np
import pygame as pg
import glm
import time
from function import *

class Cube():
    def __init__(self, app, img_name='brick.jpg'):
        self.app = app
        self.ctx = app.ctx
        self.vbo = self.get_vbo() #triangle vertex
        self.shader_program = self.get_shader_program('default')
        self.vao = self.get_vao()
        self.m_model = self.get_model_matrix()
        self.texture = self.get_texture(path=f'img/{img_name}')
        self.buffer_matrices()
        self.buffer_lights()
        self.set_texture()

    def update(self):
        #model
        self.m_model = self.update_rotation()
        self.buffer_lights()
        self.buffer_matrices()

    def update_rotation(self):
        rotation_matrix = glm.mat4x4(
                1.0,  0.0,  -0.003, 0.0,
                0.0,  1.0, -0.002, 0.0,
                0.003,  0.002,  1.0, 0.0,
                0.0, 0.0, 0.0, 1.0)
        new_model = self.m_model #*rotation_matrix
        return new_model

    def get_texture(self,path):
        texture = pg.image.load(path).convert()
        texture = pg.transform.flip(texture, flip_x = True, flip_y = False)
        texture = self.ctx.texture(size = texture.get_size(), components=3,
                                   data = pg.image.tostring(texture, 'RGB'))
        return texture

    def set_texture(self):
        self.shader_program['u_texture_0']=0
        self.texture.use()


    def get_model_matrix(self):
        m_model = glm.mat4()
        return m_model

    def buffer_matrices(self):
        self.shader_program['m_proj'].write(self.app.camera.m_proj)
        self.shader_program['m_view'].write(self.app.camera.m_view)
        self.shader_program['m_model'].write(self.m_model)

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
            light_pos = (0,0,0)
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

    def destroy(self):
        self.vbo.release()
        self.shader_program.release()
        self.vao.release()

    def get_vao(self):
        vao = self.ctx.vertex_array(self.shader_program, [(self.vbo, '2f 3f 3f', 'in_texcoord', 'in_position', 'in_normales')])
        return vao
    
    def get_vertex_data(self):
        vertices = [(-1,-1,1), (1,-1,1), (1,1,1), (-1,1,1),
                    (-1,1,-1), (-1,-1,-1), (1,-1,-1), (1,1,-1)]
        indices = [(0,2,3), (0,1,2),
                   (1,7,2), (1,6,7),
                   (6,5,4), (4,7,6),
                   (3,4,5), (3,5,0),
                   (3,7,4), (3,2,7),
                   (0,6,1), (6,0,5)]
        vertex_data = self.get_data(vertices, indices)

        tex_coord = [(0,0),(1,0),(1,1),(0,1)]
        tex_coord_indices = [(0,2,3), (0,1,2),
                            (0,2,3), (0,1,2),
                            (0,1,2), (2,3,0),
                            (2,3,0), (2,0,1),
                            (0,2,1), (0,3,2),
                            (3,1,2), (1,3,0)]
        tex_coord_data = self.get_data(tex_coord, tex_coord_indices)

        #normal infos
        normales=[]
        for i in range(0,len(vertex_data),3):
            #we have 36 values and for 3 vertices it's the same normal
            normales.append(self.get_triangle_normal(vertex_data[i], vertex_data[i+1], vertex_data[i+2]))
            normales.append(self.get_triangle_normal(vertex_data[i], vertex_data[i+1], vertex_data[i+2]))
            normales.append(self.get_triangle_normal(vertex_data[i], vertex_data[i+1], vertex_data[i+2]))
        normal_data = np.array(normales, dtype = 'f4')
        
        vertex_data = np.hstack([tex_coord_data, vertex_data, normal_data])
        return vertex_data

    #get normals
    def get_triangle_normal(self, a, b, c):
        #return a vector3 normal to the plane formed by the 3 points
        edge1 = b-a
        edge2 = c-a
        normal = glm.cross(edge1,edge2)
        return normal

    @staticmethod
    def get_data(vertices, indices):
        #separate the vertices in triangles with indices
        data = [vertices[ind] for triangle in indices for ind in triangle]
        vertex_data = np.array(data, dtype = 'f4')
        return vertex_data
    
    def get_vbo(self):
        #instantiate the tringle in a vertex buffer in GPU
        vertex_data = self.get_vertex_data()
        vbo = self.ctx.buffer(vertex_data)
        return vbo
    
    def get_shader_program(self, shader_name):
        with open(f'shaders/{shader_name}.vert') as file:
            vertex_shader = file.read()
        with open(f'shaders/{shader_name}.frag') as file:
            fragment_shader = file.read()

        program = self.ctx.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)
        return program

