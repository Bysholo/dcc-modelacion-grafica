from crear_functions import *

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

        self.node = crearNavesita(pipeline)         # Nodo que se agrega al grafo de escena

    def update(self):

        self.pos[0] +=  self.move * self.move_speed * np.cos(self.xRot) * np.cos(self.zRot)
        self.pos[1] +=  self.move * self.move_speed * np.sin(self.zRot)
        self.pos[2] += -self.move * self.move_speed * np.sin(self.xRot) * np.cos(self.zRot)
        self.xRot   +=  self.spin * self.rot_speed

        if self.pos[1] < 0.5:
            self.pos[1] = 0.5
            
            
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

        sg.findNode(self.node,"shadow_move").transform = (
            tr.translate(self.pos[0], -0.1 ,self.pos[2])
        )
        sg.findNode(self.node,"shadow_shape").transform = (
            tr.matmul([tr.rotationX(-self.xRot),tr.rotationZ(self.zRot)])
        )
        for i in range(0,3):
            sg.findNode(self.node,"shadow_shape_"+str(i)).transform = (
            tr.matmul([tr.rotationX(-self.xRot),tr.rotationZ(self.zRot)])
            )