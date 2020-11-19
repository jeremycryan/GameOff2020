##!/usr/bin/env python3

import pygame

import constants as c
from primitives import GameObject

class Alert(GameObject):
    def __init__(self, game, message, player=None):
        super().__init__(game)
        self.message = message
        self.player = player
        self.age = 0
        self.surface = self.generate_surface()

    def update(self, dt, events):
        self.age += dt

    def generate_surface(self):
        # TODO generate surface for real
        return pygame.Surface((10, 10))

    def get_alpha(self):
        if self.age < c.ALERT_DURATION:
            return 255
        elif self.age < c.ALERT_DURATION + c.ALERT_FADEOUT:
            through = (self.age - c.ALERT_DURATION)/(c.ALERT_FADEOUT)
            return 1  - through
        else:
            return 0

    def draw(self, surface, offset):
        # TODO account for changes in position
        self.surface.set_alpha(self.get_alpha())
        surface.blit(self.surface, (offset))


class AlertManager(GameObject):
    def __init__(self, game):
        super().__init__(game)
        self.font = self.game.small_font
        self.alerts = []
        # TODO draw and update alerts
