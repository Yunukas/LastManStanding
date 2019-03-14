import arcade
from gameVariables import EXPLOSION

class Explosion(arcade.Sprite):
    def __init__(self):
        super().__init__()

        self.current_texture = 0
        self.texture = arcade.load_texture(EXPLOSION)
    
    def update(self):
        self.current_texture += 1
        if self.current_texture < 10:
            self.texture = arcade.load_texture(EXPLOSION)
        else:
            self.kill()