from ursina import *

from opensimplex import OpenSimplex

from player import Player
from voxel import *

# Default settings / variables for the application (Initialization)
gravity = 9.8

simplexNoise = OpenSimplex()

# Create application class
app = Ursina()

# Set settings for the window
window.title = "Minecraft: Python Edition"
window.borderless = False
window.exit_button.enabled = False
window.fps_counter.enabled = True
window.center_on_screen()

# Create the player
player = Player(gravity = gravity)

# Create the terrain using simplex noise
for i in range(-12, 12):
    for j in range(-12, 12):
        flatNoise = simplexNoise.noise2d(j, i) / 10
        hillyNoise = simplexNoise.noise2d(j, i) * 5

        worldNoise = flatNoise * hillyNoise

        voxels.append(Voxel(position = Vec3(j, worldNoise, i)))
    
def update():
    # Close game window
    if (held_keys['escape']):
        application.quit()

# Run app
app.run()