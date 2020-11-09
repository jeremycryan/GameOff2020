##!/usr/bin/env python3

import pygame

import constants as c
from primitives import PhysicsObject, Pose

class Wormhole(PhysicsObject):
    def __init__(self, game, position1, position2, angle=0, radius=20, gravity_radius=None, mass=None):
        super().__init__(game, position1, angle)
        self.pose2 = Pose(position2, 0)
        self.velocity.angle = 15
        self.radius = radius
        self.gravity_radius = gravity_radius if gravity_radius is not None else 2.5*radius
        self.mass = mass if mass is not None else radius**2
        self.ships1 = []
        self.ships2 = []

    def is_moon(self):
        """ Wormholes aren't moons, silly. """
        return False

    def get_acceleration(self, ship):
        """ Return a Pose indicating the acceleration to apply to
            the Ship.
        """
        distance1 = self.pose.distance_to(ship.pose)
        distance2 = self.pose2.distance_to(ship.pose)
        if distance1 < self.radius and not ship in self.ships2:
            self.ships1.append(ship)
            offset = self.pose-ship.pose
            offset.angle = 0
            ship.pose.add_pose(self.pose2 - self.pose + offset*2)
        if distance2 < self.radius and not ship in self.ships1:
            self.ships2.append(ship)
            offset = self.pose2-ship.pose
            offset.angle = 0
            ship.pose.add_pose(self.pose - self.pose2 + offset*2)
        if distance1 > self.radius and distance2 > self.radius:
            if ship in self.ships1:
                self.ships1.remove(ship)
            if ship in self.ships2:
                self.ships2.remove(ship)

        if distance1 == 0 or distance2 == 0:
            return Pose((0, 0), 0)
        if distance1 < self.gravity_radius:
            gravity_magnitude = self.mass * c.GRAVITY_CONSTANT / distance1**2
            gravity_vector = (self.pose - ship.pose)
        elif distance2 < self.gravity_radius:
            gravity_magnitude = self.mass * c.GRAVITY_CONSTANT / distance2**2
            gravity_vector = (self.pose2 - ship.pose)
        else:
            return Pose((0, 0), 0)
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
        pygame.draw.circle(surf, (150, 50, 250), (x, y), self.radius)

        x, y = self.pose2.get_position()
        x += offset[0]
        y += offset[1]
        pygame.draw.circle(surf, (100, 100, 100), (x, y), self.gravity_radius, 2)
        pygame.draw.circle(surf, (150, 50, 250), (x, y), self.radius)
