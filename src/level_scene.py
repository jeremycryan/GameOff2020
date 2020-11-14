##!/usr/bin/env python3

import pygame

import constants as c
from scene import Scene
from planet import Planet
from moon import Moon
from wormhole import Wormhole
from ship import Ship
from primitives import Pose

class LevelScene(Scene):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.planets = [Planet(self.game, (200, 200), 0),
                        Planet(self.game, (500, 500), 0, 50),
                        Moon(self.game, (800, 300)),
                        Wormhole(self.game, (675, 650), (600, 250))]
        self.ships = [Ship(self.game, "r90 t33 d200; t0 d500; r0 t33 d2000; r360 d260; r0 t33 d800; t0 d2500; t21 d1500; t0", self.game.players["Paul"], (500, 200), 180),
                      Ship(self.game, "t50", self.game.players["Jeremy"], (500, 200), 180)]
        self.surface = pygame.Surface((c.LEVEL_WIDTH, c.LEVEL_HEIGHT))
        self.alignment = c.LEFT, c.DOWN
        self.offset = self.get_initial_offset()

    def apply_own_offset(self, offset):
        return offset[0] + self.offset[0], offset[1] + self.offset[1]

    def update(self, dt, events):
        for ship in self.ships[::-1]:
            if ship.destroyed:
                self.ships.remove(ship)
        for object_to_update in self.ships + self.planets:
            object_to_update.update(dt, events)

    def draw(self, surf, offset=(0, 0)):
        surf.fill(c.DARK_GRAY)
        self.surface.fill(c.BLACK)
        for planet in self.planets:
            planet.draw(self.surface, offset)
        for ship in self.ships:
            ship.draw(self.surface, offset)
        surf.blit(self.surface, self.apply_own_offset(offset))

    def get_initial_offset(self):
        x = 0
        if self.alignment[0] == c.RIGHT:
            x = c.WINDOW_WIDTH - c.LEVEL_WIDTH
        elif self.alignment[0] == c.CENTER:
            x = (c.WINDOW_WIDTH - c.LEVEL_WIDTH)//2
        y = 0
        if self.alignment[1] == c.DOWN:
            y = c.WINDOW_HEIGHT - c.LEVEL_HEIGHT
        elif self.alignment[1] == c.CENTER:
            y = (c.WINDOW_HEIGHT - c.LEVEL_HEIGHT)//2
        return (x, y)
