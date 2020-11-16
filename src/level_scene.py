##!/usr/bin/env python3

import math

import pygame
import random

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
        # self.planets = [Planet(self.game, (200, 200)),
        #                 Planet(self.game, (500, 500), radius=50),
        #                 Moon(self.game, (800, 300)),
        #                 Wormhole(self.game, (725, 500), (600, 250))]
        self.spawn_level()
        # self.ships = [Ship(self.game, "r90 t33 d200; t0 d500; r0 t33 d2000; r360 d260; r0 t33 d800; t0 d2500; t21 d1500; t0", self.game.players["PlasmaStarfish"], (500, 200), 180),
        #               Ship(self.game, "t100 r180", self.game.players["superduperpacman42"], (500, 200), 180)]
        self.ships = []
        self.spawn_ship("t100", "superduperpacman42")
        
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

    def spawn_level(self, num_planets=10):
        home = self.get_edge()
        spawn_angle = self.get_angle(home, (c.LEVEL_WIDTH/2, c.LEVEL_HEIGHT/2))
        spawn_x = home[0] + int(math.cos(spawn_angle)*(c.HOME_PLANET_RADIUS+35))
        spawn_y = home[1] - int(math.sin(spawn_angle)*(c.HOME_PLANET_RADIUS+35))
        self.spawn_angle = math.degrees(spawn_angle)
        self.spawn_pos = (spawn_x, spawn_y)
        self.home_planet = Planet(self.game, home, angle=self.spawn_angle, radius=c.HOME_PLANET_RADIUS, home=True)
        self.planets = [self.home_planet]
        for i in range(100):
            moon = Pose(self.get_edge(offset=100), 0)
            if moon.distance_to(self.home_planet.pose) > 400:
                break
        self.planets.append(Moon(self.game, (moon.x, moon.y)))
        for i in range(1000):
            self.add_planet()
            if len(self.planets) >= num_planets+2:
                break
        self.add_wormhole() # for now wormhole must be added last

    def get_point(self, W=c.LEVEL_WIDTH, H=c.LEVEL_HEIGHT, border=0):
        x = int(random.random()*(W-border*2)) + border
        y = int(random.random()*(H-border*2)) + border
        return (x, y)

    def get_edge(self, W=c.LEVEL_WIDTH, H=c.LEVEL_HEIGHT, offset=0):
        perimeter = (W+H-offset*4)*2
        x = int(random.random()*(W-2*offset))
        y = int(random.random()*(H-2*offset))
        edge = int(random.random()*4)
        if edge == 0:
            x = offset
        elif edge == 1:
            x = W - offset
        elif edge == 2:
            y = offset
        elif edge == 3:
            y = H - offset
        return (x, y)

    def get_angle(self, p1, p2):
        return math.atan2(p1[1]-p2[1], p2[0]-p1[0])

    def get_viable_point(self, r):
        x, y = self.get_point()
        pose = Pose((x, y), 0)
        if pose.distance_to(self.home_planet.pose) < self.home_planet.radius + r + 100:
            return False
        for planet in self.planets:
            if pose.distance_to(planet.pose) < planet.radius + r + c.MIN_SPACING:
                return False
        return (x, y)

    def add_planet(self, r=0):
        if not r:
            r = int(random.random()*(c.MAX_PLANET_RADIUS-c.MIN_PLANET_RADIUS))+c.MIN_PLANET_RADIUS
        pos = self.get_viable_point(r)
        if not pos:
            return
        p = Planet(self.game, pos, radius=r)
        self.planets.append(p)

    def add_wormhole(self):
        for i in range(100):
            pos1 = self.get_viable_point(20)
            if pos1:
                break
        if not pos1:
            return
        for i in range(100):
            pos2 = self.get_viable_point(20)
            if pos2 and Pose(pos1, 0).distance_to(Pose(pos2, 0)) > 300:
                break
        if not pos2:
            return
        self.planets.append(Wormhole(self.game, pos1, pos2))

    def spawn_ship(self, program, name):
        player = self.game.players[name]
        ship = Ship(self.game, program, player, self.spawn_pos, self.spawn_angle)
        self.ships.append(ship)