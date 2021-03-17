from ursina import *

class Player(Entity):
    def __init__(self, position = (0, 3, 0), gravity = 9.8):
        super().__init__(
            parent = scene,
            model = 'cube',
            position = position,
            rotation = (0, 0, 0),
            color = color.orange,
            visible_self = False,
            scale_y = 1,
            collider = 'box',
            collision = True,
            origin_y = 0
        )

        self.cursor = Entity(
            parent = camera.ui,
            model = 'circle',
            color = color.white,
            scale = .008
        )

        # Default variables (Initalization)
        self.player_height = 1.25

        self.move_speed = 2.75
        self.mouse_siv = 33

        self.gravity = gravity

        self.fall_speed = 0
        self.fall_acc = .23

        self.jump_height = .21
        self.jump_speed = 0
        self.jump_acc = .865

        self.grounded = False
        self.jumping = False

        self.forward_col_ray = None
        self.sides_col_ray = None

        # Camera settings
        camera.fov = 80
        camera.orthographic = False

        # Position the camera where the players head should be
        camera.position = Vec3(self.position.x, self.position.y + self.player_height, self.position.z)
        camera.rotation = self.rotation

        mouse.locked = True
        mouse.visible = False

    def update(self):
        global gravity

        # Rotate camera to where "the player is looking"
        camera.rotation_y += mouse.velocity[0] * self.mouse_siv
        camera.rotation_x -= mouse.velocity[1] * self.mouse_siv
        camera.rotation_x = clamp(camera.rotation_x, -90, 90)
        self.rotation_y = camera.rotation_y

        # Get the direction we're trying to walk in.
        v_move = held_keys['w'] - held_keys['s']
        h_move = held_keys['d'] - held_keys['a']

        # Get direction vectors
        forward_dir = self.forward * v_move
        sides_dir = self.right * h_move

        col_ray_origin = self.world_position
        col_ray_dist = .25

        # Forward ray: check if something blocks the way when walking forward or backward
        self.forward_col_ray = boxcast(col_ray_origin, forward_dir, distance = col_ray_dist, thickness = (1, 1), ignore = (self,))
        if (self.forward_col_ray.hit):
            forward_dir = self.forward * 0

        # Sides ray: check if something blocks the way when walking sideways
        self.sides_col_ray = boxcast(col_ray_origin, sides_dir, distance = col_ray_dist, thickness = (1, 1), ignore = (self,))
        if (self.sides_col_ray.hit):
            sides_dir = self.right * 0

        direction = Vec3(forward_dir + sides_dir).normalized()

        self.position += direction * self.move_speed * time.dt

        # Position the camera where the players head should be
        camera.position = Vec3(self.position.x, self.position.y + self.player_height, self.position.z)

        # Gravity: check if any floor exists and if not, the player falls
        bottom_cast = boxcast(Vec3(self.position.x, self.position.y - (self.scale_y / 2), self.position.z), self.down, distance = .1, thickness = (1, 1), ignore = (self,))
        if not bottom_cast.hit:
            self.grounded = False
        else:
            self.fall_speed = 0
            self.jump_speed = 0
            self.grounded = True

        # Apply gravity if we're not jumping and not grounded
        if not self.grounded and not self.jumping:
            self.fall_speed += self.fall_acc * time.dt
            self.fall_speed = clamp(self.fall_speed, 0, self.gravity)
            self.position = Vec3(self.position.x, self.position.y - self.fall_speed, self.position.z)

        # If 'Space' is pressed, set self.jumping to true
        if (held_keys['space'] and self.grounded):
            self.jumping = True

        if (self.jumping):
            self.jump_speed += self.jump_acc * time.dt
            self.jump_speed = clamp(self.jump_speed, 0, self.jump_height)

            self.position = Vec3(self.position.x, self.position.y + self.jump_speed, self.position.z)

            if (self.jump_speed >= self.jump_height):
                self.jumping = False