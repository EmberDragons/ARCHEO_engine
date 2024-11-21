from texture import Texture
from vao import VAO
class Mesh:
    def __init__(self, app):
        self.app = app
        self.vao = VAO(app.ctx)
        self.texture = Texture(app.ctx)
    
    def load_texture_obj(self, name, link):
        self.texture.load_texture_obj(name, link)

    def destroy(self):
        self.vao.destroy()
        self.texture.destroy()