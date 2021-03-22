# Libraries
from ursina import *
from ursina.color import rgba
from ursina.prefabs.sky import Sky

# Local files
from player import Player
from chunk import Chunk

# Create application class
app = Ursina()

# Import textures
tex_array = [
    load_texture('assets/textures/grass_block.png'),
    load_texture('assets/textures/dirt_block.png'),
    load_texture('assets/textures/cobble_block.png'),
    load_texture('assets/textures/sand_block.png')
]

# Set settings for the window
window.title = "Minecraft: Python Edition"
window.vsync = False
window.show_ursina_splash = True
window.borderless = False
window.exit_button.enabled = False
window.fps_counter.enabled = False
window.center_on_screen()

# Create the chunks
chunks = []

chunk_amount = 1
for ch_x in range(chunk_amount):
    for ch_z in range(chunk_amount):
        chunks.append(Chunk(position = (ch_x, 0, ch_z), texture = tex_array[0], tex_arr = tex_array))

# Create the player
player = Player(block_tex = tex_array)

# Info
text = Text(
    text = 'Switch blocks with left and right arrow keys\nLook around by moving your mouse\nMove the player with WASD\nGo up with Space and down with Shift\n\nLeave by clicking Escape',
    position = (-.86, .47)
)
text.create_background(padding = .1, radius = 0)
    
def update():
    # Close game window
    if (held_keys['escape']):
        application.quit()

Sky()
base.set_frame_rate_meter(True)

# Run app
app.run()