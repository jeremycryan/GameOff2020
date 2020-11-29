##!/usr/bin/env python

import math
import random

import pygame

import constants as c
from primitives import PhysicsObject
from nugget_explosion import NuggetExplosion

class Nugget(PhysicsObject):
    def __init__(self, game, position, angle):
        super().__init__(game, position, angle)
        self.radius = 22
        self.age = random.random() * 2 * math.pi
        self.glow = pygame.image.load(c.IMAGE_PATH + "/waypoint_glow.png")
        self.period = math.pi + 1
        self.surf = pygame.image.load(c.IMAGE_PATH + "/waypoint.png")
        self.target_alpha = 128
        self.alpha = 0

    def update(self, dt, events):
        super().update(dt, events)
        self.age += dt
        if self.alpha < self.target_alpha:
            self.alpha += 128 * dt
        if self.alpha > self.target_alpha:
            self.alpha = self.target_alpha

    def draw(self, surface, offset=(0, 0)):
        x = self.pose.x + offset[0] + math.sin(self.age * (self.period + 1)) * 3
        y = self.pose.y + offset[1] + math.cos(self.age * (self.period)) * 3

        glow_width = int((85 + math.sin(self.age * (self.period - 1.25)) * 10) * (self.alpha+1)/(self.target_alpha+1))
        glow = pygame.transform.scale(self.glow, (glow_width, glow_width))
        self.surf.set_colorkey(c.MAGENTA)
        self.surf.set_alpha((self.alpha/self.target_alpha)**2 * self.target_alpha)
        surface.blit(self.surf,
            (x - self.surf.get_width()//2,
            y - self.surf.get_height()//2))
        surface.blit(glow,
            (x - glow_width//2, y - glow_width//2),
            special_flags=pygame.BLEND_ADD)

        visual_radius = 15

    def test_collision(self, ship):
        dist = (self.pose - ship.pose).magnitude()
        if dist < ship.radius + self.radius + 7 and self not in ship.nuggets:
            self.get_picked_up(ship)

    def get_picked_up(self, ship):
        ship.nuggets.add(self)
        self.game.current_scene.particles.add(NuggetExplosion(self.game, self))
        self.alpha = 25
        self.game.waypoint_collect_sound.play()

    def overlaps(self, pose, r, clearance):
        return pose.distance_to(self.pose) < self.radius + r + max(clearance, self.clearance)
