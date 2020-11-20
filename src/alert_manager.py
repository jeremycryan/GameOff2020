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
        self.lines = self.split(message)
        self.surface = self.generate_surface()

    def update(self, dt, events):
        self.age += dt

    def split(self, message):
        lines = [""]
        w = []
        for char in message+" ":
            if char == ' ' and sum(w) > c.ALERT_WIDTH - c.ALERT_MARGIN[c.LEFT] - c.ALERT_MARGIN[c.RIGHT]:
                i = lines[-1].rfind(' ')
                word = lines[-1][i:]
                w = w[i:] + [self.game.small_font_render[' '].get_width()]
                lines[-1] = lines[-1][:i]
                lines.append(word[1:]+" ")
            else:
                lines[-1] += char
                w.append(self.game.small_font_render[char].get_width())
        return lines


    def generate_surface(self):
        h = c.ALERT_MARGIN[c.UP] + len(self.lines)*(c.ALERT_MARGIN[c.DOWN] + self.game.small_font_render['0'].get_height())
        surface = pygame.Surface((c.ALERT_WIDTH, h))
        surface.fill((255,0,0))
        return surface

    def get_alpha(self):
        if self.age < c.ALERT_DURATION:
            return c.ALERT_ALPHA
        elif self.age < c.ALERT_DURATION + c.ALERT_FADEOUT:
            through = (self.age - c.ALERT_DURATION)/(c.ALERT_FADEOUT)
            return int(c.ALERT_ALPHA*(1  - through))
        else:
            return 0

    def draw(self, surface, offset):
        # TODO account for changes in position
        x = c.ALERT_MARGIN[c.LEFT]
        for i, line in enumerate(self.lines):
            y = c.ALERT_MARGIN[c.UP] + (c.ALERT_MARGIN[c.DOWN] + self.game.small_font_render['0'].get_height())*i
            self.surface.blit(self.game.small_font.render(line, 0, c.BLACK), (x, y))
        self.surface.set_alpha(self.get_alpha())
        surface.blit(self.surface, (offset))


class AlertManager(GameObject):
    def __init__(self, game):
        super().__init__(game)
        self.font = self.game.small_font
        self.alerts = []
        # TODO draw and update alerts

    def alert(self, message, player=None):
        self.alerts.append(Alert(self.game, message, player))

    def draw(self, surface):
        x = c.ALERT_PADDING[c.LEFT]
        y = c.LEVEL_HEIGHT
        for i, alert in enumerate(self.alerts[::-1]):
            y -= c.ALERT_PADDING[c.DOWN] + alert.surface.get_height()
            alert.draw(surface, (x, y))
    
    def update(self, dt):
        for i, alert in enumerate(self.alerts[:]):
            alert.update(dt, [])
            if len(self.alerts) - i > c.ALERT_NUM and alert.age < c.ALERT_DURATION:
                alert.age = c.ALERT_DURATION
            if alert.age >= c.ALERT_DURATION + c.ALERT_FADEOUT:
                self.alerts.remove(alert)

    def clear(self):
        self.alerts = []