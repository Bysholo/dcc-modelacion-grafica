# coding=utf-8
"""Showing how to handle textures on a square"""

import sys
import os
import pyglet
import numpy as np

import libs.shaders as sh
import libs.transformations as tr

from libs.shapes import rubiksCube, minecraftCube
from libs.gpu_shape import createGPUShape
from libs.assets_path import getAssetPath

from OpenGL.GL import *

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

"""
Controles:

    Cambiar Textura:
        - 1: Rubik
        - 2: Tierra Minecraft
        - 2: Madera Minecraft
        - 2: Hojas Minecraft

    Cambiar Wrap Modes: (Cicla entre 'REPEAT', 'MIRRORED REPEAT',
    'CLAMP TO EDGE' y 'MIRRORED CLAMP TO EDGE' en ese orden.)
        - Z: sWrapMode
        - X: tWrapMode

    Cambiar Filter Modes: (Cicla entre 'NEAREST' y 'LINEAR' en ese orden.)
        - C: minFilterMode
        - V: maxFilterMode

    - WASD: Movimiento de camara

    - '+': Zoom-in
    - '-': Zoom-out

    - R: Reiniciar a los valores por defecto de la textura.
    Valores por defecto:
        - sWrapMode = tWrapMode = GL_REPEAT
        - minFilterMode = maxFilterMode = GL_NEAREST

"""

WIDTH, HEIGHT = 800, 800

PERSPECTIVE_PROJECTION = 0
ORTOGRAPHIC_PROJECTION = 1

PROJECTIONS = [
    tr.perspective(60, float(WIDTH)/float(HEIGHT), 0.1, 100),  # PERSPECTIVE_PROJECTION
    tr.ortho(-8, 8, -8, 8, 0.1, 100)  # ORTOGRAPHIC_PROJECTION
]

class Controller(pyglet.window.Window):

    def __init__(self, width, height, title=f"3D Texture"):
        super().__init__(width, height, title)
        self.total_time = 0.0
        self.pipeline = sh.SimpleTextureModelViewProjectionShaderProgram()

        self.ex_shape = createGPUShape(self.pipeline, rubiksCube())

        self.tex_params = (GL_REPEAT, GL_REPEAT, GL_NEAREST, GL_NEAREST)

        self.ex_shape.texture = sh.textureSimpleSetup(
            getAssetPath("rubik.png"), *self.tex_params
        )

    def change_texture(self, cube, tex):
        self.ex_shape = createGPUShape(self.pipeline, cube)
        self.ex_shape.texture = sh.textureSimpleSetup(
            getAssetPath(tex), *self.tex_params
        )


class Camera:

    def __init__(self, at=np.array([0.0, 0.0, 0.0]), eye=np.array([1.0, 1.0, 1.0]), up=np.array([0.0, 0.0, 1.0])) -> None:
        # View parameters
        self.at = at
        self.eye = eye
        self.up = up

        # Spherical coordinates
        self.R = np.sqrt(np.square(self.eye[0]) + np.square(self.eye[1]) + np.square(self.eye[2]))
        self.theta = np.arccos(self.eye[2]/self.R)
        self.phi = np.arctan(self.eye[1]/self.eye[0])

        # Movement/Rotation speed
        self.phi_speed = 0.1
        self.theta_speed = 0.1
        self.R_speed = 0.1

        # Movement/Rotation direction
        self.phi_direction = 0
        self.theta_direction = 0
        self.R_direction = 0

        # Projections
        self.available_projections = PROJECTIONS
        self.projection = self.available_projections[PERSPECTIVE_PROJECTION]

    def set_projection(self, projection_name):
        self.projection = self.available_projections[projection_name]

    def update(self):
        self.R += self.R_speed * self.R_direction
        self.theta += self.theta_speed * self.theta_direction
        self.phi += self.phi_speed * self.phi_direction

        # Spherical coordinates
        self.eye[0] = self.R * np.sin(self.theta) * np.cos(self.phi)
        self.eye[1] = self.R * np.sin(self.theta) * np.sin(self.phi)
        self.eye[2] = (self.R) * np.cos(self.theta)


camera = Camera()
controller = Controller(width=WIDTH, height=HEIGHT)


# Setting up the clear screen color
glClearColor(0.15, 0.15, 0.15, 1.0)

glEnable(GL_DEPTH_TEST)

glUseProgram(controller.pipeline.shaderProgram)

# What happens when the user presses these keys
@controller.event
def on_key_press(symbol, modifiers):
    if symbol == pyglet.window.key._1:
        controller.change_texture(rubiksCube(), "rubik.png")
    if symbol == pyglet.window.key._2:
        controller.change_texture(minecraftCube(), "minecraft_dirt.png")
    if symbol == pyglet.window.key._3:
        controller.change_texture(minecraftCube(), "minecraft_wood.png")
    if symbol == pyglet.window.key._4:
        controller.change_texture(minecraftCube(), "minecraft_leaves.jpg")

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

    controller.set_caption(f"tex_params: {controller.tex_params}")

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    camera.update()

    view = tr.lookAt(
        camera.eye,
        camera.at,
        camera.up
    )

    glUniformMatrix4fv(glGetUniformLocation(controller.pipeline.shaderProgram, "model"), 1, GL_TRUE, tr.identity())
    glUniformMatrix4fv(glGetUniformLocation(controller.pipeline.shaderProgram, "projection"), 1, GL_TRUE, camera.projection)
    glUniformMatrix4fv(glGetUniformLocation(controller.pipeline.shaderProgram, "view"), 1, GL_TRUE, view)

    controller.pipeline.drawCall(controller.ex_shape)


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
