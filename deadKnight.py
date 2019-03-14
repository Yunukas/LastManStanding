import arcade
from gameVariables import KNIGHT_DEAD
from constants import KNIGHT_SCALE
class DeadKnight(arcade.Sprite):
    def __init__(self):
        super().__init__()

        self.texture = arcade.load_texture(KNIGHT_DEAD[0], scale=KNIGHT_SCALE + 0.1)

        self.textures = []
        self.cur_texture_index = 0

        for i in range(len(KNIGHT_DEAD)):
            self.textures.append(arcade.load_texture(KNIGHT_DEAD[i], scale=KNIGHT_SCALE + 0.1))

        self.texture_change_frames = 10
        
    def update(self):
        if self.cur_texture_index < len(KNIGHT_DEAD):
            self.texture = self.textures[self.cur_texture_index]
            self.cur_texture_index += 1