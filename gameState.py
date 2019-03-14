from enum import Enum


class GameState(Enum):
    MAIN_MENU = 0
    MAIN_MENU_CONTROLS = 1
    MAIN_MENU_CONTROLS_SHOW = 2
    PLAYING = 3
    GAME_ENDING = 4
    GAME_OVER = 5
    MISSION_COMPLETE = 6