from vbo import VBO
from shader_program import Shader_Program
import glm

#uses both shader_program and vbo to turn them into a vao
class VAO:
    def __init__(self, ctx):
        self.ctx = ctx
        self.scales = [] #every new object will have it's scale here
        self.vbo = VBO(self.ctx, self)
        self.program = Shader_Program(self.ctx)
        self.vaos={}

        #cube vao set up 
        self.vaos['cube'] = self.get_vao(
            program = self.program.programs['default'],
            vbo = self.vbo.vbos['cube'])
        
        self.vaos['pyramid'] = self.get_vao(
            program = self.program.programs['default'],
            vbo = self.vbo.vbos['pyramid'])
        
        self.vaos['ui'] = self.get_vao(
            program = self.program.programs['ui'],
            vbo = self.vbo.vbos['ui'])
    
    def load_vao(self, name):
        #object vao
        self.vbo.load_object(name) #we have created an instance of model
        self.vaos[name] = self.get_vao(
            program = self.program.programs['default'],
            vbo = self.vbo.vbos[name])
    
    
    def get_vao(self, program, vbo):
        vao = self.ctx.vertex_array(program, [(vbo.vbo, vbo.format, *vbo.attrib)])
        return vao
    
    def destroy(self):
        self.vbo.destroy()
        self.program.destroy()