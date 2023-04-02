import pyglet
import random
from pyglet import shapes
from pyglet.window import Window
from pyglet.graphics import Batch
from pyglet.app import run
import numpy as np

# Creación de ventana y bash
ventana = Window(900,700,"Vamos fak",resizable=False)

x_grid = [0]*10
for i in range(0,10):
    x_grid[i] = ventana.width*i/10

class Spaceship:
    def __init__(self,
            center=(ventana.width/2,ventana.height/2),
            body_color=(255,255,255),
            wing_color=(255,255,255),
            engine_color=(255,255,255)):

        x0 = center[0]
        y0 = center[1]

        self.batch = Batch()

        self.lBody = shapes.Triangle(x0,y0+80,x0,y0-20,x0-20,y0,
                                    color=(131, 85, 160), batch=self.batch)
        self.rBody = shapes.Triangle(x0,y0+80,x0,y0-20,x0+20,y0,
                                    color=(131, 85, 160), batch=self.batch)
        
        self.lWing = shapes.Triangle(x0-16,y0,x0-40,y0+16,x0-80,y0-20,
                                    color=(89, 77, 157), batch=self.batch)
        self.rWing = shapes.Triangle(x0+16,y0,x0+40,y0+16,x0+80,y0-20,
                                    color=(89, 77, 157), batch=self.batch)
        
        self.lUpEngine = shapes.Triangle(x0-32,y0,x0-24,y0+40,x0-8,y0-8,
                                    color=(152, 57, 71), batch=self.batch)
        self.rUpEngine = shapes.Triangle(x0+32,y0,x0+24,y0+40,x0+8,y0-8,
                                    color=(152, 57, 71), batch=self.batch)
                
        self.lLowEngine = shapes.Triangle(x0-32,y0,x0-24,y0-36,x0-8,y0-8,
                                    color=(152, 57, 71), batch=self.batch)
        self.rLowEngine = shapes.Triangle(x0+32,y0,x0+24,y0-36,x0+8,y0-8,
                                    color=(152, 57, 71), batch=self.batch)
        
    def update(self):
        self.batch.draw()

class Star:
    def __init__(self,x,y,vy,batch) -> None:
        self.batch = batch
        self.spd = vy
        self.y = y
        self.x = x
        self.body = pyglet.shapes.Star(self.x, self.y, 6, 2, 5, batch=batch)

    def update(self):
        self.body.y -= self.spd
        self.y -= self.spd
        pass


class Sky():
    def __init__(self):
        self.batch = Batch()
        self.background = shapes.Rectangle(0, 0, ventana.width, ventana.height, color=(5, 5, 30),batch=self.batch)
        self.stars = np.array([],dtype=Star)
        self.star_lines = np.array([],dtype=int)

    def gen_stars(self):
        n = random.randint(4,7)
        samp = random.sample(range(0,10),n)
        for i in range(0,n):
            self.stars = np.append(self.stars,Star(x_grid[samp[i]],ventana.height,4,self.batch))
        self.star_lines = np.append(self.star_lines,[n])

    def update(self):
        for i in range(0,len(self.stars)):
            self.stars[i].update()
        if (self.stars[0].y%100 == 0):
            self.gen_stars()
        elif self.stars[0].y < 0:
            self.stars = self.stars[self.star_lines[0]:-1]
            self.star_lines = self.star_lines[1:len(self.star_lines)]
        self.batch.draw()
        

Background = Sky()
Background.gen_stars()

Ship1 = Spaceship((ventana.width/2,ventana.height/2 + 120))
Ship2 = Spaceship((ventana.width/2 - 100,ventana.height/2))
Ship3 = Spaceship((ventana.width/2 + 100,ventana.height/2))
Ship4 = Spaceship((ventana.width/2,ventana.height/2 - 120))
Ship5 = Spaceship((ventana.width/2 + 180,ventana.height/2 - 120))
Ship6 = Spaceship((ventana.width/2 - 180,ventana.height/2 - 120))

Ships = np.array([Ship1,Ship2,Ship3,Ship4,Ship5,Ship6],dtype=Spaceship)

@ventana.event
def on_draw():
    
    ventana.clear()
    Background.update()
    for i in Ships:
        i.update()

run()
