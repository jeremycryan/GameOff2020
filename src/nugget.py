##!/usr/bin/env python

import pygame

import constants as c
from primitives import PhysicsObject
from nugget_explosion import NuggetExplosion

class Nugget(PhysicsObject):
    def __init__(self, game, position, angle):
        super().__init__(game, position, angle)
        self.radius = 15
        self.age = 0

    def update(self, dt, events):
        super().update(dt, events)
        self.age += dt

    def draw(self, surface, offset=(0, 0)):
        x = self.pose.x + offset[0]
        y = self.pose.y + offset[1]
        pygame.draw.circle(surface, c.YELLOW, (x, y), self.radius)

    def test_collision(self, ship):
        dist = (self.pose - ship.pose).magnitude()
        if dist < ship.radius + self.radius + 5 and self not in ship.nuggets:
            self.get_picked_up(ship)

    def get_picked_up(self, ship):
        ship.nuggets.add(self)
        self.game.current_scene.particles.add(NuggetExplosion(self.game, self))
