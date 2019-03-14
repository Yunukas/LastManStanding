import arcade
import enemy
from constants import ZOMBIE_SCALE, ZOMBIE_SPEED
from gameVariables import ZOMBIES

class Zombie(enemy.Enemy):
    def __init__(self):
        super().__init__()
        
        self.mirrored = False
        self.speed = ZOMBIE_SPEED
        # self.change_y = ZOMBIE_SPEED
        self.change_x = 1
        for i in range(len(ZOMBIES)):
                self.textures.append(arcade.load_texture(ZOMBIES[i], scale=ZOMBIE_SCALE))

    def changeDir(self):
        self.change_x *= -1
        self.mirrored = not self.mirrored
        self.textures = []
        for i in range(len(ZOMBIES)):
                    self.textures.append(arcade.load_texture(ZOMBIES[i], 
                    scale=ZOMBIE_SCALE, mirrored=self.mirrored))
   

    def update(self):            
        self.center_x += self.change_x * self.speed
