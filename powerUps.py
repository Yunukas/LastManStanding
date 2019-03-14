import arcade

class PowerUps(arcade.AnimatedTimeSprite):
    def __init__(self):
        super().__init__()

        self.textures = []

        self.timer = 5000


    def update(self):

        self.timer -= 10

        if self.timer == 0:
            self.kill()