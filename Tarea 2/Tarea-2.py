import sys
import os.path
import pyglet
import random

import numpy as np
import grafica_tarea.scene_graph as sg
import grafica_tarea.shaders as sh
import grafica_tarea.performance_monitor as pm
import grafica_tarea.transformations as tr
import grafica_tarea.shapes as shapes
import grafica_tarea.obj_handler as oh

from grafica_tarea.assets_path import getAssetPath
from grafica_tarea.gpu_shape import createGPUShape
from grafica_tarea.camera import Camera
from pyglet.window import Window
from OpenGL.GL import *

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

WIDTH, HEIGHT = 800, 800
PROJECTIONS = [
    tr.perspective(60, float(WIDTH)/float(HEIGHT), 0.1, 100),  # PERSPECTIVE_PROJECTION
    tr.ortho(-8, 8, -8, 8, 0.1, 100)  # ORTOGRAPHIC_PROJECTION
]

ASSETS = {
    "pochita_obj": getAssetPath("navesita.obj"),
    "pochita_tex": getAssetPath("pochita.png"),
    "fondo_tex": getAssetPath("bricks.jpg")
}
TEX_PARAMS = [GL_REPEAT, GL_REPEAT, GL_NEAREST, GL_NEAREST]

ventana = Window(width=800, height=600)

def crearNavesita(pipeline):
    #naveShape = createGPUShape(pipeline,shapes.createTextureCube(1.0, 1.0))
    naveShape = createGPUShape(pipeline, oh.read_OBJ2(ASSETS["pochita_obj"]))
    naveShape.texture = sh.textureSimpleSetup(ASSETS["pochita_tex"],*TEX_PARAMS)
    naveShapeNode = sg.SceneGraphNode("nave_shape")
    naveShapeNode.childs += [naveShape]
    naveRotNode = sg.SceneGraphNode("nave_rot")
    naveRotNode.childs += [naveShapeNode]
    naveMoveNode = sg.SceneGraphNode("nave_move")
    naveMoveNode.childs += [naveRotNode]
    naveNode = sg.SceneGraphNode("nave")
    naveNode.childs += [naveMoveNode]
    return naveNode

def crearFondo(pipeline):
    fondoShape = createGPUShape(pipeline, shapes.createTextureCubeTarea2Normals(5.0,1.0,5.0))
    fondoShape.texture = sh.textureSimpleSetup(ASSETS["fondo_tex"], *TEX_PARAMS)
    fondoNode = sg.SceneGraphNode("fondo")
    fondoNode.childs += [fondoShape]
    fondoNode.transform = tr.translate(0,0,0.5)
    return fondoNode

class Navesita:
    def __init__(self, pipeline):
        self.pos = [0,0,0]
        self.rot = 0
        self.spin = 0
        self.move = 0
        self.rot_speed = 0.1*np.pi/2
        self.move_speed = 0.1
        self.pipeline = pipeline
        self.node = crearNavesita(self.pipeline)
    
    def update(self):
        self.pos[0] += self.move*self.move_speed*np.cos(navesita.rot)
        self.pos[1] += -self.move*self.move_speed*np.sin(navesita.rot)
        self.rot += self.spin*self.rot_speed
        sg.findNode(self.node,"nave_move").transform = (
            tr.translate(navesita.pos[0],0,navesita.pos[1])
        )
        sg.findNode(self.node,"nave_rot").transform = (
            tr.rotationY(self.rot)
        )


camera = Camera()
mvpPipeline = sh.SimpleTextureModelViewProjectionShaderProgramOBJ()
navesita = Navesita(mvpPipeline)

root = sg.SceneGraphNode("root")
fondo = crearFondo(mvpPipeline)
naveNode = navesita.node
root.childs += [fondo, naveNode]

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
    if symbol == pyglet.window.key.PLUS:
        camera.R_direction -= 1
    if symbol == pyglet.window.key.MINUS:
        camera.R_direction += 1

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
    if symbol == pyglet.window.key.PLUS:
        camera.R_direction += 1
    if symbol == pyglet.window.key.MINUS:
        camera.R_direction -= 1


projectionToUse = tr.perspective(45, float(ventana.width)/float(ventana.height), 0.1, 100)


@ventana.event
def on_draw():
    ventana.clear()

    navesita.update()

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    #camera.update()

    # view = tr.lookAt(
    #     camera.eye,
    #     camera.at,
    #     camera.up
    # )

    glUniformMatrix4fv(glGetUniformLocation(mvpPipeline.shaderProgram, "projection"), 1, GL_TRUE, projectionToUse)
   

    view = tr.lookAt(
            np.array([-4,4,4]),
            np.array([0,0,0]),
            np.array([0,1,0]) )

    glUniformMatrix4fv(glGetUniformLocation(mvpPipeline.shaderProgram, "model"), 1, GL_TRUE, tr.identity())
    glUniformMatrix4fv(glGetUniformLocation(mvpPipeline.shaderProgram, "view"), 1, GL_TRUE, view)


    sg.drawSceneGraphNode(root, mvpPipeline, "model")




# Each time update is called, on_draw is called again
# That is why it is better to draw and update each one in a separated function
# We could also create 2 different gpuQuads and different transform for each
# one, but this would use more memory

pyglet.app.run()