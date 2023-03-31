import math as m
import pyglet
import random
from pyglet import shapes, gl
from pyglet.window import Window, key
from pyglet.graphics import Batch, draw
from pyglet.app import run
import numpy as np

#value = np.empty((), dtype=object)
#value[()] = (0, 0)
#a = np.full((10,10),value,dtype=tuple)
#print(a)

#def gen_rand_positions(n):
#    sampl = random.sample(range(0,10),n)
#    lista = [0]*10
#
#    for i in range(0,n):
#        lista[sampl[i]] = 1
#
#    return lista
#
#m=0
#while m<10000000:
#    n = random.randint(4,8)
#    a = gen_rand_positions(n)
#    sum = 0
#    for i in range(0,10):
#        sum += a[i]
#    if not (n == sum):
#        print(n,a,sum)
#        print("te aweonaste")
#        break
#    print(m)
#    m+=1
#
#print("puto amo")

#window = pyglet.window.Window(800, 600)
#batch = pyglet.graphics.Batch()
#
#road = pyglet.shapes.Rectangle(x=10, y=10, width=window.width-20,
#                                 height=window.height-20, color=(80, 80, 80),
#                                 batch=batch)
#
#dirt = pyglet.shapes.Rectangle(x=120, y=120, width=window.width-240,
#                                 height=window.height-240, color=(53, 40, 30),
#                                 batch=batch)
#
#class Car:
#    def __init__(self):
#        self.body = pyglet.shapes.Star(x=70, y=70, outer_radius=60, inner_radius=35,
#                                       rotation=270, num_spikes=3,
#                                       color=(255, 255, 78), batch=batch)
#        self.vx = 1
#        self.vy = 1
#
#    def udpate(self):
#        self.body.x += self.vx
#        self.body.y += self.vy
#        pass
#
#    def delete(self):
#        self.body.delete()
#
#a = np.array([Car(),0,0,0])
#
#@window.event
#def on_draw():
#    window.clear()
#        
#    print(isinstance(a[0],Car))
#    for i in range(0,4):
#        if isinstance(a[i],Car):
#            a[i].udpate()
#            if a[i].body.y > 150:
#                a[i] = 0
#        batch.draw()
#
#
#pyglet.app.run()

grid = np.array([0,0,0],dtype=int)
grid = np.append(grid,[4,0])
grid[1] = 6
for i in range(0,len(grid)):
    print(grid[i])