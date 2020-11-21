##!/usr/bin/env python3

import pygame

import constants as c
from scene import Scene
from level_scene import LevelScene
from high_score_table import HighScoreTable
from transition_gui import TransitionGui

class HighScoreScene(Scene):
    # TODO implement this class
    # TODO if time, add "modifier" voting

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for player in self.game.players:
            if player not in [item.name for item in self.game.scoreboard.scores]:
                self.game.scoreboard.add_score(player, 0)

        self.table = HighScoreTable(self.game)
        self.table.pose.x = c.WINDOW_WIDTH * 0.3
        self.age = 0
        self.shade = pygame.Surface(c.WINDOW_SIZE)
        self.shade.fill(c.BLACK)
        self.shade_alpha = 255
        self.scene_over = False
        self.side_gui = TransitionGui(self.game)

    def next_scene(self):
        return LevelScene(self.game)

    def update(self, dt, events):
        self.age += dt
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.scene_over = True
        self.table.update(dt, events)
        self.side_gui.update(dt, events)

        speed = 800
        if self.scene_over:
            self.shade_alpha += speed*dt
        else:
            self.shade_alpha -= speed*dt
        self.shade_alpha = max(0, min(255, self.shade_alpha))

        if self.scene_over and self.shade_alpha == 255:
            self.is_running = False

    def draw(self, surface, offset=(0, 0)):
        surface.fill(c.BLACK)
        self.table.draw(surface, offset)
        self.side_gui.draw(surface, offset)

        if self.shade_alpha > 0:
            self.shade.set_alpha(self.shade_alpha)
            surface.blit(self.shade, (0, 0))
