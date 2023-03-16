
class Screen(object):
    
    def __init__(self):
        self.img = loadImage('GreenKitchen2.png')
        
    def draw(self):
        background(self.img)
        
