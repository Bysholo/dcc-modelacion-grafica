class Shape:
    def __init__(self, vertices, indices):
        self.vertices = vertices
        self.indices = indices

    def __str__(self):
        return "vertices: " + str(self.vertices) + "\n"\
            "indices: " + str(self.indices)


def createTextureQuad(nx, ny):

    # Defining locations and texture coordinates for each vertex of the shape
    vertices = [
    #   positions        texture
        -0.5, -0.5, 0.0,  0, ny,
         0.5, -0.5, 0.0, nx, ny,
         0.5,  0.5, 0.0, nx, 0,
        -0.5,  0.5, 0.0,  0, 0]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
         0, 1, 2,
         2, 3, 0]

    return Shape(vertices, indices)


def createTextureCube(nx, ny, x_size):

    # Defining locations and texture coordinates for each vertex of the shape
    vertices = [
    #   positions         texture coordinates

    # Z-
        -x_size, -0.5, -0.5, 0, ny,
         x_size, -0.5, -0.5, nx, ny,
         x_size,  0.5, -0.5, nx, 0,
        -x_size,  0.5, -0.5, 0, 0,

    # Y-
        -x_size, -0.5, -0.5, 0, ny,
         x_size, -0.5, -0.5, nx, ny,
         x_size, -0.5,  0.5, nx, 0,
        -x_size, -0.5,  0.5, 0, 0
        ]
    
    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
          0, 1, 2, 2, 3, 0,  # Z+
          7, 6, 5, 5, 4, 7,  # Z-
          8, 9,10,10,11, 8,  # X+
         15,14,13,13,12,15,  # X-
         19,18,17,17,16,19,  # Y+
         20,21,22,22,23,20]  # Y-

    return Shape(vertices, indices)