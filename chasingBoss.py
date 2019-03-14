import arcade
import random
import math
from gameVariables import DRAGONS
import enemy
from constants import DRAGON_SCALE, DRAGON_SPEED

class Chaser(enemy.Enemy):
    def __init__(self):
        super().__init__()
        
        self.mirrored = False
        self.speed = DRAGON_SPEED
        self.change_x = self.speed
        self.change_y = self.speed
        self.total_hp = 100
        self.lastDirection = 'r'

        for i in range(len(DRAGONS)):
            self.textures.append(arcade.load_texture(DRAGONS[i], scale=DRAGON_SCALE, mirrored=self.mirrored))




    def chase(self, player_sprite):
        # Random 1 in 100 chance that we'll change from our old direction and
        # then re-aim toward the player
        if random.randrange(20) == 0:
            start_x = self.center_x
            start_y = self.center_y

            # Get the destination location for the bullet
            dest_x = player_sprite.center_x
            dest_y = player_sprite.center_y

            # Do math to calculate how to get the bullet to the destination.
            # Calculation the angle in radians between the start points
            # and end points. This is the angle the bullet will travel.
            x_diff = dest_x - start_x
            y_diff = dest_y - start_y
            angle = math.atan2(y_diff, x_diff)

            # Taking into account the angle, calculate our change_x
            # and change_y. Velocity is how fast the bullet travels.
            self.change_x = math.cos(angle) * self.speed
            self.change_y = math.sin(angle) * self.speed

    def changeDir(self):
        self.textures = []
        for i in range(len(DRAGONS)):
                self.textures.append(arcade.load_texture(DRAGONS[i], 
                scale=DRAGON_SCALE, mirrored=self.mirrored)) 

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y
        if self.change_x < 0 and self.lastDirection == 'r':
            self.mirrored = True
            self.lastDirection = 'l'
            self.changeDir()
        elif self.change_x > 0 and self.lastDirection == 'l':
            self.mirrored = False
            self.lastDirection = 'r'
            self.changeDir()