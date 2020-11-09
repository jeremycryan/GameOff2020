##!/usr/bin/env python3

import pygame

import constants as c
from primitives import PhysicsObject, Pose

class Planet(PhysicsObject):
    def __init__(self, game, position, angle, radius=100, gravity_radius=None, mass=None):
        super().__init__(game, position, angle)
        self.velocity.angle = 15
        self.radius = radius
        self.gravity_radius = gravity_radius if gravity_radius is not None else 2.5*radius
        self.mass = mass if mass is not None else radius**2

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
        gravity_magnitude = self.mass * c.GRAVITY_CONSTANT / distance**2
        gravity_vector = (self.pose - ship.pose)
        gravity_vector.set_angle(0)
        gravity_vector.scale_to(gravity_magnitude)
        return gravity_vector

    def update(self, dt, events):
        pass

    def draw(self, surf, offset=(0, 0)):
        x, y = self.pose.get_position()
        x += offset[0]
        y += offset[1]
        pygame.draw.circle(surf, (100, 100, 100), (x, y), self.gravity_radius, 2)
        pygame.draw.circle(surf, (200, 200, 200), (x, y), self.radius)
