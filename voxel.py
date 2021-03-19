from ursina import *
from ursina.mesh_importer import obj_to_ursinamesh, ursina_mesh_to_obj
from ursina.scripts.project_uvs import project_uvs

voxels = []

class Voxel(Entity):
    def __init__(self, position = (0, 0, 0), durab = 2, texture = 'white_cube'):
        super().__init__(
            parent = scene,
            model = 'assets/models/voxel',
            position = position,
            texture = texture,
            color = color.white,
            collider = 'box',
            collision = True,
            origin_y = 0
        )

        self.durab = durab

    def remove_durab(self):
        self.durab -= 1
        if (self.durab <= 0):
            destroy(self)