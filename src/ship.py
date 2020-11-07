##!/usr/bin/env python3

from primitives import PhysicsObject

class Ship(PhysicsObject):
    def __init__(self, game, program_string, position=(0, 0), angle=90):
        super().__init__(game, position, angle)
        self.program_string = program_string
        self.age = 0

    def update(self, dt, events):
        super().update(dt, events)
        self.age += dt
        # spaceship specific things

    def draw(self, surface, offset=(0, 0)):
        pass
        # draw a spaceship using self.pose
