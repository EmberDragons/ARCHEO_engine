import pygame as pg
import moderngl as mgl

class Texture:
    def __init__(self, app):
        self.app = app
        self.ctx = app.ctx
        self.textures = {}
        self.textures[0] = self.get_texture(path='img/brick.jpg')
        self.textures[1] = self.get_texture(path='img/glass.jpg')
        self.textures[2] = self.get_texture(path='img/white.png')
    
    def load_texture_obj(self, name, link, load_letters = False):
        if load_letters:
            self.textures[link] = self.get_texture_letter(path=link)
        else:
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
    
    def get_texture_letter(self,path):
        texture = self.drawText(path)
        texture = pg.transform.flip(texture, flip_x = True, flip_y = False)
        texture = self.ctx.texture(size = texture.get_size(), components=3,
                                   data = pg.image.tostring(texture, 'RGB'))
        return texture
    
    def drawText(self, text):                                                
        textSurface = self.app.font.render(text, True, (255, 255, 66, 255)).convert_alpha()
        return textSurface
    
    def destroy(self):
        [tex.release() for tex in self.textures.values()]