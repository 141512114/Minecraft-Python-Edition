from ursina import *
from voxel import *

class Player(Entity):
    def __init__(self, position = (0, 0, 0), gravity = 9.8, block_tex = None):
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

        # Round both direction vectors to whole numbers (ints) => works better in this voxel game
        forward_dir_ch = Vec3(round_to_closest(forward_dir.x, step = 1), 0, round_to_closest(forward_dir.z, step = 1))
        sides_dir_ch = Vec3(round_to_closest(sides_dir.x, step = 1), 0, round_to_closest(sides_dir.z, step = 1))

        # Create collision rays
        forward_ray = raycast(self_origin_pos, forward_dir_ch, distance = 1, ignore = ignore_list)
        sides_ray = raycast(self_origin_pos, sides_dir_ch, distance = 1, ignore = ignore_list)

        down_ray = boxcast(self_origin_pos, self.down, distance = 1, thickness = (e_col.scale_x, e_col.scale_y), ignore = ignore_list)
        up_ray = boxcast(camera.position, self.up, distance = 1, thickness = (e_col.scale_x, e_col.scale_y), ignore = ignore_list)

        forward_cam_ray = raycast(camera.position, forward_dir_ch, distance = 1, ignore = ignore_list)
        sides_cam_ray = raycast(camera.position, sides_dir_ch, distance = 1, ignore = ignore_list)

        # If 'Space' is pressed, set self.jumping to true
        if (held_keys['space'] and self.grounded):
            self.jumping = True

        # Check if the players collider box intersects with any other collider box
        if (not e_col.intersects().hit):
            if (not down_ray.hit):
                self.grounded = False
        else:
            # Save the entity list and walk through one by one
            col_entity_list = e_col.intersects().entities
            for i in range(len(col_entity_list)):
                col_entity_pos = col_entity_list[i].position

                # If it's inside the players y-range (so on the same layer as his collider box)
                if (col_entity_pos.y > e_col.position.y and col_entity_pos.y <= camera.position.y):
                    # Check if the player hits any collider block on it's forward direction
                    if (forward_ray.hit and forward_ray.entity == col_entity_list[i]) or (forward_cam_ray.hit and forward_cam_ray.entity == col_entity_list[i]):
                        forward_dir = self.forward * 0

                    # Check if the player hits any collider block on it's right direction
                    if (sides_ray.hit and sides_ray.entity == col_entity_list[i]) or (sides_cam_ray.hit and sides_cam_ray.entity == col_entity_list[i]):
                        sides_dir = self.right * 0

                # Check if the player is colliding with something above him
                if (up_ray.hit and up_ray.entity == col_entity_list[i]):
                    self.jump_speed = 0
                    self.jumping = False
                    self.grounded = False

                # Check if the player is colliding with something beneath him => if he does, grounded = True
                if (down_ray.hit and down_ray.entity == col_entity_list[i] and not self.jumping):
                    self.jump_speed = 0
                    self.fall_speed = 0
                    self.grounded = True

        # Apply gravity if we're not jumping and not grounded
        if (not self.grounded and not self.jumping):
            self.fall_speed += self.fall_acc * time.dt
            self.fall_speed = clamp(self.fall_speed, 0, self.gravity)
            self.position = Vec3(self.position.x, self.position.y - self.fall_speed, self.position.z)

        # If the player state 'jumping' is True, manipulate the y-position of the player
        if (self.jumping):
            self.jump_speed += self.jump_acc * time.dt
            self.jump_speed = clamp(self.jump_speed, 0, self.jump_height)

            self.position = Vec3(self.position.x, self.position.y + self.jump_speed, self.position.z)

            if (self.jump_speed >= self.jump_height):
                self.jumping = False

        # Add both directions together and normalize them so we can use the new vector for the players movement direction
        direction = Vec3(forward_dir + sides_dir).normalized()
        self.position += direction * self.move_speed * time.dt
        self.e_col.position = self.position

        # Position the camera where the players head should be
        camera.position = Vec3(self.position.x, (self.position.y - self.origin_y)  + self.player_height, self.position.z)

    def input(self, key):
        global grass_tex

        # Check if anything is in the players hit range
        if (self.hit_range_ray.hit):
            col_entity = self.hit_range_ray.entity
            # If it's of the type 'Voxel'
            if (col_entity.type == 'Voxel'):
                if (key == 'left mouse down'):
                    col_entity.remove_durab()
                elif (key == 'right mouse down'):
                    voxels.append(Voxel(position = col_entity.position + mouse.collisions[1].normal, texture = self.block_tex))