from texture import Texture
from vao import VAO
class Mesh:
    def __init__(self, app):
        self.app = app
        self.vao = VAO(app.ctx)
        self.texture = Texture(app)
    
    def load_texture_obj(self, name, link=None):
        self.vao.load_vao(name)
        if link != None:
            self.texture.load_texture_obj(name, link)

    def load_texture_letter(self, text, col, bg_col):  
        self.texture.load_texture_letter(text, col, bg_col)
    def destroy(self):
        self.vao.destroy()
        self.texture.destroy()