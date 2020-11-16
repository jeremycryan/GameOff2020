##!/usr/bin/env python3

from primitives import GameObject

class Particle(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.age = 0
        self.duration = None
        self.dead = False

    def get_alpha(self):
        return 255

    def get_scale(self):
        return 1

    def through(self, loading=1):
        """ Increase loading argument to 'frontload' the animation. """
        if self.duration is None:
            return 0
        else:
            return 1 - (1 - self.age / self.duration)**loading

    def update(self, dt, events):
        self.age += dt
        if self.duration and self.age > self.duration:
            self.destroy()

    def destroy(self):
        self.dead = True
