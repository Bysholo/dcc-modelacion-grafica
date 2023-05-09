import sys
import os.path
import pyglet
import random

import numpy as np
import grafica_tarea.scene_graph as sg
import grafica_tarea.shaders as sh
import grafica_tarea.performance_monitor as pm
import grafica_tarea.transformations as tr

from grafica_tarea.assets_path import getAssetPath
from grafica_tarea.gpu_shape import createGPUShape
from grafica_tarea.obj_handler import read_OBJ2
from grafica_tarea.shapes import createTextureCubeTarea2
from grafica_tarea.camera import Camera
from pyglet.window import Window
from OpenGL.GL import *

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

WIDTH, HEIGHT = 800, 800

PERSPECTIVE_PROJECTION = 0
ORTOGRAPHIC_PROJECTION = 1

PROJECTIONS = [
    tr.perspective(60, float(WIDTH)/float(HEIGHT), 0.1, 100),  # PERSPECTIVE_PROJECTION
    tr.ortho(-8, 8, -8, 8, 0.1, 100)  # ORTOGRAPHIC_PROJECTION
]

# ASSETS = {
#     "bricks": getAssetPath("bricks.jpg"),
#     "baboon": getAssetPath("baboon.png"),
#     "kirby": getAssetPath("kirby.png"),
#     "paine": getAssetPath("torres-del-paine-sq.jpg"),
# }

# WRAP_MODES = [
#     GL_REPEAT,
#     GL_MIRRORED_REPEAT,
#     GL_CLAMP_TO_EDGE,
#     GL_MIRROR_CLAMP_TO_EDGE
# ]

# FILTER_MODES = [
#     GL_NEAREST,
#     GL_LINEAR
# ]


ASSETS = {
    "pochita_obj": getAssetPath("navesita.obj"),
    "pochita_tex": getAssetPath("pochita.png"),
}

class Controller(Window):

    def __init__(self, width, height, title="Pochita :3"):
        super().__init__(width, height, title)
        self.total_time = 0.0


camera = Camera()
controller = Controller(width=WIDTH, height=HEIGHT)
mvpPipeline = sh.SimpleTextureModelViewProjectionShaderProgram() # No puedes usar el mismo pipeline para Nave y Bg

# Setting up the clear screen color
glClearColor(0.1, 0.1, 0.1, 1.0)

glEnable(GL_DEPTH_TEST)

glUseProgram(mvpPipeline.shaderProgram)

# Creando fondo
bgShape = createGPUShape(mvpPipeline, createTextureCubeTarea2(1.0,1.0,1.0))
tex_params = [GL_REPEAT, GL_REPEAT, GL_NEAREST, GL_NEAREST]
tex = getAssetPath("bricks.jpg")
bgShape.texture = sh.textureSimpleSetup(tex,*tex_params)
bgNode = sg.SceneGraphNode("background")
bgNode.childs += [bgShape]

# Creando nave
navesita = createGPUShape(mvpPipeline,read_OBJ2(getAssetPath("navesita.obj")))
navesita.texture = sh.textureSimpleSetup(getAssetPath("pochita.png"),*[GL_REPEAT, GL_REPEAT, GL_NEAREST, GL_NEAREST])
naveNode = sg.SceneGraphNode("navesita")
naveNode.childs += [navesita]

rootNode = sg.SceneGraphNode("root")
rootNode.childs += [bgNode,naveNode]

# What happens when the user presses these keys
@controller.event
def on_key_press(symbol, modifiers):
    if symbol == pyglet.window.key.P:
        camera.set_projection(PERSPECTIVE_PROJECTION)
    if symbol == pyglet.window.key.O:
        camera.set_projection(ORTOGRAPHIC_PROJECTION)
    if symbol == pyglet.window.key.A:
        camera.phi_direction -= 1
    if symbol == pyglet.window.key.D:
        camera.phi_direction += 1
    if symbol == pyglet.window.key.W:
        camera.theta_direction -= 1
    if symbol == pyglet.window.key.S:
        camera.theta_direction += 1
    if symbol == pyglet.window.key.PLUS:
        camera.R_direction -= 1
    if symbol == pyglet.window.key.MINUS:
        camera.R_direction += 1

    elif symbol == pyglet.window.key.ESCAPE:
        controller.close()

# What happens when the user releases these keys
@controller.event
def on_key_release(symbol, modifiers):
    if symbol == pyglet.window.key.A:
        camera.phi_direction += 1
    if symbol == pyglet.window.key.D:
        camera.phi_direction -= 1
    if symbol == pyglet.window.key.W:
        camera.theta_direction += 1
    if symbol == pyglet.window.key.S:
        camera.theta_direction -= 1
    if symbol == pyglet.window.key.PLUS:
        camera.R_direction += 1
    if symbol == pyglet.window.key.MINUS:
        camera.R_direction -= 1

@controller.event
def on_draw():
    controller.clear()

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    camera.update()

    view = tr.lookAt(
        camera.eye,
        camera.at,
        camera.up
    )

    glUniformMatrix4fv(glGetUniformLocation(mvpPipeline.shaderProgram, "model"), 1, GL_TRUE, tr.identity())
    glUniformMatrix4fv(glGetUniformLocation(mvpPipeline.shaderProgram, "projection"), 1, GL_TRUE, camera.projection)
    glUniformMatrix4fv(glGetUniformLocation(mvpPipeline.shaderProgram, "view"), 1, GL_TRUE, view)

    sg.drawSceneGraphNode(naveNode,mvpPipeline,"model")





# Each time update is called, on_draw is called again
# That is why it is better to draw and update each one in a separated function
# We could also create 2 different gpuQuads and different transform for each
# one, but this would use more memory
def update(dt, controller):
    controller.total_time += dt


if __name__ == '__main__':
    # Try to call this function 60 times per second
    pyglet.clock.schedule(update, controller)
    # Set the view
    pyglet.app.run()