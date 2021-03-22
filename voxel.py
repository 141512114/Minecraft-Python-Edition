# Libraries
from ursina import *
from ursina.shaders import basic_lighting_shader

class Voxel(Entity):
    def __init__(self, parent = scene, position = (0, 0, 0), texture = 'white_cube', tex_arr = None, durab = 1):
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
        self.tex_arr = tex_arr

        self.delay_tex = 10
        self.countdown = 0
        self.start_count = False

        if (self.tex_arr != None):
            up_col = raycast(self.position, self.up, distance = 1, ignore = (self,))
            down_col = raycast(self.position, self.down, distance = 1, ignore = (self,))

            # Check if any block is above this one
            if (up_col.hit):
                col_entity = up_col.entity
                if (col_entity.type == 'Voxel'):
                    if (col_entity.texture == col_entity.tex_arr[0] or col_entity.texture == col_entity.tex_arr[1]):
                        self.texture = self.tex_arr[1]
            else: # If not and this one is a dirt block, start the countdown which makes it to a grass block
                if (self.texture == self.tex_arr[1]):
                    self.countdown = self.delay_tex
                    self.start_count = True

            # Check if any block is beneath this one
            if (down_col.hit):
                col_entity = down_col.entity
                if (col_entity.type == 'Voxel'):
                    if (col_entity.texture == col_entity.tex_arr[0] or col_entity.texture == col_entity.tex_arr[1]):
                        col_entity.texture = self.tex_arr[1]
                        col_entity.start_count = False
                        col_entity.countdown = 0

    def update(self):
        # Little countdown for dirt block to grow into grass block
        if (self.start_count):
            if (self.countdown > 0):
                self.countdown -= time.dt
            else:
                self.texture = self.tex_arr[0]
                self.start_count = False

    def remove_durab(self):
        self.durab -= 1
        if (self.durab <= 0):
            self.update_tex()
            destroy(self)

    def update_tex(self):
        if (self.tex_arr != None):
            if (self.texture == self.tex_arr[0] or self.texture == self.tex_arr[1]):
                down_col = raycast(self.position, self.down, distance = 1, ignore = (self,))

                # Check if any block is beneath this one and if so, activate it's countdown if it's a dirt block
                if (down_col.hit):
                    col_entity = down_col.entity
                    if (col_entity.type == 'Voxel'):
                        if (col_entity.texture == col_entity.tex_arr[1]):
                            col_entity.countdown = col_entity.delay_tex
                            col_entity.start_count = True