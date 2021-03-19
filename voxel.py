from ursina import *
from ursina.mesh_importer import obj_to_ursinamesh

voxels = []

class Voxel(Entity):
    def __init__(self, position = (0, 0, 0), texture = 'white_cube', durab = 2, player = None):
        # Create mesh from the .obj file named voxel
        self.mesh = obj_to_ursinamesh(name = 'voxel', path = application.asset_folder / 'assets/models')

        # Make a copy of our original mesh
        self.tmp_mesh = Mesh(vertices = self.mesh.vertices[:], normals = self.mesh.normals[:], triangles = self.mesh.triangles[:], uvs = self.mesh.uvs[:])

        super().__init__(
            parent = scene,
            model = self.mesh,
            position = position,
            texture = texture,
            color = color.white,
            collider = 'box',
            collision = True,
            origin_y = 0
        )

        self.durab = durab
        self.e_player = player

        # Create rays which will be used to determine if any face of the voxel is visible or not
        self.ignore_list = [self, self.e_player]
        self.forward_ray = raycast(self.position, self.forward, distance = 1, ignore = self.ignore_list)
        self.back_ray = raycast(self.position, self.back, distance = 1, ignore = self.ignore_list)
        self.right_ray = raycast(self.position, self.right, distance = 1, ignore = self.ignore_list)
        self.left_ray = raycast(self.position, self.left, distance = 1, ignore = self.ignore_list)

        self.up_ray = raycast(self.position, self.up, distance = 1, ignore = self.ignore_list)
        self.down_ray = raycast(self.position, self.down, distance = 1, ignore = self.ignore_list)

        self.update_mesh()

    def update_mesh(self):
        # Check for any collision with another voxel
        self.ray_collision(ray = self.forward_ray, direction = self.forward, tmp_mesh = self.tmp_mesh)
        self.ray_collision(ray = self.back_ray, direction = self.back, tmp_mesh = self.tmp_mesh)
        self.ray_collision(ray = self.right_ray, direction = self.right, tmp_mesh = self.tmp_mesh)
        self.ray_collision(ray = self.left_ray, direction = self.left, tmp_mesh = self.tmp_mesh)

        self.ray_collision(ray = self.up_ray, direction = self.up, tmp_mesh = self.tmp_mesh)
        self.ray_collision(ray = self.down_ray, direction = self.down, tmp_mesh = self.tmp_mesh)

        # Apply changes to our copied mesh and set it to be the new voxel model
        self.model = Mesh(vertices = self.tmp_mesh.vertices[:], normals = self.tmp_mesh.normals[:], triangles = self.tmp_mesh.triangles[:], uvs = self.tmp_mesh.uvs[:])

    def single_face_update(self, direction = (0, 0, 1), tmp_mesh = None):
        if (tmp_mesh != None):
            new_dir = direction * (-1)

            col_face_ray = raycast(self.position, new_dir, distance = 1, ignore = self.ignore_list)
            if (col_face_ray.hit):
                if (col_face_ray.entity.type == 'Voxel'):
                    for i in range(len(tmp_mesh.normals)):
                        array_len_off = len(self.mesh.normals) - len(tmp_mesh.normals)
                        new_off_pos = clamp(i - array_len_off, 0, len(tmp_mesh.normals))

                        if (tmp_mesh.normals[new_off_pos] == new_dir):
                            tmp_mesh.normals.pop(new_off_pos)
                            tmp_mesh.vertices.pop(new_off_pos)
                            tmp_mesh.uvs.pop(new_off_pos)

                # Apply changes to our copied mesh and set it to be the new voxel model
                self.model = Mesh(vertices = tmp_mesh.vertices[:], normals = tmp_mesh.normals[:], triangles = tmp_mesh.triangles[:], uvs = tmp_mesh.uvs[:])

    def ray_collision(self, ray = None, direction = (0, 0, 1), tmp_mesh = None):
        if (ray != None and tmp_mesh != None) and (ray.hit):
            col_entity = ray.entity
            if (col_entity.type == 'Voxel'):
                for i in range(len(tmp_mesh.normals)):
                    array_len_off = len(self.mesh.normals) - len(tmp_mesh.normals)
                    new_off_pos = i - array_len_off

                    if (tmp_mesh.normals[new_off_pos] == direction):
                        tmp_mesh.normals.pop(new_off_pos)
                        tmp_mesh.vertices.pop(new_off_pos)
                        tmp_mesh.uvs.pop(new_off_pos)

                col_entity.single_face_update(direction = direction, tmp_mesh = col_entity.tmp_mesh)

    def remove_durab(self):
        self.durab -= 1
        if (self.durab <= 0):
            destroy(self)