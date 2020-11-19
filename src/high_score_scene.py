##!/usr/bin/env python3

import pygame

import constants as c
from scene import Scene
from level_scene import LevelScene

class HighScoreScene(Scene):
    # TODO implement this class
    # TODO if time, add "modifier" voting
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def next_scene(self):
        raise NotImplementedError()

    def update(self, dt, events):
        pass

    def draw(self, surface, offset=(0, 0)):
        pass
