import arcade
from gameVariables import SPEAR
from constants import SPEAR_SPEED, SPEAR_SCALE
import math

class Spear(arcade.Sprite):
    def __init__(self, mirrored):
        super().__init__()

        self.texture = arcade.load_texture(SPEAR, mirrored=mirrored, scale=SPEAR_SCALE)
        self.mirrored = mirrored
        if self.mirrored:
            self.angle = -10
        else:
            self.angle = 10

        self.flat = False

        self.angle_change = 0.01

    def update(self):
        self.center_x += self.change_x * SPEAR_SPEED * 1.2
        self.center_y += self.change_y * SPEAR_SPEED/3


        if self.mirrored:
            self.angle += math.sin(self.angle_change)
        else:
            self.angle -= math.sin(self.angle_change)

        ## move spear in a curve direction
        if self.angle < 1 and not self.mirrored and not self.flat:
            self.change_y = -self.change_y
            # self.angle_change = math.pi
            self.flat = True
        elif self.angle > 0 and self.mirrored and not self.flat:
            self.change_y = -self.change_y
            # self.angle_change = math.pi
            self.flat = True

        if not self.flat:
            self.angle_change += 0.01
        else:
            self.angle_change -= 0.001
