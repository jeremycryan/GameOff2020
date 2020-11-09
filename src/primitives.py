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
        self.x = new_x

    def set_y(self, new_y):
        self.y = new_y

    def set_position(self, position):
        self.x, self.y = position

    def set_angle(self, angle):
        self.angle = angle

    def get_position(self):
        return self.x, self.y

    def get_angle_radians(self):
        return self.angle*math.pi/180

    def get_unit_vector(self):
        """ Return the unit vector equivalent of the Pose's angle """
        # Note: y component is inverted because of indexing on displays;
        #       negative y points up, while positive y points down.
        unit_x = math.cos(self.get_angle_radians())
        unit_y = -math.sin(self.get_angle_radians())
        return unit_x, unit_y

    def get_weighted_position(self, weight):
        return self.x*weight, self.y*weight

    def add_position(self, position):
        add_x, add_y = position
        self.set_x(self.x + add_x)
        self.set_y(self.y + add_y)

    def add_angle(self, angle):
        self.set_angle(self.angle + angle)

    def rotate_position(self, angle):
        x = self.x*math.cos(angle*math.pi/180) \
            + self.y*math.sin(angle*math.pi/180)
        y = -self.x*math.sin(angle*math.pi/180) \
            + self.y*math.cos(angle*math.pi/180)
        self.set_position((x, y))

    def add_pose(self, other, weight=1, frame=None):
        if frame:
            other = other.copy()
            other.rotate_position(frame.angle)
        self.add_position(other.get_weighted_position(weight))
        self.add_angle(other.angle*weight)

    def distance_to(self, other):
        return (self - other).magnitude()

    def magnitude(self):
        distance = math.sqrt(self.x**2 + self.y**2)
        return distance

    def clear(self):
        self.x = 0
        self.y = 0
        self.angle = 0

    def copy(self):
        return Pose(self.get_position(), self.angle)

    def scale_to(self, magnitude):
        """ Scale the X and Y components of the Pose to have a particular
            magnitude. Angle is unchanged.
        """
        my_magnitude = self.magnitude()
        self.x *= magnitude / my_magnitude
        self.y *= magnitude / my_magnitude

    def __add__(self, other):
        copy = self.copy()
        copy.add_pose(other)
        return copy

    def __sub__(self, other):
        copy = self.copy()
        copy.add_pose(other, weight=-1)
        return copy

    def __str__(self):
        return f"<Pose x:{self.x} y:{self.y} angle:{self.angle}>"

    def __repr__(self):
        return self.__str__()


class PhysicsObject(GameObject):
    def __init__(self, game, position, angle):
        super().__init__(game)
        self.pose = Pose(position, angle)
        self.velocity = Pose(position=(0, 0), angle=0)
        self.acceleration = Pose(position=(0, 0), angle=0)

    def update(self, dt, events):
        self.velocity.add_pose(self.acceleration, weight=dt)
        self.pose.add_pose(self.velocity, weight=dt)
