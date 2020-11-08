##!/usr/bin/env python3

import pygame

from primitives import PhysicsObject
from player import Player

class Ship(PhysicsObject):
    def __init__(self, game, program_string, position=(0, 0), angle=90):
        super().__init__(game, position, angle)
        self.program_string = program_string
        self.age = 0

    def update(self, dt, events):
        super().update(dt, events)
        self.age += dt
        # spaceship specific things

    def draw(self, surface, offset=(0, 0)):
        ship_surf = pygame.Surface((60, 30))
        self.player.color = Player.random_color()
        print(self.player.color)
        pygame.draw.rect(ship_surf, self.player.color, (15, 0, 30, 30))
        pygame.draw.circle(ship_surf, self.player.color, (45, 15), 15)
        ship_surf = pygame.transform.rotate(ship_surf, self.pose.angle)
        x = self.pose.x + offset[0] - ship_surf.get_width()//2
        y = self.pose.y + offset[1] - ship_surf.get_height()//2
        surface.blit(ship_surf, (x, y))
