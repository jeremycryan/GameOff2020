##!/usr/bin/env python3

import os

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT
WINDOW_CAPTION = "Launch Party"

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

OPTION_A = "A"
OPTION_B = "B"

TIMER_POSITION = SIDE_PANEL_WIDTH//2, 40

SHIP_SCALE = 0.6

MAX_FPS = 65
TICK_LENGTH = 1/80

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
VERT_LIGHT_GRAY = 235, 235, 235

WORMHOLE_COLORS = [(0, 255, 255), (255, 220, 80), (150, 255, 100), (255, 100, 255)]

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
COMMANDS_LONG = {'t':"Thrust", 'd':"Delay", 'r':"Rotate"}
COMMANDS_MIN = {'t':(0,), 'd':(0,), 'r':(-360,)}
COMMANDS_MAX = {'t':(100,), 'd':(60000,), 'r':(360,)}
THRUST = 2

LOG_PATH = "error_log.txt"
SCORE_SAVE_PATH = "../data"
IMAGE_PATH = "../images"
FONT_PATH = "../fonts"
CONFIG_PATH = "../config"
SOUNDS_PATH = "../sounds"

GRAVITY_CONSTANT = 800

MIN_PLANET_RADIUS = 25
MAX_PLANET_RADIUS = 75
HOME_PLANET_RADIUS = 35
HOME_ANGLE_VARIATION = 20
MIN_SPACING = 60

SHIP_SPAWN_ALTITUDE = 25

MOON = 0
NUGGET = 1

MOON_ACH = 0
MOON_1_NUGGET_ACH = 1
MOON_2_NUGGET_ACH = 2

ALERT_PADDING = {RIGHT:10, LEFT:10, DOWN:10, UP:10}
ALERT_MARGIN = {RIGHT:10, LEFT:10, DOWN:10, UP:10}
ALERT_DURATION = 5
ALERT_ALPHA = 135
ALERT_FADEOUT = 0.25
ALERT_WIDTH = 300
ALERT_NUM = 3
ALERT_BACKGROUND_COLOR = BLACK
ALERT_TEXT_COLOR = WHITE
MAX_ALERT_HEIGHT = WINDOW_HEIGHT*0.65
PAUL_ALERT_LINE_SPACING = 0

SCORE_EXPIRATION = 48

JOKE_MESSAGES = (
    "Help, I'm trapped in a spaceship factory! Please let me out before they send me to the moon...",
    "Beep boop, out of mayonnaise.",
    "On behalf of NeoSpace Enterprises, we apologize for any death or dismemberment.",
    "Press A again, I dare you."
)

HINTS = (
    "When reading your code, the game ignores spaces and semicolons. Feel free to use them to keep organized!",
    "You can type !score to view your current score.",
    "You can type !recolor to re-roll your player color.",
    "Your ship rotation is measured in degrees per second, so you can calculate precise turns with the right timing.",
    "In real life, spacecraft of this size would be impractical.",
    "You only get points for an achievement if you're the first player to score it. Speed is important!",
    "This game was created by plasmastarfish and superduperpacman42 for the 2020 Github Game Off.\nIts source code is at github.com/jeremycryan.",
)

MULT_0_MESSAGES = (
    "You can only score leaderboard points in games with three or more players.\n\nGrab some friends!",
)

MULT_MESSAGES = (
    "The more players in the game, the more points are scored by achievements!\n\nThis game had {num} players.",
)

NO_PLANETS_MOD = "No planets"
DOUBLE_POINTS_MOD = "Double points"         # TODO add visual change
DOUBLE_THRUST_MOD = "Double thrust"
INVERTED_GRAVITY_MOD = "Inverted gravity"   # TODO add visual change
EXTRA_TIME_MOD = "Extra time"
MANY_WORMHOLES_MOD = "Many wormholes"
GIANT_PLANET_MOD = "Giant planets"
SMALL_PLANETS_MOD = "Small planets"
SOLAR_WIND = "Solar wind"
EXPLODING_PLANETS = "Exploding planets"

MODIFICATIONS = (
    NO_PLANETS_MOD,
    DOUBLE_POINTS_MOD,
    DOUBLE_THRUST_MOD,
    INVERTED_GRAVITY_MOD,
    EXTRA_TIME_MOD,
    MANY_WORMHOLES_MOD,
    GIANT_PLANET_MOD,
    SMALL_PLANETS_MOD,
    SOLAR_WIND,
    EXPLODING_PLANETS
)

WIND_STRENGTH = 50
PLANET_EXPLODE_RATE = 60

PARTICIPATION_POINTS = 50

PARTICIPATION = 0
OBJECTIVE = 1
