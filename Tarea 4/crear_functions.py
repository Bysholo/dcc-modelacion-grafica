import random

import numpy as np
import grafica_tarea.scene_graph as sg
import grafica_tarea.shaders as sh
import grafica_tarea.transformations as tr
import grafica_tarea.shapes as shapes
import grafica_tarea.obj_handler as oh

from grafica_tarea.assets_path import getAssetPath
from grafica_tarea.gpu_shape import createGPUShape
from OpenGL.GL import *
from navesita import *
from camera import *
from crear_functions import *

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

# Funcion para crear Shape de la nave, retornando un SceneGraphNode que la contiene
# Se incluyen además los nodos nave_rot y nave_move para tener estas transformaciones separadas
# de buena manera
def crearNavesita(pipeline):
    naveShape = createGPUShape(pipeline, oh.read_OBJ2(ASSETS["navesita_obj"]))
    naveShape.texture = sh.textureSimpleSetup(ASSETS["navesita_tex"],*TEX_PARAMS)

    shadowShape = createGPUShape(pipeline, oh.read_OBJ2(ASSETS["navesita_obj"]))
    shadowShape.texture = sh.textureSimpleSetup(ASSETS["fondoZ_tex"],*TEX_PARAMS)

    naveShapeNode = sg.SceneGraphNode("nave_shape")
    naveShapeNode.childs += [naveShape]

    shadowShapeNode = sg.SceneGraphNode("shadow_shape")
    shadowShapeNode.childs += [shadowShape]

    naveScaleNode = sg.SceneGraphNode("nave_scale")
    naveScaleNode.transform = tr.matmul([tr.rotationZ(-np.pi/2), tr.uniformScale(0.2)])
    naveScaleNode.childs += [naveShapeNode]

    shadowScaleNode = sg.SceneGraphNode("shadow_scale")
    shadowScaleNode.transform = tr.matmul([tr.rotationZ(-np.pi/2), tr.scale(0.002, 0.2, 0.2)])
    shadowScaleNode.childs += [shadowShapeNode]

    naveMoveNode = sg.SceneGraphNode("nave_move")
    naveMoveNode.childs += [naveScaleNode]

    shadowMoveNode = sg.SceneGraphNode("shadow_move")
    shadowMoveNode.childs += [shadowScaleNode]

    naveScaleNode = sg.SceneGraphNode("nave_scale")
    naveScaleNode.transform = tr.matmul([tr.rotationZ(-np.pi/2),tr.uniformScale(0.2)])
    naveScaleNode.childs += [naveShapeNode]

    naveMoveNode = sg.SceneGraphNode("nave_move")
    naveMoveNode.childs += [naveScaleNode]

    naveNode = sg.SceneGraphNode("nave")
    naveNode.childs += [naveMoveNode, shadowMoveNode]
    
    for i in range(0,3):
        newNave = sg.SceneGraphNode("nave_shape_"+str(i))
        newNave.childs += [naveShape]
        newNavePlace = sg.SceneGraphNode("nave_place_"+str(i))
        newNavePlace.childs += [newNave]
        naveScaleNode.childs += [newNavePlace]

        newShadow = sg.SceneGraphNode("shadow_shape_"+str(i))
        newShadow.childs += [shadowShape]
        newShadowPlace = sg.SceneGraphNode("shadow_place_"+str(i))
        newShadowPlace.childs += [newShadow]
        shadowScaleNode.childs += [newShadowPlace]
    naveScaleNode.childs[1].transform = tr.translate(0,-4,-4)
    naveScaleNode.childs[2].transform = tr.translate(0,-4, 4)
    naveScaleNode.childs[3].transform = tr.translate(0,-8, 0)
    shadowScaleNode.childs[1].transform = tr.translate(0,-4,-4)
    shadowScaleNode.childs[2].transform = tr.translate(0,-4, 4)
    shadowScaleNode.childs[3].transform = tr.translate(0,-8, 0)
    return naveNode

# Funcion para crear la figura que hará de fondo, retornando un SceneGraphNode que la contiene
# La Shape a utilizar es una version modificada de TextureCube, a la que se le borraron
# cuatro caras y se le agregaron las normales para poder usar el shader adecuado
# def crearFondo(pipeline):
#     fondoYShape = createGPUShape(pipeline, shapes.createTextureYQuad(60, 5, 120, 10))
#     fondoYShape.texture = sh.textureSimpleSetup(ASSETS["fondoY_tex"], *TEX_PARAMS)
#     fondoZShape = createGPUShape(pipeline, shapes.createTextureZQuad(60, 5, 120, 10))
#     fondoZShape.texture = sh.textureSimpleSetup(ASSETS["fondoZ_tex"], *TEX_PARAMS)

#     fondoYNode = sg.SceneGraphNode("fondo_y")
#     fondoYNode.childs += [fondoYShape]
#     fondoZNode = sg.SceneGraphNode("fondo_z")
#     fondoZNode.childs += [fondoZShape]
    
#     fondoNode = sg.SceneGraphNode("fondo")
#     fondoNode.childs += [fondoYNode,fondoZNode]
#     fondoNode.transform = tr.translate(-5,0,-5)
#     return fondoNode

def crearFondo(pipeline):
    fondoSahpe = createGPUShape(pipeline, oh.read_OBJ2(ASSETS["sphere_obj"]))
    fondoSahpe.texture = sh.textureSimpleSetup(ASSETS["sky_tex"], *TEX_PARAMS)

    fondoSahpeNode = sg.SceneGraphNode("fondo_shape")
    fondoSahpeNode.childs += [fondoSahpe]
    
    fondoNode = sg.SceneGraphNode("fondo")
    fondoNode.childs += [fondoSahpeNode]
    fondoNode.transform = tr.uniformScale(50)
    return fondoNode

def crearPiso(pipeline):
    pisoShape = createGPUShape(pipeline, shapes.createSizedTextureQuadWithNormal(200, 200, 200))
    pisoShape.texture = sh.textureSimpleSetup(ASSETS["sea_tex"], *TEX_PARAMS)

    pisoShapeNode = sg.SceneGraphNode("piso_shape")
    pisoShapeNode.childs += [pisoShape]
    
    pisoNode = sg.SceneGraphNode("piso")
    pisoNode.childs += [pisoShapeNode]
    pisoNode.transform = tr.translate(0.0, -1.0, 0.0)
    return pisoNode


def crearObstaculos(pipeline):
    obstaculos = sg.SceneGraphNode("obstaculos")

    # Creando e instanciando Tuberias
    pipeShape = createGPUShape(pipeline, oh.read_OBJ2(ASSETS["pipe_obj"]))
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
    turretShape = createGPUShape(pipeline, oh.read_OBJ2(ASSETS["turret_obj"]))
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
    ringShape = createGPUShape(pipeline, oh.read_OBJ2(ASSETS["ring_obj"]))
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

    return obstaculos