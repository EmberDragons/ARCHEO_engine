
class SceneRenderer:
    def __init__(self, app):
        self.app = app
        self.ctx = app.ctx
        self.mesh = app.mesh

        #depth buffer / shadows
        self.depth_texture =  self.mesh.texture.textures['depth_texture']
        self.depth_fbo = self.ctx.framebuffer(depth_attachment=self.depth_texture)

    def render_shadow(self):
        self.depth_fbo.clear()
        self.depth_fbo.use()
        for obj in self.app.scene:
            if obj.vao_name != "light":
                obj.render_shadow()

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
        self.depth_fbo.release()