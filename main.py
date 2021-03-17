from math import cos, sin
from ursina import *
import keyboard

gravity = 13.65

class Player(Entity):
    def __init__(self):
        super().__init__(
            parent = scene,
            model = 'cube',
            position = (0, 1, 0),
            rotation = (0, 0, 0),
            color = color.orange,
            visible_self = False,
            scale_y = 1,
            collider = 'box',
            collision = True,
            origin_y = 0
        )

        # Default variables (Initalization)
        self.player_height = 1.65

        self.move_speed = 2.75
        self.mouse_siv = 33

        self.fall_speed = 0
        self.fall_acc = 8.76
        self.falling = False

        self.jump_height = 11.45
        self.jump_speed = 0
        self.jump_acc = 44
        self.jumping = False

        # Camera settings
        camera.fov = 80
        camera.orthographic = False

        # Position the camera where the players head should be
        camera.position = Vec3(self.x, self.y + self.player_height, self.z)
        camera.rotation = Vec3(0, 0, 0)

        mouse.locked = True
        mouse.visible = True

    def update(self):
        global gravity

        # Rotate camera to where "the player is looking"
        look_roll = camera.rotation.y + mouse.x * self.mouse_siv
        look_pitch = clamp(camera.rotation.x - mouse.y * self.mouse_siv, -89, 89)
        camera.rotation = Vec3(look_pitch, look_roll, 0)
        self.rotation = Vec3(0, camera.rotation.y, 0)

        # Get the direction we're trying to walk in.
        v_move = held_keys['w'] - held_keys['s']
        h_move = held_keys['d'] - held_keys['a']
        self.direction = Vec3(self.forward * v_move + self.right * h_move).normalized()

        self.position += self.direction * self.move_speed * time.dt

        # Check if the player still has a floor beneath him
        if not self.jumping:
            col_floor = raycast(self.position, self.down, ignore = (self,), distance = .1)
            if not col_floor.hit:
                self.falling = True
            else:
                self.jumping = False
                self.jump_speed = 0

                self.falling = False
                self.fall_speed = 0

        # Check if the player is falling and apply gravity if he is
        if (self.falling and not self.jumping):
            self.fall_speed += self.fall_acc * time.dt
            self.fall_speed = clamp(self.fall_speed, 0, gravity)
            self.position = Vec3(self.position.x, self.position.y - self.fall_speed * time.dt, self.position.z)

        if (not self.falling and keyboard.is_pressed('space')):
            self.jumping = True

        if (self.jumping and not self.falling):
            self.jump_speed += self.jump_acc * time.dt
            self.jump_speed = clamp(self.jump_speed, 0, self.jump_height)

            self.position = Vec3(self.position.x, self.position.y + self.jump_speed * time.dt, self.position.z)

            if (self.jump_speed >= self.jump_height):
                self.jumping = False
                self.falling = True

        # Position the camera where the players head should be
        camera.position = Vec3(self.position.x, self.position.y + self.player_height, self.position.z)

    def input(self, key):
        ray_hit = raycast(camera.position, camera.forward, ignore = (self,), distance = 6)
        if (ray_hit.hit):
            col_entity = ray_hit.entity
            if (key == 'left mouse down'):
                if (col_entity.type == 'Voxel'):
                    col_entity.remove_durab()
            elif (key == 'right mouse down'):
                Voxel(position = col_entity.position + mouse.normal)

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
            origin_y = 1
        )

        self.durab = durab

    def remove_durab(self):
        self.durab -= 1
        if (self.durab <= 0):
            destroy(self)

app = Ursina()

window.title = "Minecraft: Python Edition"
window.borderless = False
window.exit_button.enabled = False
window.fps_counter.enabled = True

player = Player()

for i in range(-12, 12):
    for j in range(-12, 12):
        Voxel(position = Vec3(j, 0, i))
    

def update():
    # Close game window
    if (held_keys['escape']):
        application.quit()

app.run()