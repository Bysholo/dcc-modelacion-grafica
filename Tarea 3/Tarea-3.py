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

__author__ = "Vicente Valdebenito"

class Controller(pyglet.window.Window):
    def __init__(self, width, height, title=f"Curvas"):
        super().__init__(width, height, title)
        self.total_time = 0.0
        self.pipeline = sh.SimpleTextureModelViewProjectionShaderProgramOBJ()
        self.step = 1


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
    "blue_tex": getAssetPath("plain_light_blue.jpg")
}
TEX_PARAMS = [GL_REPEAT, GL_REPEAT, GL_NEAREST, GL_NEAREST]


# Funcion para crear Shape de la nave, retornando un SceneGraphNode que la contiene
# Se incluyen además los nodos nave_rot y nave_move para tener estas transformaciones separadas
# de buena manera
def crearNavesita(pipeline):
    naveShape = createGPUShape(pipeline, oh.read_OBJ2(ASSETS["navesita_obj"]))
    naveShape.texture = sh.textureSimpleSetup(ASSETS["navesita_tex"],*TEX_PARAMS)

    naveShapeNode = sg.SceneGraphNode("nave_shape")
    naveShapeNode.childs += [naveShape]

    naveScaleNode = sg.SceneGraphNode("nave_scale")
    naveScaleNode.transform = tr.matmul([tr.rotationZ(-np.pi/2),tr.uniformScale(0.2)])
    naveScaleNode.childs += [naveShapeNode]

    naveMoveNode = sg.SceneGraphNode("nave_move")
    naveMoveNode.childs += [naveScaleNode]

    naveNode = sg.SceneGraphNode("nave")
    naveNode.childs += [naveMoveNode]

    
    for i in range(0,3):
        new_nave_place = sg.SceneGraphNode("nave_place_"+str(i))
        new_nave = sg.SceneGraphNode("nave_shape_"+str(i))
        new_nave.childs += [naveShape]
        new_nave_place.childs += [new_nave]
        naveScaleNode.childs += [new_nave_place]
    naveScaleNode.childs[1].transform = tr.translate(0,-4,-4)
    naveScaleNode.childs[2].transform = tr.translate(0,-4, 4)
    naveScaleNode.childs[3].transform = tr.translate(0,-8, 0)
    return naveNode

# Funcion para crear la figura que hará de fondo, retornando un SceneGraphNode que la contiene
# La Shape a utilizar es una version modificada de TextureCube, a la que se le borraron
# cuatro caras y se le agregaron las normales para poder usar el shader adecuado
def crearFondo(pipeline):
    fondoYShape = createGPUShape(pipeline, shapes.createTextureYQuad(60, 5, 120, 10))
    fondoYShape.texture = sh.textureSimpleSetup(ASSETS["fondoY_tex"], *TEX_PARAMS)
    fondoZShape = createGPUShape(pipeline, shapes.createTextureZQuad(60, 5, 120, 10))
    fondoZShape.texture = sh.textureSimpleSetup(ASSETS["fondoZ_tex"], *TEX_PARAMS)

    fondoYNode = sg.SceneGraphNode("fondo_y")
    fondoYNode.childs += [fondoYShape]
    fondoZNode = sg.SceneGraphNode("fondo_z")
    fondoZNode.childs += [fondoZShape]
    
    fondoNode = sg.SceneGraphNode("fondo")
    fondoNode.childs += [fondoYNode,fondoZNode]
    fondoNode.transform = tr.translate(-5,0,-5)
    return fondoNode

# Se define una clase Navesita para poder guardar los datos de posicion y rotacion.
class Navesita:
    def __init__(self, pipeline):                   # Se entrega un pipeline en el que dibujar el nodo
        self.pos = [0,0,0]
        self.xRot = 0                               # Grado rotacion Y
        self.zRot = 0                               # Grado rotacion Z
        
        self.rot_speed = 0.1*np.pi/2                # Velocidad para rotar en Y
        self.move_speed = 0.15                      # Velocidad para desplazarse en X

        self.spin = 0                               # 0 si no se mueve, 1 si se mueve
        self.move = 0                               # 0 si no esta rotando, 1 si esta rotando
        self.mode = 0
        self.route = np.zeros((3,3))

        self.node = crearNavesita(pipeline)         # Nodo que se agrega al grafo de escena

    def update(self):

        if self.mode == 0:
            self.pos[0] +=  self.move * self.move_speed * np.cos(self.xRot) * np.cos(self.zRot)
            self.pos[1] +=  self.move * self.move_speed * np.sin(self.zRot)
            self.pos[2] += -self.move * self.move_speed * np.sin(self.xRot) * np.cos(self.zRot)
            self.xRot   +=  self.spin * self.rot_speed
            
        else:
            self.pos[0] = self.route[controller.step, 0]
            self.pos[1] = self.route[controller.step, 1]
            self.pos[2] = self.route[controller.step, 2]
            print(self.pos[0], self.pos[1], self.pos[2])

            z2 = self.route[controller.step    , 2]
            z1 = self.route[controller.step - 1, 2]
            x2 = self.route[controller.step    , 0]
            x1 = self.route[controller.step - 1, 0]
            y2 = self.route[controller.step    , 1]
            y1 = self.route[controller.step - 1, 1]

            self.xRot = np.arctan((z2 - z1)/(x2 - x1))
            self.zRot = np.arctan((y2 - y1)/(x2 - x1))
            
        sg.findNode(self.node,"nave_move").transform = (
            tr.translate(self.pos[0],self.pos[1],self.pos[2])
        )
        sg.findNode(self.node,"nave_shape").transform = (
            tr.matmul([tr.rotationX(-self.xRot),tr.rotationZ(self.zRot)])
        )
        for i in range(0,3):
            sg.findNode(self.node,"nave_shape_"+str(i)).transform = (
            tr.matmul([tr.rotationX(-self.xRot),tr.rotationZ(self.zRot)])
            )
        

navesita = Navesita(controller.pipeline)
fondo = crearFondo(controller.pipeline)
obstaculos = sg.SceneGraphNode("obstaculos")

# Creando e instanciando Tuberias
pipeShape = createGPUShape(controller.pipeline, oh.read_OBJ2(ASSETS["pipe_obj"]))
pipeShape.texture = sh.textureSimpleSetup(ASSETS["mario_pipe_tex"],*TEX_PARAMS)
pipeNode = sg.SceneGraphNode("pipe_node")
pipeNode.childs += [pipeShape]

pipe_list = [0]*5
for i in range(0,5):
    pipe_list[i] = sg.SceneGraphNode("pipe_"+str(i))
    pipe_list[i].childs += [pipeNode]
    pipe_list[i].transform = tr.matmul([tr.translate(random.randint(1,10)*10,-1,random.choice([2,-2])),tr.rotationZ(np.pi/4)])
obstaculos.childs += pipe_list

# Creando e instanciando Torretas
turretShape = createGPUShape(controller.pipeline, oh.read_OBJ2(ASSETS["turret_obj"]))
turretShape.texture = sh.textureSimpleSetup(ASSETS["navesita_tex"],*TEX_PARAMS)
turretNode = sg.SceneGraphNode("turret_node")
turretNode.childs += [turretShape]
turretNode.transform = tr.matmul([tr.translate(0,-1,3),tr.rotationY(np.pi),tr.uniformScale(0.2)])

turret_list = [0]*5
for i in range(0,5):
    turret_list[i] = sg.SceneGraphNode("turret_"+str(i))
    turret_list[i].childs += [turretNode]
    turret_list[i].transform = tr.translate(random.randint(1,10)*10,0,random.choice([0,4]))
obstaculos.childs += turret_list

# Creando e instanciando Anillos
ringShape = createGPUShape(controller.pipeline, oh.read_OBJ2(ASSETS["ring_obj"]))
ringShape.texture = sh.textureSimpleSetup(ASSETS["blue_tex"],*TEX_PARAMS)
ringNode = sg.SceneGraphNode("ring_node")
ringNode.childs += [ringShape]
ringNode.transform = tr.matmul([tr.translate(0,2,0),tr.rotationZ(np.pi/2),tr.uniformScale(0.75)])

ring_list = [0]*5
for i in range(0,5):
    ring_list[i] = sg.SceneGraphNode("turret_"+str(i))
    ring_list[i].childs += [ringNode]
    ring_list[i].transform = tr.translate(random.randint(1,10)*10,0,random.choice([0,4]))
obstaculos.childs += ring_list

# Definiendo nodo raiz y agregando elementos de la escena
escena = sg.SceneGraphNode("escena")
escena.childs += [fondo, obstaculos, navesita.node]


glUseProgram(controller.pipeline.shaderProgram)
glClearColor(0.051, 0.059, 0.106, 1.0)
glEnable(GL_DEPTH_TEST)



########################################################
## Tarea 3
########################################################



# Funciones de las curvas
def generateT(t):
    return np.array([[1, t, t**2, t**3]]).T


def hermiteMatrix(P1, P2, T1, T2):

    # Concatenando columnas
    G = np.concatenate((P1, P2, T1, T2), axis=1)

    # Matriz base de Hermite
    Mh = np.array([[1, 0, -3, 2], [0, 0, 3, -2], [0, 1, -2, 1], [0, 0, -1, 1]])

    return np.matmul(G, Mh)


def bezierMatrix(P0, P1, P2, P3):

    # Concatenando columnas
    G = np.concatenate((P0, P1, P2, P3), axis=1)

    # Matriz de base de Bezier
    Mb = np.array([[1, -3, 3, -1], [0, 3, -6, 3], [0, 0, 3, -3], [0, 0, 0, 1]])

    return np.matmul(G, Mb)

def catmullRomMatrix(P0, P1, P2, P3):

    # Concatenando columnas
    G = np.concatenate((P0, P1, P2, P3), axis=1)

    # Matriz de base de Catmull-Rom
    Mcr = np.array([[0, -0.5, 1, -0.5], [1, 0, -2.5, 1.5], [0, 0.5, 2, -1.5], [0, 0, -0.5, 0.5]])

    return np.matmul(G, Mcr)


# M is the cubic curve matrix, N is the number of samples between 0 and 1
def evalCurve(M, N):
    # The parameter t should move between 0 and 1
    ts = np.linspace(0.0, 1.0, N)

    # The computed value in R3 for each sample will be stored here
    curve = np.ndarray(shape=(N, 3), dtype=float)

    for i in range(len(ts)):
        T = generateT(ts[i])
        curve[i, 0:3] = np.matmul(M, T).T

    return curve


N = 1000
Positions = [np.array([[0, 0, 0]]).T]
Tangents = []
Move = tr.identity

def addPoint(n):
    last = Positions[-1]
    return np.array([[last[0,0] + n, last[1,0], last[2,0]]]).T

def interploatedCurve():
    global Positions
    
    if navesita.mode == 1:
        navesita.mode = 0
    else:
        navesita.mode = 1
        controller.step = 0
        if len(Positions) < 4:
            navesita.route = np.zeros((3,3))
        else:
            curves = []
            add1 = addPoint(1)
            add2 = addPoint(2)
            add3 = addPoint(3)
            if len(Positions)%4 == 3:
                Positions += [add1]
            elif len(Positions)%4 == 2:
                Positions += [add1, add2]
            elif len(Positions)%4 == 1:
                Positions += [add1, add2, add3]
            for i in range(0, len(Positions)-4):
                curves.append(
                    evalCurve(catmullRomMatrix(Positions[i], Positions[i+1], Positions[i+2], Positions[i+3]), N)
                )
            navesita.route = np.concatenate(curves)



########################################################
########################################################

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
    if symbol == pyglet.window.key.R:
        global Positions 
        global Tangents
        Positions += [np.array([[navesita.pos[0], navesita.pos[1], navesita.pos[2]]]).T]
        Tangents += [np.array([[navesita.xRot, 0, navesita.zRot]]).T]
        print("Saved position:", navesita.pos[0], navesita.pos[1], navesita.pos[2])
    if symbol == pyglet.window.key.P:
        print(Positions, Tangents)
    if symbol == pyglet.window.key._1:
        interploatedCurve()

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
    tr.perspective(60, float(WIDTH)/float(HEIGHT), 0.1, 100),  # PERSPECTIVE_PROJECTION
    tr.ortho(-8, 8, -8, 8, 0.1, 100)  # ORTOGRAPHIC_PROJECTION
]

@controller.event
def on_draw():
    controller.clear()
    navesita.update()

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # if controller.step >= N-1:
    #     controller.step = 0

    controller.step += 10
    if controller.step >= len(navesita.route[:, 0]):
        controller.step = len(navesita.route[:, 0])-1

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