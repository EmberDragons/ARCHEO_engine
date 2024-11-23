import numpy as np
import moderngl as mgl
import glm
from pywavefront import Wavefront

class VBO:
    def __init__(self, ctx):
        self.vbos={}
        self.ctx = ctx
        #all inits
        self.vbos['cube'] = CubeVBO(ctx)
        self.vbos['pyramid'] = PyramidVBO(ctx)

    def load_object(self, name):
        self.vbos[name] = ObjectVBO(self.ctx, f"model/{name}.obj")

    def destroy(self):
        [vbo.destroy() for vbo in self.vbos.values()]

class BaseVBO:
    def __init__(self, ctx):
        self.ctx=ctx
        self.vbo = self.get_vbo()
        self.format: str = None
        self.attrib: list = None
    
    def get_vertex_data(self):
        ...
        #methode to override :D ... => nothin'

    def get_vbo(self):
        #instantiate the tringle in a vertex buffer in GPU
        vertex_data = self.get_vertex_data()
        vbo = self.ctx.buffer(vertex_data)
        return vbo
    def destroy(self):
        self.vbo.release()
    
class CubeVBO(BaseVBO):
    def __init__(self, ctx):
        data = self.get_vertex_data()
        super().__init__(ctx)
        self.format = '2f 3f 3f'
        self.attrib = ['in_texcoord', 'in_position', 'in_normales']

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
    
class PyramidVBO(BaseVBO):
    def __init__(self, ctx):
        data = self.get_vertex_data()
        super().__init__(ctx)
        self.format = '2f 3f 3f'
        self.attrib = ['in_texcoord', 'in_position', 'in_normales']

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
    
    def get_vertex_data(self):
        vertices = [(0,1,0), (-1,-1,1), (-1,-1,-1), (1,-1,-1), (1,-1,1)]
        indices = [(0,2,1), (0,3,2),
                   (0,4,3), (0,1,4),
                   (1,2,3), (3,4,1)]
        vertex_data = self.get_data(vertices, indices)

        tex_coord = [(0.5,0),(0,1),(1,1),(1,0),(0,0)]
        tex_coord_indices = [(0,1,2), (0,1,2),
                             (0,1,2), (0,1,2),
                             (4,1,2), (2,3,4)]
        tex_coord_data = self.get_data(tex_coord, tex_coord_indices)

        #normal infos
        normales=[]
        for i in range(0,len(vertex_data),3):
            #we have 18 values and for 3 vertices it's the same normal
            normales.append(self.get_triangle_normal(vertex_data[i], vertex_data[i+1], vertex_data[i+2]))
            normales.append(self.get_triangle_normal(vertex_data[i], vertex_data[i+1], vertex_data[i+2]))
            normales.append(self.get_triangle_normal(vertex_data[i], vertex_data[i+1], vertex_data[i+2]))
        normal_data = np.array(normales, dtype = 'f4')
        
        vertex_data = np.hstack([tex_coord_data, vertex_data, normal_data])
        return vertex_data

class ObjectVBO(BaseVBO):
    def __init__(self, ctx, link):
        self.link = link
        super().__init__(ctx)
        self.format = '2f 3f 3f'
        self.attrib = ['in_texcoord', 'in_normales', 'in_position'] #herrrrreee all problems arise
    
    def get_vertex_data(self):
        obj = Wavefront('model/Knife.obj', parse=True,cache=True)
        verts = []
        n=0
        for name, material in obj.materials.items():
            # Contains the vertex format (string) such as "T2F_N3F_V3F"
            # Contains the vertex list of floats in the format described above
            if n<2:
                for vert in material.vertices:
                    verts.append(vert)
            n+=1
        verts = np.array(verts, dtype = 'f4')
        print(verts)
        return verts