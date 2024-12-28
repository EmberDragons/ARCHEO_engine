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
        self.textures['depth_texture']=[]
    
    def get_depth_tex(self):
        depth_texture = self.ctx.depth_texture((4096,4096))
        depth_texture.repeat_x = False
        depth_texture.repeat_y = False
        return depth_texture
    
    def get_cube_depth_tex(self):
        cube_texture = self.ctx.depth_texture_cube((4096,4096))
        return cube_texture

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
        for tex in self.textures.values():
            if type(tex) == list:
                for i in range(len(tex)):
                    if type(tex[i]) == list:
                        for y in range(len(tex[i])):
                            tex[i][y].release()
                    else:
                        tex[i].release()
            else:
                tex.release()