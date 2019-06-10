import arcade
from constants import HP_BAR_HEIGHT, HP_BAR_WIDTH, PLAYER_DAMAGE

class Enemy(arcade.AnimatedTimeSprite):
    def __init__(self):
        super().__init__()
        self.textures = []
        self.total_hp = 20
        self.damage_taken = 0
        self.speed = 10

        self.hp_bar_color = arcade.color.RED_DEVIL
        self.hp_bar_outline_color = arcade.color.BLUE

        self.hp_bar_width = HP_BAR_WIDTH
        self.hp_bar_height = HP_BAR_HEIGHT

        self.center_pos = self.center_x
        self.remaining_hp = self.total_hp

        self.rect = arcade.Shape
        self.rect_outline = arcade.Shape



    def increaseSpeed(self, speed):
        self.speed *= speed

    def getDamage(self, dmg):
        self.damage_taken += dmg
        if self.total_hp - self.damage_taken <= 0:
            self.kill()

        return self.total_hp - self.damage_taken



    def update_hp_bar_location(self):
        self.remaining_hp = self.total_hp - self.damage_taken

        ## position hp bar carefully inside the outline, when hp bar shrinks, the center changes
        # if self.remaining_hp <= self.total_hp:
        self.center_pos = (self.center_x - HP_BAR_WIDTH / 2) + (HP_BAR_WIDTH * self.remaining_hp / self.total_hp) / 2

        self.rect = arcade.create_rectangle_filled(self.center_pos, self.top + self.height * 0.1,
                                                    (self.remaining_hp / self.total_hp) * self.hp_bar_width,
                                                    self.hp_bar_height,
                                                    self.hp_bar_color, 0)

        # self.rect_outline = arcade.create_rectangle_outline(self.center_x,
        #                                                           self.top + self.height * 0.1,
        #                                                           self.hp_bar_width,
        #                                                           self.hp_bar_height,
        #                                                           self.hp_bar_outline_color, 1, 0)

    def update(self):
        ## change direction on reaching sides of the screen
        if self.left < 0:
            self.change_x *= -1
        elif self.right > 960:
            self.change_x *= -1

        # self.hp_bar_new_center_x = self.center_x
        # self.center_x += 2 * self.change_x
        # self.draw_hp_bar()

