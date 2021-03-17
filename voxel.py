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

    def input(self, key):
        # Check if cursor is hovering over voxel and if it's in range
        if (self.hovered and distance(self.position, camera.position) <= 13):
            if (key == 'left mouse down'):
                self.remove_durab()
            elif (key == 'right mouse down'):
                voxels.append(Voxel(position = self.position + mouse.normal))

    def remove_durab(self):
        self.durab -= 1
        if (self.durab <= 0):
            destroy(self)