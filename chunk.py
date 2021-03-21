from ursina import *
from ursina.shaders import basic_lighting_shader

from voxel import Voxel

chunk_size = 16
chunk_height = 4

class Chunk(Entity):
    def __init__(self, voxel_mesh = 'cube', position = (0, 0, 0), texture = 'white_cube'):
        super().__init__(
            texture = texture,
            shader = basic_lighting_shader
        )

        vertices = []
        normals = []
        uvs = []

        calc_chunk_size = int(chunk_size / 2)
        for y in range(-chunk_height, 0):
            for x in range(-calc_chunk_size, calc_chunk_size):
                for z in range(-calc_chunk_size, calc_chunk_size):
                    for v in range(len(voxel_mesh.vertices)):
                        current_vert = voxel_mesh.vertices[v]

                        position_coord = Vec3(chunk_size * position[0], 0, chunk_size * position[2])

                        x_pos = current_vert[0] + x + position_coord.x
                        y_pos = current_vert[1] + y + position_coord.y
                        z_pos = current_vert[2] + z + position_coord.z

                        vertices.append(Vec3(x_pos, y_pos, z_pos))
                        normals.append(voxel_mesh.normals[v])
                        uvs.append(voxel_mesh.uvs[v])

        self.model = Mesh(vertices = vertices, normals = normals, uvs = uvs)
        # self.collider = MeshCollider(self, self.model)
        self.clear()