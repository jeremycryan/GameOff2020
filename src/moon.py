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
        self.flags = []
        self.flag_angles = []

    def draw(self, surface, offset=(0, 0)):
        self.draw_flags(surface, offset)
        self.draw_glow(surface, offset)
        super().draw(surface, offset)

    def draw_flags(self, surface, offset=(0, 0)):
        for flag, angle in zip(self.flags, self.flag_angles):
            angle = angle + self.pose.angle
            flag_surf = pygame.transform.rotate(flag, angle)
            dist = self.radius + flag.get_width()//2
            xoff = math.cos(angle*math.pi/180) * dist
            yoff = -math.sin(angle*math.pi/180) * dist
            x = xoff + offset[0] + self.pose.x - flag_surf.get_width()//2
            y = yoff + offset[1] + self.pose.y - flag_surf.get_height()//2
            surface.blit(flag_surf, (x, y))

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
            self.game.current_scene.shake(10)
            if not self.game.player_flags[ship.player.name] in self.flags:
                self.sprout_flag(ship)

    def sprout_flag(self, ship):
        self.flags.append(ship.flag_surf)

        dx = ship.pose.x - self.pose.x
        dy = ship.pose.y - self.pose.y
        angle = math.atan2(-dy, dx)
        self.flag_angles.append(angle*180/math.pi - self.pose.angle)

    def is_moon(self):
        return True
