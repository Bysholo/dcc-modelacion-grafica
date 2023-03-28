import pyglet
import random
from pyglet import shapes, gl
from pyglet.window import Window, key
from pyglet.graphics import Batch, draw
from pyglet.app import run
import numpy as np

# Creación de ventana y bash
ventana = Window(700,900,"Les fakin go",resizable=True)
nae = Batch()

road = pyglet.shapes.Rectangle(x=10, y=10, width=ventana.width-20,
                                 height=ventana.height-20, color=(80, 80, 80),
                                 batch=nae)

poli = pyglet.shapes.Polygon(((20,20),(20,40),(25,50),(50,20)),batch=nae)

run()
