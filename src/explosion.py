##!/usr/bin/env python3

import pygame

from particle import Particle
import constants as c

class Explosion(Particle):
    def __init__(self, game, ship):
        super().__init__(game)
        self.ship = ship
        self.pose = ship.pose.copy()
        self.start_radius = 20
        self.duration = 0.4

    def get_scale(self):
        return 1 + self.through(loading=2) * 4

    def get_alpha(self):
        return 255 * (1 - self.through(loading=2))

    def update(self, dt, events):
        super().update(dt, events)

    def draw(self, surface, offset=(0, 0)):
        radius = int(self.start_radius * self.get_scale())
        surf = pygame.Surface((radius*2, radius*2))
        surf.fill(c.BLACK)
        surf.set_colorkey(c.BLACK)
        r = 255 - self.through(loading=2.5) * (255 - self.ship.player.color[0])
        g = 255 - self.through(loading=2.5) * (255 - self.ship.player.color[1])
        b = 255 - self.through(loading=2.5) * (255 - self.ship.player.color[2])

        pygame.draw.circle(surf, (r, g, b), (radius, radius), radius)
        x = self.pose.x - offset[0] - surf.get_width()//2
        y = self.pose.y - offset[1] - surf.get_height()//2
        surf.set_alpha(self.get_alpha())
        surface.blit(surf, (x, y))
