import model
class Light():
    def __init__(self,app,pos,color, intensity, size=0):
        self.app = app
        self.position = pos
        self.color = color
        self.intensity = intensity
        self.size = size
        self.create_ui()


    def create_ui(self):
        self.light_ui = model.Light(self.app,self.position)
    
    def update_light_attributes(self):
        self.position = self.light_ui.position