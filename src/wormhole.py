##!/usr/bin/env python3

import pygame
import random

import constants as c
from primitives import PhysicsObject, Pose
from planet import Planet

class Wormhole(PhysicsObject):
    def __init__(self, game, position1, position2, angle=0, radius=20, gravity_radius=None, mass=None, color=-1):
        super().__init__(game, position1, angle)
        self.pose2 = Pose(position2, 0)
        self.home = False
        self.velocity.angle = -100
        self.radius = radius
        self.gravity_radius = gravity_radius if gravity_radius is not None else 2.5*radius
        self.mass = mass if mass is not None else radius**2
        self.ships1 = []
        self.ships2 = []
        self.age = 0
        if color == -1:
            color = random.randint(0, 3)
        self.color = c.WORMHOLE_COLORS[color]
        self.surfs = self.get_surfs()

    def get_surfs(self):
        surfs = []
        alpha = 40
        if self.color != c.WORMHOLE_COLORS[3] and self.color != c.WORMHOLE_COLORS[0]:
            base = pygame.image.load(c.IMAGE_PATH + "/wormhole_bw.png").convert()
        else:
            base = pygame.image.load(c.IMAGE_PATH + "/wormhole.png").convert()
        if self.color != c.WORMHOLE_COLORS[3]:
            tint = base.copy()
            tint.fill(self.color)
            base.blit(tint, (0, 0), special_flags = pygame.BLEND_MULT)
        base.set_colorkey(base.get_at((0, 0)))
        scale = 1
        for i in range(4):
            new_surf = base.copy()
            new_surf.set_alpha(alpha)
            alpha += (255 - alpha)*0.28
            new_surf = pygame.transform.scale(new_surf,
                (int(new_surf.get_width() * scale),
                int(new_surf.get_height() * scale)))
            scale *= 0.9
            if i%2==0:
                new_surf = pygame.transform.flip(new_surf, 1, 0)
            surfs.append(new_surf)
        return surfs

    def is_moon(self):
        """ Wormholes aren't moons, silly. """
        return False

    def get_acceleration(self, ship):
        """ Return a Pose indicating the acceleration to apply to
            the Ship.
        """
        distance1 = self.pose.distance_to(ship.pose) - ship.radius
        distance2 = self.pose2.distance_to(ship.pose) - ship.radius
        freeze_length = 0.4
        if distance1 < self.radius and not ship in self.ships2:
            ship.lastWormhole = self
            ship.freeze(freeze_length)
            self.ships1.append(ship)
            offset = self.pose-ship.pose
            offset.angle = 0
            ship.pose.add_pose(self.pose2 - self.pose + offset*2)
            ship.label_pose = ship.pose.copy()
            ship.scale = 0
        if distance2 < self.radius and not ship in self.ships1:
            ship.lastWormhole = self
            ship.freeze(freeze_length)
            self.ships2.append(ship)
            offset = self.pose2-ship.pose
            offset.angle = 0
            ship.pose.add_pose(self.pose - self.pose2 + offset*2)
            ship.label_pose = ship.pose.copy()
            ship.scale = 0
        if distance1 > self.radius and distance2 > self.radius:
            if ship in self.ships1:
                self.ships1.remove(ship)
            if ship in self.ships2:
                self.ships2.remove(ship)

        if distance1 == 0 or distance2 == 0 or ship.is_frozen():
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

    def overlaps(self, pose, r, clearance):
        hit1 = pose.distance_to(self.pose) < self.radius + r + max(clearance, self.clearance)
        hit2 = pose.distance_to(self.pose2) < self.radius + r + max(clearance, self.clearance)
        return hit1 or hit2

    def draw_gravity_region(self, surf, offset=(0, 0)):
        # This is a bit jank, but hey, it's a game jam
        Planet.draw_gravity_region(self, surf, offset)
        self.pose, self.pose2 = self.pose2, self.pose
        Planet.draw_gravity_region(self, surf, offset)
        self.pose, self.pose2 = self.pose2, self.pose

    def update(self, dt, events):
        self.age += dt
        self.pose.angle += dt * self.velocity.angle
        self.pose2.angle += dt * self.velocity.angle

    def draw(self, surf, offset=(0, 0)):

        x, y = self.pose.get_position()
        x += offset[0]
        y += offset[1]
        #pygame.draw.circle(surf, (100, 100, 100), (x, y), self.gravity_radius, 2)
        speed = -1
        for i, surface in enumerate(self.surfs):
            surface = pygame.transform.rotate(surface, self.pose.angle * speed)
            surf.blit(surface, (x - surface.get_width()//2, y - surface.get_height()//2))
            speed *= -0.7

        #pygame.draw.circle(surf, (150, 50, 250), (x, y), self.radius)

        x, y = self.pose2.get_position()
        x += offset[0]
        y += offset[1]
        #pygame.draw.circle(surf, (100, 100, 100), (x, y), self.gravity_radius, 2)
        speed = -1
        for i, surface in enumerate(self.surfs):
            surface = pygame.transform.rotate(surface, self.pose.angle * speed)
            surf.blit(surface, (x - surface.get_width()//2, y - surface.get_height()//2))
            speed *= -0.7
