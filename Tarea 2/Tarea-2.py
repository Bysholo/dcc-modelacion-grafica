import sys
import os.path
import pyglet
import random

import numpy as np
import grafica_tarea.scene_graph as sg
import grafica_tarea.shaders as sh
import grafica_tarea.transformations as tr
import grafica_tarea.shapes as shapes
import grafica_tarea.obj_handler as oh

from grafica_tarea.assets_path import getAssetPath
from grafica_tarea.gpu_shape import createGPUShape
from pyglet.window import Window
from OpenGL.GL import *

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# Parametros para los objetos y texturas a importar
ASSETS = {
    "pochita_obj": getAssetPath("navesita_new.obj"),
    "pochita_tex": getAssetPath("pochita.png"),
    "fondo_tex": getAssetPath("bricks.jpg")
}
TEX_PARAMS = [GL_REPEAT, GL_REPEAT, GL_NEAREST, GL_NEAREST]

# Funcion para crear Shape de la nave, retornando un SceneGraphNode que la contiene
# Se incluyen además los nodos nave_rot y nave_move para tener estas transformaciones separadas
# de buena manera
def crearNavesita(pipeline):
    naveShape = createGPUShape(pipeline, oh.read_OBJ2(ASSETS["pochita_obj"]))
    naveShape.texture = sh.textureSimpleSetup(ASSETS["pochita_tex"],*TEX_PARAMS)
    naveShapeNode = sg.SceneGraphNode("nave_shape")
    naveShapeNode.transform = tr.matmul([tr.rotationZ(-np.pi/2),tr.uniformScale(0.1)])
    naveShapeNode.childs += [naveShape]
    naveRotNode = sg.SceneGraphNode("nave_rot")
    naveRotNode.childs += [naveShapeNode]
    naveMoveNode = sg.SceneGraphNode("nave_move")
    naveMoveNode.childs += [naveRotNode]
    naveNode = sg.SceneGraphNode("nave")
    naveNode.childs += [naveMoveNode]
    return naveNode

# Funcion para crear la figura que hará de fondo, retornando un SceneGraphNode que la contiene
# La Shape a utilizar es una version modificada de TextureCube, a la que se le borraron
# cuatro caras y se le agregaron las normales para poder usar el shader adecuado
def crearFondo(pipeline):
    fondoShape = createGPUShape(pipeline, shapes.createTextureCubeTarea2Normals(5.0,1.0,5.0))
    fondoShape.texture = sh.textureSimpleSetup(ASSETS["fondo_tex"], *TEX_PARAMS)
    fondoNode = sg.SceneGraphNode("fondo")
    fondoNode.childs += [fondoShape]
    fondoNode.transform = tr.translate(0,0,0.5)
    return fondoNode

# Se define una clase Navesita para poder guardar los datos de posicion y rotacion.
# 
class Navesita:
    def __init__(self, pipeline):                   # Se entrega un pipeline en el que dibujar el nodo
        self.pos = [0,0,0]
        self.yRot = 0                               # Grado rotacion Y
        self.zRot = 0                               # Grado rotacion Z
        self.spin = 0                               # 0 si no se mueve, 1 si se mueve
        self.move = 0                               # 0 si no esta rotando, 1 si esta rotando
        self.rot_speed = 0.1*np.pi/2                # Velocidad para rotar en Y
        self.move_speed = 0.1                       # Velocidad para desplazarse en X
        self.node = crearNavesita(pipeline)         # Nodo que se agrega al grafo de escena
    
    def update(self):
        self.pos[0] +=  self.move * self.move_speed * np.cos(self.yRot) * np.cos(self.zRot)
        self.pos[1] +=  self.move * self.move_speed * np.sin(self.zRot)
        self.pos[2] += -self.move * self.move_speed * np.sin(self.yRot) * np.cos(self.zRot)
        self.yRot   +=  self.spin * self.rot_speed
        sg.findNode(self.node,"nave_move").transform = (
            tr.translate(self.pos[0],self.pos[1],self.pos[2])
        )
        sg.findNode(self.node,"nave_rot").transform = (
            tr.matmul([tr.rotationY(self.yRot),tr.rotationZ(self.zRot)])
        )


ventana = Window(width=800, height=600)
mvpPipeline = sh.SimpleTextureModelViewProjectionShaderProgramOBJ()

navesita = Navesita(mvpPipeline)
fondo = crearFondo(mvpPipeline)
escena = sg.SceneGraphNode("escena")
escena.childs += [fondo, navesita.node]




# Setting up the clear screen color
glUseProgram(mvpPipeline.shaderProgram)

glClearColor(0.1, 0.1, 0.1, 1.0)

glEnable(GL_DEPTH_TEST)

# What happens when the user presses these keys
@ventana.event
def on_key_press(symbol, modifiers):
    if symbol == pyglet.window.key.A:
        navesita.spin = 1
    if symbol == pyglet.window.key.D:
        navesita.spin = -1
    if symbol == pyglet.window.key.W:
        navesita.move = 1
    if symbol == pyglet.window.key.S:
        navesita.move = -1

    elif symbol == pyglet.window.key.ESCAPE:
        ventana.close()

# What happens when the user releases these keys
@ventana.event
def on_key_release(symbol, modifiers):
    if symbol == pyglet.window.key.A:
        navesita.spin = 0
    if symbol == pyglet.window.key.D:
        navesita.spin = 0
    if symbol == pyglet.window.key.W:
        navesita.move = 0
    if symbol == pyglet.window.key.S:
        navesita.move = 0

@ventana.event()
def on_mouse_motion(x,y,dx,dy):
    navesita.zRot = y*np.pi/2*(np.power(1/2,7)) - 5*np.pi/4

WIDTH, HEIGHT = 800, 800
PROJECTIONS = [
    tr.perspective(60, float(WIDTH)/float(HEIGHT), 0.1, 100),  # PERSPECTIVE_PROJECTION
    tr.ortho(-8, 8, -8, 8, 0.1, 100)  # ORTOGRAPHIC_PROJECTION
]

@ventana.event
def on_draw():
    ventana.clear()

    navesita.update()

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)


    glUniformMatrix4fv(glGetUniformLocation(mvpPipeline.shaderProgram, "projection"), 1, GL_TRUE, PROJECTIONS[0])
   

    view = tr.lookAt(
            np.array([navesita.pos[0]-5,5,5]),
            np.array([navesita.pos[0],0,0]),
            np.array([0,1,0]) )

    glUniformMatrix4fv(glGetUniformLocation(mvpPipeline.shaderProgram, "model"), 1, GL_TRUE, tr.identity())
    glUniformMatrix4fv(glGetUniformLocation(mvpPipeline.shaderProgram, "view"), 1, GL_TRUE, view)


    sg.drawSceneGraphNode(escena, mvpPipeline, "model")



# Each time update is called, on_draw is called again
# That is why it is better to draw and update each one in a separated function
# We could also create 2 different gpuQuads and different transform for each
# one, but this would use more memory

ventana.set_mouse_visible(False)
pyglet.app.run()