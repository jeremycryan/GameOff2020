##!/usr/bin/env python3

import random

import pygame

from particle import Particle
import constants as c
from primitives import Pose

class DeathParticle(Particle):
    def __init__(self, game, ship):
        super().__init__(game)
        self.ship = ship
        self.pose = ship.pose.copy()
        self.velocity = Pose(((random.random() * 2 - 1) * 160,
                             (random.random() * 2 - 1) * 160),
                             random.random() * 360) + self.ship.velocity * 0.1
        self.start_radius = 40 + random.random()*30
        self.duration = 0.6

    def get_scale(self):
        return 1 - self.through(loading=2.5)

    def get_alpha(self):
        return 255 * (1 - self.through(loading=1))

    def update(self, dt, events):
        super().update(dt, events)
        self.pose += self.velocity * dt

    def draw(self, surface, offset=(0, 0)):
        radius = int(self.start_radius * self.get_scale())
        surf = pygame.Surface((radius*2, radius*2))
        surf.fill(c.BLACK)
        surf.set_colorkey(c.BLACK)
        pygame.draw.circle(surf, self.ship.player.color, (radius, radius), radius)
        x = self.pose.x - offset[0] - surf.get_width()//2
        y = self.pose.y - offset[1] - surf.get_height()//2
        surf.set_alpha(self.get_alpha())
        surface.blit(surf, (x, y))
