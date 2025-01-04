import glm

class SceneRenderer:
    def __init__(self, app):
        self.app = app
        self.ctx = app.ctx
        self.mesh = app.mesh
        self.shadowMapList = []

    def add_shadow(self, param=""):
        if param == "point":
            self.shadowMapList.append(ShadowCubeMap(self.app))
        else:
            self.shadowMapList.append(ShadowMap(self.app))

    def remove_shadow(self, indexe=-1):
        self.shadowMapList[indexe].destroy()
        self.shadowMapList.pop(indexe)
        depth_tex = self.app.mesh.texture.textures['depth_texture'].pop(indexe)
        for elt in depth_tex:
            elt.release()

    def render_shadow(self):
        # Directions for the cube map faces
        for shadowMap in self.shadowMapList:
            shadowMap.render_depth()

    def render(self):
        self.app.ctx.screen.use()
        #render scene
        for obj in self.app.scene:
            obj.render()
    
    def all_renders(self):
        #pass 1
        self.render_shadow()
        #pass 2
        self.render()
    
    def destroy(self):
        for shadowMap in self.shadowMapList:
            shadowMap.destroy()


class ShadowCubeMap():
    def __init__(self, app):
        self.app = app
        #depth buffer / shadows
        self.app.mesh.texture.textures['depth_texture'].append(self.app.mesh.texture.get_cube_depth_tex())
        self.indexe = len(self.app.scene_renderer.shadowMapList)
        self.depth_texture = self.app.mesh.texture.textures['depth_texture'][self.indexe] # this is an array
        """framebuffer"""
        self.depth_fbo = [self.app.ctx.framebuffer(
                depth_attachment=self.depth_texture[i]
        ) for i in range(6)]

    def render_depth(self):
        # Directions for the cube map faces
        for face_cube in range(6):

            self.depth_fbo[face_cube].clear()
            self.depth_fbo[face_cube].use()

            for obj in self.app.scene:
                if obj.vao_name != "light":
                    obj.render_shadow(self.indexe, face_cube) #0 is the indice of the light we are currently on
                
    def destroy(self):
        for face_cube in range(6):
            self.depth_fbo[face_cube].release()

class ShadowMap():
    def __init__(self, app):
        self.app = app
        #depth buffer / shadows
        self.app.mesh.texture.textures['depth_texture'].append(self.app.mesh.texture.get_depth_tex())
        self.indexe = len(self.app.mesh.texture.textures['depth_texture'])-1
        self.depth_texture =  self.app.mesh.texture.textures['depth_texture'][self.indexe] # this is an array
        """framebuffer"""
        self.depth_fbo = self.app.ctx.framebuffer(
                depth_attachment=self.depth_texture
        ) 

    def render_depth(self):
        # Directions for the cube map faces
        self.depth_fbo.clear()
        self.depth_fbo.use()

        for obj in self.app.scene:
            if obj.vao_name != "light":
                obj.render_shadow(self.indexe, -1) #-1 => not multiple face
                
    def destroy(self):
        self.depth_fbo.release()