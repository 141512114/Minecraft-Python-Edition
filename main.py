from ursina import *

from ursina.mesh_importer import obj_to_ursinamesh

from player import Player
from chunk import Chunk
from voxel import *

# Default settings / variables for the application (Initialization)
gravity = 9.8

# Create application class
app = Ursina()

# Import textures
grass_tex = load_texture('assets/textures/grass_block.png')

# Create mesh from the .obj file named voxel
voxel_mesh = obj_to_ursinamesh(name = 'voxel', path = application.asset_folder / 'assets/models')

# Set settings for the window
window.title = "Minecraft: Python Edition"
# window.show_ursina_splash = True
window.borderless = False
window.exit_button.enabled = False
window.fps_counter.enabled = True
window.center_on_screen()

# Create the player
player = Player(gravity = gravity, block_tex = grass_tex)

# Create chunk
chunk = Chunk(voxel_mesh = voxel_mesh, texture = grass_tex)
    
def update():
    # Close game window
    if (held_keys['escape']):
        application.quit()

# Run app
app.run()