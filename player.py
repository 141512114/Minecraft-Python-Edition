from ursina import *
from voxel import *

class Player(Entity):
    def __init__(self, position = (0, 0, 0), gravity = 9.8, block_tex = 'white_cube'):
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

        self.gravity = gravity

        self.fall_speed = 0
        self.fall_acc = .23

        self.jump_height = .21
        self.jump_speed = 0
        self.jump_acc = .865

        self.block_tex = block_tex

        # Player states
        self.grounded = False
        self.jumping = False

        # Create seperated collider box, so the player can rotate without messing with its collider
        self.e_col = Entity(
            parent = scene,
            model = 'cube',
            position = position,
            rotation = (0, 0, 0),
            color = color.white,
            visible_self = False,
            origin_y = -1
        )
        collider_size = Vec3(1, 2, 1)
        self.e_col.collider = BoxCollider(
            self.e_col,
            center = Vec3(0, -self.e_col.origin_y + (collider_size.y-1)/2, 0),
            size = collider_size
        )

        # Create cursor entity
        self.cursor = Entity(
            parent = camera.ui,
            model = 'circle',
            color = color.white,
            scale = .008
        )

        # Camera settings
        camera.fov = 80
        camera.orthographic = False

        # Position the camera where the players head should be
        camera.position = Vec3(self.position.x, (self.position.y - self.origin_y) + self.player_height, self.position.z)
        camera.rotation = self.rotation

        mouse.locked = True
        mouse.visible = False

    def update(self):
        e_col = self.e_col
        ignore_list = [self, e_col]

        self_origin_pos = Vec3(self.position.x, self.position.y - self.origin_y, self.position.z)

        # Rotate camera to where "the player is looking"
        camera.rotation_y += mouse.velocity[0] * self.mouse_siv
        camera.rotation_x -= mouse.velocity[1] * self.mouse_siv
        camera.rotation_x = clamp(camera.rotation_x, -90, 90)
        self.rotation_y = camera.rotation_y

        self.hit_range_ray = raycast(camera.position, camera.forward, distance = 13, ignore = ignore_list)

        # Get the direction we're trying to walk in.
        v_move = held_keys['w'] - held_keys['s']
        h_move = held_keys['d'] - held_keys['a']

        # Get direction vectors (but from the player entity)
        forward_dir = self.forward * v_move
        sides_dir = self.right * h_move

        # Add both directions together and normalize them so we can use the new vector for the players movement direction
        direction = Vec3(forward_dir + sides_dir).normalized()
        self.position += direction * self.move_speed * time.dt
        self.e_col.position = self.position

        # Position the camera where the players head should be
        camera.position = Vec3(self.position.x, (self.position.y - self.origin_y)  + self.player_height, self.position.z)

    def input(self, key):
        # Check if anything is in the players hit range
        if (self.hit_range_ray.hit):
            col_entity = self.hit_range_ray.entity
            # If it's of the type 'Voxel'
            if (col_entity.type == 'Voxel'):
                if (key == 'left mouse down'):
                    col_entity.remove_durab()
                elif (key == 'right mouse down'):
                    Voxel(position = col_entity.position + mouse.collisions[1].normal, texture = self.block_tex, player = self)
                    terrain.combine()