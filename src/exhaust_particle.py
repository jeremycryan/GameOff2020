##!/usr/bin/env python3

import pygame

from particle import Particle
from primitives import Pose
import constants as c

class ExhaustParticle(Particle):
    def __init__(self, game, ship):
        super().__init__(game)
        self.ship = ship
        size = 18
        if c.DOUBLE_THRUST_MOD in self.game.modifications:
            size *= 1.5
        self.surface = pygame.Surface((size, size))
        self.surface.fill(c.BLACK)
        self.surface.set_colorkey(c.BLACK)
        pygame.draw.circle(self.surface,
                           ship.player.color,
                           (size//2, size//2),
                           size//2)
        self.position = ship.pose.copy()
        self.position.add_pose(Pose((-20, 0), 0), 1, self.position)
        self.thrust = ship.thrust.copy()
        self.thrust_mag = self.thrust.magnitude()
        self.thrust.scale_to(-100)
        self.duration = 0.4
        self.intensity = 1 - (1 - self.thrust_mag/100/c.THRUST)**3

    def get_alpha(self):
        return (255 - self.through() * 255)*self.intensity

    def get_scale(self):
        return (1 - self.through())*self.intensity

    def update(self, dt, events):
        super().update(dt, events)
        rotated = self.thrust.copy()
        rotated.rotate_position(self.position.angle)
        self.position += rotated * dt * 3 * self.intensity
        self.position += self.ship.velocity * dt

    def draw(self, surface, offset=(0, 0)):
        x, y = self.position.x, self.position.y
        scale = self.get_scale()
        x += offset[0] - self.surface.get_width() * scale/2
        y += offset[1] - self.surface.get_width() * scale/2
        w = int(self.surface.get_width()*scale)
        h = int(self.surface.get_height()*scale)
        surf_to_blit = pygame.transform.scale(self.surface, (w, h))
        surf_to_blit.set_alpha(self.get_alpha())
        surface.blit(surf_to_blit, (x, y))
