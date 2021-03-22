# Libraries
from ursina import *

# Local files
from voxel import *

class Player(Entity):
    def __init__(self, position = (0, 0, 0), block_tex = 'white_cube'):
        super().__init__(
            parent = scene,
            model = 'cube',
            position = position,
            rotation = (0, 0, 0),
            color = color.orange,
            visible_self = False,
            origin_y = -1
        )

        # Default variables (Initalization)
        self.player_height = 1.27

        self.move_speed = 3.75
        self.mouse_siv = 33

        self.hit_range_ray = None

        self.block_tex = block_tex
        self.current_slot = 0

        # Create cursor entity
        self.cursor = Entity(
            parent = camera.ui,
            model = 'circle',
            color = color.white,
            scale = .008
        )

        # Create hand with block item
        self.hand = Entity(
            parent = camera,
            position = (.5, -.5, 1),
            rotation = (0, -6, 0),
            model = 'assets/models/voxel',
            texture = self.block_tex[self.current_slot],
            color = color.white,
            scale = .35
        )

        self.animate_hand_ = False
        self.animate_hand_duration = 0

        # Camera settings
        camera.fov = 80
        camera.orthographic = False

        # Position the camera where the players head should be
        camera.position = Vec3(self.position.x, (self.position.y - self.origin_y) + self.player_height, self.position.z)
        camera.rotation = self.rotation

        mouse.locked = True
        mouse.visible = False

    def update(self):
        ignore_list = [self]

        # Rotate camera to where "the player is looking"
        camera.rotation_y += mouse.velocity[0] * self.mouse_siv
        camera.rotation_x -= mouse.velocity[1] * self.mouse_siv
        camera.rotation_x = clamp(camera.rotation_x, -90, 90)
        self.rotation_y = camera.rotation_y

        if (self.animate_hand_):
            if (self.animate_hand_duration < 4):
                self.animate_hand_duration += 75 * time.dt
                self.hand.rotation = Vec3(self.animate_hand_duration * 4, 0, 0)
            else:
                self.hand.rotation = Vec3(0, 0, 0)
                self.animate_hand_duration = 0
                self.animate_hand_ = False

        self.hit_range_ray = raycast(camera.position, camera.forward, distance = 13, ignore = ignore_list)

        # Get the direction we're trying to walk in.
        v_move = held_keys['w'] - held_keys['s']
        h_move = held_keys['d'] - held_keys['a']

        # Get direction vectors (but from the player entity)
        forward_dir = self.forward * v_move
        sides_dir = self.right * h_move

        up_move = held_keys['space'] - held_keys['shift']
        self.position = Vec3(self.position.x, self.position.y + (self.move_speed * time.dt) * up_move, self.position.z)

        # Add both directions together and normalize them so we can use the new vector for the players movement direction
        direction = Vec3(forward_dir + sides_dir).normalized()
        self.position += direction * self.move_speed * time.dt

        # Position the camera where the players head should be
        camera.position = Vec3(self.position.x, (self.position.y - self.origin_y) + self.player_height, self.position.z)

    def input(self, key):
        # Check if anything is in the players hit range
        if (self.hit_range_ray.hit):
            col_entity = self.hit_range_ray.entity
            if (col_entity.type == 'Voxel'):
                if (key == 'left mouse down'): # Remove block
                    col_entity.remove_durab()
                    self.animate_hand()
                elif (key == 'right mouse down'): # Create block
                    Voxel(position = col_entity.position + mouse.normal, texture = self.block_tex[self.current_slot], tex_arr = self.block_tex)
                    self.animate_hand()

        # Basic "slot"-system. Player can switch between different block "types"
        if (key == 'left arrow'):
            if (self.current_slot > 0):
                self.current_slot -= 1
            else:
                self.current_slot = len(self.block_tex)-1

            # Update hand model to fitting texture
            self.hand.texture = self.block_tex[self.current_slot]
        elif (key == 'right arrow'):
            if (self.current_slot < len(self.block_tex)-1):
                self.current_slot += 1
            else:
                self.current_slot = 0

            # Update hand model to fitting texture
            self.hand.texture = self.block_tex[self.current_slot]

    def animate_hand(self):
        self.animate_hand_duration = 0
        self.animate_hand_ = True