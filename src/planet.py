##!/usr/bin/env python3

import random
import math

import pygame

import constants as c
from primitives import PhysicsObject, Pose

class Planet(PhysicsObject):
    def __init__(self, game, position, angle=None, radius=100, gravity_radius=None, mass=None, home=False, surf_det_size=None):
        if angle is None:
            angle = random.random()*360
        super().__init__(game, position, angle)
        self.home = home
        self.velocity.angle = 15
        if self.home:
            self.velocity.angle = 0
        self.radius = radius
        if not surf_det_size:
            surf_det_size = radius
        self.gravity_radius = gravity_radius if gravity_radius is not None else 2.7*radius
        self.mass = mass if mass is not None else radius ** 2

        self.ship_surf = pygame.image.load(c.IMAGE_PATH + "/ship.png")
        self.ship_surf.set_alpha(80)
        self.ship_surf.set_colorkey(c.MAGENTA)

        if self.home:
            self.surface = pygame.image.load(c.IMAGE_PATH + "/earth.png")
        elif surf_det_size > 50:
            self.surface = pygame.image.load(c.IMAGE_PATH + "/large_planet.png")
        else:
            self.surface = pygame.image.load(c.IMAGE_PATH + "/small_planet.png")
        self.surface = pygame.transform.scale(self.surface, (radius*2, radius*2))
        self.shadow = pygame.image.load(c.IMAGE_PATH + "/planet_shadow.png")
        self.shadow = pygame.transform.scale(self.shadow,
                                            (self.surface.get_width(),
                                            self.surface.get_height()))
        self.shadow.set_colorkey(c.WHITE)
        self.shadow.set_alpha(70)
        self.back_shadow = pygame.Surface((self.surface.get_width(), self.surface.get_height()))
        self.back_shadow.fill(c.WHITE)
        pygame.draw.circle(self.back_shadow,
                           c.BLACK,
                           (self.surface.get_width()//2,
                           self.surface.get_height()//2),
                           self.surface.get_width()//2)
        self.back_shadow.set_alpha(80)
        self.back_shadow.set_colorkey(c.WHITE)
        self.age = 0

    def is_moon(self):
        """ Planets aren't moons, silly. """
        return False

    def get_acceleration(self, ship):
        """ Return a Pose indicating the acceleration to apply to
            the Ship.
        """
        distance = self.pose.distance_to(ship.pose)
        if distance > self.gravity_radius:
            return Pose((0, 0), 0)
        if distance < self.radius + ship.radius:
            self.collide_with_ship(ship)
        if self.home:
            return Pose((0, 0), 0)
        gravity_magnitude = self.mass * c.GRAVITY_CONSTANT / distance**2
        gravity_vector = (self.pose - ship.pose)
        gravity_vector.set_angle(0)
        gravity_vector.scale_to(gravity_magnitude)
        if c.INVERTED_GRAVITY_MOD in self.game.modifications:
            return gravity_vector * -1
        return gravity_vector

    def collide_with_ship(self, ship):
        ship.destroy()

    def overlaps(self, pose, r, clearance):
        return pose.distance_to(self.pose) < self.radius + r + max(clearance, self.clearance)

    def draw(self, surf, offset=(0, 0)):
        self.draw_back_shadow(surf, offset)
        my_surface = pygame.transform.rotate(self.surface, self.pose.angle)
        ship = pygame.transform.rotate(self.ship_surf, self.pose.angle)
        x, y = self.pose.get_position()
        x += offset[0]
        y += offset[1]
        surf.blit(my_surface, (x - my_surface.get_width()//2, y - my_surface.get_height()//2))
        surf.blit(self.shadow, (x - self.shadow.get_width()//2, y - self.shadow.get_height()//2))
        pygame.draw.circle(surf, c.BLACK, (x, y), self.radius+2, width=2)
        if not self.home:
            pass

        if self.home:
            r = c.HOME_PLANET_RADIUS + c.SHIP_SPAWN_ALTITUDE
            x = self.pose.x + r * math.cos(self.pose.get_angle_radians()) + offset[0]
            y = self.pose.y + r * -math.sin(self.pose.get_angle_radians()) + offset[1]
            surf.blit(ship, (x - ship.get_width()//2, y - ship.get_height()//2))

            #self.draw_gravity_region(surf, offset)
        # pygame.draw.circle(surf, (200, 200, 200), (x, y), self.radius)

    def draw_back_shadow(self, surf, offset=(0, 0)):
        x, y = self.pose.get_position()
        x += offset[0]/2 + 12 * (self.radius/100 + 0.5) - self.back_shadow.get_width()//2
        y += offset[1]/2 + 12 * (self.radius/100 + 0.5) - self.back_shadow.get_height()//2
        surf.blit(self.back_shadow, (x, y))

    def update(self, dt, events):
        super().update(dt, events)
        self.age += dt

    def draw_gravity_region(self, surf, offset=(0, 0)):
        if self.home:
            return
        radius = self.gravity_radius
        pixels_per_degree = math.pi * 2 * radius / 360
        x, y = self.pose.get_position()
        x += offset[0]
        y += offset[0]
        w = self.gravity_radius * 2
        h = self.gravity_radius * 2
        pixels_each = 8
        dots = int((360 * pixels_per_degree / pixels_each)/10 * 10)
        angle_offset = self.age * 15 / radius
        for i in range(dots):
            angle_rad = 2 * math.pi * i/dots + (angle_offset)
            my_radius = radius + math.sin(i) * 3
            pygame.draw.circle(surf,
                            c.GRAY,
                            (x + my_radius * math.sin(angle_rad), y + my_radius * -math.cos(angle_rad)),
                            1)

        # x, y = self.pose.get_position()
        # x += offset[0]
        # y += offset[1]
        #pygame.draw.circle(surf, (100, 100, 100), (x, y), self.gravity_radius, 2)
