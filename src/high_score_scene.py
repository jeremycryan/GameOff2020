##!/usr/bin/env python3

import pygame

import constants as c
from scene import Scene
from level_scene import LevelScene
from high_score_table import HighScoreTable

class HighScoreScene(Scene):
    # TODO implement this class
    # TODO if time, add "modifier" voting

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.table = HighScoreTable(self.game)
        self.age = 0

    def next_scene(self):
        return LevelScene(self.game)

    def update(self, dt, events):
        self.age += dt
        if self.age > 5:
            self.is_running = False
        self.table.update(dt, events)

    def draw(self, surface, offset=(0, 0)):
        surface.fill(c.BLACK)
        self.table.draw(surface, offset)
