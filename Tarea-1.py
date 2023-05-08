import pyglet
import random
from pyglet import shapes
from pyglet.window import Window
from pyglet.graphics import Batch
from pyglet.app import run
import numpy as np

# Creación de ventana y bash
ventana = Window(800,600,"Vamos fak",resizable=False)

# Definicion de grilla para posicion y triggers
# Las estrellas se generan cuando pasan por algun valor de y dentro de grid_y
# La posicion en la que se generan esta dada por un valor aleatorio de grid_x e y=ventana.height
x_grid = np.zeros(40)
y_grid = np.zeros(40)
for i in range(0,40):
    x_grid[i] = ventana.width*i/40
    y_grid[i] = ventana.height*i/40

# Creacion de clase naves
# Las naves estan formadas por cuerpo interior, alas y propulsores
# Cada parte de la nave es un triangulo o serie de triangulos junto con su reflexion, l/r representan left/right
# Probablemente se puede hacer mucho mas sencillo con un TRIANGLE_FAN de OpenGL, pero no me di el tiempo de aprender
# a userlo y la tarea especificaba hacerlo con Pyglet (y pyglet.gl se sentia como un vacio legal )
class Spaceship:
    def __init__(self,
            center=(ventana.width/2,ventana.height/2),
            body_color=(255,255,255),
            wing_color=(255,255,255),
            engine_color=(255,255,255)):

        x0 = center[0]
        y0 = center[1]

        self.batch = Batch() # Para poder dibujar por separado cielo y naves

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
        
    def update(self): # Para dibujarlo sobre el cielo, se llama despues de Sky.update()
        self.batch.draw() 

# Creacion de clase estrellas
# Se definen las estrellas como clase para evitar tener tantos elementos y metodos dentro de Sky
class Star:
    def __init__(self,x,y,vy,batch,color=(255,255,255)) -> None:
        self.batch = batch
        self.spd = vy
        self.y = y
        self.x = x
        self.color = color
        self.body = pyglet.shapes.Star(self.x, self.y, 4, 2, 4, color=self.color, batch=self.batch)

    def update(self):
        self.body.y -= self.spd
        self.y -= self.spd

    def delete(self):
        self.body.delete()

class Sky():
    def __init__(self):
        self.batch = Batch()
        self.background = shapes.Rectangle(0, 0, ventana.width, ventana.height, color=(5, 5, 30),batch=self.batch)
        self.stars = np.array([Star(0,ventana.height,6,color=(5, 5, 30),batch=self.batch)],dtype=Star)
        self.star_lines = np.array([1],dtype=int)

    def gen_stars(self):
        if (self.stars[0].y in y_grid):
            n = random.randint(4,8)
            samp = random.sample(range(0,40),n)
            for i in range(0,n):
                self.stars = np.append(self.stars,Star(x_grid[samp[i]],ventana.height,6,self.batch))
            self.star_lines = np.append(self.star_lines,[n])

    def update(self):
        for i in range(0,len(self.stars)):
            self.stars[i].update()
        if self.stars[0].y < 0:
            for i in range(0,self.star_lines[0]):
                self.stars[i].delete()
            self.stars = self.stars[self.star_lines[0]:]
            self.star_lines = self.star_lines[1:len(self.star_lines)]
        self.gen_stars()
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
