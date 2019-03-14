import arcade

class Collectibles(arcade.AnimatedTimeSprite):
    def __init__(self):
        super().__init__()

        self.current_texture = 0
        self.duration = 100
        
        self.textures = []

    def update(self):
        self.duration -= 1