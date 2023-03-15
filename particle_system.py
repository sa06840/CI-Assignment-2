from processing import *
from random import uniform

# Set up some constants
NUM_PARTICLES = 2000
MAX_SPEED = 1
MAX_SIZE = 20
MAX_LIFESPAN = 500
WIDTH_BEAKER = 300
HEIGHT_BEAKER = 300

class Particle:
    def __init__(self):
        self.x = random(width/12 + (3*WIDTH_BEAKER)/4, width/12 + WIDTH_BEAKER)
        self.y = height/2.5 + HEIGHT_BEAKER
        self.size = random(2, MAX_SIZE)
        self.speed_x = random(-MAX_SPEED, MAX_SPEED)
        self.speed_y = random(-MAX_SPEED, 0)
        self.lifespan = random(MAX_LIFESPAN)
      


    
    def move(self):
        # Add a constant upward force to simulate movement up the screen
        # self.speed_y -= 0.005
            
        # Update the position of the particle
        self.x += self.speed_x
        self.y += self.speed_y
        
        # Change the color of the particle based on its position
        if self.x < width/2 and self.y > height/2:
            brightness = (self.y-height/2)/(height/2)
            fill(0, 0, brightness*255)
        elif self.y > height/2:
            brightness = (width-self.x)/width
            fill(255, 0, brightness*255)
        elif self.y < height/2:
            brightness = self.y/(height/2)
            fill(0, brightness*255, 255)
        else:
            fill(255, 0, 0)
            
        # Change the direction of the particle based on its position
        if (self.x > (width/12 + WIDTH_BEAKER) and self.y > (height/2.5)+ 5):
            self.speed_x *= -1
            self.speed_y -= 0.005
        elif (self.x < (width/12 + (3*WIDTH_BEAKER)/4) and self.y > (height/2.5)+ 5):
            self.speed_x *= -1
            self.speed_y -= 0.005
        elif (self.y < (height/2.5)):
            self.speed_x = -1
            self.speed_y = 0
        
        # Draw the particle
        ellipse(self.x, self.y, self.size, self.size)
            
        # Wrap the particle around the edges of the screen
        if self.x < 0:
            self.x = width
            self.y = random(height)
            self.speed_x = random(-MAX_SPEED, 0)
            self.speed_y = random(-MAX_SPEED, MAX_SPEED)
            self.lifespan = random(MAX_LIFESPAN)
            
        # Decrease the lifespan of the particle
        self.lifespan -= 1

particles = []

def setup():
    size(800, 600)
    # rect(50, 50, 300, 300) # Add a rectangular beaker
    for i in range(NUM_PARTICLES):
        particles.append(Particle())
        
def draw():
    background(255,255,255)
    # fill(173, 216, 230) # Set the fill color to light blue
    # rect(50, 50, 300, 300) 
    
    # Drawing the beaker
   
    fill(102, 204, 255)
    stroke(0)
    strokeWeight(10)
    rect(width/12, height/2.5, WIDTH_BEAKER, HEIGHT_BEAKER)
    
    # Adding text at the top of the screen
    fill(0)
    textSize(32)
    textAlign(CENTER)
    text("Convection Currents", width/2, 40)
    
    #Resetting stroke weight(default value) for the particles 
    strokeWeight(1)

    for particle in particles:
        particle.move()
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
