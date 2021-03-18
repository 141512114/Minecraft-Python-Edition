from ursina import *

voxels = []

class Voxel(Entity):
    def __init__(self, position = (0, 0, 0), durab = 2):
        super().__init__(
            parent = scene,
            model = 'cube',
            position = position,
            texture = 'white_cube',
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