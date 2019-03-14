import arcade
from constants import HP_BAR_HEIGHT, HP_BAR_WIDTH, PLAYER_DAMAGE

class Enemy(arcade.AnimatedTimeSprite):
    def __init__(self):
        super().__init__()
        self.textures = []
        self.total_hp = 10
        self.damage_taken = 0
        self.speed = 10

        self.hp_bar_color = arcade.color.RED_DEVIL

        self.hp_bar_width = HP_BAR_WIDTH



    def increaseSpeed(self, speed):
        self.speed *= speed

    def getDamage(self, dmg):
        self.damage_taken += dmg
        if self.total_hp - self.damage_taken <= 0:
            self.kill()

        return self.total_hp - self.damage_taken

    def on_draw(self):
        self.draw_hp_bar()

    def draw_hp_bar(self):
        remaining_hp = self.total_hp - self.damage_taken

        arcade.draw_rectangle_outline(self.center_x, self.top + self.height * 0.1,  HP_BAR_WIDTH, HP_BAR_HEIGHT, arcade.color.BLUE, 2, 0)


        center_pos = self.center_x


        ## position hp bar carefully inside the outline, when hp bar shrinks, the center changes
        if remaining_hp < self.total_hp:
            center_pos = (self.center_x - HP_BAR_WIDTH/2 ) + (HP_BAR_WIDTH * remaining_hp / self.total_hp) / 2



        arcade.draw_rectangle_filled(center_pos, self.top + self.height * 0.1, (remaining_hp/self.total_hp) *  HP_BAR_WIDTH, \
                                     HP_BAR_HEIGHT, self.hp_bar_color, 0)

    def update(self):
        ## change direction on reaching sides of the screen
        if self.left < 0:
            self.change_x *= -1
        elif self.right > 960:
            self.change_x *= -1

        self.hp_bar_new_center_x = self.center_x
        self.center_x += 2 * self.change_x
        self.draw_hp_bar()

