##!/usr/bin/env python3

import pygame

from scene import Scene
import constants as c

class StartScene(Scene):
    """ Display a black screen with a white circle for two seconds. """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.age = 0

    def update(self, dt, events):
        self.age += dt
        if self.age > 2:
            self.is_running = False

    def draw(self, surf, offset=(0, 0)):
        surf.fill(c.BLACK)
        pygame.draw.circle(surf,
            c.WHITE,
            (c.WINDOW_WIDTH//2, c.WINDOW_HEIGHT//2),
            c.WINDOW_HEIGHT//4)

    def next_scene(self):
        return None
