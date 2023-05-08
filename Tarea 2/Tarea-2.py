import pyglet
import numpy as np
import grafica_tarea.basic_shapes as bs
import grafica_tarea.scene_graph as sg
import grafica_tarea.easy_shaders as es
import grafica_tarea.performance_monitor as pm
import grafica_tarea.transformations as tr
from grafica_tarea.assets_path import getAssetPath
import random
from grafica_tarea.gpu_shape import createGPUShape
from pyglet.window import Window
from OpenGL.GL import *
import sys
import os.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


ventana = Window(800,600,"Vamos fak",resizable=False)

class Spaceship:
    def __init__(self,x,y,z,n,vx,vy,vz) -> None:
        self.position = (x,y,z,n)

WIDTH, HEIGHT = 800, 800
PROJECTIONS = [
    tr.perspective(60, float(WIDTH)/float(HEIGHT), 0.1, 100),  # PERSPECTIVE_PROJECTION
    tr.ortho(-8, 8, -8, 8, 0.1, 100)  # ORTOGRAPHIC_PROJECTION
]

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

def createStaticScene(pipeline):

    roadBaseShape = createGPUShape(pipeline, bs.createTextureQuad(1.0, 1.0))
    roadBaseShape.texture = es.textureSimpleSetup(
        getAssetPath("Road_001_basecolor.jpg"), GL_REPEAT, GL_REPEAT, GL_LINEAR_MIPMAP_LINEAR, GL_NEAREST)
    glGenerateMipmap(GL_TEXTURE_2D)

    sandBaseShape = createGPUShape(pipeline, createTiledFloor(50))
    sandBaseShape.texture = es.textureSimpleSetup(
        getAssetPath("Sand 002_COLOR.jpg"), GL_REPEAT, GL_REPEAT, GL_LINEAR_MIPMAP_LINEAR, GL_NEAREST)
    glGenerateMipmap(GL_TEXTURE_2D)

    arcShape = createGPUShape(pipeline, createTexturedArc(1.5))
    arcShape.texture = roadBaseShape.texture
    
    roadBaseNode = sg.SceneGraphNode('plane')
    roadBaseNode.transform = tr.rotationX(-np.pi/2)
    roadBaseNode.childs += [roadBaseShape]

    arcNode = sg.SceneGraphNode('arc')
    arcNode.childs += [arcShape]

    sandNode = sg.SceneGraphNode('sand')
    sandNode.transform = tr.translate(0.0,-0.1,0.0)
    sandNode.childs += [sandBaseShape]

    linearSector = sg.SceneGraphNode('linearSector')
        
    for i in range(10):
        node = sg.SceneGraphNode('road'+str(i)+'_ls')
        node.transform = tr.translate(0.0,0.0,-1.0*i)
        node.childs += [roadBaseNode]
        linearSector.childs += [node]

    linearSectorLeft = sg.SceneGraphNode('lsLeft')
    linearSectorLeft.transform = tr.translate(-2.0, 0.0, 5.0)
    linearSectorLeft.childs += [linearSector]

    linearSectorRight = sg.SceneGraphNode('lsRight')
    linearSectorRight.transform = tr.translate(2.0, 0.0, 5.0)
    linearSectorRight.childs += [linearSector]

    arcTop = sg.SceneGraphNode('arcTop')
    arcTop.transform = tr.translate(0.0,0.0,-4.5)
    arcTop.childs += [arcNode]

    arcBottom = sg.SceneGraphNode('arcBottom')
    arcBottom.transform = tr.matmul([tr.translate(0.0,0.0,5.5), tr.rotationY(np.pi)])
    arcBottom.childs += [arcNode]
    
    scene = sg.SceneGraphNode('system')
    scene.childs += [linearSectorLeft]
    scene.childs += [linearSectorRight]
    scene.childs += [arcTop]
    scene.childs += [arcBottom]
    scene.childs += [sandNode]
    
    return scene

def createCar(pipeline, r, g, b):

    # Creating shapes on GPU memory
    blackCube = bs.createColorCube(0,0,0)
    gpuBlackCube = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuBlackCube)
    gpuBlackCube.fillBuffers(blackCube.vertices, blackCube.indices, GL_STATIC_DRAW)

    chasisCube = bs.createColorCube(r,g,b)
    gpuChasisCube = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuChasisCube)
    gpuChasisCube.fillBuffers(chasisCube.vertices, chasisCube.indices, GL_STATIC_DRAW)
    
    # Cheating a single wheel
    wheel = sg.SceneGraphNode("wheel")
    wheel.transform = tr.scale(0.2, 0.8, 0.2)
    wheel.childs += [gpuBlackCube]

    wheelRotation = sg.SceneGraphNode("wheelRotation")
    wheelRotation.childs += [wheel]

    # Instanciating 2 wheels, for the front and back parts
    frontWheel = sg.SceneGraphNode("frontWheel")
    frontWheel.transform = tr.translate(0.3,0,-0.3)
    frontWheel.childs += [wheelRotation]

    backWheel = sg.SceneGraphNode("backWheel")
    backWheel.transform = tr.translate(-0.3,0,-0.3)
    backWheel.childs += [wheelRotation]
    
    # Creating the chasis of the car
    chasis = sg.SceneGraphNode("chasis")
    chasis.transform = tr.scale(1,0.7,0.5)
    chasis.childs += [gpuChasisCube]

    # All pieces together
    car = sg.SceneGraphNode("car")
    car.childs += [chasis]
    car.childs += [frontWheel]
    car.childs += [backWheel]

    return car

@ventana.event
def on_draw():
    ventana.clear()
    glClearColor(0.60, 0.85, 0.85, 1.0)

pyglet.app.run()