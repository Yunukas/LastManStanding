from constants import *
import random
from knight import Knight
from gameState import GameState
from gameVariables import EMPTY_TILE, COIN_COLLECT, WALL, WALL_RIGHT, WALL_LEFT, KNIGHT_ATTACK, \
    GAME_START_SOUND, FIRE_SOUND, GAME_OVER, GAME_OVER_SOUND, LEVEL_1_BACKGROUND, \
    MAIN_MENU_PLAY, MAIN_MENU_CONTROLS, MAIN_MENU_CONTROLS_SHOW, MONSTER_GRAWL, ZOMBIE_DEATH_SOUND, ZOMBIE_LEVEL_UP,\
    POWER_UP, MISSION_COMPLETE
from spear import Spear
from fire import Fire
from explosion import *
import chasingBoss
import sound
import os
from zombie import Zombie
from coin import Coin
from deadKnight import DeadKnight
from deadZombie import DeadZombie
from chest import  Chest
import time

def get_map(filename):
    """
    This function loads an array based on a map stored as a list of
    numbers separated by commas.
    """

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

class MyWindow(arcade.Window):
    """ Main application class. """
    
    def __init__(self):
        """
        Initializer
        """
        # Call the parent class
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT)


        # Set the working directory (where we expect to find files) to the same
        # directory this .py file is in. You can leave this out of your own
        # code, but it is needed to easily run the examples using "python -m"
        # as mentioned at the top of this program.
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)


        # game state
        self.state = GameState.MAIN_MENU
        self.temp_state = GameState.PLAYING
        self.game_end_timer = 120
        # score
        self.score = 0
        self.gold = 0
        # timer
        self.timer = 0

        ## difficulty increase timer
        self.boss_timer = 0
        self.enemy_timer = 0
        # Sprite lists
        self.player_list = None
        self.wall_list = None
        self.invisible_wall_list = None
        self.player = None
        self.enemy_list = None
        self.boss_list = None
        self.bullet_list = None
        self.explosion_list = None
        self.coin_list = None
        self.power_up_list = None
        self.fire_power_up_is_on = False
        self.shooting_fire = False
        self.dead_wizard_list = None

        # Physics engine
        self.physics_engine = None
        
        # Used for scrolling map
        self.view_left = 0
        self.view_bottom = 0

        # last direction of char
        self.lastdirection = 'r'

        self.background = None

        self.main_menu_texture  = arcade.load_texture(MAIN_MENU_PLAY)
        self.main_menu_controls_texture  = arcade.load_texture(MAIN_MENU_CONTROLS)
        self.main_menu_controls_show_texture = arcade.load_texture(MAIN_MENU_CONTROLS_SHOW)

    def draw_main_menu(self):
        """
        Draw "Main menu" across the screen.
        """
        # print("MAIN MENUIUUUU")
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                      SCREEN_WIDTH,
                                      SCREEN_HEIGHT, self.main_menu_texture, 0)

    def draw_main_menu_controls(self):
        """
        Draw "Main menu" across the screen.
        """
        # print("MAIN MENUIUUUU")
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                      SCREEN_WIDTH,
                                      SCREEN_HEIGHT, self.main_menu_controls_texture, 0)
    
    def draw_main_menu_controls_show(self):
        """
        Draw "Main menu" across the screen.
        """

        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                      SCREEN_WIDTH,
                                      SCREEN_HEIGHT, self.main_menu_controls_show_texture, 0)


    def draw_mission_complete(self):
        output = "YOU WIN! CONGRATULATIONS"
        arcade.draw_text(output, SCREEN_WIDTH//5, SCREEN_HEIGHT//1.5, arcade.color.ASPARAGUS, 30)

    def draw_game_over(self):
        """
        Draw "Game Over Screen" across the screen.
        """
        texture = arcade.load_texture(GAME_OVER)
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                      SCREEN_WIDTH,
                                      SCREEN_HEIGHT, texture, 0)
    
    def draw_game(self):
        """
        Draw the game
        """
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,SCREEN_WIDTH, SCREEN_HEIGHT, self.background)

        # Draw all the sprites.
        self.invisible_wall_list.draw()
        self.wall_list.draw()
        self.player_list.draw()
        self.enemy_list.draw()
        self.boss_list.draw()
        self.bullet_list.draw()
        self.explosion_list.draw()
        self.coin_list.draw()
        self.dead_wizard_list.draw()
        self.power_up_list.draw()


        for enemy in self.enemy_list:
            enemy.draw_hp_bar()

        for boss in self.boss_list:
            boss.draw_hp_bar()

        if self.temp_state == GameState.GAME_ENDING:
            if self.game_end_timer != 0:
                self.game_end_timer -= 1
                if self.game_end_timer % 10 == 0:
                    self.dead_wizard_list.update()
            else:
               self.state = GameState.GAME_OVER 

        output = f"Score: {self.score}"
        gold = f"Gold: {self.gold}"
        power = f"POWER: {self.player.dmg}"
        arcade.draw_text(output, 70, 5, arcade.color.WHITE, 14)
        arcade.draw_text(gold, 160, 5, arcade.color.WHITE, 14)
        arcade.draw_text(power, 250, 5, arcade.color.WHITE, 14)

        if self.temp_state == GameState.MISSION_COMPLETE:
            self.draw_mission_complete()


    def createPowerUp(self):
        power_up = Chest()

        height = random.randrange(3)
        horizontal_position = random.randrange(2)

        ## position the collectibles between invisible wall tiles and at proper heights
        if height == 0:
            power_up.bottom = 180

            if horizontal_position == 0:
                power_up.center_x = random.randrange(30, 180)
            else:
                power_up.center_x = random.randrange(760, 920)
        elif height == 1:
            power_up.bottom = 330
            if horizontal_position == 0:
                power_up.center_x = random.randrange(130, 300)
            else:
                power_up.center_x = random.randrange(640, 830)
        else:
            power_up.bottom = 485
            if horizontal_position == 0:
                power_up.center_x = random.randrange(30, 240)
            else:
                power_up.center_x = random.randrange(720, 920)

        self.power_up_list.append(power_up)


    ## create zombies with this function
    def createZombie(self):

        height = random.randrange(3)
        horizontal_position = random.randrange(2)
        new_zombie = Zombie()

        success = False

        while not success:
            ## position the zombies between invisible wall tiles and at proper heights
            if height == 0:
                new_zombie.bottom = 220
                
                if horizontal_position == 0:
                    new_zombie.center_x = random.randrange(30, 180)
                else:
                    new_zombie.center_x = random.randrange(760, 920)
            elif height == 1:
                new_zombie.bottom = 375
                if horizontal_position == 0:
                    new_zombie.center_x = random.randrange(130, 300)
                else:
                    new_zombie.center_x = random.randrange(640, 830)
            else:
                new_zombie.bottom = 527
                if horizontal_position == 0:
                    new_zombie.center_x = random.randrange(30, 240)
                else:
                    new_zombie.center_x = random.randrange(720, 920)

            hit_list = arcade.check_for_collision_with_list(new_zombie, self.enemy_list)

            if len(hit_list) == 0:
                success = True
            else:
                print('collision')


        self.enemy_list.append(new_zombie)

    def setup(self):
        """ Set up the game and initialize the variables. """

        # Sprite lists

        ## Main Char (Knight)
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.invisible_wall_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.explosion_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.dead_wizard_list = arcade.SpriteList()
        self.power_up_list = arcade.SpriteList()

        # set the game states
        self.state = GameState.MAIN_MENU
        self.temp_state = GameState.PLAYING

        # score
        self.score = 0
        self.gold = 0
        # timer
        self.timer = 0

        # booleans for special game conditions
        self.fire_power_up_is_on = False
        self.shooting_fire = False

        # time to show game end screen ( player death animation )
        # before moving to the game over screen
        self.game_end_timer = 120

        ## difficulty increase timer
        self.boss_timer = 0
        self.enemy_timer


        self.player = Knight()
        self.player.center_x = SCREEN_WIDTH // 2
        self.player.center_y = 350
        self.player.setTextureChangeDistance(20)
        self.player.setJumpSpeed = JUMP_SPEED
        self.player.setSpeed = MOVEMENT_SPEED

        self.player_list.append(self.player)


        # set background image
        self.background = arcade.load_texture(LEVEL_1_BACKGROUND)

        ## Enemies ( Boss and zombies )
        self.boss_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()

        boss = chasingBoss.Chaser()
        boss.center_x = 50
        boss.center_y = 500

        self.boss_list.append(boss)
        # Get a 2D array made of numbers based on the map
        map_array = get_map("maps/lmmap1.csv")

        for row_index in range(len(map_array)):
            for column_index in range(len(map_array[row_index])):
                
                item = map_array[row_index][column_index]

                # For this map, the numbers represent:
                # -1 = empty
                # 60 = invisible wall
                
                if item == 60:
                    hidden_wall = arcade.Sprite(EMPTY_TILE, SPRITE_SCALING)

                    hidden_wall.center_x = column_index * SCALED_TILE_SIZE + SCALED_TILE_SIZE/2
                    hidden_wall.center_y = (MAP_HEIGHT - row_index) * SCALED_TILE_SIZE

                    self.invisible_wall_list.append(hidden_wall)

        for row_index in range(len(map_array)):
            for column_index in range(len(map_array[row_index])):
                wall = arcade.Sprite(WALL, SPRITE_SCALING)
                item = map_array[row_index][column_index]

                # For this map, the numbers represent:
                # -1 = empty
                # 65 = wall left corner
                # 66 = wall
                # 67 = wall right corner


                if item == 65:
                    wall = arcade.Sprite(WALL_LEFT, SPRITE_SCALING)

                if item == 66:
                    wall = arcade.Sprite(WALL, SPRITE_SCALING)
                if item == 64:
                    wall = arcade.Sprite(WALL_RIGHT, SPRITE_SCALING)


                # if the item is one of above, add it to the list
                if item > 60:
                    wall.left = column_index * SCALED_TILE_SIZE
                    wall.top = (MAP_HEIGHT - row_index) * SCALED_TILE_SIZE

                    # Add the sprite
                    self.wall_list.append(wall)


        # Now that we've got the map, loop through and create the sprites
        
        for _ in range(ZOMBIE_COUNT):
            self.createZombie()
                    
        # Create out platformer physics engine with gravity
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player,
                                                             self.wall_list,
                                                             gravity_constant=GRAVITY)
        
        

        # Set the background color
        arcade.set_background_color(arcade.color.AMAZON)

        self.view_left = 0
        self.view_bottom = 0



    def on_draw(self):
        """
        Render the screen.
        """

        # This command has to happen before we start drawing
        arcade.start_render()

        if self.state == GameState.MAIN_MENU:
            self.draw_main_menu()
        elif self.state == GameState.MAIN_MENU_CONTROLS:
            self.draw_main_menu_controls()
        elif self.state == GameState.MAIN_MENU_CONTROLS_SHOW:
            self.draw_main_menu_controls_show()
        elif self.state == GameState.GAME_OVER:
            self.draw_game_over()
        elif self.state == GameState.PLAYING:
            self.draw_game()
        

    def on_key_press(self, key, modifiers):
        """
        Called whenever a key is pressed.
        """
        if key == arcade.key.P:
            time.sleep(10)


        if key == arcade.key.ENTER:
            if self.state == GameState.MAIN_MENU:
                gs = sound.Sound(GAME_START_SOUND)
                gs.play()
                self.setup()
                self.state = GameState.PLAYING
            elif self.state == GameState.MAIN_MENU_CONTROLS:
                self.state = GameState.MAIN_MENU_CONTROLS_SHOW
            elif self.state == GameState.GAME_OVER:
                self.setup()
                self.state = GameState.MAIN_MENU
            elif self.state == GameState.MAIN_MENU_CONTROLS_SHOW:
                self.state = GameState.MAIN_MENU_CONTROLS

        if key == arcade.key.DOWN:
            if self.state == GameState.MAIN_MENU:
                self.state = GameState.MAIN_MENU_CONTROLS
            elif self.state == GameState.MAIN_MENU_CONTROLS:
                self.state = GameState.MAIN_MENU

        if key == arcade.key.UP:
            if self.state == GameState.MAIN_MENU:
                self.state = GameState.MAIN_MENU_CONTROLS
            elif self.state == GameState.MAIN_MENU_CONTROLS:
                self.state = GameState.MAIN_MENU
            elif self.state == GameState.PLAYING:
                # This line below is new. It checks to make sure there is a platform underneath
                # the player. Because you can't jump if there isn't ground beneath your feet.
                if self.physics_engine.can_jump():
                    self.player.change_y = JUMP_SPEED

        if key == arcade.key.LEFT:
            if self.state == GameState.PLAYING:
                self.player.change_x = -MOVEMENT_SPEED
                self.lastdirection = 'l'
        if key == arcade.key.RIGHT:
            if self.state == GameState.PLAYING:
                self.player.change_x = MOVEMENT_SPEED
                self.lastdirection = 'r'
        if key == arcade.key.SPACE:
            if self.state == GameState.PLAYING:
                if len(self.bullet_list) < 1:
                    mirrored = False
                    change_x = 1

                    if self.lastdirection == 'l':
                        mirrored = True
                        change_x = -1

                    for i in range(len(KNIGHT_ATTACK)):
                        self.player.texture = arcade.load_texture(KNIGHT_ATTACK[i], scale=0.6, mirrored=mirrored)


                    if not self.shooting_fire:
                        bullet = Spear(mirrored=mirrored)
                        bullet.center_x = self.player.center_x
                        bullet.center_y = self.player.center_y
                        bullet.change_x = change_x
                        bullet.change_y = 1
                        self.bullet_list.append(bullet)
                    else:
                        bullet = Fire(scale=FIRE_BLAST_SCALE, mirrored=mirrored)
                        bullet.center_x = self.player.center_x
                        bullet.center_y = self.player.center_y
                        bullet.change_x = change_x
                        self.bullet_list.append(bullet)

                    sonic = sound.Sound(FIRE_SOUND)
                    sonic.play()

            
    def on_key_release(self, key, modifiers):
        """
        Called when the user presses a keyboard button.
        """
        if self.state == GameState.PLAYING and self.temp_state != GameState.GAME_ENDING:
            if key == arcade.key.LEFT or key == arcade.key.RIGHT:
                self.player.change_x = 0


    def update(self, delta_time):
        if self.state == GameState.PLAYING:
            """ Movement and game logic """
            self.boss_timer += 1
            self.enemy_timer += 1
            for boss in self.boss_list:
                boss.chase(self.player)


            ## create new zombies if they are less than a certain amount
            # if len(self.enemy_list) < 5:
            #     self.timer += 1
            #     if self.timer > 80:
            #         self.timer = 0
            #         self.createZombie()

            self.physics_engine.update()
        
            self.player_list.update_animation()
            self.enemy_list.update_animation()
            self.enemy_list.update()
            self.boss_list.update_animation()
            self.boss_list.update()
            self.bullet_list.update()
            self.bullet_list.update_animation()
            self.explosion_list.update()
            self.coin_list.update_animation()
            self.coin_list.update()
            self.power_up_list.update()
            self.power_up_list.update_animation()

            if self.player.center_x < 20:
                self.player.center_x = 930
            elif self.player.center_x > 940:
                self.player.center_x = 30

            # keep zombies in platforms with the help of invisible walls
            for enemy in self.enemy_list:
                hit_list = arcade.check_for_collision_with_list(enemy, self.invisible_wall_list)
                if enemy.left < 20 or enemy.right > 940:
                    enemy.changeDir()
                
                if len(hit_list) > 0:
                    enemy.changeDir()


            ## check if bullets hit enemies
            for bullet in self.bullet_list:
                if bullet.center_x < 0 or bullet.center_x > 960:
                    bullet.kill()
                hit_list = arcade.check_for_collision_with_list(bullet, self.enemy_list)
                
                if len(hit_list) > 0:
                    self.score += 1
                    bullet.kill()
                    hp = hit_list[0].getDamage(self.player.dmg)

                    # if zombie hp is 0, kill it and play sound
                    if hp <= 0:
                        zombie_dying = DeadZombie()
                        zombie_dying.center_x = hit_list[0].center_x
                        zombie_dying.center_y = hit_list[0].center_y + 20
                        self.explosion_list.append(zombie_dying)
                        zombie_death_sound = sound.Sound(ZOMBIE_DEATH_SOUND)
                        zombie_death_sound.play()

                        ## create a collectible coin
                        new_coin = Coin()
                        new_coin.center_x = hit_list[0].center_x
                        new_coin.center_y = hit_list[0].center_y
                        self.coin_list.append(new_coin)
                        for enemy in hit_list:
                            enemy.kill()
                        
            ## kill zombie corpses after their animation ends
            for item in self.explosion_list:
                if item.countdown_timer <= 0:
                    item.kill()
                
            ## boss only takes damage when other enemies are cleared
            for bullet in self.bullet_list:
                hit_list = arcade.check_for_collision_with_list(bullet, self.boss_list)
                
                if len(hit_list) > 0:
                    if(len(self.enemy_list) == 0):
                        self.boss_list[0].getDamage(self.player.dmg)
                    bullet.kill()

            ## check if player killed the boss
            if len(self.boss_list) == 0 and self.temp_state != GameState.MISSION_COMPLETE:
                mission_complete_sound = sound.Sound(MISSION_COMPLETE)
                mission_complete_sound.play()
                self.temp_state = GameState.MISSION_COMPLETE


            ## release the fire power up which makes player's bullets stronger to kill the boss
            ## this is release when enemies are cleared
            if len(self.enemy_list) == 0 and not self.fire_power_up_is_on :
                self.fire_power_up_is_on = True
                self.createPowerUp()


            ## player picks up power up
            if self.fire_power_up_is_on:
                hit_list = arcade.check_for_collision_with_list(self.player, self.power_up_list)

                if len(hit_list) > 0:
                    self.shooting_fire = True
                    power_up_sound = sound.Sound(POWER_UP)
                    power_up_sound.play()
                    self.player.dmg *= 5
                    self.power_up_list[0].kill()


            ## if boss or zombies touch the player, game is over
            if len(arcade.check_for_collision_with_list(self.player, self.boss_list)) > 0 or \
                len(arcade.check_for_collision_with_list(self.player, self.enemy_list)) > 0:

                if self.temp_state != GameState.GAME_ENDING:
                    dead_wizard  = DeadKnight()
                    dead_wizard.center_x = self.player.center_x
                    dead_wizard.center_y = self.player.center_y
                    self.temp_state = GameState.GAME_ENDING
                    self.dead_wizard_list.append(dead_wizard)
                    game_over_sound = sound.Sound(GAME_OVER_SOUND)
                    game_over_sound.play()
                    
                self.player.kill()

            ## check if player hits a coin
            coin_collect_list = arcade.check_for_collision_with_list(self.player, self.coin_list)
            if len(coin_collect_list) > 0:
                self.gold += 1
                collect_sound = sound.Sound(COIN_COLLECT)
                collect_sound.play()
                coin_collect_list[0].kill()

                if self.gold % 5 == 0:
                    self.player.dmg += 10

            ## check if spears hit walls
            if(len(self.bullet_list) > 0 ):
                hit_list = arcade.check_for_collision_with_list(self.bullet_list[0], self.wall_list)
                if len(hit_list) > 0:
                    self.bullet_list[0].kill()

            ## if game time is up, increase boss power and play a sound
            if self.boss_timer / 60 == 10 and len(self.boss_list) > 0:
                self.boss_list[0].scale *= 1.3
                self.boss_list[0].increaseSpeed(1.2)
                self.boss_list[0].total_hp *= 2

                grawl = sound.Sound(MONSTER_GRAWL)
                grawl.play()
                self.boss_timer = 0

            ## if game time is up, increase zombie power and play a sound
            if self.enemy_timer / 60 == 15 and len(self.enemy_list) > 0:
                for enemy in self.enemy_list:
                    enemy.scale *= 1.2
                    enemy.increaseSpeed(1.2)
                    enemy.total_hp *= 2
                    grawl = sound.Sound(ZOMBIE_LEVEL_UP)
                    grawl.play()
                    self.enemy_timer = 0



def main():
    window = MyWindow()
    window.setup()

    arcade.run()


main()