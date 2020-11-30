##!/usr/bin/env python3

import random

import pygame

from particle import Particle
import constants as c
from primitives import Pose

class PlanetParticle(Particle):
    def __init__(self, game, planet):
        super().__init__(game)
        self.planet = planet
        self.pose = planet.pose.copy()
        self.velocity = Pose(((random.random() * 2 - 1)**2 * 180 * random.choice((-1, 1)),
                             (random.random() * 2 - 1)**2 * 180 * random.choice((-1, 1))),
                             random.random() * 360)
        self.start_radius = (60 + random.random()*30) * planet.radius/50
        self.duration = 0.8

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
        pygame.draw.circle(surf, c.WHITE, (radius, radius), radius)
        x = self.pose.x - offset[0] - surf.get_width()//2
        y = self.pose.y - offset[1] - surf.get_height()//2
        surf.set_alpha(self.get_alpha())
        surface.blit(surf, (x, y))

class PlanetExplosion(Particle):
    def __init__(self, game, planet):
        super().__init__(game)
        self.planet = planet
        self.pose = planet.pose.copy()
        self.start_radius = planet.radius
        self.duration = 1
        self.subparticles = {PlanetParticle(self.game, self.planet) for i in range(12)}

    def get_scale(self):
        return 1 + self.through(loading=3) * 2.5

    def get_alpha(self):
        return 150 * (1 - self.through(loading=4))

    def update(self, dt, events):
        super().update(dt, events)
        for particle in self.subparticles:
            particle.update(dt, events)
        self.subparticles = {item for item in self.subparticles if not item.age > item.duration}

    def draw(self, surface, offset=(0, 0)):
        radius = int(self.start_radius * self.get_scale())
        surf = pygame.Surface((radius*2, radius*2))
        surf.fill(c.YELLOW)
        surf.set_colorkey(c.YELLOW)
        r = 255# - self.through(loading=2) * 255
        g = 255# - self.through(loading=2) * 255
        b = 255 - self.through(loading=0.2) * 128
        if self.age < 0.05:
            r, g, b = c.BLACK
        pygame.draw.circle(surf, (r, g, b), (radius, radius), radius)
        x = self.pose.x - offset[0] - surf.get_width()//2
        y = self.pose.y - offset[1] - surf.get_height()//2
        surf.set_alpha(self.get_alpha())
        if self.age < 0.1:
            surf.set_alpha(255)
        surface.blit(surf, (x, y))
        if self.age > 0.05:
            for particle in self.subparticles:
                particle.draw(surface, offset=offset)
