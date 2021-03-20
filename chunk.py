from ursina import *

from voxel import Voxel

chunk_size = 16
chunk_height = 8

class Chunk(Entity):
    def __init__(self, voxel_mesh = 'cube', texture = 'white_cube'):
        super().__init__(
            texture = texture
        )

        vertices = []

        calc_chunk_size = int(chunk_size / 2)
        for x in range(-calc_chunk_size, calc_chunk_size):
            for y in range(-calc_chunk_size, calc_chunk_size):
                for z in range(-chunk_height, 0):
                    Voxel(parent = self, model = voxel_mesh, position = Vec3(x, z, y), texture = texture)

        self.combine()
        self.collider = MeshCollider(self, self.model)