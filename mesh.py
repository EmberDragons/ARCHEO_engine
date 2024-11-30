from texture import Texture
from vao import VAO
class Mesh:
    def __init__(self, app):
        self.app = app
        self.vao = VAO(app.ctx)
        self.texture = Texture(app)
    
    def load_texture_obj(self, name, link=None, load_letters = False):
        if load_letters == False:
            self.vao.load_vao(name)
        if link != None:
            self.texture.load_texture_obj(name, link, load_letters)

    def destroy(self):
        self.vao.destroy()
        self.texture.destroy()