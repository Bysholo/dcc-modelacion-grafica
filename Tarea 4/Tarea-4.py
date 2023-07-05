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
from navesita import *
from camera import *
from crear_functions import *

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

__author__ = "Vicente Valdebenito"

class Controller(pyglet.window.Window):
    def __init__(self, width, height, title=f"Curvas"):
        super().__init__(width, height, title)
        self.total_time = 0.0
        self.pipeline = sh.SimpleTextureGouraudShaderProgram()


controller = Controller(width=800, height=600)

# Parametros para los objetos y texturas a importar
ASSETS = {
    "navesita_obj": getAssetPath("navesita_new.obj"),
    "pipe_obj": getAssetPath("mario_pipe.obj"),
    "turret_obj": getAssetPath("turret.obj"),
    "ring_obj": getAssetPath("toroide.obj"),
    "mario_pipe_tex": getAssetPath("mario-pipe-skin-square.jpg"),
    "navesita_tex": getAssetPath("pochita.png"),
    "fondoZ_tex": getAssetPath("starry_night.jpg"),
    "fondoY_tex": getAssetPath("mossy_cobblestone.jpg"),
    "blue_tex": getAssetPath("plain_light_blue.jpg"),
    "sky_tex": getAssetPath("sky.jpg"),
    "sphere_obj": getAssetPath("sphere_normals.obj"),
    "sea_tex": getAssetPath("sea.jpg")
}
TEX_PARAMS = [GL_REPEAT, GL_REPEAT, GL_NEAREST, GL_NEAREST]

navesita = Navesita(controller.pipeline)
fondo = crearFondo(controller.pipeline)
piso = crearPiso(controller.pipeline)
obstaculos = crearObstaculos(controller.pipeline)

# Definiendo nodo raiz y agregando elementos de la escena
escena = sg.SceneGraphNode("escena")
escena.childs += [fondo, obstaculos, navesita.node, piso]

glUseProgram(controller.pipeline.shaderProgram)
glClearColor(0.051, 0.059, 0.106, 1.0)
glEnable(GL_DEPTH_TEST)

view = 0

@controller.event
def on_key_press(symbol, modifiers):
    if symbol == pyglet.window.key.C:
        global view
        view = (view + 1) % 2
    if symbol == pyglet.window.key.A:
        navesita.spin = 1
    if symbol == pyglet.window.key.D:
        navesita.spin = -1
    if symbol == pyglet.window.key.W:
        navesita.move = 1
    if symbol == pyglet.window.key.S:
        navesita.move = -1
    elif symbol == pyglet.window.key.ESCAPE:
        controller.close()

@controller.event
def on_key_release(symbol, modifiers):
    if symbol == pyglet.window.key.A:
        navesita.spin = 0
    if symbol == pyglet.window.key.D:
        navesita.spin = 0
    if symbol == pyglet.window.key.W:
        navesita.move = 0
    if symbol == pyglet.window.key.S:
        navesita.move = 0

@controller.event()
def on_mouse_motion(x,y,dx,dy):
    navesita.zRot = y*np.pi/2*(np.power(1/2,7)) - 5*np.pi/4


WIDTH, HEIGHT = 800, 800
PROJECTIONS = [
    tr.perspective(60, float(WIDTH)/float(HEIGHT), 0.1, 1000),  # PERSPECTIVE_PROJECTION
    tr.ortho(-8, 8, -8, 8, 0.1, 1000)  # ORTOGRAPHIC_PROJECTION
]

@controller.event
def on_draw():
    controller.clear()
    navesita.update()

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    views = [
    tr.lookAt(
        np.array([navesita.pos[0]+2,15,15]),
        np.array([navesita.pos[0]+4,0,0]),
        np.array([0,1,0])
    ), tr.lookAt(
        np.array([navesita.pos[0] - 2, navesita.pos[1] + 1, navesita.pos[2]]),
        np.array([navesita.pos[0] + 2, navesita.pos[1] - 1, navesita.pos[2]]),
        np.array([0,1,0])
    )
    ]

    cam = views[view]

    # Setting all uniform shader variables
    
    # White light in all components: ambient, diffuse and specular.
    glUniform3f(glGetUniformLocation(controller.pipeline.shaderProgram, "La"), 4.5, 4.5, 4.5)
    glUniform3f(glGetUniformLocation(controller.pipeline.shaderProgram, "Ld"), 1.5, 1.5, 1.5)
    glUniform3f(glGetUniformLocation(controller.pipeline.shaderProgram, "Ls"), 1.5, 1.5, 1.5)

    # Object is barely visible at only ambient. Bright white for diffuse and specular components.
    glUniform3f(glGetUniformLocation(controller.pipeline.shaderProgram, "Ka"), 0.2, 0.2, 0.2)
    glUniform3f(glGetUniformLocation(controller.pipeline.shaderProgram, "Kd"), 0.9, 0.9, 0.9)
    glUniform3f(glGetUniformLocation(controller.pipeline.shaderProgram, "Ks"), 1.0, 1.0, 1.0)

    # TO DO: Explore different parameter combinations to understand their effect!
    
    glUniform3f(glGetUniformLocation(controller.pipeline.shaderProgram, "lightPosition"), 100, 100, 100)
    glUniform1ui(glGetUniformLocation(controller.pipeline.shaderProgram, "shininess"), 100)

    glUniform1f(glGetUniformLocation(controller.pipeline.shaderProgram, "constantAttenuation"), 0.0001)
    glUniform1f(glGetUniformLocation(controller.pipeline.shaderProgram, "linearAttenuation"), 0.03)
    glUniform1f(glGetUniformLocation(controller.pipeline.shaderProgram, "quadraticAttenuation"), 0.01)

    glUniformMatrix4fv(glGetUniformLocation(controller.pipeline.shaderProgram, "projection"), 1, GL_TRUE, PROJECTIONS[1])
    glUniformMatrix4fv(glGetUniformLocation(controller.pipeline.shaderProgram, "model"), 1, GL_TRUE, tr.identity())
    glUniformMatrix4fv(glGetUniformLocation(controller.pipeline.shaderProgram, "view"), 1, GL_TRUE, cam)

    # transformRed = tr.matmul([
    #     tr.translate(holeCurve[controller.step, 0], holeCurve[controller.step, 1], holeCurve[controller.step, 2])
    # ])
    # glUniformMatrix4fv(glGetUniformLocation(controller.pipeline.shaderProgram, "model"), 1, GL_TRUE, transformRed)
    # controller.pipeline.drawCall(gpuRedCube)
    
    sg.drawSceneGraphNode(escena, controller.pipeline, "model")


# Each time update is called, on_draw is called again
# That is why it is better to draw and update each one in a separated function
# We could also create 2 different gpuQuads and different transform for each
# one, but this would use more memory

def update(dt, controller):
    controller.total_time += dt

pyglet.clock.schedule(update, controller)

controller.set_mouse_visible(False)
pyglet.app.run()