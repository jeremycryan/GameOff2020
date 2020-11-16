##!/usr/bin/env python3

import math

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
        self.planets = [Planet(self.game, (200, 200)),
                        Planet(self.game, (500, 500), radius=50),
                        Moon(self.game, (800, 300)),
                        Wormhole(self.game, (725, 500), (600, 250))]
        self.ships = [Ship(self.game, "r90 t33 d200; t0 d500; r0 t33 d2000; r360 d260; r0 t33 d800; t0 d2500; t21 d1500; t0", self.game.players["PlasmaStarfish"], (500, 200), 180),
                      Ship(self.game, "t100 r180", self.game.players["superduperpacman42"], (500, 200), 180)]
        self.surface = pygame.Surface((c.LEVEL_WIDTH, c.LEVEL_HEIGHT))
        self.alignment = c.LEFT, c.DOWN
        self.offset = self.get_initial_offset()
        self.particles = set()
        self.screenshake_time = 0
        self.screenshake_amp = 0
        self.age = 0

    def shake(self, amp=15):
        self.screenshake_amp = max(self.screenshake_amp, amp)
        self.screenshake_time = 0

    def apply_screenshake(self, offset):
        x = offset[0] + self.screenshake_amp * math.cos(self.screenshake_time * 24)
        y = offset[1] + self.screenshake_amp * math.cos(self.screenshake_time * 24)
        return (x, y)

    def apply_own_offset(self, offset):
        return offset[0] + self.offset[0], offset[1] + self.offset[1]

    def update(self, dt, events):
        self.age += dt
        for ship in self.ships[::-1]:
            if ship.destroyed:
                self.ships.remove(ship)
        for object_to_update in self.ships + self.planets:
            object_to_update.update(dt, events)
        for particle in self.particles:
            particle.update(dt, events)
        self.particles = {item for item in self.particles if not item.dead}

        self.screenshake_time += dt
        self.screenshake_amp *= 0.003**dt
        self.screenshake_amp = max(0, self.screenshake_amp - 10*dt)

    def draw(self, surf, offset=(0, 0)):
        offset_with_shake = self.apply_screenshake(offset)
        surf.fill(c.BLACK)
        self.surface.fill(c.DARK_GRAY)
        self.draw_lines()
        for planet in self.planets:
            planet.draw(self.surface, offset_with_shake)
        for particle in self.particles:
            particle.draw(self.surface, offset_with_shake)
        for ship in self.ships:
            ship.draw(self.surface, offset_with_shake)
        surf.blit(self.surface, self.apply_own_offset(offset))

    def draw_lines(self):
        border = 15
        line_period = 80
        line_width = 50
        offset = (self.age * 25) % line_period
        x = - c.WINDOW_HEIGHT - border + offset
        y_low = c.WINDOW_HEIGHT + border
        y_high = - border
        y_height = y_low - y_high
        while x < c.WINDOW_WIDTH + border:
            pygame.draw.line(self.surface,
                             c.DARKER_GRAY,
                             (x, y_low),
                             (x+y_height, y_high),
                             width=line_width)
            x += line_period

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
