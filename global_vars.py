import sys
import pygame
from enum import Enum

FILE_HISCORE = "save.bin"

# Timings
FPS: int = 60
FRAME_LENGTH: int = 1000 // FPS

BIRD_SPR_FLAP_INTERVAL = 80

VEL_Y_MAX: float = +8.0
VEL_Y_MIN: float = -8.0

GRAVITY_ACCEL: float = -0.5
FLAP_STRENGTH: float = 15

INPUT_REPEAT_DELAY: int = 500
INPUT_REPEAT_INTERVAL: int = 100

SCREEN_SIZE: (int,int) = (288, 512)
SCREEN_W, SCREEN_H = SCREEN_SIZE

WINDOW_SIZE: (int,int) = (423, 768)
WINDOW_W, WINDOW_H = WINDOW_SIZE

"""
DIM variables are associated with the actual pixel sizes of the elements Do not
confuse these with non-DIM variables, which are associated with number of
blocks on the grid.
"""

INT_MAX: int = sys.maxsize
INT_MIN: int = -sys.maxsize - 1

COLOR_BACKGROUND = pygame.Color("#000000")
# COLOR_FONT = pygame.Color("#e3e3e3")
COLOR_FONT_FG = pygame.Color("#000000")
COLOR_FONT_BG = pygame.Color("#e3e3e3")
COLOR_UI_BG = pygame.Color("#ded696")
DIR_FONT = "./font"

DIR_SPR = "./sprites"
DIR_SPR_BIRD = f"{DIR_SPR}/bird"
DIR_SPR_PIPE = f"{DIR_SPR}/pipe"
DIR_SPR_BG = f"{DIR_SPR}/bg"
DIR_SPR_TEXT = f"{DIR_SPR}/text"

SPR_TEXT_SIZE = (24,36)
TEXT_W, TEXT_H = SPR_TEXT_SIZE

BIRD_SPR_DIM: (int,int) = (34,24)
BIRD_W, BIRD_H = BIRD_SPR_DIM
BIRD_SPR_COUNT: int=4
BIRD_POS_START: (int,int) = (SCREEN_W/3,SCREEN_H/2)

BIRD_INTERPOLATE_MIN_MAX:(int,int) = (-0.75, 0.75)
BIRD_INTERPOLATE_Y_MIN, BIRD_INTERPOLATE_Y_MAX = BIRD_INTERPOLATE_MIN_MAX

PIPE_DIM = (52,320)
PIPE_W, PIPE_H = PIPE_DIM

PIPE_X_START: int=SCREEN_W
PIPE_X_GAP: int=(SCREEN_W/1.75)

PIPE_Y_MIN_MAX = (-250, -75)
PIPE_Y_MIN, PIPE_Y_MAX = PIPE_Y_MIN_MAX
PIPE_Y_GAP_MIN: int=445
PIPE_Y_GAP_MAX: int=450
PIPE_Y_VAR: int=100

PIPE_Y_TOP_START: int=-120
PIPE_Y_BOTTOM_START: int=300

GROUND_POS: (int,int) = (0, 400)
SCROLL_SPEED: int = 2

UI_SCORE_POS: (int,int) = ((SCREEN_W-TEXT_W*8)/2, 75)
UI_GAMEOVER_SIZE: (int,int) = (192,42)
GAMEOVER_W, GAMEOVER_H = UI_GAMEOVER_SIZE
UI_GAMEOVER_POS: (int,int) = ((SCREEN_W-GAMEOVER_W)/2, ((SCREEN_H-GAMEOVER_H)/2)-150)

class PipeColor(Enum):
    RED = 0,
    GREEN = 1,

class PipeDirection(Enum):
    DOWN = 0
    UP = 1

class BgType(Enum):
    DAY = 0
    NIGHT = 1

class BirdColor(Enum):
    BLUE = 0
    RED = 1
    YELLOW = 2

class FontSize(Enum):
    SMALL = 0
    MED = 1
    LARGE = 2

class InputKey(Enum):
    FLAP_KB = pygame.K_SPACE
    FLAP_MOUSE = pygame.BUTTON_LEFT
    PAUSE = pygame.K_p
    QUIT  = pygame.K_ESCAPE

class GameState(Enum):
    PREGAME = 0
    PLAYING = 1
    GAMEOVER = 2
