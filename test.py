import arcade
import random
import os
from constants import *
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Move with a Sprite Animation Example"

COIN_SCALE = 0.1
COIN_COUNT = 50

MOVEMENT_SPEED = 5

def get_map(filename):
    # Open the file
        map_file = open(filename)

        # Create an empty list of rows that will hold our map
        map_array = []

        # Read in a line from the file
        for line in map_file:

            # Strip the whitespace, and \n at the end
            line = line.strip()

            # This creates a list by splitting line everywhere there is a comma.
            map_row = line.split(",")

            # The list currently has all the numbers stored as text, and we want it
            # as a number. (e.g. We want 1 not "1"). So loop through and convert
            # to an integer.
            for index, item in enumerate(map_row):
                map_row[index] = int(item)

            # Now that we've completed processing the row, add it to our map array.
            map_array.append(map_row)

        # Done, return the map.
        return map_array


class MyGame(arcade.Window):
    """ Main application class. """
    
    def __init__(self, width, height, title):
        """
        Initializer
        """
        super().__init__(width, height, title)

        # Set the working directory (where we expect to find files) to the same
        # directory this .py file is in. You can leave this out of your own
        # code, but it is needed to easily run the examples using "python -m"
        # as mentioned at the top of this program.
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        """ Set up the game and initialize the variables. """

        # Sprite lists
        self.all_sprites_list = None
        self.coin_list = None

        # Set up the player
        self.score = 0
        self.player = None

    def setup(self):
        self.all_sprites_list = arcade.SpriteList()
        # self.coin_list = arcade.SpriteList()

        # Set up the player
        self.score = 0
        self.player = arcade.AnimatedWalkingSprite()

        CHARACTER_SCALE = 1
        self.player.stand_right_textures = []
        self.player.stand_right_textures.append(arcade.load_texture("images/adventurer-idle-00.png",
                                                                    scale=CHARACTER_SCALE))
        self.player.stand_left_textures = []
        self.player.stand_left_textures.append(arcade.load_texture("images/adventurer-idle-00.png",
                                                                   scale=CHARACTER_SCALE, mirrored=True))

        self.player.walk_right_textures = []

        self.player.walk_right_textures.append(arcade.load_texture("images/adventurer-run-00.png",
                                                                   scale=CHARACTER_SCALE))
        self.player.walk_right_textures.append(arcade.load_texture("images/adventurer-run-01.png",
                                                                   scale=CHARACTER_SCALE))
        self.player.walk_right_textures.append(arcade.load_texture("images/adventurer-run-02.png",
                                                                   scale=CHARACTER_SCALE))
        self.player.walk_right_textures.append(arcade.load_texture("images/adventurer-run-03.png",
                                                                   scale=CHARACTER_SCALE))
        self.player.walk_right_textures.append(arcade.load_texture("images/adventurer-run-04.png",
                                                                   scale=CHARACTER_SCALE))
        self.player.walk_right_textures.append(arcade.load_texture("images/adventurer-run-05.png",
                                                                   scale=CHARACTER_SCALE))                                                 

        self.player.walk_left_textures = []
        self.player.walk_left_textures.append(arcade.load_texture("images/adventurer-run-00.png",
                                                                   scale=CHARACTER_SCALE, mirrored=True))
        self.player.walk_left_textures.append(arcade.load_texture("images/adventurer-run-01.png",
                                                                   scale=CHARACTER_SCALE, mirrored=True))
        self.player.walk_left_textures.append(arcade.load_texture("images/adventurer-run-02.png",
                                                                   scale=CHARACTER_SCALE, mirrored=True))
        self.player.walk_left_textures.append(arcade.load_texture("images/adventurer-run-03.png",
                                                                   scale=CHARACTER_SCALE, mirrored=True))
        self.player.walk_left_textures.append(arcade.load_texture("images/adventurer-run-04.png",
                                                                   scale=CHARACTER_SCALE, mirrored=True))
        self.player.walk_left_textures.append(arcade.load_texture("images/adventurer-run-05.png",
                                                                   scale=CHARACTER_SCALE, mirrored=True))  
        
        self.player.texture_change_distance = 10

        self.player.center_x = SCREEN_WIDTH // 2
        self.player.center_y = SCREEN_HEIGHT // 2
        self.player.scale = 2

        self.all_sprites_list.append(self.player)

        # Get a 2D array made of numbers based on the map
        map_array = get_map("maps/lmmap.csv")

        # Now that we've got the map, loop through and create the sprites
        for row_index in range(len(map_array)):
            for column_index in range(len(map_array[row_index])):
                
                item = map_array[row_index][column_index]

                # For this map, the numbers represent:
                # -1 = empty
                # 44 = grass
                
                if item == 44:
                    wall = arcade.Sprite("images/platformer/Tiles/Spring/128x128/Grass.png", SPRITE_SCALING)
        
                if item >= 0:
                    # Calculate where the sprite goes
                    wall.left = column_index * SCALED_TILE_SIZE
                    wall.top = (MAP_HEIGHT - row_index) * SCALED_TILE_SIZE

                    # if row_index == 15:
                    #     wall.bottom = 0

                    # if item == 48:
                    #     bg.top = 150

                    # Add the sprite
                    self.all_sprites_list.append(wall)
                    
        # Create out platformer physics engine with gravity
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player,
                                                             self.all_sprites_list,
                                                             gravity_constant=GRAVITY)

        # Set the background color
        arcade.set_background_color(arcade.color.AMAZON)

        # for i in range(COIN_COUNT):
        #     coin = arcade.AnimatedTimeSprite(scale=0.5)
        #     coin.center_x = random.randrange(SCREEN_WIDTH)
        #     coin.center_y = random.randrange(SCREEN_HEIGHT)

        #     coin.textures = []
        #     coin.textures.append(arcade.load_texture("images/coin01.png", scale=COIN_SCALE))
        #     coin.textures.append(arcade.load_texture("images/coin01.png", scale=COIN_SCALE))
        #     coin.textures.append(arcade.load_texture("images/coin01.png", scale=COIN_SCALE))
        #     coin.textures.append(arcade.load_texture("images/coin01.png", scale=COIN_SCALE))
        #     coin.textures.append(arcade.load_texture("images/coin01.png", scale=COIN_SCALE))
        #     coin.textures.append(arcade.load_texture("images/coin01.png", scale=COIN_SCALE))
        #     coin.cur_texture_index = random.randrange(len(coin.textures))

        #     self.coin_list.append(coin)
        #     self.all_sprites_list.append(coin)

        # Set the background color
        arcade.set_background_color(arcade.color.AMAZON)

    def on_draw(self):
        """
        Render the screen.
        """

        # This command has to happen before we start drawing
        arcade.start_render()

        # Draw all the sprites.
        self.all_sprites_list.draw()

        # Put the text on the screen.
        output = f"Score: {self.score}"
        arcade.draw_text(output, 10, 20, arcade.color.WHITE, 14)

    def on_key_press(self, key, modifiers):
        """
        Called whenever the mouse moves.
        """
        if key == arcade.key.UP:
            # This line below is new. It checks to make sure there is a platform underneath
            # the player. Because you can't jump if there isn't ground beneath your feet.
            if self.physics_engine.can_jump():
                self.player.change_y = JUMP_SPEED
        elif key == arcade.key.LEFT:
            self.player.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player.change_x = MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        """
        Called when the user presses a mouse button.
        """
        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player.change_x = 0

    def update(self, delta_time):
        """ Movement and game logic """
        self.physics_engine.update()
        self.all_sprites_list.update()
        self.all_sprites_list.update_animation()

        # # Generate a list of all sprites that collided with the player.
        # hit_list = arcade.check_for_collision_with_list(self.player, self.coin_list)

        # # Loop through each colliding sprite, remove it, and add to the score.
        # for coin in hit_list:
        #     coin.kill()
        #     self.score += 1


def main():
    """ Main method """
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()