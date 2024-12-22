import model
import glm

class Light():
    def __init__(self,app,pos,color, intensity):
        self.app = app
        self.position = pos
        self.color = color
        self.intensity = intensity
        self.create_ui()

        self.direction = glm.vec3(0,0,0)
        self.m_view_l = self.get_view_mat()


    def create_ui(self):
        self.light_ui = model.Light(self.app,self.position, intensity=self.intensity, color=self.color)
    
    def update_light_attributes(self):
        self.m_view_l = self.get_view_mat()
        self.position = self.light_ui.position
        self.intensity = self.light_ui.intensity
        self.color = self.light_ui.color

    def get_view_mat(self):
        return glm.lookAt(self.position, self.direction, glm.vec3(0,1,0))