import pyglet
from pyglet import shapes, gl
from pyglet.window import Window, key
from pyglet.graphics import Batch, draw
from pyglet.app import run
import numpy as np

# Creación de ventana y bash
ventana = Window(900,700,"Vamos fak",resizable=True)
batch = Batch()

class Spaceship:
    def __init__(self,
            center=(ventana.width/2,ventana.height/2),
            body_color=(255,255,255),
            wing_color=(255,255,255),
            engine_color=(255,255,255)):

        x0 = center[0]
        y0 = center[1]
        self.lBody = pyglet.shapes.Triangle(x0,y0+80,x0,y0-20,x0-20,y0,
                                    color=(131, 85, 160), batch=batch)
        self.rBody = pyglet.shapes.Triangle(x0,y0+80,x0,y0-20,x0+20,y0,
                                    color=(131, 85, 160), batch=batch)
        
        self.lWing = pyglet.shapes.Triangle(x0-16,y0,x0-40,y0+16,x0-80,y0-20,
                                    color=(89, 77, 157), batch=batch)
        self.rWing = pyglet.shapes.Triangle(x0+16,y0,x0+40,y0+16,x0+80,y0-20,
                                    color=(89, 77, 157), batch=batch)
        
        self.lUpEngine = pyglet.shapes.Triangle(x0-32,y0,x0-24,y0+40,x0-8,y0-8,
                                    color=(152, 57, 71), batch=batch)
        self.rUpEngine = pyglet.shapes.Triangle(x0+32,y0,x0+24,y0+40,x0+8,y0-8,
                                    color=(152, 57, 71), batch=batch)
                
        self.lLowEngine = pyglet.shapes.Triangle(x0-32,y0,x0-24,y0-36,x0-8,y0-8,
                                    color=(152, 57, 71), batch=batch)
        self.rLowEngine = pyglet.shapes.Triangle(x0+32,y0,x0+24,y0-36,x0+8,y0-8,
                                    color=(152, 57, 71), batch=batch)

road = pyglet.shapes.Rectangle(x=10, y=10, width=ventana.width-20,
                                 height=ventana.height-20, color=(80, 80, 80),
                                 batch=batch)
Ship1 = Spaceship((ventana.width/2,ventana.height*2/3))
Ship2 = Spaceship((ventana.width*2/6,ventana.height/2))
Ship3 = Spaceship((ventana.width*4/6,ventana.height/2))
Ship4 = Spaceship((ventana.width/6,ventana.height/3))
Ship5 = Spaceship((ventana.width*3/6,ventana.height/3))
Ship6 = Spaceship((ventana.width*5/6,ventana.height/3))

@ventana.event
def on_draw():
    ventana.clear()
    batch.draw()

run()
