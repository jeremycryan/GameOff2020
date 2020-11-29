##!/usr/bin/env python3

import random
from math import sin

import pygame

from particle import Particle
from primitives import Pose
import constants as c

class WindParticle(Particle):

    def __init__(self, game):
        super().__init__(game)
        x = random.random() * c.LEVEL_WIDTH
        y = random.random() * c.LEVEL_WIDTH

        if not hasattr(self.game, "solar_wind_direction"):
            self.game.solar_wind_direction = random.choice((c.UP, c.DOWN, c.LEFT, c.RIGHT))

        margin = 20
        if self.game.solar_wind_direction == c.UP:
            y = c.LEVEL_HEIGHT + margin
        elif self.game.solar_wind_direction == c.DOWN:
            y = -margin
        elif self.game.solar_wind_direction == c.LEFT:
            x = c.LEVEL_WIDTH + margin
        elif self.game.solar_wind_direction == c.RIGHT:
            x = -margin
        self.destroy_margin = 50

        self.layer = random.choice((1, 2, 3))
        self.radius = 5 - self.layer
        self.speed = 1600/self.layer

        self.pose = Pose((x, y), 0)
        self.velocity = Pose((self.game.solar_wind_direction), 0) * self.speed

        self.color = random.choice([
            (255, 255, 100),
            (255, 180, 100),
            (255, 100, 100)
        ])

        self.age = random.random() * 100

    def update(self, dt, events):
        super().update(dt, events)
        self.pose += self.velocity * dt
        if self.pose.x > c.WINDOW_WIDTH + self.destroy_margin or \
            self.pose.y > c.WINDOW_HEIGHT + self.destroy_margin or \
            self.pose.x < -self.destroy_margin or \
            self.pose.y < -self.destroy_margin:
            self.destroy()

    def draw(self, surface, offset=(0, 0)):
        x, y = self.pose.get_position()
        if self.game.solar_wind_direction in (c.UP, c.DOWN):
            x += sin(self.age * 10) * 30/self.layer
            width = self.radius
            height = self.radius * 3
        else:
            width = self.radius * 3
            height = self.radius
            y += sin(self.age * 10) * 30/self.layer
        pygame.draw.ellipse(surface, self.color, (x - width//2, y - width//2, width, height))
