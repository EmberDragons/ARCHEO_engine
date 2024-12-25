import model
import glm

class Light():
    def __init__(self,app,pos,color, intensity, name=None, param =None):
        self.name = name
        self.app = app
        self.position = pos
        self.color = color
        self.intensity = intensity
        self.create_ui()

        self.direction = glm.vec3(0,0,0)
        self.m_view_l = self.get_dir_view_mat()
        self.m_proj_l = self.get_dir_proj_mat()

        self.type_of_light = param
        if self.type_of_light == "point":
            self.m_view_l = self.get_point_view_mat()
            self.m_proj_l = self.get_point_proj_mat()


    def create_ui(self):
        self.light_ui = model.Light(self.app,self.position, intensity=self.intensity, color=self.color, name = self.name)
    
    def update_light_attributes(self):
        if self.type_of_light == 'point':
            self.set_point_view_mat()
        else:
            self.set_dir_view_mat()
        
        self.position = self.light_ui.position
        self.intensity = self.light_ui.intensity
        self.color = self.light_ui.color

    def set_dir_view_mat(self):
        self.m_view_l = self.get_dir_view_mat()
    def get_dir_view_mat(self):
        return glm.lookAt(self.position, self.direction, glm.vec3(0,1,0))
    def get_dir_proj_mat(self):
        #with near = 0.1 and far = 100
        return glm.ortho(-100,100,-100,100,0.1,100) #directional light ig
    

    def set_point_view_mat(self):
        self.m_view_l = self.get_point_view_mat()
    def get_point_view_mat(self):
        return [glm.lookAt(self.position, self.position+glm.vec3(1,0,0), glm.vec3(0,-1,0)),
                glm.lookAt(self.position, self.position+glm.vec3(-1,0,0), glm.vec3(0,-1,0)),
                glm.lookAt(self.position, self.position+glm.vec3(0,1,0), glm.vec3(0,0,1)),
                glm.lookAt(self.position, self.position+glm.vec3(0,-1,0), glm.vec3(0,0,-1)),
                glm.lookAt(self.position, self.position+glm.vec3(0,0,1), glm.vec3(0,-1,0)),
                glm.lookAt(self.position, self.position+glm.vec3(0,0,-1), glm.vec3(0,-1,0)), 
        ]
    def get_point_proj_mat(self):
        #with near = 0.1 and far = 100
        return glm.perspective(glm.radians(90),1,0.1,100) #point light ig
