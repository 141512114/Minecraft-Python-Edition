from ursina import *
from ursina.shaders import basic_lighting_shader

class Voxel(Entity):
    def __init__(self, parent = scene, position = (0, 0, 0), texture = 'white_cube', durab = 1):
        super().__init__(
            parent = parent,
            model = 'assets/models/voxel',
            position = position,
            collider = 'box',
            texture = texture,
            color = color.white,
            shader = basic_lighting_shader
        )

        self.durab = durab

    def remove_durab(self):
        self.durab -= 1
        if (self.durab <= 0):
            destroy(self)