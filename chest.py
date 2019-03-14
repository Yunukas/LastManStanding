from powerUps import PowerUps
from gameVariables import CHESTS
from constants import CHEST_SCALE
import arcade

class Chest(PowerUps):
    def __init__(self):
        super().__init__()

        self.texture = arcade.load_texture(CHESTS[0])
        for img in CHESTS:
            self.textures.append(arcade.load_texture(img, scale=CHEST_SCALE))


        self.texture_change_frames = 10