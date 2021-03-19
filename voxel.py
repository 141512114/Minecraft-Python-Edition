from ursina import *
from ursina.mesh_importer import obj_to_ursinamesh, ursina_mesh_to_obj
from ursina.scripts.project_uvs import project_uvs

voxels = []

class Voxel(Entity):
<<<<<<< HEAD
    def __init__(self, position = (0, 0, 0), texture = None, durab = 2):
        mesh = obj_to_ursinamesh(name = 'voxel', path = application.asset_folder / 'models', outpath = application.compressed_models_folder)
        print(mesh.triangles)
        model = ursina_mesh_to_obj(mesh = mesh)

        super().__init__(
            parent = scene,
            model = model,
            position = position,
            texture = texture,
=======
    def __init__(self, position = (0, 0, 0), durab = 2):
        super().__init__(
            parent = scene,
            model = 'cube',
            position = position,
            texture = 'white_cube',
            color = color.white,
>>>>>>> parent of 8155f5f (Added voxel model and texture)
            collider = 'box',
            collision = True,
            origin_y = 0
        )

        self.durab = durab

    def remove_durab(self):
        self.durab -= 1
        if (self.durab <= 0):
            destroy(self)