##!/usr/bin/env python3

import pygame

from planet import Planet

class Moon(Planet):
    def __init__(self, game, position):
        super().__init__(game, position, 0, radius=50)

    def is_moon(self):
        return True

    def draw(self, surf, offset=(0, 0)):
        x, y = self.pose.get_position()
        x += offset[0]
        y += offset[1]
        pygame.draw.circle(surf, (100, 100, 100), (x, y), self.gravity_radius, 2)
        pygame.draw.circle(surf, (200, 100, 100), (x, y), self.radius)
