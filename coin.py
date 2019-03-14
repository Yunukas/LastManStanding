from collectibles import Collectibles
from gameVariables import COINS
from constants import CHARACTER_SCALE
import arcade

class Coin(Collectibles):
    def __init__(self):
        super().__init__()
        self.texture = arcade.load_texture(COINS[0], scale=CHARACTER_SCALE)
        for i in range(len(COINS)):
            self.textures.append(arcade.load_texture(COINS[i], scale=CHARACTER_SCALE))