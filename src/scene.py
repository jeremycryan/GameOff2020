##!/usr/bin/env python3

import pygame

import constants as c
from primitives import GameObject

class Scene(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_running = True

    def main(self):
        lag = 0
        while self.is_running:
            dt, events = self.game.update_globals()
            lag += dt
            while lag > c.TICK_LENGTH:
                lag -= c.TICK_LENGTH
                self.update(c.TICK_LENGTH, events)
            self.draw(self.game.screen)
            self.game.update_screen()

    def next_scene(self):
        raise NotImplementedError()
