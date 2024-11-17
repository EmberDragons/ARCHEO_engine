from vbo import VBO
from shader_program import Shader_Program

#uses both shader_program and vbo to turn them into a vao
class VAO:
    def __init__(self, ctx):
        self.ctx = ctx
        self.vbo = VBO(self.ctx)
        self.program = Shader_Program(self.ctx)
        self.vaos={}

        #cube vao set up 
        self.vaos['cube'] = self.get_vao(
            program = self.program.programs['default'],
            vbo = self.vbo.vbos['cube'])
    
    def get_vao(self, program, vbo):
        vao = self.ctx.vertex_array(program, [(vbo.vbo, vbo.format, *vbo.attrib)])
        return vao
    
    def destroy(self):
        self.vbo.destroy()
        self.program.destroy()