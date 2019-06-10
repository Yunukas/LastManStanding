import arcade
from gameVariables import FIRE_BLAST
from constants import FIRE_BLAST_SPEED, FIRE_BLAST_SCALE

class Fire(arcade.AnimatedTimeSprite):
    def __init__(self, mirrored):
        super().__init__()

        self.textures = []

        for i in range(len(FIRE_BLAST)):
            self.textures.append(arcade.load_texture(FIRE_BLAST[i], mirrored=mirrored, scale=FIRE_BLAST_SCALE))


    def update(self):
        self.center_x += self.change_x * FIRE_BLAST_SPEED