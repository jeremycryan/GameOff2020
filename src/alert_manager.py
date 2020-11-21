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
        self.surface = self.generate_surface().convert_alpha()

    def update(self, dt, events):
        self.age += dt

    def split(self, message):
        # lines = [""]
        # w = []
        # for char in message+" ":
        #     if char == ' ' and sum(w) > c.ALERT_WIDTH - c.ALERT_MARGIN[c.LEFT] - c.ALERT_MARGIN[c.RIGHT]:
        #         i = lines[-1].rfind(' ')
        #         word = lines[-1][i:]
        #         w = w[i:] + [self.game.small_font_render[' '].get_width()]
        #         lines[-1] = lines[-1][:i]
        #         lines.append(word[1:]+" ")
        #     else:
        #         lines[-1] += char
        #         w.append(self.game.small_font_render[char].get_width())
        # return lines
        lines = []
        max_width = c.ALERT_WIDTH - c.ALERT_MARGIN[c.RIGHT] - c.ALERT_MARGIN[c.LEFT]
        cur_width = 0
        space_width = self.game.other_alert_font.render(" ", 1, c.WHITE).get_width()
        current_line = ""
        for word in message.split():
            render = self.game.other_alert_font.render(word, 1, c.WHITE)
            width = render.get_width()
            if cur_width + width + space_width > max_width:
                cur_width = 0
                lines.append(current_line)
                current_line = ""
            current_line += word + " "
            cur_width += width + space_width
        lines.append(current_line)
        return lines


    def generate_surface(self):
        zero_height = self.game.other_alert_font.render("0", 0, c.WHITE).get_height()

        h = c.ALERT_MARGIN[c.UP] + len(self.lines)*(c.PAUL_ALERT_LINE_SPACING + zero_height) - c.PAUL_ALERT_LINE_SPACING + c.ALERT_MARGIN[c.DOWN]
        surface = pygame.Surface((c.ALERT_WIDTH, h))
        surface.fill(c.MAGENTA)
        surface.set_colorkey(c.MAGENTA)
        pygame.draw.rect(surface, c.ALERT_BACKGROUND_COLOR, (0, 0, surface.get_width(), surface.get_height()), border_radius=7)

        x = c.ALERT_MARGIN[c.LEFT]
        for i, line in enumerate(self.lines):
            y = c.ALERT_MARGIN[c.UP] + (c.PAUL_ALERT_LINE_SPACING + zero_height)*i
            surface.blit(self.game.other_alert_font.render(line, 1, c.ALERT_TEXT_COLOR), (x, y))
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
        self.surface.set_alpha(self.get_alpha())
        surface.blit(self.surface, (offset))


class AlertManager(GameObject):
    def __init__(self, game):
        super().__init__(game)
        self.font = self.game.small_font
        self.alerts = []
        self.yoff = 0
        # TODO draw and update alerts

    def alert(self, message, player=None):
        self.alerts.append(Alert(self.game, message, player))
        self.yoff += self.alerts[-1].surface.get_height() + c.ALERT_PADDING[c.UP] + c.ALERT_PADDING[c.DOWN]

    def draw(self, surface):
        x = c.ALERT_PADDING[c.LEFT]
        y = c.LEVEL_HEIGHT
        for i, alert in enumerate(self.alerts[::-1]):
            y -= c.ALERT_PADDING[c.DOWN] + alert.surface.get_height()
            alert.draw(surface, (x, y + self.yoff))

    def total_height(self, offset=0):
        margins = c.ALERT_PADDING[c.UP] + c.ALERT_PADDING[c.DOWN]
        height = sum([alert.surface.get_height() + margins for alert in self.alerts[:len(self.alerts) - offset]])
        return height

    def update(self, dt):
        if self.yoff > 0:
            dy = self.yoff
            self.yoff -= dy ** dt * 15
            if self.yoff < 3:
                self.yoff = 0
        offset = 0
        index = 0
        while self.total_height(offset) - self.yoff > c.MAX_ALERT_HEIGHT:
            if self.alerts[index].age < c.ALERT_DURATION:
                self.alerts[index].age = c.ALERT_DURATION
            index += 1
            offset += 1
        for i, alert in enumerate(self.alerts[:]):
            alert.update(dt, [])
            # if len(self.alerts) - i > c.ALERT_NUM and alert.age < c.ALERT_DURATION:
            #     alert.age = c.ALERT_DURATION
            if alert.age >= c.ALERT_DURATION + c.ALERT_FADEOUT:
                self.alerts.remove(alert)

    def clear(self):
        self.alerts = []
