##!/usr/bin/env python3

import math

class GameObject:
    def __init__(self, game):
        self.game = game

    def update(self, dt, events):
        raise NotImplementedError()

    def draw(self, surf, offset=(0, 0)):
        raise NotImplementedError()


class Pose:
    def __init__(self, position, angle):
        """ Initialize the Pose.

            position: two-length tuple (x, y)
            angle: angle, in degrees counterclockwise from right ->
        """
        self.set_position(position)
        self.angle = angle

    def set_x(self, new_x):
        self.x = x

    def set_y(self, new_y):
        self.y = y

    def set_position(self, position):
        self.x, self.y = position

    def set_angle(self, angle):
        self.angle = angle

    def get_angle_radians(self):
        return self.angle*math.pi/180

    def get_unit_vector(self):
        """ Return the unit vector equivalent of the Pose's angle """
        # Note: y component is inverted because of indexing on displays;
        #       negative y points up, while positive y points down.
        unit_x = angle*math.cos(self.get_angle_radians())
        unit_y = -angle*math.sin(self.get_angle_radians())
        return unit_x, unit_y

    def get_weighted_position(self, weight):
        return self.x*weight, self.y*weight

    def add_position(self, position):
        add_x, add_y = position
        self.set_x(self.x + add_x)
        self.set_y(self.y + add_y)

    def add_angle(self, angle):
        self.set_angle(self.angle + angle)

    def add_pose(self, other, weight=1):
        self.add_position(other.get_weighted_position(other_weight))
        self.add_angle(other.angle*other_weight)

    def clear(self):
        self.x = 0
        self.y = 0
        self.angle = 0

    def __add__(self, other):
        self.add_pose(other)


class PhysicsObject(GameObject):
    def __init__(self, game, position, angle):
        super().__init__(game)
        self.pose = Pose(position, angle)
        self.velocity = Pose(position=(0, 0), angle=0)
        self.acceleration = Pose(position=(0, 0), angle=0)

    def update(self, dt, events):
        self.pose.add_pose(self.velocity, weight=dt)
        self.velocity.add_pose(self.acceleration, weight=dt)
