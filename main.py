from ursina import *
from ursina.prefabs.sky import Sky

from player import Player
from chunk import Chunk

# Create application class
app = Ursina()

# Import textures
grass_tex = load_texture('assets/textures/grass_block.png')

# Set settings for the window
window.title = "Minecraft: Python Edition"
window.vsync = False
# window.show_ursina_splash = True
window.borderless = False
window.exit_button.enabled = False
window.fps_counter.enabled = False
window.center_on_screen()

# Create the chunks
chunks = []

chunk_amount = 1
for ch_x in range(chunk_amount):
    for ch_z in range(chunk_amount):
        chunks.append(Chunk(position = (ch_x, 0, ch_z), texture = grass_tex))

# Create the player
player = Player(block_tex = grass_tex)
    
def update():
    # Close game window
    if (held_keys['escape']):
        application.quit()

Sky()
base.set_frame_rate_meter(True)

# Run app
app.run()