import pyglet
from pyglet.window import Window, key
from pyglet import shapes
from pyglet.app import run
from pyglet.graphics import Batch
import numpy as np

# Creación de ventana y bash
ventana = Window(700,900,"Vamos fak",resizable=True)
batch = Batch()

road = pyglet.shapes.Rectangle(x=10, y=10, width=ventana.width-20,
                                 height=ventana.height-20, color=(80, 80, 80),
                                 batch=batch)

class Spaceship:
    def __init__(self,center=(ventana.width/2,ventana.height/2)):
        x0 = center[0]
        y0 = center[1]
        self.lBody = pyglet.shapes.Triangle(x0,y0+70,x0-20,y0,x0,y0-30,
                                       color=(190, 33, 78), batch=batch)
        self.rBody = pyglet.shapes.Triangle(x0,y0+70,x0+20,y0,x0,y0-30,
                                       color=(190, 33, 78), batch=batch)
        self.lEngine = pyglet.shapes.Triangle(x0,y0+70,x0-20,y0,x0,y0-30,
                                       color=(190, 33, 78), batch=batch)
        self.rEngine = pyglet.shapes.Triangle(x0,y0+70,x0+20,y0,x0,y0-30,
                                       color=(190, 33, 78), batch=batch)
        self.lWing = pyglet.shapes.Triangle(x0,y0+70,x0-20,y0,x0,y0-30,
                                       color=(190, 33, 78), batch=batch)
        self.rWing = pyglet.shapes.Triangle(x0,y0+70,x0+20,y0,x0,y0-30,
                                       color=(190, 33, 78), batch=batch)

Ship1 = Spaceship()

@ventana.event
def on_key_release(symbol, modifiers):
    if symbol == key.SPACE:
        ventana.set_fullscreen(not ventana._fullscreen)

@ventana.event
def on_key_press(symbol, modifiers):
    if symbol == key.A:
        print('The "A" key was pressed.')

@ventana.event
def on_draw():
    ventana.clear()
    batch.draw()

run()
