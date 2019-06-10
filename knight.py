import movingChar
from constants import KNIGHT_SCALE, PLAYER_DAMAGE
import arcade
from gameVariables import KNIGHT_IDLE, KNIGHT_RUN

class Knight(movingChar.MovingChar):
    def __init__(self):
        super().__init__()

        self.movementSpeed = 0
        self.jumpSpeed = 0
        self.texture_change_distance = 30
        self.scale = KNIGHT_SCALE
        
        self.dmg = PLAYER_DAMAGE
        
        self.stand_right_textures.append(arcade.load_texture(KNIGHT_IDLE, scale=KNIGHT_SCALE))
   
        self.stand_left_textures.append(arcade.load_texture(KNIGHT_IDLE, scale=KNIGHT_SCALE, mirrored=True))

        for i in range(4):
            self.walk_right_textures.append(arcade.load_texture(KNIGHT_RUN[i], scale=KNIGHT_SCALE))


        for i in range(4):
            self.walk_left_textures.append(arcade.load_texture(KNIGHT_RUN[i], scale=KNIGHT_SCALE, mirrored=True))
    def setSpeed(self, speed):
        self.movementSpeed = speed
    
    def setJumpSpeed(self, jumpSpeed):
        self.jumpSpeed = jumpSpeed
    
    def setTextureChangeDistance(self, tcd):
        self.texture_change_distance = tcd