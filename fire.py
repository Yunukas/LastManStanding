import arcade
from gameVariables import FIRE_BLAST
from constants import FIRE_BLAST_SPEED

class Fire(arcade.AnimatedTimeSprite):
    def __init__(self, scale, mirrored):
        super().__init__(scale=scale)

        self.textures = []

        for i in range(len(FIRE_BLAST)):
            self.textures.append(arcade.load_texture(FIRE_BLAST[i], mirrored=mirrored))

    def update(self):
        self.center_x += self.change_x * FIRE_BLAST_SPEED