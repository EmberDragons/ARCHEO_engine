import pygame as pg
import moderngl as mgl

class Texture:
    def __init__(self, ctx):
        self.ctx = ctx
        self.textures = {}
        self.textures[0] = self.get_texture(path='img/brick.jpg')
        self.textures[1] = self.get_texture(path='img/glass.jpg')
    
    def load_texture_obj(self, name, link):
        self.textures[name] = self.get_texture(path=link)

    def get_texture(self,path):
        texture = pg.image.load(path).convert()
        texture = pg.transform.flip(texture, flip_x = True, flip_y = False)
        texture = self.ctx.texture(size = texture.get_size(), components=3,
                                   data = pg.image.tostring(texture, 'RGB'))
        #mipmap the best!
        texture.filter = (mgl.LINEAR_MIPMAP_LINEAR,mgl.LINEAR)
        texture.build_mipmaps()
        
        #anisotropy
        texture.anisotropy = 32.0
        return texture

    def destroy(self):
        [tex.release() for tex in self.textures.values()]