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
        self.textures[3] = self.get_texture(path='img/icon.png')
    
    def load_texture_obj(self, name, link):
        self.textures[name] = self.get_texture(path=link)
    def load_texture_letter(self, text, col, bg_col):
        self.textures[text] = self.get_texture_letter(text, col, bg_col)

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
    
    def get_texture_letter(self, text, color, bg_color):
        s_texture = self.drawText(text, color, bg_color)
        s_texture = pg.transform.flip(s_texture, flip_x = True, flip_y = False)
        texture  = self.ctx.texture(size=s_texture.get_size(), components=3, data=pg.image.tostring(s_texture, 'RGB'))
        return texture
    
    def drawText(self, text, color, bg_color):
        textSurface = self.app.font.render(text, True, (color[0]*255,color[1]*255,color[2]*255, 255), (bg_color[0]*255, bg_color[1]*255, bg_color[2]*255, 0))
        return textSurface
    
    def destroy(self):
        [tex.release() for tex in self.textures.values()]