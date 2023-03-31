import pyglet
import random
from pyglet import shapes
from pyglet.window import Window
from pyglet.graphics import Batch
from pyglet.app import run
import numpy as np

# Creación de ventana y bash
ventana = Window(900,700,"Vamos fak",resizable=False)
batch = Batch()

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
        self.lBody = shapes.Triangle(x0,y0+80,x0,y0-20,x0-20,y0,
                                    color=(131, 85, 160), batch=batch)
        self.rBody = shapes.Triangle(x0,y0+80,x0,y0-20,x0+20,y0,
                                    color=(131, 85, 160), batch=batch)
        
        self.lWing = shapes.Triangle(x0-16,y0,x0-40,y0+16,x0-80,y0-20,
                                    color=(89, 77, 157), batch=batch)
        self.rWing = shapes.Triangle(x0+16,y0,x0+40,y0+16,x0+80,y0-20,
                                    color=(89, 77, 157), batch=batch)
        
        self.lUpEngine = shapes.Triangle(x0-32,y0,x0-24,y0+40,x0-8,y0-8,
                                    color=(152, 57, 71), batch=batch)
        self.rUpEngine = shapes.Triangle(x0+32,y0,x0+24,y0+40,x0+8,y0-8,
                                    color=(152, 57, 71), batch=batch)
                
        self.lLowEngine = shapes.Triangle(x0-32,y0,x0-24,y0-36,x0-8,y0-8,
                                    color=(152, 57, 71), batch=batch)
        self.rLowEngine = shapes.Triangle(x0+32,y0,x0+24,y0-36,x0+8,y0-8,
                                    color=(152, 57, 71), batch=batch)

class Star:
    def __init__(self,x,y,vy) -> None:
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
        self.background = shapes.Rectangle(0, 0, ventana.width, ventana.height, color=(5, 5, 30),batch=batch)
        self.stars = np.array([],dtype=Star)
        self.star_lines = np.array([],dtype=int)

    def gen_stars(self):
        n = random.randint(4,7)
        samp = random.sample(range(0,10),n)
        for i in range(0,n):
            self.stars = np.append(self.stars,Star(x_grid[samp[i]],ventana.height,5))
        self.star_lines = np.append(self.star_lines,[n])

background = Sky()
background.gen_stars()

Ship1 = Spaceship((ventana.width/2,ventana.height/2 + 120))
Ship2 = Spaceship((ventana.width/2 - 100,ventana.height/2))
Ship3 = Spaceship((ventana.width/2 + 100,ventana.height/2))
Ship4 = Spaceship((ventana.width/2,ventana.height/2 - 120))
Ship5 = Spaceship((ventana.width/2 + 180,ventana.height/2 - 120))
Ship6 = Spaceship((ventana.width/2 - 180,ventana.height/2 - 120))

@ventana.event
def on_draw():
    
    ventana.clear()
    if (background.stars[0].y%100 == 0):
        background.gen_stars()
    if background.stars[0].y < 0:
        background.stars = background.stars[background.star_lines[0]:-1]
        background.star_lines = background.star_lines[1:-1]
    for i in range(0,len(background.stars)):
        if isinstance(background.stars[i],Star):
            background.stars[i].update()
    batch.draw()

run()
