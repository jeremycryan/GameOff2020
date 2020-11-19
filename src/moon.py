##!/usr/bin/env python3

import math

import pygame

from planet import Planet
import constants as c
from death_particle import DeathParticle

class Moon(Planet):
    def __init__(self, game, position):
        super().__init__(game, position, 0, radius=30)
        self.mass *= 2
        self.surface = pygame.image.load(c.IMAGE_PATH + "/moon.png")
        self.glow = pygame.image.load(c.IMAGE_PATH + "/moonglow.png")
        self.glow.set_alpha(50)

    def draw(self, surface, offset=(0, 0)):
        self.draw_glow(surface, offset)
        super().draw(surface, offset)

    def draw_glow(self, surface, offset=(0, 0)):
        scale = math.sin(self.age * math.pi) * 0.08 + 0.92
        glow = pygame.transform.scale(self.glow,
                                      (int(self.glow.get_width() * scale),
                                      int(self.glow.get_height() * scale)))
        x = offset[0] + self.pose.x - glow.get_width()//2
        y = offset[1] + self.pose.y - glow.get_height()//2
        surface.blit(glow, (x, y), special_flags=pygame.BLEND_ADD)

    def collide_with_ship(self, ship):
        # TODO give points, proceed to next level, etc.
        ship.has_hit_moon = True
        self.game.current_scene.achievement_row.score_ship(ship)
        if ship in self.game.current_scene.ships:
            self.game.current_scene.ships.remove(ship)
            for i in range(5):
                self.game.current_scene.particles.add(DeathParticle(self.game, ship))
            self.sprout_flag(ship)

    def sprout_flag(self, ship):
        # not implemented yet, unfortunately
        pass

    def is_moon(self):
        return True
