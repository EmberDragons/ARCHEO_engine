import model
class Light():
    def __init__(self,app,pos,color, intensity):
        self.app = app
        self.position = pos
        self.color = color
        self.intensity = intensity
        self.create_ui()


    def create_ui(self):
        self.light_ui = model.Light(self.app,self.position, intensity=self.intensity, color=self.color)
    
    def update_light_attributes(self):
        self.position = self.light_ui.position
        self.intensity = self.light_ui.intensity
        self.color = self.light_ui.color