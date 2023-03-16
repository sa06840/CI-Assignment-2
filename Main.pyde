from processing import *
from random import uniform
import math
from screen import Screen
from saucepan import Saucepan

# Set up some constants
NUM_PARTICLES = 50
MAX_SPEED = 1
MAX_SIZE = 15
MAX_LIFESPAN = 500
WIDTH_BEAKER = 200
HEIGHT_BEAKER = 250
FLAME_INTENSITY=0.1
WIDTH_HEATSOURCE = 60
HEIGHT_HEATSOURCE = 30



class Particle:
    def __init__(self):
        self.x = random(width/12 , width/12 + WIDTH_BEAKER)
        self.y = random(height/3.5 , height/3.5 + HEIGHT_BEAKER)
        # self.size = random(2, MAX_SIZE)
        self.size = MAX_SIZE
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
        self.R= self.redfactor*255 
        self.G = self.greenfactor*255
        self.B = self.bluefactor*255
        fill(self.R,self.G,self.B)
        # self.color_change()
    
    
        # print(self.factor)
        # self.brightness += 0.001
         
        # Change the color of the particle based on its position
        if self.x > (width/12 + WIDTH_BEAKER - WIDTH_HEATSOURCE) and self.y > (height/3.5 + HEIGHT_BEAKER - 30):
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
        if (self.x - self.size/2)< (width/12) or (self.x + self.size/2) > (width/12 + WIDTH_BEAKER):
            self.speed_x *= -1
        if (self.y  + self.size/2)> (height/3.5 + HEIGHT_BEAKER) or (self.y - self.size/2 ) < (height/3.5) :
            self.speed_y *= -1
    
    # Draw the particle
    def display(self):
        ellipse(self.x, self.y, self.size, self.size)
    
    def lifeSpan(self):  
        # Decrease the lifespan of the particle
        self.lifespan -= 1
        
    def collide(self):
        # for other in particles:
        #     if other != self:
        #         distance = dist(self.x, self.y, other.x, other.y)
        #         if distance < self.size/2 + other.size/2:
                    
        #             c1=(2*other.size)/self.size + other.size
                    
        #             self.speed_x *= -1
        #             self.speed_y *= -1
        #             other.speed_x *= -1
        #             other.speed_y *= -1
        for other in particles:
            if other != self:
                distance = dist(self.x, self.y, other.x, other.y)
                if distance < self.size/2 + other.size/2:
                    # Calculate new velocities using elastic collision formula
                    temp_x = self.speed_x
                    temp_y = self.speed_y 
                    self.speed_x = other.speed_x
                    self.speed_y = other.speed_y
                    
                    other.speed_x = temp_x
                    other.speed_y = temp_y
                    
                    currentEnergy = 100*self.redfactor + 10*self.greenfactor + self.bluefactor
                    otherEnergy = 100*other.redfactor + 10*other.greenfactor + other.bluefactor
                    
                    if (currentEnergy > otherEnergy):
                        # tempR = other.redfactor
                        # tempG = other.greenfactor
                        # tempB = other.bluefactor
                        
                        other.redfactor += 0.5
                        other.greenfactor += 0.5
                        other.bluefactor += 0.5
                        
                        self.redfactor -= 0.5
                        self.greenfactor -= 0.5
                        self.bluefactor -= 0.5
                        
                    

particles = []

def setup():
    size(994, 501)
    # rect(50, 50, 300, 300) # Add a rectangular beaker
    for i in range(NUM_PARTICLES):
        particles.append(Particle())
        
def drawElements():
    
    # Drawing the beaker
    fill(102, 204, 255)
    stroke(0,255,0)
    strokeWeight(0)
    rect(width/12, height/3.5, WIDTH_BEAKER, HEIGHT_BEAKER)
    
    # Drawing arrows
    fill(0,100,0)
    stroke(0,100,0)
    strokeWeight(10)
    line(width/2 + 40, height/2 + 20, width/4 + 35, height/4 + 20)
    
    fill(0,100,0)
    stroke(0,100,0)
    strokeWeight(10)
    line(552, 385, 281, 427)

    
    # Drawing the heat source
    fill(255, 0, 0)
    stroke(255,255,255)
    strokeWeight(0)
    rect(width/12 + WIDTH_BEAKER - WIDTH_HEATSOURCE, height/3.5 + HEIGHT_BEAKER + 10 , WIDTH_HEATSOURCE, HEIGHT_HEATSOURCE)
    
    # Adding text at the top of the screen
    fill(0)
    textSize(40)
    textAlign(CENTER)
    text("Boiling Water", width/2, 90)

def draw():
    screen = Screen()
    screen.draw()
    
    saucepan = Saucepan()
    saucepan.draw(width/2.2, height/2.2)
    
    drawElements()
    
    #Resetting stroke weight(default value) for the particles 
    strokeWeight(1)

    for particle in particles:
        particle.move()
        particle.display()
        # particle.lifeSpan()
        particle.check_boundaries()
        particle.collide()
        
    # If the particle has died, create a new one
    particles[:] = [particle for particle in particles if particle.lifespan > 0]
    if len(particles) < NUM_PARTICLES:
        particles.append(Particle())
        
def mousePressed():
    # global MAX_SIZE
    # # MAX_SIZE = uniform(5, 30)
    # MAX_SIZE =   MAX_SIZE/2
    print(mouseX, mouseY)
    
def keyPressed():
    # global MAX_SPEED
    if key == ' ':
    #     MAX_SPEED = uniform(0, 5)
        global MAX_SIZE
        MAX_SIZE =   MAX_SIZE * 2
