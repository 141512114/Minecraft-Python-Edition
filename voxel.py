from ursina import *

class Voxel(Entity):
    def __init__(self, parent = scene, model = 'cube', position = (0, 0, 0), texture = 'white_cube', durab = 2):
        # Make a copy of our original mesh
        self.tmp_mesh = Mesh(vertices = model.vertices[:], normals = model.normals[:], triangles = model.triangles[:], uvs = model.uvs[:])

        super().__init__(
            parent = parent,
            model = model,
            position = position,
            texture = texture,
            color = color.white
        )

        # Create seperated collider box, so the player can rotate without messing with its collider
        e_col = Entity(
            parent = scene,
            model = 'cube',
            position = position,
            rotation = (0, 0, 0),
            color = color.white,
            visible_self = False,
            origin_y = -1
        )
        collider_size = Vec3(1, 2, 1)
        e_col.collider = BoxCollider(
            e_col,
            center = Vec3(0, -e_col.origin_y + (collider_size.y-1)/2, 0),
            size = collider_size
        )

        self.durab = durab

    def remove_durab(self):
        self.durab -= 1
        if (self.durab <= 0):
            destroy(self)