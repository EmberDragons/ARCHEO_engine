import glm
import moderngl as mgl
from OpenGL import GL

class SceneRenderer:
    def __init__(self, app):
        self.app = app
        self.ctx = app.ctx
        self.mesh = app.mesh
        if self.app.lights[0].type_of_light == "point":
            self.shadowMap = ShadowCubeMap(app)
        else:
            self.shadowMap = ShadowMap(app)

    def render_shadow(self):
        # Directions for the cube map faces
        self.shadowMap.render_depth()

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
        self.shadowMap.destroy()
class ShadowCubeMap():
    def __init__(self, app):
        self.std_ctx = mgl.create_context(standalone=True)
        self.app = app
        #depth buffer / shadows
        self.app.mesh.texture.textures['depth_texture'].append(self.app.mesh.texture.get_cube_depth_tex(self.std_ctx))
        self.depth_texture_cube = self.app.mesh.texture.textures['depth_texture'][0] # this is an array
        """framebuffer"""
        self.depth_fbo = self.app.ctx.framebuffer(
                depth_attachment = self.app.ctx.depth_texture((4096,4096))
        )
        self.depth_cubemap_id = self.depth_texture_cube.glo  # OpenGL texture ID

    def render_depth(self):
        # Directions for the cube map faces
        for face_cube in range(6):
            # Bind the framebuffer
            GL.glBindFramebuffer(GL.GL_FRAMEBUFFER, self.depth_fbo.glo)

    # Attach the specific face of the cubemap as the depth attachment
            GL.glFramebufferTexture2D(
                GL.GL_FRAMEBUFFER,
                GL.GL_DEPTH_ATTACHMENT,
                GL.GL_TEXTURE_CUBE_MAP_POSITIVE_X + face_cube,  # Select the face
                self.depth_cubemap_id,                          # The cubemap texture
                0                                          # Mipmap level
            )
            self.depth_fbo.clear()
            self.depth_fbo.use()

            for obj in self.app.scene:
                if obj.vao_name != "light":
                    obj.render_shadow(0, face_cube) #0 is the indice of the light we are currently on

    def destroy(self):
        for i in range(6):
            self.depth_fbo[i].release() 

class ShadowMap():
    def __init__(self, app):
        self.app = app
        #depth buffer / shadows
        self.app.mesh.texture.textures['depth_texture'].append(self.app.mesh.texture.get_depth_tex())
        self.depth_texture =  self.app.mesh.texture.textures['depth_texture'][0] # this is an array
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
                obj.render_shadow(0, -1) #-1 => not multiple face
                
    def destroy(self):
        self.depth_fbo.release() 