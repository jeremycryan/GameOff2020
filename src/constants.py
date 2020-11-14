##!/usr/bin/env python3

import os

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT

MAX_FPS = 60
TICK_LENGTH = 1/100

BLACK = 0, 0, 0
WHITE = 255, 255, 255
RED = 255, 0, 0
GREEN = 0, 255, 0
BLUE = 0, 0, 255
YELLOW = 255, 255, 0
CYAN = 0, 255, 255
MAGENTA = 255, 0, 255

COMMANDS = {"thrust":'t', "delay":'d', "rotate":'r'}
COMMANDS_MIN = {'t':(0,), 'd':(0,), 'r':(-360,)}
COMMANDS_MAX = {'t':(100,), 'd':(60000,), 'r':(360,)}
THRUST = 2

LOG_PATH = "error_log.txt"
SCORE_SAVE_PATH = "../data"

GRAVITY_CONSTANT = 600
