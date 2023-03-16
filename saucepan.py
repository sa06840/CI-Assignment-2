

class Saucepan(object):

    def __init__(self):
        self.img = loadImage('saucepan2.png')
        self.x = 500
        
    def draw(self, cx, cy):
        self.img.resize(200,190)
        image(self.img, cx,cy)
        
