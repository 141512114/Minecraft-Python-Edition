from ursina import *

from voxel import Voxel

chunk_size = 12
chunk_height = 2

class Chunk(Entity):
    def __init__(self, voxel_mesh = 'cube', position = (0, 0, 0), texture = 'white_cube'):
        super().__init__()

        # Create as many voxels as the chunk allows to
        calc_chunk_size = int(chunk_size / 2)
        for y in range(-chunk_height, 0):
            for x in range(-calc_chunk_size, calc_chunk_size):
                for z in range(-calc_chunk_size, calc_chunk_size):
                    Voxel(model = voxel_mesh, position = (x + chunk_size * position[0], y, z + chunk_size * position[2]), texture = texture)