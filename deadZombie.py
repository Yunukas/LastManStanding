import arcade
from gameVariables import ZOMBIE_BLOOD
from constants import ZOMBIE_SCALE

class DeadZombie(arcade.Sprite):
    def __init__(self):
        super().__init__()

        self.texture = arcade.load_texture(ZOMBIE_BLOOD[0], scale=ZOMBIE_SCALE + 0.2)

        self.textures = []
        self.cur_texture_index = 0

        self.countdown_timer = 180

        for i in range(len(ZOMBIE_BLOOD)):
            self.textures.append(arcade.load_texture(ZOMBIE_BLOOD[i], scale=ZOMBIE_SCALE + 0.2))

    def update(self):
        self.countdown_timer -= 1

        if self.cur_texture_index < len(ZOMBIE_BLOOD):
            if self.countdown_timer > 0:
                self.texture = self.textures[self.cur_texture_index]
                self.cur_texture_index += 1