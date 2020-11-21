##!/usr/bin/env python3

import os

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT
FULLSCREEN = False

LEVEL_WIDTH = int(WINDOW_WIDTH * 0.8)
LEVEL_HEIGHT = int(WINDOW_HEIGHT * 1.0)

SIDE_PANEL_WIDTH = WINDOW_WIDTH - LEVEL_WIDTH
SIDE_PANEL_HEIGHT = WINDOW_HEIGHT
SIDE_PANEL_SIZE = SIDE_PANEL_WIDTH, SIDE_PANEL_HEIGHT

ACHIEVEMENT_WIDTH = 237
ACHIEVEMENT_POINTS_WIDTH = 70

ACHIEVEMENT_LABEL_WIDTH = SIDE_PANEL_WIDTH
ACHIEVEMENT_LABEL_HEIGHT = 40
ACHIEVEMENT_LABEL_SIZE = ACHIEVEMENT_LABEL_WIDTH, ACHIEVEMENT_LABEL_HEIGHT

SCORE_ROW_PADDING = 15
SCORE_TILE_PADDING = 6
SCORE_ROW_HEIGHT = 45 + SCORE_TILE_PADDING * 2
EMPTY = "Empty"
SCORE_EVEN_COLOR = 140, 180, 220
SCORE_ODD_COLOR = 110, 150, 195
SCORE_TABLE_PADDING = 0
SCORE_TABLE_COLOR = (40, 70, 90)
SCORE_TABLE_WIDTH = int(WINDOW_WIDTH * 0.6)
SCORE_TABLE_HEIGHT = WINDOW_HEIGHT

ALERT_SIDE_PADDING = 20
ALERT_LINE_SPACING = 20
ALERT_BODY_SPACE = 4

TIMER_POSITION = SIDE_PANEL_WIDTH//2, 40

SHIP_SCALE = 0.6

MAX_FPS = 65
TICK_LENGTH = 1/100

BLACK = 0, 0, 0
WHITE = 255, 255, 255
RED = 255, 0, 0
GREEN = 0, 255, 0
BLUE = 0, 0, 255
YELLOW = 255, 255, 0
CYAN = 0, 255, 255
MAGENTA = 255, 0, 255
GRAY = 128, 128, 128
MEDIUM_DARK_GRAY = 80, 80, 80
DARK_GRAY = 50, 46, 57
DARKER_GRAY = 45, 42, 52
LIGHT_GRAY = 192, 192, 192

RIGHT = (1, 0)
UP = (0, -1)
LEFT = (-1, 0)
DOWN = (0, 1)
CENTER = (0, 0)

TEXT_BLIT_WIDTH = 2
TEXT_BLIT_OFFSETS = ((-TEXT_BLIT_WIDTH, 0),
                    (-TEXT_BLIT_WIDTH//2, TEXT_BLIT_WIDTH//2),
                    (0, TEXT_BLIT_WIDTH),
                    (TEXT_BLIT_WIDTH//2, TEXT_BLIT_WIDTH//2),
                    (TEXT_BLIT_WIDTH, 0),
                    (TEXT_BLIT_WIDTH//2, -TEXT_BLIT_WIDTH//2),
                    (0, -TEXT_BLIT_WIDTH),
                    (-TEXT_BLIT_WIDTH//2, -TEXT_BLIT_WIDTH//2))

COMMANDS = {"thrust":'t', "delay":'d', "rotate":'r'}
COMMANDS_MIN = {'t':(0,), 'd':(0,), 'r':(-360,)}
COMMANDS_MAX = {'t':(100,), 'd':(60000,), 'r':(360,)}
THRUST = 2

LOG_PATH = "error_log.txt"
SCORE_SAVE_PATH = "../data"
IMAGE_PATH = "../images"
FONT_PATH = "../fonts"

GRAVITY_CONSTANT = 800

MIN_PLANET_RADIUS = 25
MAX_PLANET_RADIUS = 75
HOME_PLANET_RADIUS = 25
MIN_SPACING = 60

MOON = 0
NUGGET = 1

ALERT_PADDING = {RIGHT:10, LEFT:10, DOWN:10, UP:10}
ALERT_MARGIN = {RIGHT:10, LEFT:10, DOWN:10, UP:10}
ALERT_DURATION = 4
ALERT_ALPHA = 135
ALERT_FADEOUT = 0.25
ALERT_WIDTH = 300
ALERT_NUM = 3
ALERT_BACKGROUND_COLOR = BLACK
ALERT_TEXT_COLOR = WHITE
MAX_ALERT_HEIGHT = WINDOW_HEIGHT*0.65
PAUL_ALERT_LINE_SPACING = 0

JOKE_MESSAGES = (
    "Help, I'm trapped in a spaceship factory! Please let me out before they send me to the moon...",
    "Beep boop, out of mayonnaise.",
    "On behalf of NeoSpace Enterprises, we apologize for any death or dismemberment.",
    "Press A again, I dare you."
)

HINTS = (
    "When reading your code, the game ignores spaces and semicolons. Feel free to use them to keep organized!",
    "You can type !score to view your current score.\n(...or at least we intend to implement it!)",
    "Your ship rotation is measured in degrees per second, so you can calculate precise turns with the right timing.",
    "You only get points for an achievement if you're the first player to score it. Speed is important!",
    "This game was created by plasmastarfish and superduperpacman42 for the 2020 Github Game Off.\nIts source code is at github.com/jeremycryan.",
)

MULT_0_MESSAGES = (
    "You can only score leaderboard points in games with three or more players.\n\nThis game had {num} players.",
)

MULT_MESSAGES = (
    "The more players in the game, the more points are scored by achievements!\n\nThis game had {num} players.",
)
