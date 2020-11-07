##!/usr/bin/env python3

from scene import Scene

class LevelScene(Scene):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def update(self, dt, events):
        pass

    def draw(self, surf, offset=(0, 0)):
        pass
