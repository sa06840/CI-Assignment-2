from processing import *
from random import uniform

# Set up some constants
NUM_PARTICLES = 1000
MAX_SPEED = 0.2
MAX_SIZE = 20
MAX_LIFESPAN = 500
WIDTH_BEAKER = 300
HEIGHT_BEAKER = 300
FLAME_INTENSITY=0.1
WIDTH_HEATSOURCE = 60
HEIGHT_HEATSOURCE = 30

class Particle:
    def __init__(self):
        self.x = random(width/12 , width/12 + WIDTH_BEAKER)
        self.y = random(height/2.5 , height/2.5 + HEIGHT_BEAKER)
        # self.size = random(2, MAX_SIZE)
        self.size = 13
        self.speed_x = random(-MAX_SPEED, MAX_SPEED)
        self.speed_y = random(-MAX_SPEED, MAX_SPEED)
        self.lifespan = random(MAX_LIFESPAN)
        
        #RGB colors
        self.bluefactor = 1
        self.greenfactor = 0
        self.redfactor = 0
        
        self.flag=0
        

      

    def move(self):
        # Add a constant upward force to simulate movement up the screen
        # self.speed_y -= 0.005
            
        # Update the position of the particle
        self.x += self.speed_x
        self.y += self.speed_y

        #Initial Colors of the particles
        fill(self.redfactor*255 , self.greenfactor*255, self.bluefactor*255)
        # self.color_change()
    
    
    
    
            # print(self.factor)
        # self.brightness += 0.001
         
        # Change the color of the particle based on its position
        if self.x > (width/12 + WIDTH_BEAKER - WIDTH_HEATSOURCE) and self.y > (height/2.5 + HEIGHT_BEAKER - 30):
            self.color_change()
            self.speed_y -= 0.005
            self.speed_x += 0.001
           
        #     fill(0, 0, brightness*255)
        # elif self.y > height/2:
        #     brightness = (width-self.x)/width
            
        #     fill(255, 0, brightness*255)
        # elif self.y < height/2:
        #     brightness = self.y/(height/2)
        #     print (brightness)
        #     fill(0, brightness*255, 255)
        
        # else:
        #     fill(255, 0, 0)
            
    def color_change(self):
        
        if self.greenfactor < 1 and self.flag==0:
            self.greenfactor+=FLAME_INTENSITY
            # print(self.greenfactor)
        
        if self.greenfactor >=1.0 and self.redfactor <1:
           self.redfactor +=FLAME_INTENSITY
           self.flag=1
           # print(self.greenfactor, self.redfactor)
        
        if  self.redfactor >= 1:
            self.bluefactor-=FLAME_INTENSITY
            self.greenfactor-=FLAME_INTENSITY   
        
    # Change the direction of the particle based on its position
    def check_boundaries(self):
        if self.x < (width/12) or self.x > (width/12 + WIDTH_BEAKER):
            self.speed_x *= -1
        if self.y > (height/2.5 + HEIGHT_BEAKER) or self.y < (height/2.5) :
            self.speed_y *= -1
    
    # Draw the particle
    def display(self):
        ellipse(self.x, self.y, self.size, self.size)
    
    def lifeSpan(self):  
        # Decrease the lifespan of the particle
        self.lifespan -= 1

particles = []

def setup():
    size(800, 600)
    # rect(50, 50, 300, 300) # Add a rectangular beaker
    for i in range(NUM_PARTICLES):
        particles.append(Particle())
        
def draw():
    background(0)
    # fill(173, 216, 230) # Set the fill color to light blue
    # rect(50, 50, 300, 300) 
    
    # Drawing the beaker
    # fill(102, 204, 255) light blue
    fill(255, 255, 255)
    stroke(255,255,255)
    strokeWeight(10)
    rect(width/12, height/2.5, WIDTH_BEAKER, HEIGHT_BEAKER)
    
    # Drawing the heat source
    fill(255, 0, 0)
    stroke(255,255,255)
    strokeWeight(0)
    rect(width/12 + WIDTH_BEAKER - WIDTH_HEATSOURCE, height/2.5 + HEIGHT_BEAKER + 20 , WIDTH_HEATSOURCE, HEIGHT_HEATSOURCE)
    
    # Adding text at the top of the screen
    fill(255,255,255)
    textSize(32)
    textAlign(CENTER)
    text("Convection Currents", width/2, 40)
    
    #Resetting stroke weight(default value) for the particles 
    strokeWeight(1)

    for particle in particles:
        particle.move()
        particle.display()
        # particle.lifeSpan()
        particle.check_boundaries()
        
    # If the particle has died, create a new one
    particles[:] = [particle for particle in particles if particle.lifespan > 0]
    if len(particles) < NUM_PARTICLES:
        particles.append(Particle())
        
def mousePressed():
    global MAX_SIZE
    # MAX_SIZE = uniform(5, 30)
    MAX_SIZE =   MAX_SIZE/2
    
def keyPressed():
    # global MAX_SPEED
    if key == ' ':
    #     MAX_SPEED = uniform(0, 5)
        global MAX_SIZE
        MAX_SIZE =   MAX_SIZE * 2
