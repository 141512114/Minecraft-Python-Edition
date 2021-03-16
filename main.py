from ursina import *

move_speed = 2

app = Ursina()

window.borderless = False

camera.fov = 80
camera.orthographic = False

class Player(Entity):
    def __init__(self):
        super().__init__(
            parent = scene,
            model = "cube",
            color = color.orange,
            scale_y = 2
        )

    def update(self):
        # Horizontal movement for the player (x axis)
        h_move = held_keys['d'] - held_keys['a']
        if (h_move != 0):
            player.x += h_move * move_speed * time.dt

        # "Vertical" movement for the player (z axis)
        v_move = held_keys['w'] - held_keys['s']
        if (v_move != 0):
            player.z += v_move * move_speed * time.dt

        camera.position = Vec3(player.x, player.y, player.z)

class Voxel(Button):
    def __init__(self):
        super().__init__(
            parent = scene,
            model = "cube",
            texture = "white_cube",
            color = color.white,
            origin_y = 1
        )

player = Player()
cube = Voxel()

def update():
    # Close game window
    if (held_keys['escape']):
        app.quit()

app.run()